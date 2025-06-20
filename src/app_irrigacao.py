
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

st.set_page_config(page_title="Análise de Irrigação com ML", layout="wide")

st.title("🌱 Previsão de Irrigação Inteligente com Machine Learning")

# Carregar base
csv_path = os.path.join("..", "tests", "Crop_recommendation.csv")
df = pd.read_csv(csv_path)

st.subheader("🔍 Dados Originais")
st.dataframe(df.head())

# Regras de probabilidade por faixa
def prob_umidade(um):
    if um <= 30: return 1.0
    elif um <= 50: return 0.7
    elif um <= 80: return 0.4
    elif um <= 90: return 0.1
    else: return 0.01

def prob_chuva(ch):
    if ch <= 30: return 1.0
    elif ch <= 50: return 0.7
    elif ch <= 100: return 0.4
    elif ch <= 150: return 0.1
    else: return 0.01

def prob_temperatura(tp):
    if tp <= 10: return 0.1
    elif tp <= 25: return 0.5
    elif tp <= 29: return 0.6
    elif tp <= 32: return 0.7
    else: return 0.9

def classificar_irrigacao(row):
    p1 = prob_umidade(row["humidity"])
    p2 = prob_chuva(row["rainfall"])
    p3 = prob_temperatura(row["temperature"])
    media = np.mean([p1, p2, p3])
    return "Sim" if media > 0.5 else "Nao"

# Aplicar lógica personalizada
df_reduzido = df[["temperature", "humidity", "rainfall"]].copy()
df_reduzido["irrigando"] = df_reduzido.apply(classificar_irrigacao, axis=1)

# Balanceamento com SMOTE
X = df_reduzido[["temperature", "humidity", "rainfall"]]
y = df_reduzido["irrigando"].map({"Nao": 0, "Sim": 1})
smote = SMOTE(random_state=42)
X_bal, y_bal = smote.fit_resample(X, y)

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.25, random_state=42)

# Sidebar - escolha do modelo
st.sidebar.header("⚙️ Modelo de Classificação")
modelo_escolhido = st.sidebar.selectbox("Selecione o modelo", ["Decision Tree", "Random Forest", "Logistic Regression"])

if modelo_escolhido == "Decision Tree":
    modelo = DecisionTreeClassifier(random_state=42)
elif modelo_escolhido == "Random Forest":
    modelo = RandomForestClassifier(random_state=42)
else:
    modelo = LogisticRegression(max_iter=1000)

# Treinar modelo
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# Métricas
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

st.subheader("📊 Avaliação do Modelo")
st.markdown(f"""
- **Acurácia:** `{acc:.2f}`
- **Precisão:** `{prec:.2f}`
- **Recall:** `{rec:.2f}`
- **F1-score:** `{f1:.2f}`
""")

# Matriz de Confusão
st.subheader("📉 Matriz de Confusão")
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Não", "Sim"], yticklabels=["Não", "Sim"], ax=ax)
ax.set_xlabel("Previsto")
ax.set_ylabel("Real")
st.pyplot(fig)

# Previsão interativa
st.sidebar.subheader("🌡️ Nova Previsão Manual")
temp = st.sidebar.slider("Temperatura (°C)", 10.0, 45.0, 25.0)
umid = st.sidebar.slider("Umidade (%)", 10.0, 100.0, 60.0)
chuva = st.sidebar.slider("Chuva (mm)", 0.0, 300.0, 50.0)

amostra = pd.DataFrame([[temp, umid, chuva]], columns=["temperature", "humidity", "rainfall"])
predito = modelo.predict(amostra)[0]

st.sidebar.markdown(f"### 💧 Irrigação: **{'Sim' if predito == 1 else 'Não'}**")

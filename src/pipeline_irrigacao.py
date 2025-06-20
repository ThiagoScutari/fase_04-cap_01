
import os
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho para o CSV original
csv_path = os.path.join("..", "tests", "Crop_recommendation.csv")

# Carregar os dados
df = pd.read_csv(csv_path)
df_reduzido = df[["temperature", "humidity", "rainfall"]].copy()

# Funções para obter probabilidade por faixa
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

# Calcular a média das probabilidades e classificar
def classificar_irrigacao(row):
    p1 = prob_umidade(row["humidity"])
    p2 = prob_chuva(row["rainfall"])
    p3 = prob_temperatura(row["temperature"])
    media = np.mean([p1, p2, p3])
    return "Sim" if media > 0.5 else "Nao"

# Aplicar a lógica
df_reduzido["irrigando"] = df_reduzido.apply(classificar_irrigacao, axis=1)

# Separar X e y
X = df_reduzido[["temperature", "humidity", "rainfall"]]
y = df_reduzido["irrigando"].map({"Nao": 0, "Sim": 1})

# Aplicar SMOTE
smote = SMOTE(random_state=42)
X_bal, y_bal = smote.fit_resample(X, y)

# Divisão em treino/teste
X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.25, random_state=42)

# Função para treinar e avaliar modelo
def avaliar_modelo(modelo, nome):
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n📌 Modelo: {nome}")
    print(f"Acurácia:  {acc:.2f}")
    print(f"Precisão:  {prec:.2f}")
    print(f"Recall:    {rec:.2f}")
    print(f"F1-score:  {f1:.2f}")

    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Não", "Sim"], yticklabels=["Não", "Sim"])
    plt.title(f"Matriz de Confusão - {nome}")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.show()

# Avaliação dos modelos
avaliar_modelo(DecisionTreeClassifier(random_state=42), "Decision Tree")
avaliar_modelo(RandomForestClassifier(random_state=42), "Random Forest")
avaliar_modelo(LogisticRegression(max_iter=1000), "Logistic Regression")

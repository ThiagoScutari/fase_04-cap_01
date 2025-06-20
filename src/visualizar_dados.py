import os
import sqlite3
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

# Caminhos do projeto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENSORES_DB = os.path.join(PROJECT_ROOT, "database", "sensores.db")
WEBDATA_DB = os.path.join(PROJECT_ROOT, "database", "webdata.db")
TESTS_CSV = os.path.join(PROJECT_ROOT, "tests", "Crop_recommendation.csv")

def carregar_dados(db_path, tabela):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
    conn.close()
    return df

def exibir_tabela(df, titulo):
    print(f"\n{titulo}")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def resumo_estatistico(df, campos):
    print("\nResumo estatístico:")
    print(df[campos].describe())

def gerar_graficos():
    df = pd.read_csv(TESTS_CSV)
    df.rename(columns={"label": "evento"}, inplace=True)

    # 1. Heatmap
    correlacoes = df.groupby("evento")[["temperature", "humidity", "rainfall"]].mean().corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlacoes, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Mapa de Calor das Correlações (Temperatura, Umidade, Chuva)")
    plt.tight_layout()
    plt.show()

    # 2. Barplot: Umidade por cultura
    plt.figure(figsize=(12, 6))
    media_umidade = df.groupby("evento")["humidity"].mean().sort_values(ascending=False)
    sns.barplot(x=media_umidade.index, y=media_umidade.values, palette="Blues_r")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Umidade Média")
    plt.title("Umidade Média por Cultura")
    plt.tight_layout()
    plt.show()

    # 3. Scatterplot: Chuva
    plt.figure(figsize=(12, 6))
    sns.stripplot(data=df, x="evento", y="rainfall", jitter=True, palette="Greens")
    plt.xticks(rotation=45, ha="right")
    plt.title("Distribuição da Chuva por Cultura")
    plt.ylabel("Chuva (mm)")
    plt.tight_layout()
    plt.show()

    # 4. Lineplots separados: Temperatura / Umidade / Chuva por Cultura (visuais lado a lado)
    culturas_ordenadas = df.groupby("evento")[["temperature", "humidity", "rainfall"]].mean().sort_values(by="temperature").index
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharex=True)

    sns.lineplot(ax=axes[0], data=df, x="evento", y="temperature", estimator="mean", ci=None)
    axes[0].set_title("Temperatura Média por Cultura")
    axes[0].tick_params(axis='x', rotation=90)

    sns.lineplot(ax=axes[1], data=df, x="evento", y="humidity", estimator="mean", ci=None)
    axes[1].set_title("Umidade Média por Cultura")
    axes[1].tick_params(axis='x', rotation=90)

    sns.lineplot(ax=axes[2], data=df, x="evento", y="rainfall", estimator="mean", ci=None)
    axes[2].set_title("Chuva Média por Cultura")
    axes[2].tick_params(axis='x', rotation=90)

    plt.tight_layout()
    plt.show()  # Mostra os três subplots juntos

    # 5. Gráfico único com 3 linhas sobrepostas
    df_grouped = df.groupby("evento")[["temperature", "humidity", "rainfall"]].mean().loc[culturas_ordenadas]
    df_grouped.reset_index(inplace=True)

    plt.figure(figsize=(14, 6))
    plt.plot(df_grouped["evento"], df_grouped["temperature"], label="Temperatura", marker="o")
    plt.plot(df_grouped["evento"], df_grouped["humidity"], label="Umidade", marker="s")
    plt.plot(df_grouped["evento"], df_grouped["rainfall"], label="Chuva", marker="^")

    plt.xticks(rotation=90)
    plt.ylabel("Média")
    plt.title("Comparativo: Temperatura, Umidade e Chuva por Cultura")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("Qual base de dados deseja visualizar?")
    print("[1] sensores.db (leitura dos sensores)")
    print("[2] webdata.db (dados obtidos da web)")
    print("[3] Análises gráficas (Crop_recommendation.csv)")
    escolha = input("Digite 1, 2 ou 3: ").strip()

    if escolha == "1":
        df = carregar_dados(SENSORES_DB, "leituras")
        if df.empty:
            print("Nenhum dado em sensores.db")
            return
        exibir_tabela(df.tail(10), "Últimas Leituras dos Sensores")
        resumo_estatistico(df, ["umidade", "ph"])

        irrigando = df[df["irrigando"] == "Sim"]
        if not irrigando.empty:
            exibir_tabela(irrigando.tail(5), "Últimas com Irrigação Ativa")

    elif escolha == "2":
        df = carregar_dados(WEBDATA_DB, "web_data")
        if df.empty:
            print("Nenhum dado em webdata.db")
            return
        exibir_tabela(df.tail(10), "Últimos Dados Web Importados")
        resumo_estatistico(df, ["temperatura", "umidade", "chuva"])

    elif escolha == "3":
        gerar_graficos()

    else:
        print("Escolha inválida. Execute novamente e digite 1, 2 ou 3.")

if __name__ == "__main__":
    main()

import os
import sqlite3
import pandas as pd
from tabulate import tabulate

# Caminhos do projeto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENSORES_DB = os.path.join(PROJECT_ROOT, "database", "sensores.db")
WEBDATA_DB = os.path.join(PROJECT_ROOT, "database", "webdata.db")

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

def main():
    print("Qual base de dados deseja visualizar?")
    print("[1] sensores.db (leitura dos sensores)")
    print("[2] webdata.db (dados obtidos da web)")
    escolha = input("Digite 1 ou 2: ").strip()

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

    else:
        print("Escolha inválida. Execute novamente e digite 1 ou 2.")

if __name__ == "__main__":
    main()

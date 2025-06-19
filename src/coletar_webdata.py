import os
import sqlite3
import pandas as pd
from datetime import datetime

# --- Caminhos de projeto ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "webdata.db")
CSV_PATH = os.path.join(PROJECT_ROOT, "tests", "Crop_recommendation.csv")

# --- Criação da tabela no novo banco ---
def inicializar_banco():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperatura REAL,
            umidade REAL,
            chuva REAL,
            evento TEXT
        )
    ''')
    conn.commit()
    return conn

# --- Inserção de dados vindos do CSV ---
def importar_csv_para_banco(csv_path, conn, limite=1000):
    df = pd.read_csv(csv_path)

    # Verifica se colunas esperadas existem
    colunas_esperadas = ['temperature', 'humidity', 'rainfall', 'label']
    if not all(col in df.columns for col in colunas_esperadas):
        print("CSV não tem o formato esperado.")
        return

    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for i, row in df.head(limite).iterrows():
        cursor.execute('''
            INSERT INTO web_data (timestamp, temperatura, umidade, chuva, evento)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            now,
            row['temperature'],
            row['humidity'],
            row['rainfall'],
            row['label']
        ))
    conn.commit()
    print(f"{limite} registros importados para webdata.db")

def main():
    conn = inicializar_banco()
    importar_csv_para_banco(CSV_PATH, conn)
    conn.close()

if __name__ == "__main__":
    main()

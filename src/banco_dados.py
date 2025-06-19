import sqlite3
import serial
from datetime import datetime
import os

# --- Caminhos ---
DB_PATH = os.path.join("database", "sensores.db")

# --- Configuração da porta serial RFC2217 (vinda do ESP32 via PlatformIO) ---
SERIAL_URL = 'rfc2217://localhost:4000'
BAUDRATE = 115200

# --- Criação do banco e da tabela ---
def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            umidade REAL,
            ph REAL,
            fosforo TEXT,
            potassio TEXT,
            irrigando TEXT
        )
    ''')
    conn.commit()
    return conn

# --- Inserção dos dados no banco ---
def inserir_leitura(conn, dados):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leituras (timestamp, umidade, ph, fosforo, potassio, irrigando)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()

# --- Loop principal de leitura da serial e gravação no banco ---
def monitorar_serial():
    conn = inicializar_banco()

    try:
        ser = serial.serial_for_url(SERIAL_URL, baudrate=BAUDRATE, timeout=1)
        print("Conectado à serial RFC2217 (porta 4000)")
        print("Gravando dados no banco...")
    except Exception as e:
        print(f"Erro ao conectar à serial: {e}")
        return

    try:
        while True:
            linha = ser.readline().decode('utf-8').strip()

            # Ignorar cabeçalho ou linha vazia
            if linha == "" or linha.startswith("timestamp") or "Tempo(ms):" in linha:
                continue

            try:
                # Exemplo: 2025-06-19 19:52:31,57.5,6.3,Sim,Nao,Sim
                partes = linha.split(',')

                if len(partes) != 6:
                    continue  # linha inválida

                timestamp, umidade, ph, fosforo, potassio, irrigando = partes
                dados = (timestamp.strip(), float(umidade), float(ph), fosforo.strip(), potassio.strip(), irrigando.strip())

                inserir_leitura(conn, dados)
                print(f"Inserido: {dados}")

            except Exception as e:
                print(f"Erro ao processar linha: {linha}\n{e}")
                continue

    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
    finally:
        conn.close()
        ser.close()
        print("Conexão com banco e serial encerradas.")

# --- Execução direta ---
if __name__ == '__main__':
    monitorar_serial()

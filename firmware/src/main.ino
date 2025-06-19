#include <WiFi.h>
#include "secrets.h"           // Contém WIFI_SSID e WIFI_PASSWORD
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// --- Definições de pinos ---
#define DHTPIN 27
#define DHTTYPE DHT22
#define P_BUTTON_PIN 12
#define K_BUTTON_PIN 14
#define LDR_PIN 34
#define RELAY_PIN 26
#define LED_PIN 25

// --- Instâncias ---
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// --- Parâmetros da lógica ---
const float PH_MIN = 5.5;
const float PH_MAX = 7.5;
const float UMIDADE_LIMITE = 60.0;

void conectarWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando ao Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Conectado ao Wi-Fi!");
  configTime(-3 * 3600, 0, "pool.ntp.org");  // Fuso horário de Brasília (UTC-3)
}

void setup() {
  Serial.begin(115200);

  // Conexão Wi-Fi (necessária para RFC2217 funcionar no Wokwi)
  conectarWiFi();

  // Pinos
  pinMode(P_BUTTON_PIN, INPUT_PULLUP);
  pinMode(K_BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Sensores
  dht.begin();
  lcd.init();
  lcd.backlight();

  Serial.println("timestamp,umidade,ph,fosforo,potassio,irrigando");
}

void loop() {
  // Leitura dos sensores
  bool fosforo = digitalRead(P_BUTTON_PIN) == LOW;
  bool potassio = digitalRead(K_BUTTON_PIN) == LOW;
  int ldrValue = analogRead(LDR_PIN);
  float ph = map(ldrValue, 0, 4095, 0, 14); // Simulação de pH
  float umidade = dht.readHumidity();

  // Lógica de irrigação
  bool precisaIrrigar = false;
  if (!isnan(umidade) && ph >= PH_MIN && ph <= PH_MAX && (!fosforo || !potassio)) {
    if (umidade < UMIDADE_LIMITE) {
      precisaIrrigar = true;
    }
  }

  // Ações
  digitalWrite(RELAY_PIN, precisaIrrigar ? HIGH : LOW);
  digitalWrite(LED_PIN, precisaIrrigar ? HIGH : LOW);

  // LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Umid:");
  lcd.print(umidade, 0);
  lcd.print("% pH:");
  lcd.print(ph, 1);

  lcd.setCursor(0, 1);
  lcd.print("P:");
  lcd.print(fosforo ? "S" : "N");
  lcd.print(" K:");
  lcd.print(potassio ? "S" : "N");
  lcd.print(" ");
  lcd.print(precisaIrrigar ? "Bomb:ON" : "Bomb:OFF");

  // Envio via Serial
struct tm timeinfo;
if (!getLocalTime(&timeinfo)) {
  Serial.print("1970-01-01 00:00:00"); // fallback
} else {
  char timestamp[20];
  strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", &timeinfo);
  Serial.print(timestamp);
}
  Serial.print(",");
  Serial.print(umidade, 1);
  Serial.print(",");
  Serial.print(ph, 1);
  Serial.print(",");
  Serial.print(fosforo ? "Sim" : "Nao");
  Serial.print(",");
  Serial.print(potassio ? "Sim" : "Nao");
  Serial.print(",");
  Serial.println(precisaIrrigar ? "Sim" : "Nao");

  delay(2000);
}

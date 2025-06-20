
# 🌾 FarmTech Solutions — Sistema Inteligente de Irrigação com Machine Learning

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="docs/fiap.jpeg" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>

> Projeto desenvolvido como parte da **Fase 4** do curso da **FIAP** — com o diferencial de ter **unificado entregas pendentes da Fase 3**, elevando a entrega a um novo nível de complexidade, completude e inovação. Nota máxima é o mínimo esperado!

---

## 📌 Grupo: 37

## 👨‍🎓 Integrantes:
- Thiago Scutari – RM562831 | thiago.scutari@outlook.com  
- Henrique Ribeiro Siqueira – RM565044 | henrique.ribeiro1201@gmail.com  
- Mariana Cavalcante Oliveira – RM561678 | mari.kvalcant@gmail.com  

## 👩‍🏫 Professores:

### Tutor  
- Leonardo Ruiz Orabona  

### Coordenador  
- Andrei Godoi Chiovato  


---

## 📌 Descrição do Projeto

Este projeto simula, por meio de sensores virtuais conectados a um ESP32, um sistema inteligente de irrigação agrícola que:

- Lê dados de sensores de umidade, pH, fósforo e potássio;
- Exibe métricas em tempo real em um display LCD I2C;
- Aciona automaticamente uma bomba d’água com base em critérios definidos;
- Armazena os dados em um banco SQLite (`sensores.db`);
- Complementa os dados com informações climáticas simuladas (`webdata.db`);
- Aplica algoritmos de *Machine Learning* para prever a necessidade de irrigação;
- Disponibiliza tudo em um painel Streamlit totalmente interativo.

> 💡 **Destaque:** Este projeto cobre **do hardware simulado à inteligência preditiva**, com registro, visualização, predição e painel integrado. Tudo em um repositório unificado.

---

## 🧪 Tecnologias e Bibliotecas

| Tecnologia          | Finalidade                              |
|---------------------|------------------------------------------|
| ESP32 + Wokwi       | Simulação do circuito físico             |
| C++ / PlatformIO     | Leitura dos sensores + lógica de controle |
| Python + SQLite     | Banco de dados e processamento de dados |
| Pandas, Seaborn     | Análise estatística e visualização       |
| Scikit-learn        | Aplicação de Machine Learning            |
| Streamlit           | Interface interativa para o usuário      |

---

## 🔧 Componentes e Circuito

<p align="center">
  <img src="docs/circuitos_wokwi.png" width="600">
</p>

### 📟 Display LCD em tempo real

| Estado da bomba | Exemplo de leitura |
|-----------------|--------------------|
| **Desligada**   | ![bomba off](docs/bomba_desligada.png) |
| **Ligada**      | ![bomba on](docs/bomba_ligada.png)      |

---

## 📉 Monitoramento Serial

<p align="center">
  <img src="docs/monitor_serial.png" width="700">
</p>

---

## 🧬 Machine Learning Aplicado

- Simulamos uma base com mais de 4.000 registros.
- Utilizamos:
  - `DecisionTreeClassifier`
  - `RandomForestClassifier`
  - `LogisticRegression`
- Balanceamos os dados com **SMOTE** para evitar viés nos modelos.
- Aplicamos uma **lógica probabilística personalizada** baseada em faixas de temperatura, umidade e chuva para classificar a irrigação (`Sim` / `Não`).

---

## 📊 Análise Gráfica dos Dados

### 🔥 Heatmap de Correlação

<p align="center">
  <img src="docs/heat_map.png" width="400">
</p>

### 📊 Umidade Média por Cultura

<p align="center">
  <img src="docs/bar_plot.png" width="600">
</p>

### 📈 Temperatura / Umidade / Chuva por Cultura

<p align="center">
  <img src="docs/line_plot1.png" width="800">
</p>

### 📉 Comparativo de Linhas Sobrepostas

<p align="center">
  <img src="docs/line_plot2.png" width="800">
</p>

### 🌧️ Distribuição da Chuva

<p align="center">
  <img src="docs/scatter_plot.png" width="600">
</p>

---

## 🖥️ Visualização Terminal com Pandas

<p align="center">
  <img src="docs/visualizar_dados.png" width="500">
</p>

---

## Organização do Repositório

```
📦 trabalho_2/
├── docs/                  # Imagens e documentação do projeto
├── src/                   # Códigos-fonte: C++, Python, Streamlit
├── database/              # sensores.db e webdata.db
├── tests/                 # Base simulada: Crop_recommendation.csv
└── README.md              # Este arquivo
```

---

## 🌐 Painel Streamlit

- Interface amigável para prever se a irrigação será ativada com base em:
  - Temperatura (slider)
  - Umidade
  - Chuva
- Escolha do modelo em tempo real;
- Visualização da matriz de confusão.

---

## ⚠️ Nota sobre o projeto

> ❗**Importante:** A Fase 3 não foi entregue anteriormente. Este projeto incorpora **toda a estrutura esperada da Fase 3 + Fase 4**, com:
- Sensoriamento completo;
- Banco de dados e persistência;
- Visualização e análise;
- Predição e Streamlit.

---

## ✅ Conclusões

Este projeto demonstrou de forma prática e integrada o uso de diversas tecnologias para resolver um problema real no contexto da agricultura inteligente:

- **Circuito completo no Wokwi com ESP32**: simulação funcional da leitura de sensores como umidade, pH, fósforo e potássio, além do controle de relé e visualização no display LCD.
- **Persistência de dados com SQLite**: registro contínuo das leituras dos sensores e dos dados obtidos da web, garantindo histórico confiável e acessível para análise futura.
- **Aplicação de Machine Learning**: foram treinados três modelos (Decision Tree, Random Forest e Logistic Regression), todos avaliados com métricas como **acurácia**, **F1-score** e **matriz de confusão**, garantindo previsões consistentes sobre a necessidade de irrigação.
- **Análise exploratória profunda**: gráficos de correlação, médias e distribuições que revelam padrões e comportamentos entre variáveis como temperatura, umidade e chuva em diferentes culturas.
- **Interface interativa com Streamlit**: painel visual onde o usuário pode ajustar os parâmetros dos sensores, escolher o modelo de ML, visualizar os resultados em tempo real e entender a decisão da irrigação com base nas entradas fornecidas.

A junção de hardware simulado, coleta realista de dados, aprendizado de máquina e interface amigável representa um **MVP robusto**, versátil e com forte aplicabilidade no campo do agronegócio.


---

## Referências

- [Wokwi ESP32 Simulador](https://wokwi.com)
- [Scikit-learn](https://scikit-learn.org/)
- [FIAP ON](https://on.fiap.com.br)
- [Kaggle](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset?resource=download)
- [ChatGPT](https://chatgpt.com/)
---

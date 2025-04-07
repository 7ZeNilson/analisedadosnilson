# Análise RFM com Python para Farmácia - Meu Projeto de Portfolio

Olá! Neste projeto, compartilho o processo de desenvolvimento de uma análise de Recência, Frequência e Valor Monetário (RFM) para clientes de uma farmácia. O objetivo principal foi segmentar a base de clientes com base em seu comportamento de compra, possibilitando a criação de estratégias de marketing mais eficazes e personalizadas.

## 🛠️ Ferramentas e Tecnologias que Utilizei

Para este projeto, utilizei as seguintes ferramentas e bibliotecas em Python:

* **Python:** A linguagem de programação principal onde todo o código foi desenvolvido.
* **`oracledb`:** Esta biblioteca foi essencial para estabelecer a conexão e interagir com o banco de dados Oracle, onde os dados transacionais da farmácia estão armazenados.
* **`pandas`:** Uma poderosa biblioteca para manipulação e análise de dados. Usei seus DataFrames para organizar e trabalhar com os dados extraídos do banco de dados.
* **`matplotlib`:** A biblioteca fundamental para a criação de gráficos e visualizações de dados, permitindo a representação visual dos resultados da análise RFM.
* **`seaborn`:** Construída sobre o Matplotlib, o Seaborn me proporcionou uma interface de alto nível para criar gráficos estatísticos mais atraentes e informativos com menos código.

## ⚙️ Preparação do Ambiente

O primeiro passo foi garantir que todas as ferramentas necessárias estivessem configuradas. Isso incluiu:

1.  **Instalação do Python:** Certifiquei-me de ter uma versão recente do Python instalada no meu ambiente de desenvolvimento.
2.  **Instalação das Bibliotecas:** Utilizei o `pip` para instalar as bibliotecas `oracledb`, `pandas`, `matplotlib` e `seaborn` através do comando:
    ```bash
    pip install oracledb pandas matplotlib seaborn
    ```
3.  **Configuração do Acesso ao Banco de Dados Oracle:** Obtive as credenciais e informações de conexão para o banco de dados Oracle que continha os dados de transação da farmácia. Isso envolveu o DSN (Data Source Name), nome de usuário e senha.

## 🚀 Etapas da Análise RFM

Aqui descrevo o passo a passo de como conduzi a análise RFM:

### 1. Conectando ao Banco de Dados Oracle

O primeiro passo crucial foi estabelecer uma conexão com o banco de dados Oracle. Utilizei a biblioteca `oracledb` para isso, configurando o DSN e fornecendo as credenciais de acesso:

```python
import oracledb

# 🔹 Configuração da Conexão com o Oracle
dsn = oracledb.makedsn("localhost", "0000", service_name="xx")
conn = oracledb.connect(user="xxxxx", password="xxxxx", dsn=dsn)


Neste ponto, a variável conn representa a conexão ativa com o banco de dados, permitindo que eu execute consultas SQL.

2. Extraindo os Dados Relevantes com SQL
Para calcular as métricas RFM, precisei extrair os dados de transação dos clientes. Elaborei uma consulta SQL que calculava a última data de compra (Recência), a contagem total de transações (Frequência) e o valor total gasto (Valor Monetário) para cada cliente:

Python

# 🔹 Consulta SQL para obter os dados de RFM
query = """
WITH RFM AS (
    SELECT
        t.ID_CLIENTE,
        MAX(t.DATA_VENDA) AS ULTIMA_COMPRA,
        COUNT(t.ID_TRANSACAO) AS FREQUENCIA,
        SUM(t.TOTAL_PRODUTO) AS VALOR_MONETARIO
    FROM SYSTEM.F_TRANSACOES_FARMACIA t
    GROUP BY t.ID_CLIENTE
)
SELECT
    r.ID_CLIENTE,
    ROUND(TO_NUMBER(SYSDATE - r.ULTIMA_COMPRA)) AS RECENCIA,
    r.FREQUENCIA,
    r.VALOR_MONETARIO
FROM RFM r
ORDER BY RECENCIA ASC
"""
Essa consulta utiliza uma subconsulta (WITH RFM AS (...)) para agregar os dados por ID_CLIENTE e, em seguida, calcula a diferença em dias entre a data atual (SYSDATE) e a última compra para obter a Recência.

3. Carregando os Dados no Pandas DataFrame
Com os dados extraídos através da consulta SQL, o próximo passo foi carregá-los em um DataFrame do Pandas. Isso facilitou a manipulação e análise dos dados em Python:

Python

import pandas as pd

# 🔹 Carregar os dados no Pandas
df_rfm = pd.read_sql(query, conn)
A função pd.read_sql() executou a consulta no banco de dados através da conexão conn e armazenou o resultado no DataFrame df_rfm.

4. Encerrando a Conexão com o Banco de Dados
Após a extração dos dados, foi importante fechar a conexão com o banco de dados Oracle para liberar os recursos:

Python

# 🔹 Fechar a conexão
conn.close()
5. Visualização da Distribuição da Recência
Para entender como os clientes estão distribuídos em relação ao tempo desde a última compra, criei um histograma utilizando a biblioteca seaborn:

Python

import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 Configuração do Estilo dos Gráficos
sns.set_style("whitegrid")

# 🔹 Gráfico 1: Distribuição da Recência
plt.figure(figsize=(10, 5))
sns.histplot(df_rfm['RECENCIA'], bins=30, kde=True, color='blue')
plt.title("Distribuição da Recência dos Clientes")
plt.xlabel("Recência (dias)")
plt.ylabel("Número de Clientes")
plt.grid(True)
plt.show()
Este gráfico me permitiu visualizar a concentração de clientes em diferentes faixas de recência, identificando a proporção de clientes ativos e inativos.

6. Análise da Relação entre Frequência e Valor Monetário
Para explorar a relação entre o número de compras e o valor total gasto pelos clientes, utilizei um gráfico de dispersão:

Python

# 🔹 Gráfico 2: Scatterplot Frequência x Valor Monetário
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df_rfm, x="FREQUENCIA", y="VALOR_MONETARIO", color='green', alpha=0.6)
plt.title("Frequência x Valor Monetário")
plt.xlabel("Frequência (Número de Compras)")
plt.ylabel("Valor Monetário Total (R$)")
plt.grid(True)
plt.show()
Este gráfico ajudou a identificar clientes com alta frequência de compra e alto valor gasto, que são geralmente os clientes mais valiosos para o negócio.

7. Visualização da Distribuição das Variáveis RFM com Boxplots
Para obter uma visão geral da distribuição de cada uma das métricas RFM (Recência, Frequência e Valor Monetário), utilizei boxplots:

Python

# 🔹 Gráfico 3: Boxplot das Variáveis RFM
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.boxplot(y=df_rfm['RECENCIA'], color='skyblue')
plt.title("Boxplot da Recência")
plt.ylabel("Recência (dias)")
plt.grid(True)

plt.subplot(1, 3, 2)
sns.boxplot(y=df_rfm['FREQUENCIA'], color='lightcoral')
plt.title("Boxplot da Frequência")
plt.ylabel("Frequência")
plt.grid(True)

plt.subplot(1, 3, 3)
sns.boxplot(y=df_rfm['VALOR_MONETARIO'], color='lightgreen')
plt.title("Boxplot do Valor Monetário")
plt.ylabel("Valor Monetário (R$)")
plt.grid(True)

plt.tight_layout()
plt.show()
Os boxplots forneceram informações sobre a mediana, quartis e possíveis outliers para cada métrica, ajudando a entender a dispersão dos dados.

📊 Resultados e Próximos Passos
Através desta análise, consegui visualizar a distribuição dos clientes em relação à recência de compra, a relação entre a frequência e o valor monetário de suas compras, e a distribuição geral de cada uma das métricas RFM.

![image](https://github.com/user-attachments/assets/64082629-b679-48b9-a2f7-f382ef517bd7)

![image](https://github.com/user-attachments/assets/2255e3e4-1d2c-4316-a60c-37902b4cdd88)


Os próximos passos lógicos para este projeto seriam:

Segmentação de Clientes: Utilizar os valores de RFM para segmentar os clientes em grupos distintos (por exemplo, clientes "ouro", "prata", "bronze", clientes "em risco de churn"). Isso pode ser feito através da definição de limites (thresholds) para cada métrica ou utilizando algoritmos de clustering.
Desenvolvimento de Estratégias de Marketing Personalizadas: Com os segmentos de clientes definidos, seria possível criar campanhas de marketing direcionadas para cada grupo. Por exemplo, oferecer descontos para clientes inativos para incentivá-los a retornar ou recompensar clientes de alto valor.
Integração com Ferramentas de CRM: Integrar os resultados da segmentação RFM com sistemas de CRM (Customer Relationship Management) para automatizar as ações de marketing e o acompanhamento dos clientes.
Este projeto demonstra minha capacidade de conectar-me a bancos de dados, manipular e analisar dados utilizando Python e suas bibliotecas, e visualizar os resultados de forma clara e informativa. A análise RFM é uma técnica poderosa para entender o comportamento do cliente e pode gerar insights valiosos para a tomada de decisões de negócios. Agradeço por explorar meu trabalho!

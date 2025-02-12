import mysql.connector # type: ignore
import pandas as pd
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
excel_file = os.path.join(current_dir, "cotas_produtos.xlsx")

df = pd.read_excel(excel_file)

df['data_cotacao'] = pd.to_datetime(df['data_cotacao'], errors='coerce')
df['data_cotacao'] = df['data_cotacao'].fillna(pd.Timestamp('1900-01-01'))
df['data_cotacao'] = df['data_cotacao'].dt.strftime('%Y-%m-%d')

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistema_teste"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS totalidade_produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT,
    nome_produto VARCHAR(255),
    categoria_produto VARCHAR(255),
    preco_unitario DECIMAL(10, 2),
    quantidade INT,
    data_cotacao DATE,
    preco_total DECIMAL(10, 2)
)
""")

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO totalidade_produtos (produto_id, nome_produto, categoria_produto, preco_unitario, quantidade, data_cotacao, preco_total)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['produto_id'], row['nome_produto'], row['categoria_produto'], row['preco_unitario'], row['quantidade'], row['data_cotacao'], row['preco_total']))

conn.commit()

cursor.close()
conn.close()

print("Dados importados com sucesso!")
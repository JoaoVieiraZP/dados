import mysql.connector # type: ignore
import pandas as pd
import openpyxl
from openpyxl.styles import Alignment
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
excel_file = os.path.join(current_dir, "cotas_produtos.xlsx")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistema_teste"
)

query = """
SELECT 
    cotas.id, 
    cotas.produto_id, 
    produtos.nome AS nome_produto, 
    produtos.categoria AS categoria_produto, 
    cotas.preco_unitario, 
    cotas.quantidade, 
    cotas.data_cotacao
FROM cotas
JOIN produtos ON cotas.produto_id = produtos.id;
"""

df = pd.read_sql(query, conn)
conn.close()

df['preco_total'] = df['preco_unitario'] * df['quantidade']
print(df)

df.to_excel(excel_file, index=False)

wb = openpyxl.load_workbook(excel_file)
sheet = wb.active

for col in sheet.columns:
    max_length = 0
    column = col[0].column_letter
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
            cell.alignment = Alignment(horizontal="right")
        except:
            pass
    adjusted_width = (max_length + 2)
    sheet.column_dimensions[column].width = adjusted_width

wb.save(excel_file)

print(f"Arquivo Excel '{excel_file}' gerado com sucesso com colunas ajustadas e alinhadas!")
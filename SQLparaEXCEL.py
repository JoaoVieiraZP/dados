import mysql.connector
import pandas as pd
import openpyxl
from openpyxl.styles import Alignment
import os

def export_mysql_table_to_excel(table_name_to_export, output_excel_name, db_config):
    """
    Exporta uma tabela específica do MySQL para um arquivo Excel,
    ajustando automaticamente a largura das colunas e o alinhamento.

    Args:
        table_name_to_export (str): O nome da tabela no MySQL a ser exportada.
        output_excel_name (str): O nome do arquivo Excel de saída (ex: "meus_dados.xlsx").
        db_config (dict): Dicionário com as configurações de conexão do MySQL.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    excel_file = os.path.join(current_dir, output_excel_name)

    conn = None # Inicializa conn para o bloco finally
    try:
        conn = mysql.connector.connect(**db_config)
        print(f"Conectado ao banco de dados '{db_config['database']}'.")

        # Query para selecionar todos os dados da tabela escolhida
        query = f"SELECT * FROM {table_name_to_export};"
        print(f"Executando query: {query}")

        df = pd.read_sql(query, conn)
        print(f"Dados da tabela '{table_name_to_export}' lidos com sucesso. {len(df)} linhas encontradas.")

        if df.empty:
            print(f"A tabela '{table_name_to_export}' está vazia. Nenhum dado para exportar para Excel.")
            return

        # Exportar para Excel
        df.to_excel(excel_file, index=False)
        print(f"Dados exportados para '{excel_file}'. Iniciando ajustes de formatação...")

        # Ajustes de formatação com openpyxl
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for col in sheet.columns:
            max_length = 0
            column_letter = col[0].column_letter
            for cell in col:
                try:
                    # Converte para string antes de calcular o comprimento
                    cell_value_str = str(cell.value) if cell.value is not None else ""
                    if len(cell_value_str) > max_length:
                        max_length = len(cell_value_str)
                    # Alinha todas as células à direita
                    cell.alignment = Alignment(horizontal="right")
                except Exception as e:
                    # Captura qualquer erro durante o processamento da célula
                    pass # Apenas ignora e continua

            # +2 para um pequeno padding
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column_letter].width = adjusted_width

        wb.save(excel_file)
        print(f"Arquivo Excel '{excel_file}' gerado e formatado com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        if err.errno == 1146: # ER_NO_SUCH_TABLE
            print(f"A tabela '{table_name_to_export}' não existe no banco de dados '{db_config['database']}'.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

# --- Configurações e Execução ---
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "", # Deixe em branco se não houver senha
        "database": "sistema_teste"
    }

    # Definimos o nome da tabela no MySQL que queremos exportar
    table_to_export = "tabela_teste"
    # Definimos o nome do arquivo Excel de saída
    output_excel_filename = "teste_dos_testes.xlsx"

    print(f"\n--- Exportando a tabela '{table_to_export}' para '{output_excel_filename}' ---")
    export_mysql_table_to_excel(table_to_export, output_excel_filename, db_config)

    print("\nProcesso de exportação concluído.")
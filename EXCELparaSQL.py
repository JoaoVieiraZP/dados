import mysql.connector
import pandas as pd
import os

def import_excel_to_mysql(excel_file_path, db_config, table_name=None):
    """
    Importa dados de uma planilha Excel para um banco de dados MySQL,
    criando a tabela dinamicamente com base nas colunas do Excel.

    Args:
        excel_file_path (str): O caminho completo para o arquivo Excel.
        db_config (dict): Um dicionário com as configurações de conexão do MySQL
                          (host, user, password, database).
        table_name (str, optional): O nome da tabela no MySQL. Se None, o nome
                                    será derivado do nome do arquivo Excel.
    """
    try:
        # Leitura do arquivo Excel
        if not os.path.exists(excel_file_path):
            raise FileNotFoundError(f"O arquivo Excel não foi encontrado: {excel_file_path}")

        print(f"Lendo o arquivo Excel: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        print(f"Planilha '{os.path.basename(excel_file_path)}' lida com sucesso. {len(df)} linhas encontradas.")

        if df.empty:
            print("O DataFrame está vazio. Nenhuns dados para importar.")
            return

        # Determinar o nome da tabela no MySQL
        if table_name is None:
            # Pega o nome do arquivo sem a extensão e usa como nome da tabela
            table_name = os.path.splitext(os.path.basename(excel_file_path))[0]
            # Normaliza o nome para ser um nome de tabela SQL válido (e.g., espaços para underscores)
            table_name = table_name.lower().replace(" ", "_").replace("-", "_")
        
        print(f"Nome da tabela MySQL a ser criada/atualizada: '{table_name}'")

        # Conexão ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Conectado ao banco de dados MySQL.")

        # Mapeamento de tipos de dados Pandas para MySQL e geração da instrução CREATE TABLE
        column_definitions = []
        # Adicionar uma coluna de ID auto-incrementável por padrão
        column_definitions.append("id INT PRIMARY KEY AUTO_INCREMENT")

        for column, dtype in df.dtypes.items():
            column_name_sql = column.lower().replace(" ", "_").replace("-", "_") # Normalizar nome da coluna
            sql_type = "VARCHAR(255)" # Tipo padrão caso não seja reconhecido outro tipo

            if pd.api.types.is_integer_dtype(dtype):
                sql_type = "INT"
            elif pd.api.types.is_float_dtype(dtype) or pd.api.types.is_numeric_dtype(dtype):
                sql_type = "DECIMAL(18, 4)"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                sql_type = "DATETIME"
                # Convertendo para datetime se ainda não for e preenchendo NaT com valor padrão
                df[column] = pd.to_datetime(df[column], errors='coerce')
                # Para MySQL, DATETIME pode aceitar NULL, então o preenchimento é opcional e depende do requisito.
            elif pd.api.types.is_bool_dtype(dtype):
                sql_type = "BOOLEAN"

            # Evita duplicar a coluna 'id' se ela já existir no Excel e for mapeada
            if column_name_sql != 'id':
                column_definitions.append(f"{column_name_sql} {sql_type}")
            
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
        
        print(f"\nTentando criar/verificar tabela: {create_table_query}")
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Tabela '{table_name}' verificada/criada com sucesso.")

        # Inserção de Dados
        # Remove a coluna 'id' do DataFrame se ela existir, pois ela é auto-incrementável
        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        # Prepara a instrução INSERT dinamicamente
        columns_to_insert = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]
        placeholders = ', '.join(['%s'] * len(columns_to_insert))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns_to_insert)}) VALUES ({placeholders})"
        
        print(f"\nIniciando importação de {len(df)} linhas para '{table_name}'...")
        
        # Converte o DataFrame para uma lista de tuplas para inserção em massa
        # Trata valores de data/hora para o formato que o MySQL espera (string 'YYYY-MM-DD HH:MM:SS')
        data_to_insert = []
        for index, row in df.iterrows():
            row_values = []
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    row_values.append(None)
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    # Converte Timestamp do pandas para string no formato MySQL
                    row_values.append(value.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(value) else None)
                else:
                    row_values.append(value)
            data_to_insert.append(tuple(row_values))

        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        print(f"Dados importados com sucesso para a tabela '{table_name}'! Total de {cursor.rowcount} registros inseridos.")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        if err.errno == 1054:
            print("Verifique se os nomes das colunas no seu Excel correspondem aos esperados ou se há um erro de digitação.")
        elif err.errno == 1146:
            print("A tabela não existe. Ela deveria ter sido criada automaticamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
        print("Conexão com o banco de dados fechada.")

# --- Configurações e Execução ---
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Exemplo para o novo arquivo de teste (obs: substituir "tabela_teste" para o nome do arquivo)
    excel_file_test = os.path.join(current_dir, "tabela_teste.xlsx")

    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "sistema_teste"
    }

    print("\n--- Importando ---")
    # Chame a função de importação para o seu novo arquivo
    import_excel_to_mysql(excel_file_test, db_config)

    print("\nProcesso de importação concluído.")
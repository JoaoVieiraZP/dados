import mysql.connector
import pandas as pd
import os

def import_excel_to_mysql(excel_file_path, db_config, table_name=None, import_mode="append"):
    """
    Importa dados de uma planilha Excel para um banco de dados MySQL,
    criando a tabela dinamicamente com base nas colunas do Excel.

    Args:
        excel_file_path (str): O caminho completo para o arquivo Excel.
        db_config (dict): Um dicionário com as configurações de conexão do MySQL.
        table_name (str, optional): O nome da tabela no MySQL. Se None, o nome
                                    será derivado do nome do arquivo Excel.
        import_mode (str): O modo de importação. "append" (padrão) ou "overwrite".
    """
    conn = None 
    cursor = None 
    try:
        if not os.path.exists(excel_file_path):
            raise FileNotFoundError(f"O arquivo Excel não foi encontrado: {excel_file_path}")

        print(f"Lendo o arquivo Excel: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        print(f"Planilha '{os.path.basename(excel_file_path)}' lida com sucesso. {len(df)} linhas encontradas.")

        if df.empty:
            print("O DataFrame está vazio. Nenhuns dados para importar.")
            return

        if table_name is None:
            table_name = os.path.splitext(os.path.basename(excel_file_path))[0]
            table_name = table_name.lower().replace(" ", "_").replace("-", "_")
        
        print(f"Nome da tabela MySQL a ser criada/atualizada: '{table_name}'")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Conectado ao banco de dados MySQL.")

        # --- Lógica de TRUNCATE TABLE para modo "overwrite" ---
        if import_mode == "overwrite": 
            print(f"Modo de importação: SOBRESCREVER. Tentando truncar tabela '{table_name}'...")
            try:
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                table_exists = cursor.fetchone()
                if table_exists:
                    cursor.execute(f"TRUNCATE TABLE {table_name};")
                    conn.commit()
                    print(f"Tabela '{table_name}' truncada com sucesso.")
                else:
                    print(f"Tabela '{table_name}' não existe, será criada. Não há necessidade de truncar.")
            except mysql.connector.Error as err:
                print(f"Erro ao tentar truncar tabela (ignorado se a tabela não existir): {err}")
            except Exception as e:
                print(f"Erro inesperado ao tentar truncar tabela: {e}")
                raise 

        # Criação da tabela (sempre tenta criar IF NOT EXISTS)
        column_definitions = []
        column_definitions.append("id INT PRIMARY KEY AUTO_INCREMENT")

        for column, dtype in df.dtypes.items():
            column_name_sql = column.lower().replace(" ", "_").replace("-", "_") 
            sql_type = "VARCHAR(255)"

            if pd.api.types.is_integer_dtype(dtype):
                sql_type = "INT"
            elif pd.api.types.is_float_dtype(dtype) or pd.api.types.is_numeric_dtype(dtype):
                sql_type = "DECIMAL(18, 4)"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                sql_type = "DATETIME"
                df[column] = pd.to_datetime(df[column], errors='coerce')
            elif pd.api.types.is_bool_dtype(dtype):
                sql_type = "BOOLEAN"
            
            if column_name_sql != 'id':
                column_definitions.append(f"{column_name_sql} {sql_type}")
            
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
        
        print(f"\nTentando criar/verificar tabela: {create_table_query}")
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Tabela '{table_name}' verificada/criada com sucesso.")

        # Inserção de Dados
        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        columns_to_insert = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]
        placeholders = ', '.join(['%s'] * len(columns_to_insert))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns_to_insert)}) VALUES ({placeholders})"
        
        print(f"\nIniciando importação de {len(df)} linhas para '{table_name}'...")
        
        data_to_insert = []
        for index, row in df.iterrows():
            row_values = []
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    row_values.append(None)
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    row_values.append(value.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(value) else None)
                else:
                    row_values.append(value)
            data_to_insert.append(tuple(row_values))

        if data_to_insert:
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            print(f"Dados importados com sucesso para a tabela '{table_name}'! Total de {cursor.rowcount} registros inseridos.")
        else:
            print("Nenhum dado válido para inserir.")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
        raise 
    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        raise 
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        raise 
    finally:
        if cursor: 
            cursor.close()
        if conn:
            conn.close()
        print("Conexão com o banco de dados fechada.")
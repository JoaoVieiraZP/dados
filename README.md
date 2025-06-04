Sincronização Flexível entre MySQL e Excel
Este projeto oferece um conjunto de scripts Python projetados para facilitar a sincronização bidirecional e dinâmica entre um banco de dados MySQL e arquivos Excel. Ele permite que você extraia dados de qualquer tabela do seu MySQL para uma planilha Excel e, inversamente, importe dados de qualquer planilha Excel para uma nova tabela no seu banco de dados.

1. Script de Exportação: export_mysql_to_excel.py
Este script foi aprimorado para ser genérico, permitindo que você exporte qualquer tabela do seu banco de dados MySQL para um arquivo Excel com formatação automática.

Funcionalidades:
Conexão Dinâmica ao Banco de Dados: Conecta-se a um banco de dados MySQL (configurado para sistema_teste por padrão) usando credenciais configuráveis.
Exportação de Tabela Flexível: Você pode especificar o nome de qualquer tabela existente no seu banco de dados. O script constrói dinamicamente a consulta SELECT * FROM nome_da_tabela; para extrair todos os dados dela.
Processamento e Exportação: Os dados da tabela selecionada são lidos para um DataFrame do pandas.
Geração de Arquivo Excel Formatado: Os dados são exportados para um arquivo Excel com o nome que você definir. O script utiliza openpyxl para ajustar automaticamente a largura das colunas e alinhar o conteúdo à direita, garantindo uma visualização limpa e profissional.
Como Usar:
Salve o código do script de exportação como export_mysql_to_excel.py.

Configure suas credenciais MySQL no bloco db_config no final do arquivo.

No bloco if __name__ == "__main__":, especifique a tabela MySQL que deseja exportar e o nome do arquivo Excel de saída.

Python

# Exemplo de uso:
export_mysql_table_to_excel("nome_da_sua_tabela", "nome_do_arquivo_saida.xlsx", db_config)
Execute o script a partir do seu terminal (preferencialmente Anaconda Prompt se você usa Conda) com python export_mysql_to_excel.py.

2. Script de Importação: import_excel_to_mysql.py
Este script foi modificado para ser altamente flexível, permitindo que você importe dados de qualquer arquivo Excel e crie uma nova tabela no MySQL com base na estrutura da planilha.

Funcionalidades:
Leitura Dinâmica de Arquivos Excel: Lê dados de qualquer arquivo .xlsx que você especificar.
Criação de Tabela Dinâmica no MySQL:
Inspeciona as colunas e os tipos de dados do arquivo Excel.
Gera automaticamente uma instrução SQL CREATE TABLE IF NOT EXISTS com base nessas informações, criando uma nova tabela no MySQL.
Mapeia os tipos de dados do pandas (inferidos do Excel) para os tipos de dados correspondentes no MySQL (ex: inteiros para INT, números decimais para DECIMAL, datas para DATETIME, textos para VARCHAR).
Adiciona uma chave primária auto-incrementável (id INT PRIMARY KEY AUTO_INCREMENT) por padrão.
Tratamento de Dados: Converte datas e valores ausentes (NaN/NaT) para formatos compatíveis com MySQL (NULL ou data padrão).
Inserção Otimizada de Dados: Insere todos os dados do Excel na tabela MySQL recém-criada de forma eficiente, usando executemany para múltiplas inserções.
Como Usar:
Salve o código do script de importação como import_excel_to_mysql.py.

Configure suas credenciais MySQL no bloco db_config no final do arquivo.

No bloco if __name__ == "__main__":, especifique o caminho para o seu arquivo Excel de entrada.

Python

# Exemplo de uso:
excel_file_path = os.path.join(current_dir, "seu_arquivo_excel.xlsx")
import_excel_to_mysql(excel_file_path, db_config)
# Você também pode opcionalmente definir um nome de tabela específico no MySQL:
# import_excel_to_mysql(excel_file_path, db_config, table_name="nome_tabela_mysql")
Execute o script a partir do seu terminal (preferencialmente Anaconda Prompt se você usa Conda) com python import_excel_to_mysql.py.

Objetivo Geral do Projeto:
O objetivo principal deste projeto é fornecer ferramentas Python flexíveis e automatizadas para facilitar o fluxo de dados entre planilhas Excel e bancos de dados MySQL. Seja para gerar relatórios personalizados ou para importar conjuntos de dados variados, esses scripts eliminam a necessidade de manipulação manual e codificação fixa, tornando a gestão de dados mais eficiente e menos propensa a erros.
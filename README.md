## Resumo do Projeto

Este projeto contém dois scripts que facilitam a integração entre um banco de dados MySQL e um arquivo Excel, permitindo a extração de dados, a manipulação e a reintegração desses dados de volta ao banco.

### Funcionalidade do Primeiro Script (SQLparaEXCEL):
1. **Conexão com o Banco de Dados**: O script se conecta a um banco de dados MySQL local utilizando a biblioteca `mysql.connector`.
2. **Consulta SQL**: Executa uma consulta para recuperar dados das tabelas `cotas` e `produtos`, como informações sobre produtos e suas cotações.
3. **Processamento de Dados**: O `pandas` é usado para processar e calcular o preço total de cada produto (preço unitário multiplicado pela quantidade).
4. **Geração do Arquivo Excel**: Os dados processados são exportados para um arquivo Excel (`cotas_produtos.xlsx`), com ajustes automáticos nas larguras das colunas e alinhamento dos valores.

### Funcionalidade do Segundo Script (EXCELparaSQL):
O segundo script realiza a importação dos dados de volta para o banco de dados:
1. **Leitura do Arquivo Excel**: O script abre o arquivo Excel gerado pelo primeiro script e lê seus dados com o `pandas`.
2. **Tratamento de Data**: As datas são convertidas corretamente para o formato esperado no banco de dados, com valores ausentes sendo preenchidos com uma data padrão.
3. **Criação da Tabela**: O script cria uma tabela chamada `totalidade_produtos` no banco de dados, caso ela ainda não exista.
4. **Inserção dos Dados**: Insere os dados extraídos do arquivo Excel na tabela `totalidade_produtos` do banco de dados MySQL.

### Objetivo:
- O projeto facilita a extração de dados de cotações de produtos a partir de um banco de dados MySQL e a reintegração desses dados em forma de uma tabela de estoque detalhada.
- É útil para automatizar o processo de geração de relatórios e análise de dados de cotação, além de permitir uma fácil importação de dados para o banco de dados.

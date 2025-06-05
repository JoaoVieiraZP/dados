# Sincronizador MySQL & Excel

## Visão Geral do Projeto

Este projeto oferece um conjunto de scripts Python projetados para facilitar a **sincronização bidirecional e dinâmica entre um banco de dados MySQL e arquivos Excel**. Ele permite que você extraia dados de qualquer tabela do seu MySQL para uma planilha Excel e, inversamente, importe dados de qualquer planilha Excel para uma nova tabela no seu banco de dados.

Com uma interface gráfica (GUI) moderna e intuitiva, o aplicativo elimina a necessidade de conhecimentos de programação para realizar essas tarefas de integração de dados.

## Funcionalidades Principais

* **Interface Gráfica (GUI) Moderna:** Desenvolvida com `CustomTkinter` para uma experiência de usuário intuitiva e visualmente atraente.
* **Importação Flexível (Excel para MySQL):**
    * Lê dados de **qualquer arquivo Excel (.xlsx/.xls)**.
    * **Criação Dinâmica de Tabela:** Gera automaticamente uma nova tabela no MySQL com base nas colunas e tipos de dados do Excel, se ela não existir.
    * **Modos de Importação:** Escolha entre "Adicionar (Append)" para incluir novos registros ou "Sobrescrever (Truncate & Insert)" para limpar a tabela existente e inserir os novos dados.
* **Exportação Flexível (MySQL para Excel):**
    * Exporta dados de **qualquer tabela existente no MySQL** para um arquivo Excel.
    * **Seleção de Tabela:** O aplicativo lista automaticamente as tabelas disponíveis no banco de dados para fácil seleção.
    * **Formatação Automática:** O arquivo Excel gerado tem as larguras das colunas e o alinhamento ajustados para melhor legibilidade.
* **Persistência de Configurações:** Salva e carrega automaticamente as credenciais de conexão do MySQL para uso futuro, otimizando o fluxo de trabalho.
* **Feedback em Tempo Real:** Barra de status com mensagens coloridas e desativação de botões durante as operações para uma melhor experiência do usuário.
* **Processamento em Segundo Plano:** Utiliza threads para que a interface gráfica permaneça responsiva durante operações demoradas.

## Tecnologias Utilizadas

* **Python 3.9+** (Linguagem de Programação)
* **`CustomTkinter`**: Para a criação da interface gráfica moderna.
* **`pandas`**: Para leitura, manipulação e exportação eficiente de dados tabulares.
* **`mysql-connector-python`**: Para conexão e interação com o banco de dados MySQL.
* **`openpyxl`**: Para manipulação e estilização de arquivos Excel.
* **`threading`**: Para operações assíncronas e interface responsiva.
* **`json`**: Para persistência de configurações.

## Como Usar o Aplicativo (Para Usuários Finais - Sem Python)

Para usuários que desejam apenas rodar o aplicativo sem se preocupar com Python ou dependências:

1.  **Baixe os arquivos:**
    * Vá para a seção [**Releases**](https://github.com/JoaoVieiraZP/dados/releases) do repositório no GitHub.
    * Baixe a última versão do arquivo `app_gui.exe` e, se desejar manter suas configurações de DB, o arquivo `db_config.json` (se já tiver sido gerado na sua máquina).
2.  **Organize os arquivos:**
    * Crie uma nova pasta em seu computador para o aplicativo (ex: `Sincronizador Dados`).
    * Coloque o `app_gui.exe` dentro desta pasta.
    * **Importante:** Se você já usou o aplicativo antes e quer manter suas configurações de banco de dados, copie seu `db_config.json` pessoal para esta mesma pasta. Caso contrário, o aplicativo criará um novo na primeira vez que você salvar as configurações.
3.  **Execute o aplicativo:**
    * Clique duas vezes em `app_gui.exe`.

**Requisito Crucial:** O computador onde o aplicativo será executado deve ter um **servidor MySQL (como XAMPP, WAMP, MySQL Workbench, etc.) instalado e rodando** e acessível pelo aplicativo (ex: no `localhost` ou em um IP de rede). O aplicativo apenas se conecta ao servidor, ele não o instala.

## Como Rodar o Código Fonte (Para Desenvolvedores/Colaboradores)

Se você deseja explorar o código, desenvolver ou colaborar:

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/JoaoVieiraZP/dados.git](https://github.com/JoaoVieiraZP/dados.git) my-project-name
    cd my-project-name
    ```
2.  **Crie e Ative o Ambiente Conda (Recomendado):**
    ```bash
    conda create -n rstudio python=3.9
    conda activate rstudio
    ```
3.  **Instale as Dependências Python:**
    ```bash
    pip install mysql-connector-python pandas openpyxl customtkinter
    ```
4.  **Execute o Aplicativo:**
    ```bash
    python src/app_gui.py
    ```
    * Na primeira execução, o aplicativo gerará um arquivo `db_config.json` na raiz da pasta do projeto após você salvar as configurações do banco de dados na interface.

## Melhorias Futuras

* **Mapeamento de Colunas Avançado:** Permitir que o usuário defina mapeamentos personalizados de colunas e tipos de dados durante a importação.
* **Mais Modos de Importação:** Implementar modos como UPSERT (Atualizar/Inserir) ou UPDATE ONLY.
* **Gerenciamento de Erros Aprimorado:** Log de erros para um arquivo e notificação mais detalhada na GUI.
* **Suporte a Outros Bancos de Dados:** Expandir a compatibilidade para PostgreSQL, SQLite, etc.
* **Internacionalização (i18n):** Adicionar suporte a múltiplos idiomas.

## Contato

Sinta-se à vontade para entrar em contato se tiver dúvidas ou sugestões!

* **João Pedro Vieira Pereira**
* [GitHub](https://github.com/JoaoVieiraZP)
* [LinkedIn](https://www.linkedin.com/in/jo%C3%A3o-pedro-vieira-pereira-7aab772b1/)

---

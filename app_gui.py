import tkinter as tk # Ainda necessário para filedialog, messagebox, StringVar
from tkinter import filedialog, messagebox
import os
import threading
import mysql.connector # Importar aqui para que o messagebox possa usá-lo no erro
import json # Para salvar e carregar configurações

import customtkinter as ctk # Biblioteca para a interface moderna

# --- IMPORTANTE: Certifique-se de que os nomes dos arquivos abaixo estão corretos ---
# Seus arquivos EXCELparaSQL.py e SQLparaEXCEL.py devem estar na mesma pasta.
from EXCELparaSQL import import_excel_to_mysql 
from SQLparaEXCEL import export_mysql_table_to_excel

class AppMySQLXLSX:
    def __init__(self, master):
        self.master = master
        
        # Configura o tema do CustomTkinter (global para a aplicação)
        ctk.set_appearance_mode("dark") # Opções: "System", "dark", "light"
        ctk.set_default_color_theme("blue") # Opções: "blue", "green", "dark-blue"
        
        master.title("Sincronizador MySQL <-> Excel")
        
        # --- CONTROLE DE TAMANHO E REDIMENSIONAMENTO DA JANELA ---
        # ESCOLHA APENAS UMA DAS OPÇÕES ABAIXO (comente as outras):

        # OPÇÃO 1: ABRIR MAXIMIZADA (Janela Cheia, mas com barra de título)
        self.master.state('zoomed') 
        self.master.resizable(True, True) # Permite ao usuário redimensionar depois de maximizar

        # OPÇÃO 2: ABRIR EM UM TAMANHO FIXO ESPECÍFICO (ex: 600x400) E NÃO REDIMENSIONÁVEL
        # self.master.geometry("600x400") # Defina a largura e altura desejadas
        # self.master.resizable(False, False) # Impede o usuário de redimensionar

        # OPÇÃO 3: ABRIR EM UM TAMANHO FIXO MAIOR E PERMITIR REDIMENSIONAMENTO
        # self.master.geometry("800x600") # Defina a largura e altura desejadas
        # self.master.resizable(True, True) # Permite ao usuário redimensionar
        
        # --- FIM DO CONTROLE DE TAMANHO ---

        # --- CONFIGURAÇÕES DO BANCO DE DADOS (Carregadas/Salvas de arquivo) ---
        self.config_file = "db_config.json"
        self.db_config_values = self.load_db_config() 
        # tk.StringVar para campos de entrada vinculados
        self.db_host_var = tk.StringVar(value=self.db_config_values.get("host", "localhost"))
        self.db_user_var = tk.StringVar(value=self.db_config_values.get("user", "root"))
        self.db_password_var = tk.StringVar(value=self.db_config_values.get("password", "")) # Senha não salva por padrão
        self.db_database_var = tk.StringVar(value=self.db_config_values.get("database", "sistema_teste"))

        # --- Frame de Configurações do DB (no topo) ---
        # Usamos CTkFrame para o agrupamento, e CTkLabel para o título
        self.db_config_frame = ctk.CTkFrame(master, corner_radius=10)
        self.db_config_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.db_config_frame, text="Configurações do Banco de Dados", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, columnspan=4, pady=5, padx=5, sticky="ew")

        # Entradas e Labels para Host, Usuário, Senha, Database
        ctk.CTkLabel(self.db_config_frame, text="Host:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_db_host = ctk.CTkEntry(self.db_config_frame, textvariable=self.db_host_var, width=150)
        self.entry_db_host.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        
        ctk.CTkLabel(self.db_config_frame, text="Usuário:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.entry_db_user = ctk.CTkEntry(self.db_config_frame, textvariable=self.db_user_var, width=150)
        self.entry_db_user.grid(row=1, column=3, sticky="ew", padx=5, pady=2)
        
        ctk.CTkLabel(self.db_config_frame, text="Senha:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_db_password = ctk.CTkEntry(self.db_config_frame, textvariable=self.db_password_var, width=150, show="*")
        self.entry_db_password.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        
        ctk.CTkLabel(self.db_config_frame, text="Database:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.entry_db_database = ctk.CTkEntry(self.db_config_frame, textvariable=self.db_database_var, width=150)
        self.entry_db_database.grid(row=2, column=3, sticky="ew", padx=5, pady=2)

        # Botões de Salvar Configs DB e Testar Conexão
        self.btn_save_db_config = ctk.CTkButton(self.db_config_frame, text="Salvar Configs DB", command=self.save_db_config)
        self.btn_save_db_config.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        self.btn_test_db_connection = ctk.CTkButton(self.db_config_frame, text="Testar Conexão", command=self.test_db_connection)
        self.btn_test_db_connection.grid(row=3, column=2, columnspan=2, pady=10, padx=5, sticky="ew")
        
        self.db_config_frame.grid_columnconfigure(1, weight=1)
        self.db_config_frame.grid_columnconfigure(3, weight=1)

        # --- Frame Principal (Botões de Escolha Importar/Exportar) ---
        self.main_frame = ctk.CTkFrame(master, corner_radius=10)
        self.main_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.main_frame, text="Selecione uma operação:", font=ctk.CTkFont(size=14)).pack(pady=15, fill="x")

        self.btn_import = ctk.CTkButton(self.main_frame, text="Importar Excel para MySQL", command=self.show_import_widgets, height=40, font=ctk.CTkFont(size=12, weight="bold"))
        self.btn_import.pack(pady=10, fill="x", padx=60)

        self.btn_export = ctk.CTkButton(self.main_frame, text="Exportar MySQL para Excel", command=self.show_export_widgets, height=40, font=ctk.CTkFont(size=12, weight="bold"))
        self.btn_export.pack(pady=10, fill="x", padx=60)

        # --- Frame de Importação (Inicialmente Escondido) ---
        self.import_frame = ctk.CTkFrame(master, corner_radius=10)
        self.excel_path_var = tk.StringVar() 
        self.excel_name_for_import_entry_var = tk.StringVar() 
        self.import_mode_var = tk.StringVar(value="Adicionar (Append)") 

        ctk.CTkLabel(self.import_frame, text="Caminho do Arquivo Excel:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_excel_path = ctk.CTkEntry(self.import_frame, textvariable=self.excel_path_var, width=300)
        self.entry_excel_path.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.btn_browse_excel = ctk.CTkButton(self.import_frame, text="Procurar", command=self.browse_excel_file, width=80)
        self.btn_browse_excel.grid(row=0, column=2, pady=5, padx=5)

        ctk.CTkLabel(self.import_frame, text="Nome da Tabela no MySQL (opcional):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_excel_name_for_import = ctk.CTkEntry(self.import_frame, textvariable=self.excel_name_for_import_entry_var, width=300)
        self.entry_excel_name_for_import.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5, padx=5)

        ctk.CTkLabel(self.import_frame, text="Modo de Importação:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.import_mode_combobox = ctk.CTkComboBox(self.import_frame, variable=self.import_mode_var,
                                                 values=["Adicionar (Append)", "Sobrescrever (Truncate & Insert)"],
                                                 state="readonly", width=200)
        self.import_mode_combobox.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
        self.import_mode_combobox.set("Adicionar (Append)") 

        self.btn_execute_import = ctk.CTkButton(self.import_frame, text="Executar Importação", command=self.run_import_in_thread, height=40, font=ctk.CTkFont(size=12, weight="bold"))
        self.btn_execute_import.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.btn_back_import = ctk.CTkButton(self.import_frame, text="← Voltar", command=self.show_main_widgets)
        self.btn_back_import.grid(row=4, column=0, columnspan=3, pady=5)
        self.import_frame.columnconfigure(1, weight=1) 

        # --- Frame de Exportação (Inicialmente Escondido) ---
        self.export_frame = ctk.CTkFrame(master, corner_radius=10)
        self.table_name_var = tk.StringVar() 
        self.output_excel_name_var = tk.StringVar(value="dados_exportados.xlsx") 

        ctk.CTkLabel(self.export_frame, text="Tabela MySQL a Exportar:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.table_name_combobox = ctk.CTkComboBox(self.export_frame, variable=self.table_name_var, state="readonly", width=300)
        self.table_name_combobox.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
        self.table_name_combobox.bind("<<ComboboxSelected>>", self.on_table_selected)

        ctk.CTkLabel(self.export_frame, text="Nome do Arquivo Excel de Saída (.xlsx):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_output_excel = ctk.CTkEntry(self.export_frame, textvariable=self.output_excel_name_var, width=300)
        self.entry_output_excel.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.btn_browse_save_excel = ctk.CTkButton(self.export_frame, text="Salvar Como...", command=self.browse_save_excel_file, width=80)
        self.btn_browse_save_excel.grid(row=1, column=2, pady=5, padx=5)

        self.btn_execute_export = ctk.CTkButton(self.export_frame, text="Executar Exportação", command=self.run_export_in_thread, height=40, font=ctk.CTkFont(size=12, weight="bold"))
        self.btn_execute_export.grid(row=2, column=0, columnspan=3, pady=20)

        self.btn_back_export = ctk.CTkButton(self.export_frame, text="← Voltar", command=self.show_main_widgets)
        self.btn_back_export.grid(row=3, column=0, columnspan=3, pady=5)
        self.export_frame.columnconfigure(1, weight=1)

        # --- Barra de Status ---
        self.status_bar = ctk.CTkLabel(master, text="Pronto para uso.", anchor="w", fg_color=("gray80", "gray20"), corner_radius=5)
        self.status_bar.pack(side="bottom", fill="x", ipady=5, padx=20, pady=10) 

        # Esconde todos os frames de operação ao iniciar
        self.hide_all_operation_widgets()
        master.update_idletasks() # Atualiza para obter as dimensões corretas dos widgets
        # A centralização é chamada dentro de show_main_widgets, import/export widgets para ajuste
        self.show_main_widgets() 

    def load_db_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Erro de Configuração", "Arquivo de configuração (db_config.json) inválido. Usando valores padrão.")
        return {} 

    def save_db_config(self):
        config_data = {
            "host": self.db_host_var.get(),
            "user": self.db_user_var.get(),
            "database": self.db_database_var.get()
        }
        try:
            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=4)
            self.set_status("Configurações do banco de dados salvas com sucesso!", "green") 
        except Exception as e:
            self.set_status(f"Erro ao salvar configurações: {e}", "red") 

    def test_db_connection(self):
        current_db_config = {
            "host": self.db_host_var.get(),
            "user": self.db_user_var.get(),
            "password": self.db_password_var.get(),
            "database": self.db_database_var.get()
        }
        try:
            conn = mysql.connector.connect(**current_db_config)
            conn.close()
            self.set_status("Conexão com o banco de dados bem-sucedida!", "green")
        except mysql.connector.Error as e:
            self.set_status(f"Erro de conexão com o banco de dados: {e}", "red")
        except Exception as e:
            self.set_status(f"Erro inesperado ao testar conexão: {e}", "red")

    def get_current_db_config(self):
        return {
            "host": self.db_host_var.get(),
            "user": self.db_user_var.get(),
            "password": self.db_password_var.get(),
            "database": self.db_database_var.get()
        }

    def fetch_mysql_tables(self):
        self.set_status("Buscando tabelas no banco de dados...", "blue") 
        self.toggle_buttons_state("disabled")
        try:
            conn = mysql.connector.connect(**self.get_current_db_config())
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in cursor]
            self.table_name_combobox.configure(values=tables) 
            if tables:
                self.table_name_var.set(tables[0]) 
            else:
                self.table_name_var.set("")
            self.set_status(f"Tabelas carregadas: {len(tables)} encontradas.", "green")
        except mysql.connector.Error as e:
            self.set_status(f"Erro ao carregar tabelas: {e}\nVerifique a conexão e se o banco de dados existe.", "red")
            self.table_name_combobox.configure(values=[])
            self.table_name_var.set("")
        except Exception as e:
            self.set_status(f"Erro inesperado ao buscar tabelas: {e}", "red")
            self.table_name_combobox.configure(values=[])
            self.table_name_var.set("")
        finally:
            self.toggle_buttons_state("normal")
            if 'cursor' in locals() and cursor: cursor.close()
            if 'conn' in locals() and conn: conn.close()

    def on_table_selected(self, event):
        self.set_status(f"Tabela '{self.table_name_var.get()}' selecionada para exportação.", "blue")

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def set_status(self, message, text_color): 
        self.status_bar.configure(text=message, text_color=text_color)
        self.master.update_idletasks()

    def hide_all_operation_widgets(self):
        self.main_frame.pack_forget()
        self.import_frame.pack_forget()
        self.export_frame.pack_forget()
        # Ao esconder, definimos um tamanho padrão que se ajusta aos frames principais
        self.master.geometry("700x580") 

    def show_main_widgets(self):
        self.hide_all_operation_widgets()
        self.main_frame.pack(pady=10, padx=20, expand=True, fill="both")
        self.master.geometry("700x580") # Tamanho para a tela principal
        self.center_window()
        self.set_status("Pronto para uso.", "gray70") 

    def show_import_widgets(self):
        self.hide_all_operation_widgets()
        self.import_frame.pack(pady=10, padx=20, fill="x")
        self.master.geometry("700x480") # Tamanho para a tela de importação
        self.center_window()
        self.set_status("Selecione o arquivo Excel e o modo de importação.", "gray70")

    def show_export_widgets(self):
        self.hide_all_operation_widgets()
        self.export_frame.pack(pady=10, padx=20, fill="x")
        self.master.geometry("700x480") # Tamanho para a tela de exportação
        self.center_window()
        self.fetch_mysql_tables() # Busca as tabelas ao mostrar o frame de exportação
        self.set_status("Selecione a tabela e o local de saída do Excel.", "gray70")

    def browse_excel_file(self):
        filepath = filedialog.askopenfilename(
            title="Selecionar Arquivo Excel para Importar",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if filepath:
            self.excel_path_var.set(filepath)
            if not self.excel_name_for_import_entry_var.get():
                file_name_without_ext = os.path.splitext(os.path.basename(filepath))[0]
                normalized_name = file_name_without_ext.lower().replace(" ", "_").replace("-", "_")
                self.excel_name_for_import_entry_var.set(normalized_name)
            self.set_status("Arquivo Excel selecionado.", "blue")

    def browse_save_excel_file(self):
        filepath = filedialog.asksaveasfilename(
            title="Salvar Arquivo Excel Como",
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if filepath:
            self.output_excel_name_var.set(filepath)
            self.set_status("Local de salvamento do Excel selecionado.", "blue")

    def toggle_buttons_state(self, state):
        ctk_state = "normal" if state == "normal" else "disabled"

        widgets_to_toggle = [
            self.btn_import, self.btn_export,
            self.btn_browse_excel, self.btn_execute_import, self.btn_back_import,
            self.import_mode_combobox, self.entry_excel_path, self.entry_excel_name_for_import,
            
            self.table_name_combobox, self.btn_browse_save_excel, self.btn_execute_export, self.btn_back_export,
            self.entry_output_excel,

            self.entry_db_host, self.entry_db_user, self.entry_db_password, self.entry_db_database,
            self.btn_save_db_config, self.btn_test_db_connection
        ]
        
        for widget in widgets_to_toggle:
            # Verifica se o widget é um objeto válido e se possui o método .configure()
            if widget is not None and hasattr(widget, 'configure'):
                try:
                    # Verifica se o widget suporta o argumento 'state'
                    # Alguns widgets CustomTkinter podem não ter 'state' no .configure() dict
                    # (ex: CTkLabel, CTkFrame), mas os que estão nesta lista (botões, entries, comboboxes) têm.
                    if 'state' in widget.configure(): 
                        widget.configure(state=ctk_state)
                    # Adicionalmente, para CTkComboBox, o 'state' também pode ser ajustado com .set_state()
                    # mas .configure(state=...) é mais genérico e funciona.
                except Exception as e:
                    # Captura qualquer erro inesperado ao configurar o widget, como um TclError
                    print(f"Warning: Could not configure state for widget {type(widget).__name__} (ID: {id(widget)}): {e}. Skipping.")
                    # Continua para o próximo widget na lista
                    pass # Não re-lança o erro, apenas o imprime.


    def run_import_in_thread(self):
        self.toggle_buttons_state("disabled")
        self.set_status("Importando dados... Por favor, aguarde.", "orange") 
        thread = threading.Thread(target=self.execute_import_logic)
        thread.start()

    def execute_import_logic(self):
        excel_filepath = self.excel_path_var.get()
        table_name_optional = self.excel_name_for_import_entry_var.get()
        selected_import_mode = self.import_mode_var.get() 
        
        import_mode_param = "append" 
        if "Sobrescrever" in selected_import_mode:
            import_mode_param = "overwrite"

        if not excel_filepath:
            self.set_status("Erro: Por favor, selecione um arquivo Excel para importar.", "red")
            self.toggle_buttons_state("normal")
            return

        try:
            current_db_config = self.get_current_db_config()
            import_excel_to_mysql(
                excel_filepath,
                current_db_config,
                table_name=table_name_optional if table_name_optional else None,
                import_mode=import_mode_param 
            )
            self.set_status("Dados importados para o MySQL com sucesso!", "green")
        except FileNotFoundError as e:
            self.set_status(f"Erro de Arquivo: {e}", "red")
        except mysql.connector.Error as e: 
            self.set_status(f"Erro no MySQL: {e}\nVerifique as credenciais, o nome do banco de dados ou a existência da tabela.", "red")
        except Exception as e:
            self.set_status(f"Ocorreu um erro inesperado durante a importação: {e}", "red")
        finally:
            self.toggle_buttons_state("normal")

    def run_export_in_thread(self):
        self.toggle_buttons_state("disabled")
        self.set_status("Exportando dados... Por favor, aguarde.", "orange")
        thread = threading.Thread(target=self.execute_export_logic)
        thread.start()

    def execute_export_logic(self):
        table_name_to_export = self.table_name_var.get()
        output_excel_filename = self.output_excel_name_var.get()

        if not table_name_to_export:
            self.set_status("Erro: Por favor, selecione uma tabela MySQL para exportar.", "red")
            self.toggle_buttons_state("normal")
            return
        if not output_excel_filename:
            self.set_status("Erro: Por favor, digite o nome do arquivo Excel de saída.", "red")
            self.toggle_buttons_state("normal")
            return
        if not output_excel_filename.endswith(".xlsx"):
            output_excel_filename += ".xlsx"

        try:
            current_db_config = self.get_current_db_config()
            export_mysql_table_to_excel(table_name_to_export, output_excel_filename, current_db_config)
            self.set_status(f"Tabela '{table_name_to_export}' exportada para '{output_excel_filename}' com sucesso!", "green")
        except FileNotFoundError as e:
            self.set_status(f"Erro de Arquivo: Não foi possível criar o arquivo Excel - {e}", "red")
        except mysql.connector.Error as e:
            self.set_status(f"Erro no MySQL: {e}\nVerifique as credenciais ou se a tabela '{table_name_to_export}' existe.", "red")
        except Exception as e:
            self.set_status(f"Ocorreu um erro inesperado durante a exportação: {e}", "red")
        finally:
            self.toggle_buttons_state("normal")


if __name__ == "__main__":
    root = ctk.CTk()
    app = AppMySQLXLSX(root)
    root.mainloop()
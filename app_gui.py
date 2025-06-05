import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import mysql.connector
import json

from EXCELparaSQL import import_excel_to_mysql
from SQLparaEXCEL import export_mysql_table_to_excel

class AppMySQLXLSX:
    def __init__(self, master):
        self.master = master
        master.title("Sincronizador MySQL <-> Excel")
        master.geometry("700x580")
        master.resizable(False, False)
        master.configure(bg="#2E3440")

        # --- Configurações de estilo para ttk ---
        style = ttk.Style()
        style.theme_use("clam") 
        
        BACKGROUND_DARK = "#2E3440"
        BACKGROUND_MEDIUM = "#3B4252"
        FOREGROUND_LIGHT = "#E5E9F0"
        ACCENT_BLUE = "#81A1C1"
        ACCENT_GREEN = "#A3BE8C"
        ACCENT_RED = "#BF616A"
        ACCENT_YELLOW = "#EBCB8B"

        style.configure("TFrame", background=BACKGROUND_MEDIUM)
        style.configure("TLabel", background=BACKGROUND_MEDIUM, foreground=FOREGROUND_LIGHT, font=("Segoe UI", 10))
        style.configure("TButton", background=ACCENT_BLUE, foreground=FOREGROUND_LIGHT, font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat")
        style.map("TButton", background=[('active', ACCENT_BLUE), ('pressed', ACCENT_BLUE)], foreground=[('active', BACKGROUND_DARK)])
        
        style.configure("TEntry", fieldbackground=BACKGROUND_DARK, foreground=FOREGROUND_LIGHT, insertcolor=FOREGROUND_LIGHT, borderwidth=1, relief="solid")
        style.map("TEntry", fieldbackground=[('focus', BACKGROUND_MEDIUM)])

        style.configure("TCombobox", fieldbackground=BACKGROUND_DARK, foreground=FOREGROUND_LIGHT, selectbackground=BACKGROUND_MEDIUM, selectforeground=FOREGROUND_LIGHT, background=BACKGROUND_DARK, arrowcolor=FOREGROUND_LIGHT)
        style.map("TCombobox", fieldbackground=[('readonly', BACKGROUND_DARK)], background=[('readonly', BACKGROUND_DARK)])
        style.configure("TCombobox.Border", borderwidth=1, relief="solid") 

        # --- CONFIGURAÇÕES DO BANCO DE DADOS (Carregadas/Salvas de arquivo) ---
        self.config_file = "db_config.json"
        self.db_config_values = self.load_db_config()
        self.db_host_var = tk.StringVar(value=self.db_config_values.get("host", "localhost"))
        self.db_user_var = tk.StringVar(value=self.db_config_values.get("user", "root"))
        self.db_password_var = tk.StringVar(value=self.db_config_values.get("password", "")) 
        self.db_database_var = tk.StringVar(value=self.db_config_values.get("database", "sistema_teste"))

        # --- Frame de Configurações do DB (no topo) ---
        self.db_config_frame = ttk.LabelFrame(master, text="Configurações do Banco de Dados", padding="15 15 15 15", relief="raised")
        self.db_config_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(self.db_config_frame, text="Host:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_db_host = ttk.Entry(self.db_config_frame, textvariable=self.db_host_var, width=20)
        self.entry_db_host.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        
        ttk.Label(self.db_config_frame, text="Usuário:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.entry_db_user = ttk.Entry(self.db_config_frame, textvariable=self.db_user_var, width=20)
        self.entry_db_user.grid(row=0, column=3, sticky="ew", padx=5, pady=2)
        
        ttk.Label(self.db_config_frame, text="Senha:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_db_password = ttk.Entry(self.db_config_frame, textvariable=self.db_password_var, width=20, show="*")
        self.entry_db_password.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        
        ttk.Label(self.db_config_frame, text="Database:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.entry_db_database = ttk.Entry(self.db_config_frame, textvariable=self.db_database_var, width=20)
        self.entry_db_database.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        self.btn_save_db_config = ttk.Button(self.db_config_frame, text="Salvar Configs DB", command=self.save_db_config)
        self.btn_save_db_config.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        self.btn_test_db_connection = ttk.Button(self.db_config_frame, text="Testar Conexão", command=self.test_db_connection)
        self.btn_test_db_connection.grid(row=2, column=2, columnspan=2, pady=10, padx=5, sticky="ew")
        
        self.db_config_frame.grid_columnconfigure(1, weight=1)
        self.db_config_frame.grid_columnconfigure(3, weight=1)

        # --- Frame Principal (Botões de Escolha) ---
        self.main_frame = ttk.Frame(master, padding="20 20 20 20", relief="raised")
        self.main_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(self.main_frame, text="Selecione uma operação:", font=("Segoe UI", 14)).pack(pady=15, fill="x")

        self.btn_import = ttk.Button(self.main_frame, text="Importar Excel para MySQL", command=self.show_import_widgets, style="TButton")
        self.btn_import.pack(pady=10, ipady=10, fill="x", padx=60)

        self.btn_export = ttk.Button(self.main_frame, text="Exportar MySQL para Excel", command=self.show_export_widgets, style="TButton")
        self.btn_export.pack(pady=10, ipady=10, fill="x", padx=60)

        # --- Frame de Importação (Inicialmente Escondido) ---
        self.import_frame = ttk.Frame(master, padding="20 20 20 20", relief="raised")
        self.excel_path_var = tk.StringVar()
        self.excel_name_for_import_entry_var = tk.StringVar()
        self.import_mode_var = tk.StringVar(value="Adicionar (Append)")

        ttk.Label(self.import_frame, text="Caminho do Arquivo Excel:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_excel_path = ttk.Entry(self.import_frame, textvariable=self.excel_path_var, width=45)
        self.entry_excel_path.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.btn_browse_excel = ttk.Button(self.import_frame, text="Procurar", command=self.browse_excel_file)
        self.btn_browse_excel.grid(row=0, column=2, pady=5, padx=5)

        ttk.Label(self.import_frame, text="Nome da Tabela no MySQL (opcional):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_excel_name_for_import = ttk.Entry(self.import_frame, textvariable=self.excel_name_for_import_entry_var, width=45)
        self.entry_excel_name_for_import.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5, padx=5)

        ttk.Label(self.import_frame, text="Modo de Importação:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.import_mode_combobox = ttk.Combobox(self.import_frame, textvariable=self.import_mode_var,
                                                 values=["Adicionar (Append)", "Sobrescrever (Truncate & Insert)"],
                                                 state="readonly", width=30)
        self.import_mode_combobox.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
        self.import_mode_combobox.set("Adicionar (Append)") 

        self.btn_execute_import = ttk.Button(self.import_frame, text="Executar Importação", command=self.run_import_in_thread, style="TButton")
        self.btn_execute_import.grid(row=3, column=0, columnspan=3, pady=20, ipady=10)
        
        self.btn_back_import = ttk.Button(self.import_frame, text="← Voltar", command=self.show_main_widgets)
        self.btn_back_import.grid(row=4, column=0, columnspan=3, pady=5)
        self.import_frame.columnconfigure(1, weight=1)

        # --- Frame de Exportação (Inicialmente Escondido) ---
        self.export_frame = ttk.Frame(master, padding="20 20 20 20", relief="raised")
        self.table_name_var = tk.StringVar()
        self.output_excel_name_var = tk.StringVar(value="dados_exportados.xlsx")

        ttk.Label(self.export_frame, text="Tabela MySQL a Exportar:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.table_name_combobox = ttk.Combobox(self.export_frame, textvariable=self.table_name_var, state="readonly", width=45)
        self.table_name_combobox.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
        self.table_name_combobox.bind("<<ComboboxSelected>>", self.on_table_selected)

        ttk.Label(self.export_frame, text="Nome do Arquivo Excel de Saída (.xlsx):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_output_excel = ttk.Entry(self.export_frame, textvariable=self.output_excel_name_var, width=45)
        self.entry_output_excel.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.btn_browse_save_excel = ttk.Button(self.export_frame, text="Salvar Como...", command=self.browse_save_excel_file)
        self.btn_browse_save_excel.grid(row=1, column=2, pady=5, padx=5)

        self.btn_execute_export = ttk.Button(self.export_frame, text="Executar Exportação", command=self.run_export_in_thread, style="TButton")
        self.btn_execute_export.grid(row=2, column=0, columnspan=3, pady=20, ipady=10)

        self.btn_back_export = ttk.Button(self.export_frame, text="← Voltar", command=self.show_main_widgets)
        self.btn_back_export.grid(row=3, column=0, columnspan=3, pady=5)
        self.export_frame.columnconfigure(1, weight=1)

        # --- Barra de Status na parte inferior ---
        self.status_bar = ttk.Label(master, text="Pronto para uso.", relief="sunken", anchor="w", background=BACKGROUND_DARK, foreground=FOREGROUND_LIGHT, font=("Segoe UI", 9))
        self.status_bar.pack(side="bottom", fill="x", ipady=5)

        # Esconde todos os frames de operação ao iniciar
        self.hide_all_operation_widgets()
        # Centraliza a janela após todos os widgets serem criados
        master.update_idletasks()
        self.center_window() 
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
            # OBS: A senha não fica salva por questão de segurança do banco!
        }
        try:
            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=4)
            self.set_status("Configurações do banco de dados salvas com sucesso!", "#A3BE8C")
        except Exception as e:
            self.set_status(f"Erro ao salvar configurações: {e}", "#BF616A")

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
            self.set_status("Conexão com o banco de dados bem-sucedida!", "#A3BE8C")
        except mysql.connector.Error as e:
            self.set_status(f"Erro de conexão com o banco de dados: {e}", "#BF616A")
        except Exception as e:
            self.set_status(f"Erro inesperado ao testar conexão: {e}", "#BF616A")

    def get_current_db_config(self):
        return {
            "host": self.db_host_var.get(),
            "user": self.db_user_var.get(),
            "password": self.db_password_var.get(),
            "database": self.db_database_var.get()
        }

    def fetch_mysql_tables(self):
        self.set_status("Buscando tabelas no banco de dados...", "#EBCB8B")
        self.toggle_buttons_state("disabled")
        try:
            conn = mysql.connector.connect(**self.get_current_db_config())
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in cursor]
            self.table_name_combobox['values'] = tables
            if tables:
                self.table_name_var.set(tables[0])
            else:
                self.table_name_var.set("")
            self.set_status(f"Tabelas carregadas: {len(tables)} encontradas.", "#E5E9F0")
        except mysql.connector.Error as e:
            self.set_status(f"Erro ao carregar tabelas: {e}\nVerifique a conexão e se o banco de dados existe.", "#BF616A")
            self.table_name_combobox['values'] = []
            self.table_name_var.set("")
        except Exception as e:
            self.set_status(f"Erro inesperado ao buscar tabelas: {e}", "#BF616A")
            self.table_name_combobox['values'] = []
            self.table_name_var.set("")
        finally:
            self.toggle_buttons_state("normal")
            if 'cursor' in locals() and cursor: cursor.close()
            if 'conn' in locals() and conn: conn.close()

    def on_table_selected(self, event):
        self.set_status(f"Tabela '{self.table_name_var.get()}' selecionada para exportação.", "#E5E9F0")

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def set_status(self, message, color="#E5E9F0"):
        self.status_bar.config(text=message, foreground=color)
        self.master.update_idletasks()

    def hide_all_operation_widgets(self):
        self.main_frame.pack_forget()
        self.import_frame.pack_forget()
        self.export_frame.pack_forget()
        self.master.geometry("700x580") 

    def show_main_widgets(self):
        self.hide_all_operation_widgets()
        self.main_frame.pack(pady=10, padx=20, expand=True, fill="both")
        self.master.geometry("700x580")
        self.center_window()
        self.set_status("Pronto para uso.", "#E5E9F0")

    def show_import_widgets(self):
        self.hide_all_operation_widgets()
        self.import_frame.pack(pady=10, padx=20, fill="x")
        self.master.geometry("700x480") 
        self.center_window()
        self.set_status("Selecione o arquivo Excel e o modo de importação.", "#E5E9F0")

    def show_export_widgets(self):
        self.hide_all_operation_widgets()
        self.export_frame.pack(pady=10, padx=20, fill="x")
        self.master.geometry("700x480") 
        self.center_window()
        self.fetch_mysql_tables()
        self.set_status("Selecione a tabela e o local de saída do Excel.", "#E5E9F0")

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
            self.set_status("Arquivo Excel selecionado.", "#E5E9F0")

    def browse_save_excel_file(self):
        filepath = filedialog.asksaveasfilename(
            title="Salvar Arquivo Excel Como",
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if filepath:
            self.output_excel_name_var.set(filepath)
            self.set_status("Local de salvamento do Excel selecionado.", "#E5E9F0")

    def toggle_buttons_state(self, state):
        # Lista de todos os widgets que devem ter seu estado alterado
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
            # Verifica se o widget possui o método config e o argumento 'state'
            if hasattr(widget, 'config') and 'state' in widget.config():
                widget.config(state=state)


    def run_import_in_thread(self):
        self.toggle_buttons_state("disabled")
        self.set_status("Importando dados... Por favor, aguarde.", "#EBCB8B") 
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
            self.set_status("Erro: Por favor, selecione um arquivo Excel para importar.", "#BF616A")
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
            self.set_status("Dados importados para o MySQL com sucesso!", "#A3BE8C")
        except FileNotFoundError as e:
            self.set_status(f"Erro de Arquivo: {e}", "#BF616A")
        except mysql.connector.Error as e: 
            self.set_status(f"Erro no MySQL: {e}\nVerifique as credenciais, o nome do banco de dados ou a existência da tabela.", "#BF616A")
        except Exception as e:
            self.set_status(f"Ocorreu um erro inesperado durante a importação: {e}", "#BF616A")
        finally:
            self.toggle_buttons_state("normal")

    def run_export_in_thread(self):
        self.toggle_buttons_state("disabled")
        self.set_status("Exportando dados... Por favor, aguarde.", "#EBCB8B")
        thread = threading.Thread(target=self.execute_export_logic)
        thread.start()

    def execute_export_logic(self):
        table_name_to_export = self.table_name_var.get()
        output_excel_filename = self.output_excel_name_var.get()

        if not table_name_to_export:
            self.set_status("Erro: Por favor, selecione uma tabela MySQL para exportar.", "#BF616A")
            self.toggle_buttons_state("normal")
            return
        if not output_excel_filename:
            self.set_status("Erro: Por favor, digite o nome do arquivo Excel de saída.", "#BF616A")
            self.toggle_buttons_state("normal")
            return
        if not output_excel_filename.endswith(".xlsx"):
            output_excel_filename += ".xlsx"

        try:
            current_db_config = self.get_current_db_config()
            export_mysql_table_to_excel(table_name_to_export, output_excel_filename, current_db_config)
            self.set_status(f"Tabela '{table_name_to_export}' exportada para '{output_excel_filename}' com sucesso!", "#A3BE8C")
        except FileNotFoundError as e:
            self.set_status(f"Erro de Arquivo: Não foi possível criar o arquivo Excel - {e}", "#BF616A")
        except mysql.connector.Error as e:
            self.set_status(f"Erro no MySQL: {e}\nVerifique as credenciais ou se a tabela '{table_name_to_export}' existe.", "#BF616A")
        except Exception as e:
            self.set_status(f"Ocorreu um erro inesperado durante a exportação: {e}", "#BF616A")
        finally:
            self.toggle_buttons_state("normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppMySQLXLSX(root)
    root.mainloop()
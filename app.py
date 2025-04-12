from tkinter import messagebox
import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import sqlite3


class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados criado com sucesso")

    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado")

    def cria_tabela(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconecta_db()

    def cadastrar_user(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        print("Usuário:", self.username_cadastro)
        print("Email:", self.email_cadastro)
        print("Senha:", self.senha_cadastro)
        print("Confirmação:", self.confirma_senha_cadastro)

        self.conecta_db()

        try:
            if(self.username_cadastro == "" or self.email_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de login", message="ERRO!!!\nPor favor preencha todos os campos!")
            elif(len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de login", message="O nome do usuário deve conter pelo menos 4 caracteres.")
            elif(len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de login", message="A senha deve conter pelo menos 4 caracteres.")
            elif(self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showwarning(title="Sistema de login", message="As senhas não coincidem.")
            else:
                self.cursor.execute("""
                    INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
                    VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
                self.conn.commit()
                messagebox.showinfo(title="Sistema de login", message=f"Parabéns {self.username_cadastro}, seus dados foram cadastrados com sucesso!")
                self.limpa_entry_cadastro()
        except Exception as e:
            messagebox.showerror(title="Sistema de login", message=f"Erro no processamento do seu cadastro!\n{e}")
        finally:
            self.desconecta_db()

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.conecta_db()

        try:
            self.cursor.execute("""SELECT * FROM Usuarios WHERE Username = ? AND Senha = ?""", (self.username_login, self.senha_login))
            self.verifica_dados = self.cursor.fetchone()

            if (self.username_login == "" or self.senha_login == ""):
                messagebox.showwarning(title="Sistema de login", message="Por favor, preencha todos os campos!")
            elif self.verifica_dados:
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_login}, login feito com sucesso!")
                self.limpa_entry_login()
            else:
                messagebox.showerror(title="Sistema de login", message="Dados não encontrados no sistema. Verifique suas informações ou cadastre-se.")
        except Exception as e:
            messagebox.showerror(title="Sistema de login", message=f"Erro ao tentar fazer login.\n{e}")
        finally:
            self.desconecta_db()


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()

    def configuracoes_da_janela_inicial(self):
        self.geometry("800x600")
        self.title("Sistema de Login")
        self.resizable(False, False)

    def redimensionar_imagem(self, caminho, largura, altura):
        imagem = Image.open(caminho)
        imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagem)

    def tela_de_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.img = self.redimensionar_imagem("logi-img.png", 400, 600)
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.place(x=0, y=0)

        self.frame_login = ctk.CTkFrame(self, width=350, height=580)
        self.frame_login.place(x=420, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Century Gothic bold", 24))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=330, placeholder_text="Seu nome de usuário..", font=("Century Gothic", 16), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=330, placeholder_text="Sua senha..", font=("Century Gothic", 16), corner_radius=15, show="°")
        self.senha_login_entry.grid(row=2, column=0, pady=10, padx=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", font=("Century Gothic", 12), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, pady=10, padx=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=330, text="FAZER LOGIN", font=("Century Gothic", 16), corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, pady=10, padx=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=330, fg_color="green", hover_color="#050", text="FAZER CADASTRO", font=("Century Gothic", 16), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, pady=10, padx=10)

    def tela_de_cadastro(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=580)
        self.frame_cadastro.place(x=420, y=10)

        self.lb_title_cadastro = ctk.CTkLabel(self.frame_cadastro, text="Crie sua conta", font=("Century Gothic bold", 24))
        self.lb_title_cadastro.grid(row=0, column=0, padx=10, pady=10)

        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Seu nome de usuário..", font=("Century Gothic", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Email..", font=("Century Gothic", 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, pady=5, padx=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Senha..", font=("Century Gothic", 16), corner_radius=15, show="°")
        self.senha_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Confirme sua senha..", font=("Century Gothic", 16), corner_radius=15, show="°")
        self.confirma_senha_entry.grid(row=4, column=0, pady=5, padx=10)

        self.ver_senha_cadastro = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Century Gothic", 12), corner_radius=20)
        self.ver_senha_cadastro.grid(row=5, column=0, pady=10, padx=5)

        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=330, fg_color="green", hover_color="#050", text="CADASTRAR", font=("Century Gothic", 16), corner_radius=15, command=self.cadastrar_user)
        self.btn_cadastrar_user.grid(row=6, column=0, pady=5, padx=10)

        self.btn_voltar_login = ctk.CTkButton(self.frame_cadastro, width=330, text="VOLTAR PARA LOGIN", font=("Century Gothic", 16), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.btn_voltar_login.grid(row=7, column=0, pady=5, padx=10)

    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)


if __name__ == "__main__":
    app = App()
    app.mainloop()

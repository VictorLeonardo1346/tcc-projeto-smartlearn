from tkinter import messagebox
import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import sqlite3
import webbrowser
import os

class BackEnd():
    def conecta_db(self):
        caminho_absoluto = os.path.abspath("Sistema_cadastros.db")
        self.conn = sqlite3.connect(caminho_absoluto)
        self.cursor = self.conn.cursor()

    def desconecta_db(self):
        self.conn.close()

    def cria_tabela(self):
        self.conecta_db()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Usuarios(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL,
            Confirma_Senha TEXT NOT NULL
        );""")
        self.conn.commit()
        self.desconecta_db()

    def cadastrar_user(self):
        username = self.username_cadastro_entry.get()
        email = self.email_cadastro_entry.get()
        senha = self.senha_cadastro_entry.get()
        confirma_senha = self.confirma_senha_entry.get()

        self.conecta_db()
        try:
            if not username or not email or not confirma_senha:
                messagebox.showerror("Erro", "Preencha todos os campos!")
            elif len(username) < 4:
                messagebox.showwarning("Aviso", "O nome deve ter pelo menos 4 caracteres")
            elif len(senha) < 4:
                messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres")
            elif senha != confirma_senha:
                messagebox.showwarning("Aviso", "As senhas não coincidem")
            else:
                self.cursor.execute("INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha) VALUES (?, ?, ?, ?)",
                                    (username, email, senha, confirma_senha))
                self.conn.commit()
                messagebox.showinfo("Sucesso", f"Cadastro de {username} realizado!")
                self.limpa_entry_cadastro()
        finally:
            self.desconecta_db()

    def verifica_login(self):
        username = self.username_login_entry.get()
        senha = self.senha_login_entry.get()
        perfil = self.perfil_var.get()

        self.conecta_db()
        try:
            self.cursor.execute("SELECT * FROM Usuarios WHERE Username=? AND Senha=?", (username, senha))
            resultado = self.cursor.fetchone()
            if not username or not senha:
                messagebox.showwarning("Aviso", "Preencha todos os campos")
            elif resultado:
                self.username_login = username  # Para usar na tela de boas-vindas
                if perfil == "Aluno":
                    self.pagina_aluno()
                else:
                    self.pagina_professor()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos")
        finally:
            self.desconecta_db()


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Sistema de Login")
        self.resizable(False, False)
        self.configure(fg_color="#2E2E2E")
        self.cria_tabela()
        self.tela_de_login()

    def redimensionar_imagem(self, caminho, largura, altura):
        imagem = Image.open(caminho)
        imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagem)

    def centralizar_frame(self, frame, largura, altura):
        self.update_idletasks()
        x = (self.winfo_width() - largura) // 2
        y = (self.winfo_height() - altura) // 2
        frame.place(x=x, y=y)

    # Tela de login
    def tela_de_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Imagem de fundo
        self.img = self.redimensionar_imagem("logi-img.png", 800, 600)
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.place(x=0, y=0)
        self.lb_img.lower()

        # Frame centralizado
        self.frame_login = ctk.CTkFrame(self, width=350, height=400, fg_color="#FF0000", corner_radius=0)
        self.centralizar_frame(self.frame_login, 350, 400)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Century Gothic", 24), text_color="white")
        self.lb_title.pack(pady=20)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=330, placeholder_text="Nome de usuário")
        self.username_login_entry.pack(pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=330, placeholder_text="Senha", show="°")
        self.senha_login_entry.pack(pady=10)

        self.perfil_var = StringVar(value="Aluno")
        frame_radios = Frame(self.frame_login, bg="#FF0000")
        frame_radios.pack(pady=10)
        Radiobutton(frame_radios, text="Aluno", variable=self.perfil_var, value="Aluno", bg="#FF0000", fg="white", selectcolor="#2E2E2E").pack(side=LEFT, padx=10)
        Radiobutton(frame_radios, text="Professor", variable=self.perfil_var, value="Professor", bg="#FF0000", fg="white", selectcolor="#2E2E2E").pack(side=LEFT, padx=10)

        frame_botoes = Frame(self.frame_login, bg="#FF0000")
        frame_botoes.pack(pady=20)
        ctk.CTkButton(frame_botoes, width=150, text="FAZER LOGIN", command=self.verifica_login).pack(side=LEFT, padx=10)
        ctk.CTkButton(frame_botoes, width=150, text="CADASTRAR", fg_color="green", hover_color="#050", command=self.tela_de_cadastro).pack(side=LEFT, padx=10)

        # Barra inferior fixa
        self.barra_inferior = ctk.CTkFrame(self, height=30, fg_color="#660000")
        self.barra_inferior.pack(side=BOTTOM, fill=X)

    # Tela de cadastro de usuarios
    def tela_de_cadastro(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Imagem de fundo
        self.img = self.redimensionar_imagem("logi-img.png", 800, 600)
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.place(x=0, y=0)
        self.lb_img.lower()

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=400, fg_color="#FF0000", corner_radius=0)
        self.centralizar_frame(self.frame_cadastro, 350, 400)

        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Cadastro de Usuário", font=("Century Gothic", 24), text_color="white")
        self.lb_title.pack(pady=20)

        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Nome de usuário")
        self.username_cadastro_entry.pack(pady=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="E-mail")
        self.email_cadastro_entry.pack(pady=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Senha", show="°")
        self.senha_cadastro_entry.pack(pady=10)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Confirme a senha", show="°")
        self.confirma_senha_entry.pack(pady=10)

        ctk.CTkButton(self.frame_cadastro, width=330, text="FAZER CADASTRO", fg_color="green", hover_color="#050", command=self.cadastrar_user).pack(pady=10)
        ctk.CTkButton(self.frame_cadastro, width=330, text="VOLTAR", fg_color="#555555", hover_color="#333333", command=self.tela_de_login).pack(pady=5)

        # Barra inferior fixa
        self.barra_inferior = ctk.CTkFrame(self, height=30, fg_color="#660000")
        self.barra_inferior.pack(side=BOTTOM, fill=X)

    # pagina de boas vindas
    def pagina_aluno(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Barra inferior fixa
        self.barra_inferior = ctk.CTkFrame(self, height=30, fg_color="#660000")
        self.barra_inferior.pack(side=BOTTOM, fill=X)

        # Boas-vindas
        ctk.CTkLabel(self, text=f"Bem-vindo(a) Aluno, {self.username_login}!", font=("Century Gothic", 24), text_color="white").place(relx=0.5, rely=0.3, anchor=CENTER)

        # Botões centralizados
        ctk.CTkButton(self, text="IR PARA QUESTIONÁRIO", font=("Century Gothic", 16), command=self.abrir_questionario).place(relx=0.5, rely=0.45, anchor=CENTER)
        ctk.CTkButton(self, text="SAIR DO SISTEMA", font=("Century Gothic", 16), fg_color="red", hover_color="#800", command=self.tela_de_login).place(relx=0.5, rely=0.55, anchor=CENTER)

    def pagina_professor(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Barra inferior fixa
        self.barra_inferior = ctk.CTkFrame(self, height=30, fg_color="#660000")
        self.barra_inferior.pack(side=BOTTOM, fill=X)

        # Boas-vindas
        ctk.CTkLabel(self, text=f"Bem-vindo(a) Professor, {self.username_login}!", font=("Century Gothic", 24), text_color="white").place(relx=0.5, rely=0.3, anchor=CENTER)

        # Botões centralizados
        ctk.CTkButton(self, text="GERENCIAR QUESTIONÁRIOS", font=("Century Gothic", 16)).place(relx=0.5, rely=0.45, anchor=CENTER)
        ctk.CTkButton(self, text="SAIR DO SISTEMA", font=("Century Gothic", 16), fg_color="red", hover_color="#800", command=self.tela_de_login).place(relx=0.5, rely=0.55, anchor=CENTER)

    def abrir_questionario(self):
        caminho_html = os.path.abspath("questionario/index.html")
        webbrowser.open_new_tab(f"file:///{caminho_html}")

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

import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import os
from tkinter import messagebox
import sqlite3

BASE_URL = "http://127.0.0.1:5001"  # URL do Flask

# ----------------------------
# Página de Login
# ----------------------------
class LoginPage:
    def __init__(self, app, user_manager, professores_fixos):
        self.app = app
        self.user_manager = user_manager
        self.professores_fixos = professores_fixos

    def mostrar(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        # Imagem de fundo
        self.img = self.app.redimensionar_imagem("assets/logi-img.png", 800, 600)
        self.lb_img = ctk.CTkLabel(self.app, text=None, image=self.img)
        self.lb_img.image = self.img
        self.lb_img.place(x=0, y=0)
        self.lb_img.lower()

        # Frame central
        self.frame = ctk.CTkFrame(self.app, width=350, height=400, fg_color="#FF0000", corner_radius=0)
        self.app.centralizar_frame(self.frame, 350, 400)

        # Título
        ctk.CTkLabel(self.frame, text="Faça o seu Login", font=("Century Gothic", 24), text_color="white").pack(pady=20)

        # Entradas
        self.username_entry = ctk.CTkEntry(self.frame, width=330, placeholder_text="Nome de usuário ou e-mail")
        self.username_entry.pack(pady=10)
        self.senha_entry = ctk.CTkEntry(self.frame, width=330, placeholder_text="Senha", show="°")
        self.senha_entry.pack(pady=10)

        # Perfil
        self.perfil_var = StringVar(value="Aluno")
        frame_radios = Frame(self.frame, bg="#FF0000")
        frame_radios.pack(pady=10)
        Radiobutton(frame_radios, text="Aluno", variable=self.perfil_var, value="Aluno", bg="#FF0000", fg="white", selectcolor="#2E2E2E").pack(side=LEFT, padx=10)
        Radiobutton(frame_radios, text="Professor", variable=self.perfil_var, value="Professor", bg="#FF0000", fg="white", selectcolor="#2E2E2E").pack(side=LEFT, padx=10)

        # Botões
        frame_botoes = Frame(self.frame, bg="#FF0000")
        frame_botoes.pack(pady=20)
        ctk.CTkButton(frame_botoes, width=150, text="FAZER LOGIN", command=self.verifica_login).pack(side=LEFT, padx=10)
        ctk.CTkButton(frame_botoes, width=150, text="CADASTRAR", fg_color="green", hover_color="#050", command=self.app.mostrar_cadastro).pack(side=LEFT, padx=10)

        # Barra inferior
        ctk.CTkFrame(self.app, height=30, fg_color="#660000").pack(side=BOTTOM, fill=X)

    def verifica_login(self):
        username = self.username_entry.get()
        senha = self.senha_entry.get()
        perfil = self.perfil_var.get()

        if not username or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        if perfil == "Aluno":
            if self.user_manager.login(username, senha):
                self.app.username_login = username
                self.app.mostrar_aluno()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos")
        elif perfil == "Professor":
            if username in self.professores_fixos and self.professores_fixos[username]["senha"] == senha:
                self.app.username_login = self.professores_fixos[username]["nome"]
                self.app.mostrar_professor()
            else:
                messagebox.showerror("Erro", "Usuário ou senha de professor incorretos")

# ----------------------------
# Página de Cadastro
# ----------------------------
class CadastroPage:
    def __init__(self, app, user_manager):
        self.app = app
        self.user_manager = user_manager

    def mostrar(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.img = self.app.redimensionar_imagem("assets/logi-img.png", 800, 600)
        lb_img = ctk.CTkLabel(self.app, text=None, image=self.img)
        lb_img.image = self.img
        lb_img.place(x=0, y=0)
        lb_img.lower()

        self.frame = ctk.CTkFrame(self.app, width=350, height=400, fg_color="#FF0000", corner_radius=0)
        self.app.centralizar_frame(self.frame, 350, 400)

        ctk.CTkLabel(self.frame, text="Cadastro de Aluno", font=("Century Gothic", 24), text_color="white").pack(pady=20)

        # Entradas
        self.username_entry = ctk.CTkEntry(self.frame, width=330, placeholder_text="Nome de usuário")
        self.username_entry.pack(pady=10)
        self.email_entry = ctk.CTkEntry(self.frame, width=330, placeholder_text="E-mail")
        self.email_entry.pack(pady=10)
        self.senha_entry = ctk.CTkEntry(self.frame, width=330, placeholder_text="Senha", show="°")
        self.senha_entry.pack(pady=10)
        self.confirma_entry = ctk.CTkEntry(self.frame, width=330, placeholder_text="Confirme a senha", show="°")
        self.confirma_entry.pack(pady=10)

        # Botões
        ctk.CTkButton(self.frame, width=330, text="FAZER CADASTRO", fg_color="green", hover_color="#050", command=self.cadastrar).pack(pady=10)
        ctk.CTkButton(self.frame, width=330, text="VOLTAR", fg_color="#555555", hover_color="#333333", command=self.app.mostrar_login).pack(pady=5)

        # Barra inferior
        ctk.CTkFrame(self.app, height=30, fg_color="#660000").pack(side=BOTTOM, fill=X)

    def cadastrar(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        confirma_senha = self.confirma_entry.get()
        if self.user_manager.cadastrar(username, email, senha, confirma_senha):
            self.username_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.senha_entry.delete(0, END)
            self.confirma_entry.delete(0, END)

# ----------------------------
# Página do Aluno
# ----------------------------
class AlunoPage:
    def __init__(self, app):
        self.app = app

    def mostrar(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        # Barra inferior
        ctk.CTkFrame(self.app, height=30, fg_color="#660000").pack(side=BOTTOM, fill=X)

        # Saudação
        ctk.CTkLabel(
            self.app,
            text=f"Bem-vindo(a) Aluno, {self.app.username_login}!",
            font=("Century Gothic", 24),
            text_color="white"
        ).place(relx=0.5, rely=0.3, anchor=CENTER)

        # Botões
        ctk.CTkButton(
            self.app,
            text="ACESSAR FORMULÁRIOS",
            font=("Century Gothic", 16),
            fg_color="#007ACC",
            hover_color="#005F99",
            command=self.abrir_questionario
        ).place(relx=0.5, rely=0.5, anchor=CENTER)

        ctk.CTkButton(
            self.app,
            text="SAIR DO SISTEMA",
            font=("Century Gothic", 16),
            fg_color="red",
            hover_color="#800",
            command=self.app.mostrar_login
        ).place(relx=0.5, rely=0.58, anchor=CENTER)

    def abrir_questionario(self):
        """Abre o questionário mais recente salvo no banco, se existir"""
        try:
            conn = sqlite3.connect("banco.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM questionarios ORDER BY id DESC LIMIT 1")
            dado = cursor.fetchone()
            conn.close()

            if dado:
                id_questionario = dado[0]
                url = f"{BASE_URL}/aluno/responder/{id_questionario}"
                webbrowser.open_new_tab(url)
            else:
                messagebox.showinfo("Aviso", "Nenhum questionário encontrado no banco.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o questionário.\n{e}")

# ----------------------------
# Página do Professor
# ----------------------------
class ProfessorPage:
    def __init__(self, app):
        self.app = app

    def mostrar(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        # Barra inferior
        ctk.CTkFrame(self.app, height=30, fg_color="#660000").pack(side=BOTTOM, fill=X)

        # Saudação
        ctk.CTkLabel(
            self.app,
            text=f"Bem-vindo(a) Professor, {self.app.username_login}!",
            font=("Century Gothic", 24),
            text_color="white"
        ).place(relx=0.5, rely=0.3, anchor=CENTER)

        # Botão criar questionário
        ctk.CTkButton(
            self.app,
            text="CRIAR QUESTIONÁRIO",
            font=("Century Gothic", 16),
            fg_color="#007ACC",
            hover_color="#005F99",
            command=self.abrir_criacao_questionario
        ).place(relx=0.5, rely=0.45, anchor=CENTER)

        # Botão gerenciar questionários (opcional)
        ctk.CTkButton(
            self.app,
            text="GERENCIAR QUESTIONÁRIOS",
            font=("Century Gothic", 16)
        ).place(relx=0.5, rely=0.52, anchor=CENTER)

        # Botão sair
        ctk.CTkButton(
            self.app,
            text="SAIR DO SISTEMA",
            font=("Century Gothic", 16),
            fg_color="red",
            hover_color="#800",
            command=self.app.mostrar_login
        ).place(relx=0.5, rely=0.59, anchor=CENTER)

    def abrir_criacao_questionario(self):
        caminho_html = os.path.abspath("criacaoQuestionario/quiz_form.html")
        webbrowser.open_new_tab(f"file:///{caminho_html}")

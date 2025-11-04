# backend/aluno.py
from tkinter import messagebox
from .bancodedados import Database  

class UserManager:
    def __init__(self):
        self.db = Database()

    def cadastrar(self, username, email, senha, confirma_senha):
        if not username or not email or not senha or not confirma_senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return False
        if len(username) < 4:
            messagebox.showwarning("Aviso", "O nome deve ter pelo menos 4 caracteres")
            return False
        if len(senha) < 4:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 4 caracteres")
            return False
        if senha != confirma_senha:
            messagebox.showwarning("Aviso", "As senhas não coincidem")
            return False

        # Usa a conexão e cursor já criados no Database
        conn = self.db.conn
        cursor = self.db.cursor

        cursor.execute(
            "INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha) VALUES (?, ?, ?, ?)",
            (username, email, senha, confirma_senha)
        )
        conn.commit()

        messagebox.showinfo("Sucesso", f"Cadastro de {username} realizado com sucesso!")
        return True

    def login(self, username, senha):
        """
        Retorna (id, username) se login for bem sucedido, senão retorna None.
        """
        user = self.db.verifica_login(username, senha)
        # verifica_login retorna a linha inteira (Id, Username, Email, Senha, Confirma_Senha)
        if user:
            user_id = user[0]
            messagebox.showinfo("Login", f"Bem-vindo(a), {username}!")
            return user_id
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            return None

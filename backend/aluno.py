from tkinter import messagebox
from bancodedados import Database  

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

        conn, cursor = self.db.connect()
        cursor.execute(
            "INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha) VALUES (?, ?, ?, ?)",
            (username, email, senha, confirma_senha)
        )
        conn.commit()
        self.db.close()
        messagebox.showinfo("Sucesso", f"Cadastro de {username} realizado!")
        return True

    def login(self, username, senha):
        conn, cursor = self.db.connect()
        cursor.execute("SELECT * FROM Usuarios WHERE Username=? AND Senha=?", (username, senha))
        result = cursor.fetchone()
        self.db.close()
        return result is not None

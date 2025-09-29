import sqlite3
import os

class Database:
    def __init__(self, db_name="sistema_cadastros.db"):
        caminho_absoluto = os.path.abspath(db_name)
        self.conn = sqlite3.connect(caminho_absoluto)
        self.cursor = self.conn.cursor()
        self.cria_tabela()

    def cria_tabela(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Usuarios(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL,
            Confirma_Senha TEXT NOT NULL
        );""")
        self.conn.commit()

    def cadastrar_user(self, username, email, senha, confirma_senha):
        self.cursor.execute(
            "INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha) VALUES (?, ?, ?, ?)",
            (username, email, senha, confirma_senha),
        )
        self.conn.commit()

    def verifica_login(self, username, senha):
        self.cursor.execute(
            "SELECT * FROM Usuarios WHERE Username=? AND Senha=?", (username, senha)
        )
        return self.cursor.fetchone()

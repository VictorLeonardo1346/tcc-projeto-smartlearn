import sqlite3
import os

class Database:
    def __init__(self, db_name="sistema_cadastros.db"):
        caminho_absoluto = os.path.abspath(db_name)
        # Permite uso em múltiplas threads (necessário para Flask)
        self.conn = sqlite3.connect(caminho_absoluto, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cria_tabela()

    def cria_tabela(self):
        # Tabela de usuários
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)

        # Tabela de questionários
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Questionarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Materia TEXT NOT NULL,
                Titulo TEXT NOT NULL,
                Dificuldade TEXT NOT NULL,
                DataEntrega TEXT NOT NULL
            );
        """)

        # Tabela de questões
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Questoes(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                QuestionarioId INTEGER NOT NULL,
                Enunciado TEXT NOT NULL,
                AlternativaA TEXT,
                AlternativaB TEXT,
                AlternativaC TEXT,
                AlternativaD TEXT,
                Correta TEXT,
                ImagemPath TEXT,
                FOREIGN KEY (QuestionarioId) REFERENCES Questionarios(Id)
            );
        """)

        self.conn.commit()

    # ---------------------------------
    # Usuários
    # ---------------------------------
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

    # ---------------------------------
    # Questionários e Questões
    # ---------------------------------
    def criar_questionario(self, materia, titulo, dificuldade, data_entrega):
        self.cursor.execute("""
            INSERT INTO Questionarios (Materia, Titulo, Dificuldade, DataEntrega)
            VALUES (?, ?, ?, ?)
        """, (materia, titulo, dificuldade, data_entrega))
        self.conn.commit()
        return self.cursor.lastrowid

    def adicionar_questao(self, questionario_id, enunciado, alternativas, correta, Imagem=None):
        # alternativas deve ser uma lista de 4 elementos [a, b, c, d]
        self.cursor.execute("""
            INSERT INTO Questoes (
                QuestionarioId, Enunciado, AlternativaA, AlternativaB, AlternativaC, AlternativaD, Correta, ImagemPath
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            questionario_id,
            enunciado,
            alternativas[0] if len(alternativas) > 0 else None,
            alternativas[1] if len(alternativas) > 1 else None,
            alternativas[2] if len(alternativas) > 2 else None,
            alternativas[3] if len(alternativas) > 3 else None,
            correta,
            Imagem
        ))
        self.conn.commit()

    def listar_questionarios(self):
        self.cursor.execute("SELECT Id, Materia, Titulo, Dificuldade, DataEntrega FROM Questionarios ORDER BY Id DESC")
        return self.cursor.fetchall()

    def buscar_questoes(self, questionario_id):
        self.cursor.execute("""
            SELECT Id, Enunciado, AlternativaA, AlternativaB, AlternativaC, AlternativaD, Correta, ImagemPath
            FROM Questoes WHERE QuestionarioId = ?
        """, (questionario_id,))
        return self.cursor.fetchall()


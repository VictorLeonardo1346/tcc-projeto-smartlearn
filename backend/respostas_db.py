# backend/respostas_db.py
import sqlite3
import os
from datetime import datetime

class RespostasDB:
    def __init__(self, db_name="respostas_enviadas_aluno.db"):
        path = os.path.abspath(db_name)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cria_tabelas()

    def cria_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Respostas(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                AlunoId INTEGER NOT NULL,
                QuestionarioId INTEGER NOT NULL,
                QuestaoId INTEGER NOT NULL,
                Resposta TEXT,
                Correta TEXT,
                Pontos INTEGER,
                EnviadoEm TEXT
            );
        """)
        self.conn.commit()

    # Verifica se o aluno já respondeu o questionário
    def aluno_ja_respondeu(self, aluno_id, questionario_id):
        self.cursor.execute("""
            SELECT COUNT(*) FROM Respostas
            WHERE AlunoId = ? AND QuestionarioId = ?
        """, (aluno_id, questionario_id))
        return self.cursor.fetchone()[0] > 0

    # Salvar resposta individual
    def salvar_resposta(self, aluno_id, questionario_id, questao_id, resposta, correta, pontos):
        agora = datetime.utcnow().isoformat()
        self.cursor.execute("""
            INSERT INTO Respostas (AlunoId, QuestionarioId, QuestaoId, Resposta, Correta, Pontos, EnviadoEm)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (aluno_id, questionario_id, questao_id, resposta, correta, pontos, agora))
        self.conn.commit()

    # Salvar respostas em lote
    def salvar_respostas_em_lote(self, aluno_id, questionario_id, respostas_list):
        for r in respostas_list:
            self.salvar_resposta(
                aluno_id,
                questionario_id,
                r.get("questao_id"),
                r.get("resposta"),
                r.get("correta"),
                r.get("pontos", 0)
            )

    # Total da nota
    def calcular_pontuacao_final(self, aluno_id, questionario_id):
        self.cursor.execute("""
            SELECT SUM(Pontos) FROM Respostas
            WHERE AlunoId = ? AND QuestionarioId = ?
        """, (aluno_id, questionario_id))
        total = self.cursor.fetchone()[0]
        return total if total else 0

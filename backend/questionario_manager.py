import json
from tkinter import messagebox
from .bancodedados import Database

class QuestionarioManager:
    def __init__(self):
        self.db = Database()

    def salvar_questionario(self, materia, titulo, dificuldade, data_entrega, questoes_json):
        """
        Salva um questionário e suas questões no banco.
        questoes_json é uma lista de dicionários com:
        {
            'pergunta': str,
            'alternativas': [a, b, c, d],
            'correta': 'a'|'b'|'c'|'d'
        }
        """
        cursor = self.db.cursor
        conn = self.db.conn

        cursor.execute(
            "INSERT INTO Questionarios (Materia, Titulo, Dificuldade, DataEntrega) VALUES (?, ?, ?, ?)",
            (materia, titulo, dificuldade, data_entrega)
        )
        questionario_id = cursor.lastrowid

        for q in questoes_json:
            cursor.execute(
                """INSERT INTO Questoes
                (QuestionarioId, Enunciado, AlternativaA, AlternativaB, AlternativaC, AlternativaD, Correta)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    questionario_id,
                    q["pergunta"],
                    q["alternativas"][0] if len(q["alternativas"]) > 0 else None,
                    q["alternativas"][1] if len(q["alternativas"]) > 1 else None,
                    q["alternativas"][2] if len(q["alternativas"]) > 2 else None,
                    q["alternativas"][3] if len(q["alternativas"]) > 3 else None,
                    q["correta"],
                )
            )

        conn.commit()
        messagebox.showinfo("Sucesso", f"Atividade '{titulo}' salva com sucesso!")

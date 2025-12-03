import sqlite3

# Cria ou conecta ao banco
conn = sqlite3.connect("desempenho.db")
cursor = conn.cursor()

# Cria tabela Desempenho
cursor.execute("""
CREATE TABLE IF NOT EXISTS Desempenho (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    AlunoId INTEGER NOT NULL,
    QuestionarioId INTEGER NOT NULL,
    QuestaoId INTEGER NOT NULL,
    TempoResposta REAL,
    Erros INTEGER,
    DificuldadeAtual TEXT,
    ProximaDificuldade TEXT,
    DataRegistro DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("Banco desempenho.db criado com sucesso!")

import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE Questoes
SET DificuldadeQuestao = LOWER(DificuldadeQuestao)
""")

conn.commit()
conn.close()

print("Dificuldades corrigidas para minúsculo!")

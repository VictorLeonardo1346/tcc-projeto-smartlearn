import sqlite3

# conecta no banco
conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

# apagar todas as questões
cursor.execute("DELETE FROM Questoes")
print("Todas as questões apagadas.")

# apagar todos os questionários
cursor.execute("DELETE FROM Questionarios")
print("Todos os questionários apagados.")

# resetar autoincrement (SQLite: tabela sqlite_sequence)
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Questoes'")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Questionarios'")
print("IDs reiniciados para 1.")

# salvar alterações
conn.commit()
conn.close()

print("Banco totalmente limpo e IDs reiniciados!")

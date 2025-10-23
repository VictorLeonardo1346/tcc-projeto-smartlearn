import sqlite3

# Caminho para o banco de dados
banco = "Sistema_cadastros.db"  # altere se o nome for diferente

# Conexão com o banco
con = sqlite3.connect(banco)
cur = con.cursor()

try:
    # 1️⃣ Apaga usuários de teste
    cur.execute("DELETE FROM usuarios WHERE Username IN ('teste', 'tets');")
    
    # 2️⃣ Remove todos os outros, exceto 'pedro' (opcional)
    cur.execute("DELETE FROM usuarios WHERE Username != 'pedro';")

    # 3️⃣ Zera o contador de autoincremento da tabela (coluna correta: 'name')
    cur.execute("DELETE FROM sqlite_sequence WHERE name='usuarios';")

    # 4️⃣ Define o ID do usuário pedro como 1
    cur.execute("UPDATE usuarios SET id = 1 WHERE Username = 'pedro';")

    con.commit()
    print("✅ Limpeza concluída com sucesso!")
except Exception as e:
    print("❌ Erro ao limpar tabela:", e)
finally:
    con.close()

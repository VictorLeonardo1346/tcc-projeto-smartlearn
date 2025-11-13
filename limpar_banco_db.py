import sqlite3

# Caminhos dos bancos
banco_principal = "banco.db"
banco_respostas = "respostas_enviadas_aluno.db"

def limpar_banco_principal():
    try:
        con = sqlite3.connect(banco_principal)
        cur = con.cursor()

        # Apagar dados das tabelas de questionários e questões
        cur.execute("DELETE FROM Questoes;")
        cur.execute("DELETE FROM Questionarios;")

        con.commit()
        con.close()
        print("✅ Tabelas 'Questoes' e 'Questionarios' limpas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao limpar o banco principal: {e}")

def limpar_banco_respostas():
    try:
        con = sqlite3.connect(banco_respostas)
        cur = con.cursor()

        # Apagar dados do ranking
        cur.execute("DELETE FROM ranking;")

        con.commit()
        con.close()
        print("✅ Tabela 'ranking' limpa com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao limpar o banco de respostas: {e}")

if __name__ == "__main__":
    limpar_banco_principal()
    limpar_banco_respostas()
    print("🧹 Limpeza concluída!")

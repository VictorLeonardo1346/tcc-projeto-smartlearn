import sqlite3

DB_PATH = "banco.db"

def limpar_tabela(tabela):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabela};")  # deleta todos os registros
    conn.commit()
    conn.close()
    print(f"Tabela '{tabela}' limpa com sucesso!")

if __name__ == "__main__":
    limpar_tabela("Questionarios")

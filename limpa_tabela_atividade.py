import os

arquivo = "banco.db"

if os.path.exists(arquivo):
    os.remove(arquivo)
    print("✅ banco.db deletado com sucesso! Ele será recriado quando o sistema rodar.")
else:
    print("⚠️ banco.db não existia, o sistema vai criar um novo.")


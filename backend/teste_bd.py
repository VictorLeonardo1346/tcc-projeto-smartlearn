from bancodedados import Database

# Inicializa o banco
db = Database(db_name="banco.db")

# 1️⃣ Cria um questionário de teste
questionario_id = db.criar_questionario(
    materia="Matemática",
    titulo="Teste de Adição",
    dificuldade="Fácil",
    data_entrega="2025-12-10"
)
print("Questionário criado com ID:", questionario_id)

# 2️⃣ Adiciona questões manualmente
db.adicionar_questao(
    questionario_id,
    enunciado="Quanto é 2 + 2?",
    alternativas=["1", "2", "3", "4"],
    correta="d"
)

db.adicionar_questao(
    questionario_id,
    enunciado="Quanto é 5 - 3?",
    alternativas=["1", "2", "3", "4"],
    correta="b"
)

print("Questões adicionadas!")

# 3️⃣ Busca todas as questões desse questionário
questoes = db.buscar_questoes(questionario_id)
print("Questões no banco:")
for q in questoes:
    print(q)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.bancodedados import Database

app = Flask(__name__)
CORS(app)

# Inicializa o banco
db = Database(db_name="banco.db")

# ----------------------------
# Rota para salvar questionário (PROFESSOR)
# ----------------------------
@app.route("/salvar_questionario", methods=["POST"])
def salvar_questionario():
    dados = request.get_json()

    materia = dados.get("materia", "")
    titulo = dados.get("titulo", "")
    dificuldade = dados.get("dificuldade", "")
    data_entrega = dados.get("dataEntrega", "")
    questoes = dados.get("questoes", [])

    try:
        questionario_id = db.criar_questionario(materia, titulo, dificuldade, data_entrega)

        for q in questoes:
            enunciado = q.get("enunciado", "")
            alternativas = q.get("alternativas", {})
            correta = q.get("correta", "")

            db.adicionar_questao(
                questionario_id,
                enunciado,
                [alternativas.get("a"), alternativas.get("b"), alternativas.get("c"), alternativas.get("d")],
                correta
            )

        return jsonify({
            "status": "sucesso",
            "mensagem": "Questionário salvo com sucesso!",
            "id": questionario_id
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# ----------------------------
# LISTAR QUESTIONÁRIOS (ALUNO)
# ----------------------------
@app.route("/api/questionarios", methods=["GET"])
def api_questionarios():
    try:
        rows = db.listar_questionarios()
        lista = []
        for r in rows:
            lista.append({
                "id": r[0],
                "materia": r[1],
                "titulo": r[2],
                "dificuldade": r[3],
                "dataEntrega": r[4]
            })
        return jsonify(lista)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# ----------------------------
# BUSCAR QUESTÕES DE UM QUESTIONÁRIO (ALUNO)
# ----------------------------
@app.route("/api/questoes/<int:questionario_id>", methods=["GET"])
def buscar_questoes(questionario_id):
    try:
        rows = db.buscar_questoes(questionario_id)
        questoes = []
        for r in rows:
            questoes.append({
                "id": r[0],
                "enunciado": r[1],
                "alternativas": [r[2], r[3], r[4], r[5]],
                "correta": r[6]
            })
        return jsonify(questoes)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# ----------------------------
# PÁGINAS FRONTEND DO ALUNO
# ----------------------------
@app.route("/aluno")
def aluno_home():
    return render_template("aluno_listar.html")


@app.route("/aluno/responder/<int:questionario_id>")
def aluno_responder(questionario_id):
    return render_template("aluno_responder.html", id=questionario_id)


# ----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "API do SmartLearn rodando!"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)

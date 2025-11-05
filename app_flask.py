from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from backend.bancodedados import Database
from backend.respostas_db import RespostasDB
import os

app = Flask(__name__)
CORS(app)

# Bancos
db = Database(db_name="banco.db")  # questionarios e questoes
res_db = RespostasDB(db_name="respostas_enviadas_aluno.db")  # respostas dos alunos

# ----------------------------
# SALVAR QUESTIONÁRIO (PROFESSOR)
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
            enunciado = q.get("pergunta", "")
            alternativas = q.get("alternativas", [])
            correta = q.get("correta", "")

            db.adicionar_questao(
                questionario_id,
                enunciado,
                [alternativas[0] if len(alternativas) > 0 else "",
                 alternativas[1] if len(alternativas) > 1 else "",
                 alternativas[2] if len(alternativas) > 2 else "",
                 alternativas[3] if len(alternativas) > 3 else ""],
                correta
            )

        return jsonify({"status": "sucesso", "mensagem": "Questionário salvo com sucesso!", "id": questionario_id})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ----------------------------
# LISTAR QUESTIONÁRIOS (API)
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
# BUSCAR QUESTÕES (API)
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
# SALVAR RESPOSTAS DO ALUNO (API)
# ----------------------------
@app.route("/api/salvar_respostas", methods=["POST"])
def salvar_respostas():
    dados = request.get_json()
    aluno_id = dados.get("aluno_id")
    questionario_id = dados.get("questionario_id")
    respostas = dados.get("respostas", [])

    if not aluno_id or not questionario_id:
        return jsonify({"status": "erro", "mensagem": "aluno_id e questionario_id são obrigatórios"}), 400

    try:
        gabarito_rows = db.buscar_questoes(questionario_id)
        gabarito = {r[0]: r[6] for r in gabarito_rows}

        total_questoes = len(gabarito)
        pontos_por_questao = 100 / total_questoes if total_questoes > 0 else 0

        respostas_para_salvar = []
        total_pontos = 0
        acertos = 0
        erros = 0

        for r in respostas:
            qid = r.get("questao_id")
            resp = r.get("resposta")
            correta = gabarito.get(qid)
            pontos = pontos_por_questao if (correta is not None and resp == correta) else 0

            if pontos > 0:
                acertos += 1
            else:
                erros += 1

            total_pontos += pontos

            respostas_para_salvar.append({
                "questao_id": qid,
                "resposta": resp,
                "correta": correta,
                "pontos": pontos
            })

        res_db.salvar_respostas_em_lote(aluno_id, questionario_id, respostas_para_salvar)
        taxa_acertos = (acertos / total_questoes) * 100 if total_questoes else 0

        return jsonify({
            "status": "sucesso",
            "mensagem": "Respostas salvas",
            "pontos_totais": total_pontos,
            "acertos": acertos,
            "erros": erros,
            "taxa_acertos": taxa_acertos
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ----------------------------
# SERVIR ARQUIVOS DO QUIZ (CRIACAOQUESTIONARIO)
# ----------------------------
@app.route("/criacaoQuestionario/<path:filename>")
def criacao_questionario_files(filename):
    return send_from_directory(os.path.join(os.getcwd(), "criacaoQuestionario"), filename)

# ----------------------------
# TEMPLATES - ALUNO
# ----------------------------
@app.route("/aluno")
def aluno_home():
    questionarios = db.listar_questionarios()
    return render_template("aluno_listar.html", questionarios=questionarios)

@app.route("/aluno/responder/<int:questionario_id>")
def aluno_responder(questionario_id):
    return render_template("aluno_responder.html", id=questionario_id, aluno_id=1)

@app.route("/aluno/resultado")
def aluno_resultado():
    return render_template("aluno_resultado.html")

# ----------------------------
# RANKING DO ALUNO
# ----------------------------
@app.route("/aluno/ranking")
def aluno_ranking():
    user_name = request.args.get("user_name", "Você")
    score = request.args.get("score", 0)
    qid = request.args.get("qid", "")
    return render_template("rankingAluno/ranking.html", user_name=user_name, score=score, qid=qid)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "API do SmartLearn rodando!"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)

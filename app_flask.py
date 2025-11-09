from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from backend.bancodedados import Database
from backend.respostas_db import RespostasDB
import sqlite3

app = Flask(__name__)
CORS(app)
app.secret_key = "chave_super_secreta"

# Bancos
db = Database(db_name="banco.db")
res_db = RespostasDB(db_name="respostas_enviadas_aluno.db")
db_cadastros = Database(db_name="Sistema_cadastros.db")

# ----------------------------
# LOGIN
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    nome = request.form.get("nome")
    senha = request.form.get("senha")

    if not nome or not senha:
        return render_template("login.html", mensagem="Preencha todos os campos")

    db_users = Database("Sistema_cadastros.db")
    usuario = db_users.verifica_login(nome, senha)

    if usuario:
        session["aluno_id"] = usuario[0]
        session["aluno_nome"] = usuario[1]
        return redirect("/aluno")
    else:
        return render_template("login.html", mensagem="Usuário ou senha incorretos")

# ----------------------------
# LOGOUT
# ----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

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
                [
                    alternativas[0] if len(alternativas) > 0 else "",
                    alternativas[1] if len(alternativas) > 1 else "",
                    alternativas[2] if len(alternativas) > 2 else "",
                    alternativas[3] if len(alternativas) > 3 else ""
                ],
                correta
            )
        return jsonify({"status": "sucesso", "mensagem": "Questionário salvo com sucesso!", "id": questionario_id})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ----------------------------
# API QUESTIONÁRIOS
# ----------------------------
@app.route("/api/questionarios", methods=["GET"])
def api_questionarios():
    try:
        rows = db.listar_questionarios()
        lista = [{"id": r[0], "materia": r[1], "titulo": r[2], "dificuldade": r[3], "dataEntrega": r[4]} for r in rows]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ----------------------------
# API QUESTÕES
# ----------------------------
@app.route("/api/questoes/<int:questionario_id>", methods=["GET"])
def buscar_questoes(questionario_id):
    try:
        rows = db.buscar_questoes(questionario_id)
        questoes = [{"id": r[0], "enunciado": r[1], "alternativas": [r[2], r[3], r[4], r[5]], "correta": r[6]} for r in rows]
        return jsonify(questoes)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ----------------------------
# SALVAR RESPOSTAS
# ----------------------------
@app.route("/api/salvar_respostas", methods=["POST"])
def salvar_respostas():
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"status": "erro", "mensagem": "JSON inválido"}), 400

    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return jsonify({"status": "erro", "mensagem": "Sessão expirada. Faça login novamente."}), 403

    questionario_id = dados.get("questionario_id")
    respostas = dados.get("respostas", [])

    if questionario_id is None:
        return jsonify({"status": "erro", "mensagem": "questionario_id é obrigatório"}), 400

    gabarito_rows = db.buscar_questoes(questionario_id)
    if not gabarito_rows:
        return jsonify({"status": "erro", "mensagem": "Questionário sem questões ou inexistente"}), 400

    gabarito = {r[0]: r[6] for r in gabarito_rows}
    total_questoes = len(gabarito)
    pontos_por_questao = 100.0 / total_questoes if total_questoes > 0 else 0.0

    acertos = erros = total_pontos = 0
    respostas_para_salvar = []

    for item in respostas:
        qid = int(item.get("questao_id", 0))
        resp = item.get("resposta")
        correta = gabarito.get(qid)
        acertou = (correta is not None and resp == correta)
        pontos = pontos_por_questao if acertou else 0.0
        acertos += 1 if acertou else 0
        erros += 0 if acertou else 1
        total_pontos += pontos
        respostas_para_salvar.append({"questao_id": qid, "resposta": resp, "correta": correta, "pontos": round(pontos, 2)})

    res_db.salvar_respostas_em_lote(aluno_id, questionario_id, respostas_para_salvar)

    con = sqlite3.connect("respostas_enviadas_aluno.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        AlunoId INTEGER,
        QuestionarioId INTEGER,
        Pontos REAL
    )""")
    cur.execute("INSERT INTO Ranking (AlunoId, QuestionarioId, Pontos) VALUES (?, ?, ?)",
                (aluno_id, questionario_id, round(total_pontos, 2)))
    con.commit()
    con.close()

    taxa_acertos = (acertos / total_questoes) * 100.0 if total_questoes else 0.0
    return jsonify({"status": "sucesso", "mensagem": "Respostas recebidas", "pontos_totais": round(total_pontos,2), "acertos": acertos, "erros": erros, "total": total_questoes, "taxa": round(taxa_acertos,2)})

# ----------------------------
# TEMPLATES ALUNO
# ----------------------------
@app.route("/aluno")
def aluno_home():
    aluno_nome = session.get("aluno_nome")
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login"))

    questionarios = db.listar_questionarios()
    return render_template("aluno_listar.html", questionarios=questionarios, aluno_nome=aluno_nome)

@app.route("/aluno/responder/<int:questionario_id>")
def aluno_responder(questionario_id):
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login"))
    return render_template("aluno_responder.html", id=questionario_id, aluno_id=aluno_id)

@app.route("/aluno/resultado")
def aluno_resultado():
    return render_template("aluno_resultado.html")

@app.route("/aluno/ranking")
def aluno_ranking():
    con = sqlite3.connect("respostas_enviadas_aluno.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        AlunoId INTEGER,
        QuestionarioId INTEGER,
        Pontos REAL
    )""")
    cur.execute("""SELECT AlunoId, SUM(Pontos) as total FROM Ranking GROUP BY AlunoId ORDER BY total DESC""")
    ranking = cur.fetchall()
    con.close()
    ranking_lista = [{"posicao": i+1, "aluno": f"Aluno {r[0]}", "pontos": round(r[1] or 0,2)} for i,r in enumerate(ranking)]
    return render_template("rankingAluno/ranking.html", ranking=ranking_lista)

# ----------------------------
# STATIC FILES
# ----------------------------
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# ----------------------------
# HOME
# ----------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)

from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from backend.bancodedados import Database
from backend.respostas_db import RespostasDB
import os
import sqlite3
from flask_session import Session  # ✅ Correto


app = Flask(__name__)
CORS(app)
app.secret_key = "chave_super_secreta"

# ✅ Configuração correta da sessão
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = os.path.join(os.getcwd(), "flask_sessions")
os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)

Session(app)

# =============================
# Inicialização dos bancos
# =============================
db = Database(db_name="banco.db")
res_db = RespostasDB(db_name="respostas_enviadas_aluno.db")
db_cadastros = Database(db_name="Sistema_cadastros.db")

# =============================
# ROTA: servir arquivos da pasta criacaoQuestionario
# =============================
@app.route("/criacaoQuestionario/<path:filename>")
def criacao_questionario_files(filename):
    raiz = os.path.join(os.getcwd(), "criacaoQuestionario")
    return send_from_directory(raiz, filename)

# =============================
# ROTA: página do professor para criar questionário
# =============================
@app.route("/professor/criar_questionario", methods=["GET"])
def criar_questionario():
    raiz = os.path.join(os.getcwd(), "criacaoQuestionario")
    return send_from_directory(raiz, "quiz_form.html")

# =============================
# LOGIN (agora com suporte a force_login)
# =============================
@app.route("/login", methods=["GET", "POST"])
def login():
    # 🔹 Se a URL tiver ?force_login=true, apaga a sessão antiga
    if request.args.get("force_login") == "true":
        session.clear()

    if request.method == "GET":
        return render_template("login.html")

    nome = request.form.get("nome")
    senha = request.form.get("senha")

    if not nome or not senha:
        return render_template("login.html", mensagem="Preencha todos os campos")

    usuario = db_cadastros.verifica_login(nome, senha)

    if usuario:
        session["aluno_id"] = usuario[0]
        session["aluno_nome"] = usuario[1]
        return redirect("/aluno")
    else:
        return render_template("login.html", mensagem="Usuário ou senha incorretos")

# =============================
# LOGOUT
# =============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------------
# 📘 Rotas do Professor
# -------------------------------
@app.route("/professor/gerenciar")
def gerenciar_questionarios():
    # Agora abre diretamente a página do professor sem exigir login
    return render_template("professor_gerenciar.html")


@app.route("/visualizar_questionario/<int:questionario_id>")
def visualizar_questionario(questionario_id):
    # Também remove a checagem de login
    return render_template("professor_visualizar.html", questionario_id=questionario_id)

# -------------------------------
# 🗑️ API - Excluir Questionário
# -------------------------------
@app.route("/api/excluir_questionario/<int:id>", methods=["DELETE"])
def excluir_questionario(id):
    try:
        db.cursor.execute("DELETE FROM Questoes WHERE QuestionarioId = ?", (id,))
        db.cursor.execute("DELETE FROM Questionarios WHERE Id = ?", (id,))
        db.conn.commit()
        return jsonify({"status": "sucesso", "mensagem": "Questionário excluído com sucesso!"})
    except Exception as e:
        print("Erro ao excluir questionário:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# =============================
# SALVAR QUESTIONÁRIO (PROFESSOR)
# =============================
@app.route("/salvar_questionario", methods=["POST"])
def salvar_questionario():
    try:
        materia = request.form.get("materia", "")
        titulo = request.form.get("titulo", "")
        dificuldade = request.form.get("dificuldade", "")
        data_entrega = request.form.get("dataEntrega", "")

        questoes = []
        index = 0
        while True:
            pergunta = request.form.get(f"pergunta_{index}")
            if not pergunta:
                break

            alternativas = [
                request.form.get(f"alt1_{index}", ""),
                request.form.get(f"alt2_{index}", ""),
                request.form.get(f"alt3_{index}", ""),
                request.form.get(f"alt4_{index}", ""),
            ]
            correta = request.form.get(f"correta_{index}", "")

            questoes.append({
                "pergunta": pergunta,
                "alternativas": alternativas,
                "correta": correta,
                "index": index
            })
            index += 1

        # 📂 Cria a pasta de uploads (se não existir)
        UPLOAD_FOLDER = os.path.join("static", "uploads")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # 💾 Salva o questionário no banco
        questionario_id = db.criar_questionario(materia, titulo, dificuldade, data_entrega)

        # 💾 Salva cada questão e sua imagem (se enviada)
        for q in questoes:
            imagem_file = request.files.get(f"imagem_{q['index']}")
            imagem_path = None

            if imagem_file and imagem_file.filename:
                nome_arquivo = f"q{questionario_id}_{q['index']}_{imagem_file.filename}"
                caminho_completo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
                caminho_completo = caminho_completo.replace("\\", "/")  # 🔹 Aqui está o trecho do Windows

                imagem_file.save(caminho_completo)

                # Caminho acessível via URL (Flask serve via /uploads)
                imagem_path = f"/uploads/{nome_arquivo}"

            db.adicionar_questao(
                questionario_id,
                q["pergunta"],
                q["alternativas"],
                q["correta"],
                imagem_path
            )

        return jsonify({
            "status": "sucesso",
            "mensagem": "Questionário salvo com sucesso!",
            "id": questionario_id
        })

    except Exception as e:
        print("Erro ao salvar questionário:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500



# =============================
# API: listar questionários
# =============================
@app.route("/api/questionarios", methods=["GET"])
def api_questionarios():
    try:
        rows = db.listar_questionarios()
        lista = [{"id": r[0], "materia": r[1], "titulo": r[2], "dificuldade": r[3], "dataEntrega": r[4]} for r in rows]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# =============================
# API: buscar questões de um questionário
# =============================
@app.route("/api/questoes/<int:questionario_id>", methods=["GET"])
def buscar_questoes(questionario_id):
    try:
        rows = db.buscar_questoes(questionario_id)
        questoes = [{"id": r[0], "enunciado": r[1], "alternativas": [r[2], r[3], r[4], r[5]], "correta": r[6], "imagem": r[7] if r[7] else None} for r in rows]
        return jsonify(questoes)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# =============================
# API: salvar respostas do aluno
# =============================
@app.route("/api/salvar_respostas", methods=["POST"])
def salvar_respostas():
    dados = request.get_json(force=True, silent=True)
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

    acertos = 0
    total_pontos = 0.0
    respostas_para_salvar = []

    for item in respostas:
        try:
            qid = int(item.get("questao_id", 0))
        except Exception:
            continue
        resp = str(item.get("resposta", ""))
        correta = gabarito.get(qid)
        acertou = (correta is not None and resp == str(correta))
        pontos = pontos_por_questao if acertou else 0.0
        if acertou:
            acertos += 1
        total_pontos += pontos
        respostas_para_salvar.append({"questao_id": qid, "resposta": resp, "correta": correta, "pontos": round(pontos, 2)})

    try:
        res_db.salvar_respostas_em_lote(aluno_id, questionario_id, respostas_para_salvar)
    except Exception:
        pass

    # --- Atualiza tabela Ranking ---
    try:
        con = sqlite3.connect("respostas_enviadas_aluno.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            AlunoId INTEGER,
            QuestionarioId INTEGER,
            Pontos REAL
        )""")

        cur.execute(
            "SELECT id FROM Ranking WHERE AlunoId = ? AND QuestionarioId = ?",
            (aluno_id, questionario_id)
        )
        existente = cur.fetchone()

        if existente:
            cur.execute(
                "UPDATE Ranking SET Pontos = ? WHERE id = ?",
                (round(total_pontos, 2), existente[0])
            )
        else:
            cur.execute(
                "INSERT INTO Ranking (AlunoId, QuestionarioId, Pontos) VALUES (?, ?, ?)",
                (aluno_id, questionario_id, round(total_pontos, 2))
            )

        con.commit()
        con.close()
    except Exception as e:
        print("Erro ao atualizar ranking:", e)

    session["ultimo_questionario_id"] = questionario_id
    session["ultimo_pontos"] = round(total_pontos, 2)
    session["ultimo_acertos"] = acertos
    session["ultimo_erros"] = total_questoes - acertos
    session["ultimo_total"] = total_questoes
    session["ultimo_taxa"] = round((acertos / total_questoes) * 100, 2) if total_questoes > 0 else 0

    return jsonify({
        "status": "sucesso",
        "mensagem": "Respostas salvas com sucesso!",
        "pontos_totais": round(total_pontos, 2),
        "acertos": acertos,
        "erros": total_questoes - acertos,
        "total": total_questoes,
        "taxa": session["ultimo_taxa"]
    })

# =============================
# TELA ALUNO - HOME (corrigida)
# =============================
@app.route("/aluno")
def aluno_home():
    aluno_id = session.get("aluno_id")

    # 🔹 Se não houver sessão, força o login
    if not aluno_id:
        return redirect(url_for("login", force_login="true"))

    aluno_nome = session.get("aluno_nome")
    questionarios = db.listar_questionarios()
    return render_template("aluno_listar.html", questionarios=questionarios, aluno_nome=aluno_nome)

# =============================
# TELA RESPONDER
# =============================
@app.route("/aluno/responder/<int:questionario_id>")
def aluno_responder(questionario_id):
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login", force_login="true"))
    return render_template("aluno_responder.html", id=questionario_id, aluno_id=aluno_id)

# =============================
# TELA RESULTADO
# =============================
@app.route("/aluno/resultado")
def aluno_resultado():
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login", force_login="true"))
    return render_template(
        "aluno_resultado.html",
        questionario_id=session.get("ultimo_questionario_id"),
        pontos=session.get("ultimo_pontos", 0),
        acertos=session.get("ultimo_acertos", 0),
        erros=session.get("ultimo_erros", 0),
        total=session.get("ultimo_total", 0),
        taxa=session.get("ultimo_taxa", 0),
        aluno_nome=session.get("aluno_nome")
    )

# =============================
# TELA RANKING
# =============================
@app.route("/aluno/ranking")
def aluno_ranking():
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login", force_login="true"))

    ultimo_questionario_id = session.get("ultimo_questionario_id")

    con_respostas = sqlite3.connect("respostas_enviadas_aluno.db")
    cur_respostas = con_respostas.cursor()
    con_cadastros = sqlite3.connect("Sistema_cadastros.db")
    cur_cadastros = con_cadastros.cursor()

    cur_respostas.execute("""
        CREATE TABLE IF NOT EXISTS Ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            AlunoId INTEGER,
            QuestionarioId INTEGER,
            Pontos REAL
        )
    """)
    con_respostas.commit()

    cur_respostas.execute("SELECT AlunoId, QuestionarioId, Pontos FROM Ranking")
    resultados = cur_respostas.fetchall()

    alunos_nomes = {}
    for (AlunoId, _, _) in resultados:
        if AlunoId not in alunos_nomes:
            cur_cadastros.execute("SELECT Username FROM usuarios WHERE Id = ?", (AlunoId,))
            aluno = cur_cadastros.fetchone()
            alunos_nomes[AlunoId] = aluno[0] if aluno else f"Aluno {AlunoId}"

    ranking_atividade = []
    if ultimo_questionario_id:
        ranking_atividade = [
            {"AlunoId": r[0], "nome": alunos_nomes.get(r[0], f"Aluno {r[0]}"), "pontos": round(r[2], 2)}
            for r in resultados if r[1] == ultimo_questionario_id
        ]
        ranking_atividade.sort(key=lambda x: x["pontos"], reverse=True)

    soma_pontos = {}
    for (AlunoId, _, pontos) in resultados:
        soma_pontos[AlunoId] = soma_pontos.get(AlunoId, 0) + pontos

    ranking_geral = [
        {"AlunoId": aid, "nome": alunos_nomes.get(aid, f"Aluno {aid}"), "pontos": round(pts, 2)}
        for aid, pts in soma_pontos.items()
    ]
    ranking_geral.sort(key=lambda x: x["pontos"], reverse=True)

    con_respostas.close()
    con_cadastros.close()

    return render_template(
        "rankingAluno/ranking.html",
        ranking_atividade=ranking_atividade,
        ranking_geral=ranking_geral,
        user_name=session.get("aluno_nome"),
        user_score=soma_pontos.get(aluno_id, 0),
        qid=ultimo_questionario_id
    )

# =============================
# ARQUIVOS ESTÁTICOS
# =============================
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/uploads/<path:filename>")
def uploads(filename):
     return send_from_directory(os.path.join("static", "uploads"), filename)
    

# =============================
# HOME
# =============================
@app.route("/")
def home():
    return redirect(url_for("login", force_login="true"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)

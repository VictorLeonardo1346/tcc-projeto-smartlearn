from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for, flash
from flask_cors import CORS
from backend.bancodedados import Database
from backend.respostas_db import RespostasDB
import os
import sqlite3

app = Flask(__name__)
CORS(app)
app.secret_key = "chave_super_secreta"

# =============================
# Inicialização dos bancos
# =============================
db = Database(db_name="banco.db")  # questionários e questões
res_db = RespostasDB(db_name="respostas_enviadas_aluno.db")  # respostas individuais e utilitários
db_cadastros = Database(db_name="Sistema_cadastros.db")  # usuários (alunos)

# =============================
# ROTA: servir arquivos da pasta criacaoQuestionario (HTML/CSS/JS)
# =============================
# Essa rota permite que seus arquivos dentro da pasta /criacaoQuestionario sejam servidos diretamente.
@app.route("/criacaoQuestionario/<path:filename>")
def criacao_questionario_files(filename):
    raiz = os.path.join(os.getcwd(), "criacaoQuestionario")
    return send_from_directory(raiz, filename)

# =============================
# ROTA: página do professor para criar questionário (usa arquivo na pasta raiz/criacaoQuestionario)
# =============================
@app.route("/professor/criar_questionario", methods=["GET"])
def criar_questionario():
    # devolve o arquivo quiz_form.html diretamente da pasta criacaoQuestionario
    raiz = os.path.join(os.getcwd(), "criacaoQuestionario")
    return send_from_directory(raiz, "quiz_form.html")

# =============================
# LOGIN
# =============================
@app.route("/login", methods=["GET", "POST"])
def login():
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

# =============================
# SALVAR QUESTIONÁRIO (PROFESSOR) - API (recebe JSON do quiz_form.js)
# =============================
@app.route("/salvar_questionario", methods=["POST"])
def salvar_questionario():
    dados = request.get_json()
    if not dados:
        return jsonify({"status": "erro", "mensagem": "JSON inválido"}), 400

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
            correta = q.get("correta", "")  # conforme seu script.js: valor tipo "1"/"2"/"3"/"4"
            # garante 4 alternativas (se faltar, deixa string vazia)
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

# =============================
# API: listar questionários (usado pela lista do aluno)
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
        questoes = [{"id": r[0], "enunciado": r[1], "alternativas": [r[2], r[3], r[4], r[5]], "correta": r[6]} for r in rows]
        return jsonify(questoes)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# =============================
# API: salvar respostas do aluno (usa session para pegar aluno_id)
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

    # monta gabarito id -> correta
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
        resp = str(item.get("resposta", ""))  # lembrando: seu quiz_form grava "1"/"2"/"3"/"4"
        correta = gabarito.get(qid)
        acertou = (correta is not None and resp == str(correta))
        pontos = pontos_por_questao if acertou else 0.0
        if acertou:
            acertos += 1
        total_pontos += pontos
        respostas_para_salvar.append({"questao_id": qid, "resposta": resp, "correta": correta, "pontos": round(pontos, 2)})

    # salva respostas via RespostasDB
    try:
        res_db.salvar_respostas_em_lote(aluno_id, questionario_id, respostas_para_salvar)
    except Exception:
        # não interrompe se falhar aqui (só logamos)
        pass

    # atualiza tabela Ranking
    try:
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
    except Exception:
        pass

    # grava resultado na sessão para mostrar na tela /aluno/resultado
    session["ultimo_questionario_id"] = questionario_id
    session["ultimo_pontos"] = round(total_pontos, 2)
    session["ultimo_acertos"] = acertos
    session["ultimo_erros"] = total_questoes - acertos
    session["ultimo_total"] = total_questoes
    session["ultimo_taxa"] = round((acertos / total_questoes) * 100, 2) if total_questoes > 0 else 0

    return jsonify({"status": "sucesso", "mensagem": "Respostas salvas com sucesso!", "pontos_totais": round(total_pontos,2), "acertos": acertos, "erros": total_questoes - acertos, "total": total_questoes, "taxa": session["ultimo_taxa"]})

# =============================
# TELA ALUNO - HOME
# =============================
@app.route("/aluno")
def aluno_home():
    aluno_nome = session.get("aluno_nome")
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login"))

    questionarios = db.listar_questionarios()
    return render_template("aluno_listar.html", questionarios=questionarios, aluno_nome=aluno_nome)

# =============================
# TELA RESPONDER
# =============================
@app.route("/aluno/responder/<int:questionario_id>")
def aluno_responder(questionario_id):
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login"))
    return render_template("aluno_responder.html", id=questionario_id, aluno_id=aluno_id)

# =============================
# TELA RESULTADO (lê dados da sessão)
# =============================
@app.route("/aluno/resultado")
def aluno_resultado():
    aluno_id = session.get("aluno_id")
    if not aluno_id:
        return redirect(url_for("login"))

    questionario_id = session.get("ultimo_questionario_id")
    total_pontos = session.get("ultimo_pontos", 0)
    acertos = session.get("ultimo_acertos", 0)
    erros = session.get("ultimo_erros", 0)
    total_questoes = session.get("ultimo_total", 0)
    taxa = session.get("ultimo_taxa", 0)

    return render_template(
        "aluno_resultado.html",
        questionario_id=questionario_id,
        pontos=total_pontos,
        acertos=acertos,
        erros=erros,
        total=total_questoes,
        taxa=taxa,
        aluno_nome=session.get("aluno_nome")
    )

# =============================
# TELA RANKING
# =============================
@app.route("/aluno/ranking")
def aluno_ranking():
    aluno_id = session.get("aluno_id")
    aluno_nome = session.get("aluno_nome")
    questionario_id = session.get("questionario_id")
    pontos = session.get("pontos", 0)

    if not aluno_id:
        return redirect(url_for("login"))

    con = sqlite3.connect("respostas_enviadas_aluno.db")
    cur = con.cursor()

    # Cria tabela se não existir
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            AlunoId INTEGER,
            AlunoNome TEXT,
            QuestionarioId INTEGER,
            Pontos REAL
        )
    """)

    # 🔄 Atualiza/insere pontuação do aluno atual na atividade
    cur.execute("""
        INSERT INTO Ranking (AlunoId, AlunoNome, QuestionarioId, Pontos)
        VALUES (?, ?, ?, ?)
    """, (aluno_id, aluno_nome, questionario_id, pontos))
    con.commit()

    # 📊 Ranking da atividade atual
    cur.execute("""
        SELECT AlunoNome, Pontos
        FROM Ranking
        WHERE QuestionarioId = ?
        ORDER BY Pontos DESC
    """, (questionario_id,))
    ranking_atividade = cur.fetchall()

    # 📈 Ranking geral (todas as atividades)
    cur.execute("""
        SELECT AlunoNome, SUM(Pontos) as total
        FROM Ranking
        GROUP BY AlunoNome
        ORDER BY total DESC
    """)
    ranking_todas = cur.fetchall()
    con.close()

    # Transforma em lista de dicionários para o Jinja
    ranking_atividade_lista = [
        {"posicao": i + 1, "nome": nome, "pontos": round(pontos, 2)}
        for i, (nome, pontos) in enumerate(ranking_atividade)
    ]
    ranking_todas_lista = [
        {"posicao": i + 1, "nome": nome, "pontos": round(pontos, 2)}
        for i, (nome, pontos) in enumerate(ranking_todas)
    ]

    return render_template(
        "rankingAluno/ranking.html",
        user_name=aluno_nome,
        score=pontos,
        qid=questionario_id,
        ranking_atividade=ranking_atividade_lista,
        ranking_todas=ranking_todas_lista
    )

# =============================
# ROTAS AUXILIARES PARA SERVIR ARQUIVOS ESTÁTICOS (mantidas caso use /static)
# =============================
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# =============================
# HOME
# =============================
@app.route("/")
def home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)

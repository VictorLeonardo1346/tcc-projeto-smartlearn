import sqlite3
import numpy as np
from sklearn.tree import DecisionTreeClassifier

mapa_dif = {"facil": 0, "medio": 1, "dificil": 2}
mapa_inv = {0: "facil", 1: "medio", 2: "dificil"}

def carregar_dados():
    conn = sqlite3.connect("desempenho.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TempoResposta, Erros, DificuldadeAtual, ProximaDificuldade
        FROM Desempenho
        WHERE TempoResposta IS NOT NULL
        AND Erros IS NOT NULL
        AND DificuldadeAtual IS NOT NULL
        AND ProximaDificuldade IS NOT NULL
    """)

    dados = cursor.fetchall()
    conn.close()

    if len(dados) == 0:
        return None, None

    X = []
    y = []

    for temp, erros, atual, prox in dados:

        atual = str(atual).lower().strip()
        prox  = str(prox).lower().strip()

        if atual not in mapa_dif or prox not in mapa_dif:
            continue

        X.append([
            float(temp),
            int(erros),
            mapa_dif[atual]
        ])
        y.append(mapa_dif[prox])

    if len(X) == 0:
        return None, None

    return np.array(X), np.array(y)


def treinar_modelo():
    X, y = carregar_dados()

    if X is None:
        print("⚠️ Nenhum dado ainda — IA usando regras simples.")
        return None

    modelo = DecisionTreeClassifier()
    modelo.fit(X, y)
    return modelo


def prever_proxima_dificuldade(tempo, erros, dificuldade_atual):

    dificuldade_atual = str(dificuldade_atual).lower().strip()

    # fallback caso dificuldade inválida
    if dificuldade_atual not in mapa_dif:
        dificuldade_atual = "medio"

    modelo = treinar_modelo()

    # Sem treino suficiente → regras simples
    if modelo is None:
        if erros >= 2:
            return "facil"
        if tempo < 5 and erros == 0:
            return "dificil"
        return "medio"

    X_novo = np.array([[float(tempo), int(erros), mapa_dif[dificuldade_atual]]])

    pred = modelo.predict(X_novo)[0]
    return mapa_inv[pred]

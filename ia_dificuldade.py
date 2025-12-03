import sqlite3
import numpy as np
from sklearn.tree import DecisionTreeClassifier

CAMINHO_DB = "desempenho.db"

def carregar_dados_para_treino():
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TempoResposta, Erros, DificuldadeAtual, ProximaDificuldade
        FROM Desempenho
        WHERE TempoResposta IS NOT NULL AND Erros IS NOT NULL
        AND DificuldadeAtual IS NOT NULL AND ProximaDificuldade IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 5:
        return None, None

    X = []
    y = []

    mapa = {"facil": 0, "medio": 1, "dificil": 2}

    for tempo, erros, atual, prox in rows:
        if atual in mapa and prox in mapa:
            X.append([tempo, erros, mapa[atual]])
            y.append(mapa[prox])

    return np.array(X), np.array(y)


def treinar_modelo():
    X, y = carregar_dados_para_treino()

    if X is None:
        return None

    modelo = DecisionTreeClassifier()
    modelo.fit(X, y)
    return modelo


def calcular_proxima_dificuldade(tempo_resposta, erros, dificuldade_atual):
    mapa = {"facil": 0, "medio": 1, "dificil": 2}
    mapa_inv = {0: "facil", 1: "medio", 2: "dificil"}

    modelo = treinar_modelo()

    # Caso o modelo ainda não tenha dados suficientes
    if modelo is None:
        # Regra simples:
        if erros >= 2:
            return "facil"
        if tempo_resposta < 5 and erros == 0:
            return "dificil"
        return "medio"

    entrada = np.array([[tempo_resposta, erros, mapa[dificuldade_atual]]])

    pred = modelo.predict(entrada)[0]
    return mapa_inv[pred]
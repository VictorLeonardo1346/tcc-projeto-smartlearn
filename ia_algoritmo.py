import sqlite3
import numpy as np
from sklearn.tree import DecisionTreeClassifier

mapa_dif = {"facil": 0, "medio": 1, "dificil": 2}
mapa_inv = {0: "facil", 1: "medio", 2: "dificil"}


# ---------------------------------------------
# CARREGA DADOS DO BANCO
# ---------------------------------------------
def carregar_dados():
    print("\n🟦 [IA] Carregando dados do banco desempenho.db...")

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

    print(f"🟦 [IA] Total de registros encontrados: {len(dados)}")

    if len(dados) == 0:
        print("⚠️ [IA] Nenhum dado encontrado — voltando None.")
        return None, None

    X = []
    y = []

    for temp, erros, atual, prox in dados:
        atual = str(atual).lower().strip()
        prox  = str(prox).lower().strip()

        if atual not in mapa_dif or prox not in mapa_dif:
            print(f"⚠️ [IA] Registro ignorado (dif inválida): atual={atual}, prox={prox}")
            continue

        X.append([float(temp), int(erros), mapa_dif[atual]])
        y.append(mapa_dif[prox])

    print(f"🟦 [IA] Dados válidos para treino: {len(X)} entradas")

    if len(X) == 0:
        print("⚠️ [IA] Nenhum dado válido encontrado — voltando None.")
        return None, None

    return np.array(X), np.array(y)


# ---------------------------------------------
# TREINO DO MODELO
# ---------------------------------------------
def treinar_modelo():
    print("\n🟩 [IA] Iniciando treinamento...")

    X, y = carregar_dados()

    if X is None:
        print("⚠️ [IA] Sem dados suficientes — modelo NÃO treinado.")
        return None

    modelo = DecisionTreeClassifier()
    modelo.fit(X, y)

    print("🟩 [IA] Modelo treinado com sucesso!")
    print(f"🟩 [IA] Samples: {len(X)}")

    return modelo


# ---------------------------------------------
# PREVISÃO DA PRÓXIMA DIFICULDADE
# ---------------------------------------------
def prever_proxima_dificuldade(tempo, erros, dificuldade_atual):
    dificuldade_atual = str(dificuldade_atual).lower().strip()

    print("\n🟨 ===============================================")
    print("🟨 [IA] PREVISÃO DE DIFICULDADE")
    print("🟨 -----------------------------------------------")
    print(f"🟨 Tempo resposta:     {tempo}")
    print(f"🟨 Erros:              {erros}")
    print(f"🟨 Dif. atual entrada: {dificuldade_atual}")
    print("🟨 ===============================================")

    # fallback
    if dificuldade_atual not in mapa_dif:
        print("⚠️ [IA] Dificuldade inválida, normalizando para 'medio'")
        dificuldade_atual = "medio"

    modelo = treinar_modelo()

    # caso não haja dados suficientes
    if modelo is None:
        print("\n⚠️ [IA] Usando regra manual (IA simples).")
        if erros >= 2:
            print("➡️ Retorno: facil")
            return "facil"
        if tempo < 5 and erros == 0:
            print("➡️ Retorno: dificil")
            return "dificil"
        print("➡️ Retorno: medio")
        return "medio"

    entrada = np.array([[float(tempo), int(erros), mapa_dif[dificuldade_atual]]])

    print(f"🟧 [IA] Entrada para o modelo: {entrada}")

    pred = modelo.predict(entrada)[0]

    print(f"🟧 [IA] Predição numérica: {pred}")
    print(f"🟧 [IA] Predição final: {mapa_inv[pred]}")

    return mapa_inv[pred]

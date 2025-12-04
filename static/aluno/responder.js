let questaoAtual = null;
let respondidas = [];
let indiceAtual = 0;
let dificuldadeAtual = "medio";
let inicioTempo = 0;

async function carregarProximaQuestao() {
    const area = document.getElementById("questionArea");
    const progressInfo = document.getElementById("progressInfo");
    const progressFill = document.getElementById("progressFill");

    const params = new URLSearchParams();
    params.append("dificuldade", dificuldadeAtual);
    respondidas.forEach(id => params.append("respondidas[]", id));

    const resp = await fetch(`/api/proxima_questao/${questionarioId}?${params.toString()}`);
    questaoAtual = await resp.json();

    if (!questaoAtual || questaoAtual.status === "fim") {
        window.location.href = "/aluno/resultado";
        return;
    }

    inicioTempo = Date.now();
    mostrarQuestao(area, progressInfo, progressFill);
}

function mostrarQuestao(area, progressInfo, progressFill) {
    area.innerHTML = "";
    indiceAtual++;

    progressInfo.textContent = `Pergunta ${indiceAtual}`;
    progressFill.style.width = `${(indiceAtual / (indiceAtual + 2) * 100).toFixed(0)}%`;

    const titulo = document.createElement("div");
    titulo.className = "pergunta-texto";
    titulo.textContent = questaoAtual.enunciado;
    area.appendChild(titulo);

    if (questaoAtual.imagem) {
        const img = document.createElement("img");
        img.src = questaoAtual.imagem;
        img.className = "imagem-questao";
        area.appendChild(img);
    }

    const opcoes = document.createElement("div");
    opcoes.className = "opcoes";

    questaoAtual.alternativas.forEach((texto, idx) => {
        const botao = document.createElement("button");
        botao.className = "alternativa-btn";
        botao.textContent = `${String.fromCharCode(65 + idx)}) ${texto}`;

        botao.onclick = async () => {
            const correta = Number(questaoAtual.correta);
            const acertou = (idx + 1) === correta;

            if (acertou) botao.classList.add("correto");
            else botao.classList.add("errado");

            document.querySelectorAll(".alternativa-btn").forEach(b => b.disabled = true);

            const tempoResposta = (Date.now() - inicioTempo) / 1000;

            // envia desempenho para IA
            await fetch("/api/registrar_desempenho", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    aluno_id: alunoId,
                    questionario_id: questionarioId,
                    questao_id: questaoAtual.id,
                    tempo_resposta: tempoResposta,
                    erros: acertou ? 0 : 1,
                    dificuldade_atual: dificuldadeAtual
                })
            });

            // atualiza dificuldade usando IA simples
            dificuldadeAtual = acertou ? "dificil" : "facil";

            respondidas.push(questaoAtual.id);

            setTimeout(() => {
                carregarProximaQuestao();
            }, 1000);
        };

        opcoes.appendChild(botao);
    });

    area.appendChild(opcoes);
}

window.addEventListener("DOMContentLoaded", carregarProximaQuestao);

// static/aluno/responder.js
window.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("questionsContainer");
    const btnEnviar = document.getElementById("submitBtn");

    if (!container) return;

    async function carregarQuestoes() {
        try {
            const resp = await fetch(`/api/questoes/${questionarioId}`);
            if (!resp.ok) throw new Error("Falha ao buscar questões");
            const questoes = await resp.json();

            container.innerHTML = "";

            questoes.forEach((q, i) => {
                const div = document.createElement("div");
                div.className = "question";

                const enunciado = document.createElement("p");
                enunciado.innerHTML = `<b>${i + 1}. ${q.enunciado}</b>`;
                div.appendChild(enunciado);

                const optionsDiv = document.createElement("div");
                optionsDiv.className = "options";

                const alternativas = q.alternativas || ["", "", "", ""];

                ["a", "b", "c", "d"].forEach((letra, idx) => {
                    const label = document.createElement("label");
                    const radio = document.createElement("input");
                    radio.type = "radio";
                    radio.name = `q${q.id}`;
                    radio.value = letra;
                    label.appendChild(radio);
                    label.append(` ${letra.toUpperCase()}) ${alternativas[idx] ?? ""}`);
                    optionsDiv.appendChild(label);
                });

                div.appendChild(optionsDiv);
                container.appendChild(div);
            });

        } catch (err) {
            console.error(err);
            alert("Erro ao carregar questões: " + err.message);
        }
    }

    async function enviarRespostas() {
        // coleta respostas marcadas
        const radiosChecked = document.querySelectorAll("input[type=radio]:checked");
        const respostasUsuario = {};
        radiosChecked.forEach(r => {
            const qid = Number(r.name.replace("q", ""));
            if (!Number.isNaN(qid)) respostasUsuario[qid] = r.value;
        });

        // transforma para o formato esperado pela API
        const listaEnvio = Object.entries(respostasUsuario).map(([qid, resp]) => ({
            questao_id: Number(qid),
            resposta: resp
        }));

        try {
            const resp = await fetch("/api/salvar_respostas", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    aluno_id: 1, // provisório
                    questionario_id: Number(questionarioId),
                    respostas: listaEnvio
                })
            });

            const dados = await resp.json();
            if (!resp.ok || dados.status !== "sucesso") {
                throw new Error(dados.mensagem || "Erro desconhecido do servidor");
            }

            // recebe do servidor: pontos_totais, acertos, erros, total, taxa
            const params = new URLSearchParams({
                qid: questionarioId,
                score: dados.pontos_totais,
                acertos: dados.acertos,
                erros: dados.erros,
                total: dados.total,
                taxa: dados.taxa,
                user_name: "Aluno 1"
            });

            // redireciona para a página de resultado com os parâmetros vindos do servidor
            window.location.href = `/aluno/resultado?${params.toString()}`;

        } catch (err) {
            console.error(err);
            alert("Erro ao enviar respostas: " + (err.message || err));
        }
    }

    btnEnviar.addEventListener("click", enviarRespostas);
    carregarQuestoes();
});

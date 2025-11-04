window.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("questionsContainer");
    const btnEnviar = document.getElementById("submitBtn");

    if (!container) return;

    let gabarito = {};
    let totalQuestions = 0;

    async function carregarQuestoes() {
        try {
            const resp = await fetch(`/api/questoes/${questionarioId}`);
            if (!resp.ok) throw new Error("Falha ao buscar questões");
            const questoes = await resp.json();

            container.innerHTML = "";
            gabarito = {};
            totalQuestions = questoes.length;

            questoes.forEach((q, i) => {
                gabarito[q.id] = q.correta;

                const div = document.createElement("div");
                div.className = "question";

                const enunciado = document.createElement("p");
                enunciado.innerHTML = `<b>${i + 1}. ${q.enunciado}</b>`;
                div.appendChild(enunciado);

                const optionsDiv = document.createElement("div");
                optionsDiv.className = "options";

                const alternativas = q.alternativas || ["", "", "", ""];

                ["a","b","c","d"].forEach((letra, idx) => {
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
            alert("Erro ao carregar questões.");
        }
    }

    function calcularResultados(respostasUsuario) {
        let acertos = 0;
        for (const [qidStr, resp] of Object.entries(respostasUsuario)) {
            const qid = Number(qidStr);
            if (gabarito[qid] === resp) acertos++;
        }
        const pontosPorQuestao = totalQuestions > 0 ? Math.round(100 / totalQuestions) : 0;
        const totalPontos = acertos * pontosPorQuestao;
        return { acertos, totalPontos };
    }

    async function enviarRespostas() {
        const radiosChecked = document.querySelectorAll("input[type=radio]:checked");
        const respostasUsuario = {};
        radiosChecked.forEach(r => {
            const qid = Number(r.name.replace("q", ""));
            if (!Number.isNaN(qid)) respostasUsuario[qid] = r.value;
        });

        const resultados = calcularResultados(respostasUsuario);

        const listaEnvio = Object.entries(respostasUsuario).map(([qid, resp]) => ({
            questao_id: Number(qid),
            resposta: resp
        }));

        try {
            await fetch("/api/salvar_respostas", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    questionario_id: Number(questionarioId),
                    respostas: listaEnvio
                })
            });

            const params = new URLSearchParams({
                qid: questionarioId,
                score: resultados.totalPontos,
                acertos: resultados.acertos,
                total: totalQuestions
            });

            window.location.href = `/aluno/resultado?${params.toString()}`;
        } catch (err) {
            console.error(err);
            alert("Erro ao enviar respostas.");
        }
    }

    btnEnviar.addEventListener("click", enviarRespostas);
    carregarQuestoes();
});

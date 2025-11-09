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

        ["1", "2", "3", "4"].forEach((valor, idx) => {
          const label = document.createElement("label");
          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = `q${q.id}`;
          radio.value = valor;
          label.appendChild(radio);
          label.append(` ${String.fromCharCode(65 + idx)}) ${alternativas[idx] ?? ""}`);
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
    const radiosChecked = document.querySelectorAll("input[type=radio]:checked");
    const respostasUsuario = {};
    radiosChecked.forEach((r) => {
      const qid = Number(r.name.replace("q", ""));
      if (!Number.isNaN(qid)) respostasUsuario[qid] = r.value;
    });

    const listaEnvio = Object.entries(respostasUsuario).map(([qid, resp]) => ({
      questao_id: Number(qid),
      resposta: resp,
    }));

    try {
      const resp = await fetch("/api/salvar_respostas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questionario_id: Number(questionarioId),
          respostas: listaEnvio,
        }),
      });

      const dados = await resp.json();
      if (!resp.ok || dados.status !== "sucesso") {
        throw new Error(dados.mensagem || "Erro desconhecido do servidor");
      }

      // ✅ Agora redireciona direto para a rota que lê da sessão
      window.location.href = "/aluno/resultado";
    } catch (err) {
      console.error(err);
      alert("Erro ao enviar respostas: " + (err.message || err));
    }
  }

  btnEnviar.addEventListener("click", enviarRespostas);
  carregarQuestoes();
});

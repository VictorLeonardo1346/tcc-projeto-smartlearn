// static/aluno/responder.js
let indiceAtual = 0;
let questaoAtual = null;

let tempoInicio = 0;
let dificuldadeAtual = "medio"; // dificuldade inicial padrão
let erros = 0;

window.addEventListener("DOMContentLoaded", () => {
  const area = document.getElementById("questionArea");
  const progressInfo = document.getElementById("progressInfo");
  const progressFill = document.getElementById("progressFill");

  carregarProximaQuestao();

  async function carregarProximaQuestao() {
    console.log("📡 Buscando questão com dificuldade:", dificuldadeAtual);

    const resp = await fetch(`/api/proxima_questao/${questionarioId}?dificuldade=${dificuldadeAtual}`);
    questaoAtual = await resp.json();
    console.log("➡️ Resposta da API:", questaoAtual);

    // ------------------------------
    // CORREÇÃO DO BUG DA TELA FINAL
    // ------------------------------
    if (questaoAtual.status === "fim") {

      console.warn("⚠️ Nenhuma questão nessa dificuldade:", dificuldadeAtual);

      // Fallback: tentar dificuldade MÉDIA sempre funciona como padrão
      dificuldadeAtual = "medio";

      const resp2 = await fetch(`/api/proxima_questao/${questionarioId}?dificuldade=${dificuldadeAtual}`);
      questaoAtual = await resp2.json();
      console.log("➡️ Tentativa fallback:", questaoAtual);

      if (!questaoAtual.id) {
        console.error("❌ Nenhuma questão disponível — encerrando questionário");
        window.location.href = "/aluno/resultado";
        return;
      }
    }

    // Se ainda assim a questão não existe → finaliza
    if (!questaoAtual.id) {
      console.error("❌ Questão inválida, indo para resultado");
      window.location.href = "/aluno/resultado";
      return;
    }

    mostrarQuestao();
  }

  function mostrarQuestao() {
    erros = 0;
    tempoInicio = Date.now();

    area.innerHTML = "";

    progressInfo.textContent = `Pergunta ${indiceAtual + 1}`;
    progressFill.style.width = `${((indiceAtual + 1) * 10)}%`;

    const q = questaoAtual;

    const titulo = document.createElement("div");
    titulo.className = "pergunta-texto";
    titulo.textContent = `${q.enunciado}`;
    area.appendChild(titulo);

    if (q.imagem) {
      const img = document.createElement("img");
      img.src = q.imagem;
      img.className = "imagem-questao";
      area.appendChild(img);
    }

    const opcoes = document.createElement("div");
    opcoes.className = "opcoes";

    q.alternativas.forEach((texto, idx) => {
      const botao = document.createElement("button");
      botao.className = "alternativa-btn";
      botao.textContent = `${String.fromCharCode(65 + idx)}) ${texto}`;
      botao.onclick = () => responder(idx + 1);
      opcoes.appendChild(botao);
    });

    area.appendChild(opcoes);
  }

  async function responder(valor) {
    const tempoFinal = (Date.now() - tempoInicio) / 1000;

    const correta = Number(questaoAtual.correta);
    erros = valor === correta ? 0 : 1;

    console.log("📝 Registrando desempenho:", {
      aluno_id: alunoId,
      questionario_id: questionarioId,
      questao_id: questaoAtual.id,
      tempo_resposta: tempoFinal,
      erros: erros,
      dificuldade_atual: dificuldadeAtual
    });

    const resp = await fetch("/salvar_questionario", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        aluno_id: alunoId,
        questionario_id: questionarioId,
        questao_id: questaoAtual.id,
        tempo_resposta: tempoFinal,
        erros: erros,
        dificuldade_atual: dificuldadeAtual
      })
    });

    const dados = await resp.json();
    console.log("🤖 IA escolheu próxima dificuldade:", dados.proxima_dificuldade);

    dificuldadeAtual = dados.proxima_dificuldade;

    indiceAtual++;
    carregarProximaQuestao();
  }
});


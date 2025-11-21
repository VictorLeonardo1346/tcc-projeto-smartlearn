// static/aluno/responder.js
let questoes = [];
let indiceAtual = 0;
let respostasUsuario = {};

window.addEventListener("DOMContentLoaded", () => {
  const area = document.getElementById("questionArea");
  const btnProxima = document.getElementById("proximaPerguntaBtn");
  const btnEnviar = document.getElementById("submitBtn");

  const progressInfo = document.getElementById("progressInfo");
  const progressFill = document.getElementById("progressFill");

  async function carregarQuestoes() {
    const resp = await fetch(`/api/questoes/${questionarioId}`);
    questoes = await resp.json();
    mostrarQuestao(); // só aqui a barra pode ser atualizada
  }

  function mostrarQuestao() {
    const q = questoes[indiceAtual];
    area.innerHTML = "";

    atualizarProgresso(); // <-- CORREÇÃO

    const titulo = document.createElement("div");
    titulo.className = "pergunta-texto";
    titulo.textContent = `${indiceAtual + 1}. ${q.enunciado}`;
    area.appendChild(titulo);

    if (q.imagem) {
      const img = document.createElement("img");
      img.src = q.imagem;
      img.className = "imagem-questao";
      area.appendChild(img);
    }

    const opcoes = document.createElement("div");
    opcoes.className = "opcoes";

    const alternativas = [
      q.alternativas?.[0],
      q.alternativas?.[1],
      q.alternativas?.[2],
      q.alternativas?.[3],
    ];

    alternativas.forEach((texto, idx) => {
      const botao = document.createElement("button");
      botao.className = "alternativa-btn";
      botao.textContent = `${String.fromCharCode(65 + idx)}) ${texto}`;

      botao.onclick = () => responder(idx + 1, botao, q);

      opcoes.appendChild(botao);
    });

    area.appendChild(opcoes);

    btnProxima.style.display = "none";
  }

  function responder(valor, botao, q) {
    if (respostasUsuario[q.id] !== undefined) return;

    respostasUsuario[q.id] = valor;

    const correta = Number(q.correta);

    const botoes = document.querySelectorAll(".alternativa-btn");
    botoes.forEach((b, i) => {
      const numero = i + 1;
      if (numero === correta) b.classList.add("correto");
      if (numero === valor && numero !== correta) b.classList.add("errado");
      b.style.pointerEvents = "none";
    });

    if (indiceAtual < questoes.length - 1) {
      btnProxima.style.display = "block";
    } else {
      btnEnviar.style.display = "block";
    }
  }

  btnProxima.onclick = () => {
    indiceAtual++;
    mostrarQuestao();
  };

  btnEnviar.onclick = async () => {
    const listaEnvio = Object.entries(respostasUsuario).map(([qid, resp]) => ({
      questao_id: Number(qid),
      resposta: resp,
    }));

    const resp = await fetch("/api/salvar_respostas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        questionario_id: Number(questionarioId),
        respostas: listaEnvio,
      }),
    });

    const dados = await resp.json();
    if (dados.status === "sucesso") {
      window.location.href = "/aluno/resultado";
    } else {
      alert("Erro ao enviar respostas");
    }
  };

  function atualizarProgresso() {
    const total = questoes.length;
    const atual = indiceAtual + 1;

    progressInfo.textContent = `Pergunta ${atual} de ${total}`;

    const porcentagem = (atual / total) * 100;
    progressFill.style.width = `${porcentagem}%`;
  }

  carregarQuestoes();
});

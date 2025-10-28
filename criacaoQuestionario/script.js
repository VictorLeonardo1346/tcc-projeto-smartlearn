// criacaoQuestionario/script.js
let questionCount = 0;
let dificuldadeSelecionada = null;

// Seleciona a dificuldade
function setDificuldade(nivel) {
  dificuldadeSelecionada = nivel;
  document.getElementById("nivelSelecionado").innerText =
    "Selecionado: " + nivel;
}

// Adiciona uma questão ao formulário
function addQuestion() {
  questionCount++;
  const container = document.getElementById("questionsContainer");

  const div = document.createElement("div");
  div.classList.add("question");
  div.id = "question-" + questionCount;

  const label = document.createElement("label");
  label.textContent = "Questão " + questionCount;
  div.appendChild(label);

  const inputPergunta = document.createElement("input");
  inputPergunta.type = "text";
  inputPergunta.placeholder = "Digite a questão aqui";
  div.appendChild(inputPergunta);

  const optionsDiv = document.createElement("div");
  optionsDiv.classList.add("options");

  ["a", "b", "c", "d"].forEach((letra) => {
    const optLabel = document.createElement("label");

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "correct-" + questionCount;
    radio.value = letra;

    const altInput = document.createElement("input");
    altInput.type = "text";
    altInput.placeholder = `Texto da alternativa ${letra.toUpperCase()}`;

    optLabel.textContent = letra + ") ";
    optLabel.appendChild(radio);
    optLabel.appendChild(altInput);
    optionsDiv.appendChild(optLabel);
  });

  div.appendChild(optionsDiv);
  container.appendChild(div);
}

// Remove a última questão adicionada
function removeQuestion() {
  if (questionCount > 0) {
    const last = document.getElementById("question-" + questionCount);
    last.remove();
    questionCount--;
  }
}

// Limpa todo o formulário
function deletarAtividade() {
  if (confirm("Tem certeza que deseja deletar esta atividade?")) {
    document.getElementById("titulo").value = "";
    document.getElementById("materia").value = "";
    document.getElementById("dataEntrega").value = "";
    document.getElementById("nivelSelecionado").innerText = "";
    dificuldadeSelecionada = null;

    const container = document.getElementById("questionsContainer");
    container.innerHTML = "";
    questionCount = 0;
  }
}

// Captura envio do formulário
document.getElementById("quizForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  if (!dificuldadeSelecionada) {
    alert("Por favor, selecione a dificuldade da atividade.");
    return;
  }

  const materia = document.getElementById("materia").value;
  const titulo = document.getElementById("titulo").value;
  const dataEntrega = document.getElementById("dataEntrega").value;

  if (!materia || !titulo || !dataEntrega) {
    alert("Por favor, preencha todos os campos obrigatórios.");
    return;
  }

  const questoes = [];
  const questions = document.querySelectorAll(".question");

  questions.forEach((q) => {
    const pergunta = q.querySelector("input[type='text']").value;
    const alternativasInputs = q.querySelectorAll(".options input[type='text']");
    const radios = q.querySelectorAll("input[type='radio']");
    let correta = null;

    radios.forEach((r) => {
      if (r.checked) correta = r.value;
    });

    const alternativas = [
      alternativasInputs[0]?.value || "",
      alternativasInputs[1]?.value || "",
      alternativasInputs[2]?.value || "",
      alternativasInputs[3]?.value || ""
    ];

    questoes.push({ pergunta, alternativas, correta });
  });

  const atividade = {
    materia,
    titulo,
    dificuldade: dificuldadeSelecionada,
    dataEntrega,
    questoes,
  };

  console.log("Enviando atividade:", atividade);

  try {
    const resp = await fetch("http://127.0.0.1:5001/salvar_questionario", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(atividade),
    });

    const data = await resp.json();
    if (data.status === "sucesso") {
      alert(data.mensagem + " (ID: " + data.id + ")");
      location.reload();
    } else {
      alert("Erro: " + data.mensagem);
    }
  } catch (err) {
    console.error("Erro ao salvar:", err);
    alert("Erro ao salvar a atividade!");
  }
});

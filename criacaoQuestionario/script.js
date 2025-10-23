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

  // Label da questão
  const label = document.createElement("label");
  label.textContent = "Questão " + questionCount;
  div.appendChild(label);

  // Input do enunciado
  const inputPergunta = document.createElement("input");
  inputPergunta.type = "text";
  inputPergunta.placeholder = "Digite a questão aqui";
  div.appendChild(inputPergunta);

  // Upload da imagem
  const imgLabel = document.createElement("label");
  imgLabel.textContent = "Imagem (opcional):";
  div.appendChild(imgLabel);

  const inputImg = document.createElement("input");
  inputImg.type = "file";
  inputImg.accept = "image/*";
  inputImg.onchange = function (event) {
    const imgPreview = div.querySelector("img");
    imgPreview.src = URL.createObjectURL(event.target.files[0]);
    imgPreview.style.display = "block";
  };
  div.appendChild(inputImg);

  const imgPreview = document.createElement("img");
  imgPreview.style.display = "none";
  imgPreview.style.maxWidth = "200px";
  imgPreview.style.marginTop = "10px";
  div.appendChild(imgPreview);

  // Alternativas
  const optionsDiv = document.createElement("div");
  optionsDiv.classList.add("options");

  ["a", "b", "c", "d"].forEach((letra, i) => {
    const optLabel = document.createElement("label");

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "correct-" + questionCount;
    radio.value = i + 1;

    const altInput = document.createElement("input");
    altInput.type = "text";
    altInput.placeholder = `Texto da alternativa ${i + 1}`;

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

// Captura envio do formulário
document.getElementById("quizForm").addEventListener("submit", function (e) {
  e.preventDefault();

  if (!dificuldadeSelecionada) {
    alert("Por favor, selecione a dificuldade da atividade.");
    return;
  }

  const materia = document.getElementById("materia").value;
  const titulo = document.getElementById("titulo").value;
  const dataEntrega = document.getElementById("dataEntrega").value;

  if (!materia) {
    alert("Por favor, selecione a matéria.");
    return;
  }

  const questoes = [];
  const questions = document.querySelectorAll(".question");

  questions.forEach((q, i) => {
    const pergunta = q.querySelector("input[type='text']").value;
    const alternativas = q.querySelectorAll(".options input[type='text']");
    const correta =
      q.querySelector("input[type='radio']:checked")?.value || null;

    questoes.push({
      pergunta,
      alternativas: Array.from(alternativas).map((a) => a.value),
      correta,
    });
  });

  const atividade = {
    materia,
    titulo,
    dificuldade: dificuldadeSelecionada,
    dataEntrega,
    questoes,
  };

  console.log("Atividade criada:", atividade);
  alert("Atividade criada com sucesso!\n" + JSON.stringify(atividade, null, 2));
});

let questionCount = 0;
let dificuldadeSelecionada = null;

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
  inputPergunta.placeholder = "Digite o enunciado da questão";
  div.appendChild(inputPergunta);

  const diffDiv = document.createElement("div");
  diffDiv.classList.add("dificuldade-questao");
  diffDiv.innerHTML = `
    <span>Dificuldade:</span>
    <button type="button" class="btn-diff facil" onclick="setDificuldadeQuestao(this, 'Fácil')">Fácil</button>
    <button type="button" class="btn-diff medio" onclick="setDificuldadeQuestao(this, 'Médio')">Médio</button>
    <button type="button" class="btn-diff dificil" onclick="setDificuldadeQuestao(this, 'Difícil')">Difícil</button>
    <span class="nivel"></span>
  `;
  div.appendChild(diffDiv);

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

  const optionsDiv = document.createElement("div");
  optionsDiv.classList.add("options");

  ["a", "b", "c", "d"].forEach((letra, i) => {
    const optLabel = document.createElement("label");
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "correct-" + questionCount;
    // valor usado como "correta" — string "1","2","3","4"
    radio.value = String(i + 1);

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

function setDificuldadeQuestao(botao, nivel) {
  const parent = botao.closest(".dificuldade-questao");
  parent.querySelectorAll(".btn-diff").forEach((b) => b.classList.remove("ativo"));
  botao.classList.add("ativo");
  parent.querySelector(".nivel").textContent = nivel;
  // define dificuldade global (se quiser dificuldade por questão, é preciso salvar por questão)
  dificuldadeSelecionada = nivel;
}

function removeQuestion() {
  if (questionCount > 0) {
    const container = document.getElementById("questionsContainer");
    container.removeChild(container.lastElementChild);
    questionCount--;
  } else {
    alert("Não há questões para remover.");
  }
}

function deletarAtividade() {
  if (confirm("Tem certeza que deseja deletar esta atividade?")) {
    document.getElementById("titulo").value = "";
    document.getElementById("materia").value = "";
    document.getElementById("dataEntrega").value = "";
    document.getElementById("questionsContainer").innerHTML = "";
    questionCount = 0;
    dificuldadeSelecionada = null;
  }
}

document.getElementById("quizForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  if (!dificuldadeSelecionada) {
    if (!confirm("Você não escolheu uma dificuldade global. Continuar mesmo assim?")) return;
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
    const pergunta = (q.querySelector("input[type='text']") || { value: "" }).value;
    const alternativasInputs = q.querySelectorAll(".options input[type='text']");
    const radios = q.querySelectorAll("input[type='radio']");
    let correta = null;
    radios.forEach((r) => { if (r.checked) correta = r.value; });

    const alternativas = [
      alternativasInputs[0]?.value || "",
      alternativasInputs[1]?.value || "",
      alternativasInputs[2]?.value || "",
      alternativasInputs[3]?.value || "",
    ];

    questoes.push({ pergunta, alternativas, correta });
  });

  const atividade = { materia, titulo, dificuldade: dificuldadeSelecionada || "", dataEntrega, questoes };

  try {
    const resp = await fetch("/salvar_questionario", {
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

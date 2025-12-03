let questionCount = 0;

// Agora a dificuldade NÃO é mais global.
// Cada questão terá sua própria dificuldade salva dentro dela.
function setDificuldadeQuestao(botao, nivel) {
  const parent = botao.closest(".dificuldade-questao");

  // Marca botão selecionado
  parent.querySelectorAll(".btn-diff").forEach((b) => b.classList.remove("ativo"));
  botao.classList.add("ativo");

  // Mostra texto no <span class="nivel">
  parent.querySelector(".nivel").textContent = nivel;

  // Salvamos a dificuldade na DIV da questão
  const questionDiv = botao.closest(".question");
  questionDiv.dataset.dificuldade = nivel;
}

function addQuestion() {
  questionCount++;
  const container = document.getElementById("questionsContainer");

  const div = document.createElement("div");
  div.classList.add("question");
  div.id = "question-" + questionCount;

  // Inicia com dificuldade vazia
  div.dataset.dificuldade = "";

  const label = document.createElement("label");
  label.textContent = "Questão " + questionCount;
  div.appendChild(label);

  const inputPergunta = document.createElement("input");
  inputPergunta.type = "text";
  inputPergunta.placeholder = "Digite o enunciado da questão";
  inputPergunta.classList.add("pergunta");
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
  inputImg.classList.add("imagem");
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
  }
}

// ---------------------- //
// SUBMIT DO FORMULÁRIO
// ---------------------- //

document.getElementById("quizForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const materia = document.getElementById("materia").value;
  const titulo = document.getElementById("titulo").value;
  const dataEntrega = document.getElementById("dataEntrega").value;

  if (!materia || !titulo || !dataEntrega) {
    alert("Por favor, preencha todos os campos obrigatórios.");
    return;
  }

  const formData = new FormData();
  formData.append("materia", materia);
  formData.append("titulo", titulo);
  formData.append("dataEntrega", dataEntrega);

  const questions = document.querySelectorAll(".question");

  questions.forEach((q, index) => {
    const pergunta = q.querySelector(".pergunta")?.value || "";

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
      alternativasInputs[3]?.value || "",
    ];

    const dificuldade = q.querySelector(".nivel")?.textContent || "";

    formData.append(`pergunta_${index}`, pergunta);
    formData.append(`alt1_${index}`, alternativas[0]);
    formData.append(`alt2_${index}`, alternativas[1]);
    formData.append(`alt3_${index}`, alternativas[2]);
    formData.append(`alt4_${index}`, alternativas[3]);
    formData.append(`correta_${index}`, correta);
    formData.append(`dificuldade_${index}`, dificuldade);

    // Enviar imagem se existir
    const imgInput = q.querySelector(".imagem");
    if (imgInput && imgInput.files.length > 0) {
      formData.append(`imagem_${index}`, imgInput.files[0]);
    }
  });

  try {
    const resp = await fetch("/salvar_questionario", {
      method: "POST",
      body: formData,
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

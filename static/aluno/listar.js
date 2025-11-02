async function carregarQuestionarios() {
  try {
    const resp = await fetch("http://127.0.0.1:5001/api/questionarios");
    const questionarios = await resp.json();

    const container = document.getElementById("cardsQuestionarios");
    container.innerHTML = "";

    questionarios.forEach(q => {
      const card = document.createElement("div");
      card.classList.add("questionario-card");

      card.innerHTML = `
        <h5>${q.titulo}</h5>
        <p><strong>Matéria:</strong> ${q.materia}</p>
        <p><strong>Dificuldade:</strong> ${q.dificuldade}</p>
        <p><strong>Entrega:</strong> ${q.dataEntrega}</p>
        <button class="btn btn-primary btn-responder">Responder</button>
      `;

      // Redireciona ao clicar no card ou no botão
      card.querySelector(".btn-responder").addEventListener("click", () => {
        window.location.href = `http://127.0.0.1:5001/aluno/responder/${q.id}`;
      });

      container.appendChild(card);
    });

  } catch (err) {
    alert("Erro ao carregar questionários!");
    console.error(err);
  }
}

carregarQuestionarios();

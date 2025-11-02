async function carregarQuestionarios() {
  try {
    const resp = await fetch("http://127.0.0.1:5001/api/questionarios");
    const questionarios = await resp.json();

    const tbody = document.querySelector("#tabelaQuestionarios tbody");
    tbody.innerHTML = "";

    questionarios.forEach(q => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${q.id}</td>
        <td>${q.materia}</td>
        <td>${q.titulo}</td>
        <td>${q.dificuldade}</td>
        <td>${q.dataEntrega}</td>
        <td><button class="btn btn-primary" onclick="responder(${q.id})">Responder</button></td>
      `;

      tbody.appendChild(tr);
    });

  } catch (err) {
    alert("Erro ao carregar questionários!");
    console.error(err);
  }
}

function responder(id) {
  window.location.href = `http://127.0.0.1:5001/aluno/responder/${id}`;
}

carregarQuestionarios();

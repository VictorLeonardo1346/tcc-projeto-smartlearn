window.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("questionariosContainer");

  try {
    const resp = await fetch("/api/questionarios");
    const questionarios = await resp.json();

    if (questionarios.length === 0) {
      container.innerHTML = "<p>Nenhum questionário encontrado.</p>";
      return;
    }

    questionarios.forEach((q) => {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <div class="info">
          <h2>${q.titulo}</h2>
          <span><b>Matéria:</b> ${q.materia}</span>
          <span><b>Dificuldade:</b> ${q.dificuldade}</span>
          <span><b>Entrega:</b> ${q.dataEntrega}</span>
        </div>
        <div class="actions">
          <button class="btn-visualizar" onclick="visualizar(${q.id})">Visualizar</button>
          <button class="btn-excluir" onclick="excluir(${q.id}, this)">Excluir</button>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error("Erro ao carregar questionários:", err);
    container.innerHTML = "<p>Erro ao carregar questionários.</p>";
  }
});

async function excluir(id, btn) {
  if (!confirm("Tem certeza que deseja excluir este questionário?")) return;

  try {
    const resp = await fetch(`/api/excluir_questionario/${id}`, {
      method: "DELETE",
    });
    const data = await resp.json();
    alert(data.mensagem);

    // Efeito suave para remover o card da tela
    const card = btn.closest(".card");
    card.style.transition = "opacity 0.3s, transform 0.3s";
    card.style.opacity = "0";
    card.style.transform = "translateY(-10px)";
    setTimeout(() => card.remove(), 300);
  } catch (err) {
    alert("Erro ao excluir questionário!");
  }
}

function visualizar(id) {
  window.location.href = `/visualizar_questionario/${id}`;
}

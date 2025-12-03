let questionarioSelecionado = null;

window.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("questionariosContainer");

  try {
    const resp = await fetch("/api/questionarios");
    const questionarios = await resp.json();

    if (!questionarios || questionarios.length === 0) {
      container.innerHTML = "<p>Nenhum questionário encontrado.</p>";
      return;
    }

    questionarios.forEach((q) => {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <div class="info">
          <h2>${escapeHtml(q.titulo)}</h2>
          <span><b>Matéria:</b> ${escapeHtml(q.materia)}</span>
          <span><b>Dificuldade:</b> ${escapeHtml(q.dificuldade)}</span>
          <span><b>Entrega:</b> ${escapeHtml(q.dataEntrega)}</span>
        </div>
        <div class="actions">
          <button class="btn-visualizar" onclick="visualizar(${
            q.id
          })">Visualizar</button>
          <button class="btn-excluir" onclick="excluir(${
            q.id
          }, this)">Excluir</button>
          <button class="btn-adicionar-turma" onclick="abrirModal(${
            q.id
          })">Adicionar à Turma</button>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error("Erro ao carregar questionários:", err);
    container.innerHTML = "<p>Erro ao carregar questionários.</p>";
  }
});

// pequena função para escapar HTML em strings vindas do backend
function escapeHtml(text) {
  if (!text && text !== 0) return "";
  return String(text).replace(/[&<>"']/g, (m) => {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[m];
  });
}

async function excluir(id, btn) {
  if (!confirm("Tem certeza que deseja excluir este questionário?")) return;

  try {
    const resp = await fetch(`/api/excluir_questionario/${id}`, {
      method: "DELETE",
    });

    if (!resp.ok) throw new Error("Resposta não OK ao excluir");

    const data = await resp.json();
    alert(data.mensagem || "Questionário excluído.");

    const card = btn.closest(".card");
    card.style.opacity = "0";
    card.style.transform = "translateY(-10px)";
    setTimeout(() => card.remove(), 300);
  } catch (err) {
    console.error("Erro ao excluir:", err);
    alert("Erro ao excluir questionário!");
  }
}

function visualizar(id) {
  window.location.href = `/visualizar_questionario/${id}`;
}

/* --- MODAL DE TURMAS --- */
async function abrirModal(idQuestionario) {
  questionarioSelecionado = idQuestionario;

  const modal = document.getElementById("turmaPopup");
  const lista = document.getElementById("listaTurmas");
  const loading = document.getElementById("popupLoading");

  loading.style.display = "block";
  lista.style.display = "none";
  lista.innerHTML = "";
  modal.style.display = "flex";

  try {
    const resp = await fetch("/api/turmas");
    if (!resp.ok) throw new Error("Erro ao buscar turmas");
    const turmas = await resp.json();

    loading.style.display = "none";
    lista.style.display = "block";

    if (!turmas || turmas.length === 0) {
      lista.innerHTML = "<li>Nenhuma turma encontrada.</li>";
      return;
    }

    turmas.forEach((t) => {
      const li = document.createElement("li");
      li.textContent = t.nome;
      li.onclick = () => adicionarQuestionarioNaTurma(t.id);
      lista.appendChild(li);
    });
  } catch (err) {
    console.error("Erro ao carregar turmas:", err);
    loading.textContent = "Erro ao carregar turmas.";
  }
}

function fecharPopup() {
  document.getElementById("turmaPopup").style.display = "none";
  questionarioSelecionado = null;
}

async function adicionarQuestionarioNaTurma(idTurma) {
  if (!questionarioSelecionado) return;

  try {
    const resp = await fetch("/api/adicionar_questionario_turma", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        questionario_id: questionarioSelecionado,
        turma_id: idTurma,
      }),
    });

    const data = await resp.json();
    alert(data.mensagem || "Questionário adicionado à turma.");
    fecharPopup();
  } catch (err) {
    console.error("Erro ao adicionar questionário à turma:", err);
    alert("Erro ao adicionar questionário à turma.");
  }
}

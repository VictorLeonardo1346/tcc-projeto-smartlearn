window.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("questionsContainer");

  try {
    const resp = await fetch(`/api/questoes/${questionarioId}`);
    const questoes = await resp.json();

    container.innerHTML = "";

    if (!questoes || questoes.length === 0) {
      container.innerHTML = "<p>Nenhuma questão encontrada.</p>";
      return;
    }

    questoes.forEach((q, i) => {
      const div = document.createElement("div");
      div.className = "question";

      const enunciado = document.createElement("p");
      enunciado.innerHTML = `<b>${i + 1}. ${q.enunciado}</b>`;
      div.appendChild(enunciado);

      if (q.imagem) {
        const img = document.createElement("img");
        img.src = q.imagem;
        img.alt = "Imagem da questão";
        img.className = "imagem-questao";
        div.appendChild(img);
      }

      const alternativas = q.alternativas || ["", "", "", ""];
      alternativas.forEach((alt, idx) => {
        const p = document.createElement("p");
        p.textContent = `${String.fromCharCode(65 + idx)}) ${alt}`;
        div.appendChild(p);
      });

      container.appendChild(div);
    });
  } catch (err) {
    console.error("Erro ao carregar questões:", err);
    container.innerHTML = "<p>Erro ao carregar questões.</p>";
  }
});

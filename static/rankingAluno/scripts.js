// static/rankingAluno/scripts.js

document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".lboard_tabs ul li");
  const atividadeDiv = document.getElementById("ranking-atividade");
  const todasDiv = document.getElementById("ranking-todas");

  // Troca de abas
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      if (tab.dataset.li === "atividade") {
        atividadeDiv.classList.add("active");
        todasDiv.classList.remove("active");
      } else {
        todasDiv.classList.add("active");
        atividadeDiv.classList.remove("active");
      }
    });
  });

  // Gera visual de ranking
  function gerarRanking(containerId, lista) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!lista || lista.length === 0) {
      container.innerHTML = "<p>Nenhum resultado encontrado.</p>";
      return;
    }

    // Descobre a maior pontuação para ajustar o tamanho das barras proporcionalmente
    const maxPontos = Math.max(...lista.map(i => i.pontos));

    lista.forEach((item, index) => {
      const rankPos = index + 1;
      const widthPercent = maxPontos > 0 ? (item.pontos / maxPontos) * 100 : 0;

      let medalhaImg = "";
      if (rankPos === 1)
        medalhaImg = `<img src="/static/rankingAluno/img/medalha-ouro.gif" class="medalha-inline" alt="Ouro" />`;
      else if (rankPos === 2)
        medalhaImg = `<img src="/static/rankingAluno/img/medalha-prata.gif" class="medalha-inline" alt="Prata" />`;
      else if (rankPos === 3)
        medalhaImg = `<img src="/static/rankingAluno/img/medalha-bronze.gif" class="medalha-inline" alt="Bronze" />`;
      else medalhaImg = `<span class="no-medal"></span>`;

      const displayName =
        item.nome === window.userName ? `Você (${item.nome})` : item.nome;

      const div = document.createElement("div");
      div.className = "lboard_mem";
      div.innerHTML = `
        <div class="name">${rankPos}. ${displayName}</div>
        <div class="row-bar">
          <div class="bar"><div class="inner_bar" style="width:${widthPercent}%"></div></div>
          <div class="points"><span>${item.pontos} pts</span>${medalhaImg}</div>
        </div>
      `;
      container.appendChild(div);
    });
  }

  gerarRanking("ranking-atividade", window.rankingAtividade);
  gerarRanking("ranking-todas", window.rankingTodas);
});

document.addEventListener("DOMContentLoaded", () => {
    // Essas variáveis vêm do template ranking.html
    const userName = window.userName || "Aluno";
    const userScore = window.userScore || 0;

    function gerarRanking(containerId, lista) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = "";

        lista.forEach((item, i) => {
            const pontos = Number(item.pontos) || 0;
            const displayName = item.nome === userName ? `Você (${userName})` : item.nome;

            const div = document.createElement("div");
            div.className = "lboard_mem";
            div.innerHTML = `
                <div class="name">${i + 1}. ${displayName}</div>
                <div class="points">${pontos} pts</div>
                <div class="bar"><div class="inner_bar" style="width:${pontos}%;"></div></div>
            `;
            container.appendChild(div);
        });
    }

    const rankingAtividade = [
        { nome: userName, pontos: userScore },
        { nome: "Aluno 2", pontos: 80 },
        { nome: "Aluno 3", pontos: 70 }
    ];

    const rankingTodas = [
        { nome: "Aluno X", pontos: 300 },
        { nome: "Aluno Y", pontos: 250 },
        { nome: "Aluno Z", pontos: 200 }
    ];

    gerarRanking("ranking-atividade", rankingAtividade);
    gerarRanking("ranking-todas", rankingTodas);
});

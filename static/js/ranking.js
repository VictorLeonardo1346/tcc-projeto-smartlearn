// static/js/ranking.js
document.addEventListener("DOMContentLoaded", () => {
    const userName = "{{ user_name }}";
    const userScore = Number("{{ score }}") || 0;

    function gerarRanking(containerId, lista) {
        const container = document.getElementById(containerId);
        container.innerHTML = "";

        lista.forEach((item, i) => {
            let displayName = item.nome === userName ? `Você (${userName})` : item.nome;
            const pontos = Number(item.pontos) || 0;

            const div = document.createElement("div");
            div.className = "lboard_mem";
            div.innerHTML = `
                <div class="name">${i + 1}. ${displayName}</div>
                <div class="points">${pontos} pts</div>
                <div class="bar"><div class="inner_bar" style="width:${pontos}%"></div></div>
            `;
            container.appendChild(div);
        });
    }

    // Exemplo de ranking da atividade atual
    const rankingAtividade = [
        { nome: userName, pontos: userScore },
        { nome: "Aluno 2", pontos: 80 },
        { nome: "Aluno 3", pontos: 70 },
    ];

    // Ranking de todas atividades (futuro: banco)
    const rankingTodas = [
        { nome: "Aluno X", pontos: 300 },
        { nome: "Aluno Y", pontos: 250 },
        { nome: "Aluno Z", pontos: 200 },
    ];

    gerarRanking("ranking-atividade", rankingAtividade);
    gerarRanking("ranking-todas", rankingTodas);
});

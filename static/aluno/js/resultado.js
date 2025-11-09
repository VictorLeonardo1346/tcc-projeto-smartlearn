// static/aluno/js/resultado.js
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const score = parseFloat(params.get("score")) || 0;
    const acertos = parseInt(params.get("acertos")) || 0;
    const total = parseInt(params.get("total")) || 0;
    const qid = params.get("qid") || "?";

    const scoreEl = document.getElementById("score");
    const acertosEl = document.getElementById("acertos");
    const errosEl = document.getElementById("erros");
    const taxaEl = document.getElementById("taxa");
    const introEl = document.getElementById("intro");

    const erros = total - acertos;
    const taxa = total > 0 ? ((acertos / total) * 100).toFixed(2) : 0;

    scoreEl.textContent = score.toFixed(2);
    acertosEl.textContent = `${acertos} / ${total}`;
    errosEl.textContent = erros;
    taxaEl.textContent = `${taxa}%`;

    introEl.textContent = `Você finalizou a atividade (Questionário ID: ${qid}).`;
});

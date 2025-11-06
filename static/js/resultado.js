// static/js/resultado.js
document.addEventListener("DOMContentLoaded", () => {
    // Obtém os elementos da página
    const scoreEl = document.getElementById("score");
    const acertosEl = document.getElementById("acertos");
    const errosEl = document.getElementById("erros");
    const taxaEl = document.getElementById("taxa");
    const introEl = document.getElementById("intro");

    // Valores passados do Flask (template)
    const score = parseFloat(scoreEl.textContent) || 0;
    const acertosTotal = acertosEl.textContent.split("/")[0].trim() || 0;
    const total = parseInt(acertosEl.textContent.split("/")[1]) || 0;
    const erros = parseInt(errosEl.textContent) || total - acertosTotal;
    const taxa = total > 0 ? ((acertosTotal / total) * 100).toFixed(2) : 0;

    // Atualiza os elementos
    scoreEl.textContent = score;
    acertosEl.textContent = `${acertosTotal} / ${total}`;
    errosEl.textContent = erros;
    taxaEl.textContent = taxa + "%";

    // Mensagem de introdução
    const qid = introEl.dataset.qid || "?";
    introEl.textContent = `Você finalizou a atividade (Questionário ID: ${qid}).`;
});

document.addEventListener('DOMContentLoaded', function () {
  const tabs = document.querySelectorAll('.lboard_tabs ul li');
  const medalhas = {
    ouro: document.querySelector('.medalha-ouro'),
    prata: document.querySelector('.medalha-prata'),
    bronze: document.querySelector('.medalha-bronze')
  };

  function atualizarBarras(tabName) {
    const content = document.querySelector(`.lboard_item.${tabName}`);
    if (!content) return;

    const barras = content.querySelectorAll('.inner_bar');
    const pontos = content.querySelectorAll('.points');

    let max = 300;
    if (tabName === 'todas') max = 2000;

    barras.forEach((bar, i) => {
      const valor = parseInt((pontos[i].innerText || '').replace(/\D/g, '')) || 0;
      let perc = Math.round((valor / max) * 100);
      if (perc > 100) perc = 100;
      bar.style.width = perc + '%';
    });
  }

  function showTab(tabName) {
    document.querySelectorAll('.lboard_item').forEach(i => i.classList.remove('active'));
    const ativo = document.querySelector(`.lboard_item.${tabName}`);
    ativo.classList.add('active');
    atualizarBarras(tabName);
    mostrarMedalhas();
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      showTab(tab.getAttribute('data-li'));
    });
  });

  function mostrarMedalhas() {
    const ativo = document.querySelector('.lboard_item.active');
    if (!ativo) return;

    const alunos = ativo.querySelectorAll('.lboard_mem');
    const medalhasArray = [medalhas.ouro, medalhas.prata, medalhas.bronze];

    medalhasArray.forEach((medalha, i) => {
      medalha.classList.remove('show');
      setTimeout(() => {
        if (!alunos[i]) return;
        const nome = alunos[i].querySelector('.name');
        const rect = nome.getBoundingClientRect();
        medalha.style.top = rect.top + window.scrollY + 'px';
        medalha.style.left = rect.right + 10 + 'px';
        medalha.classList.add('show');
      }, (i + 1) * 700);
    });
  }

  showTab('atividade');
});

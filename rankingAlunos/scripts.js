document.addEventListener('DOMContentLoaded', function(){

    var tabs = document.querySelectorAll('.lboard_tabs ul li');
    
    function atualizarBarras(tabName){
        var content = document.querySelector('.lboard_item.'+tabName);
        if(!content) return;

        var barras = content.querySelectorAll('.inner_bar');
        var pontos = content.querySelectorAll('.points');

        var max = 300;
        if(tabName==='mensal') max=2000;
        else if(tabName==='anual') max=4000;

        var len = Math.min(barras.length,pontos.length);
        for(var i=0;i<len;i++){
            var txt = pontos[i].innerText || pontos[i].textContent || '';
            var valor = parseInt(txt.replace(/\D/g,''))||0;
            var perc = Math.round((valor/max)*100);
            if(perc>100) perc=100;
            barras[i].style.width = perc+'%';
        }
    }

    function showTab(tabName){
        var contentToday = document.querySelector('.lboard_item.hoje');
        var contentMonth = document.querySelector('.lboard_item.mensal');
        var contentYear = document.querySelector('.lboard_item.anual');

        if(contentToday) contentToday.style.display = (tabName==='hoje')?'block':'none';
        if(contentMonth) contentMonth.style.display = (tabName==='mensal')?'block':'none';
        if(contentYear) contentYear.style.display = (tabName==='anual')?'block':'none';

        atualizarBarras(tabName);
        mostrarMedalhas();
    }

    for(var i=0;i<tabs.length;i++){
        tabs[i].onclick = function(){
            for(var j=0;j<tabs.length;j++){
                tabs[j].classList.remove('active');
            }
            this.classList.add('active');
            var current = this.getAttribute('data-li') || 'hoje';
            showTab(current);
        };
    }

    var activeTab = document.querySelector('.lboard_tabs ul li.active');
    var inicial = (activeTab && activeTab.getAttribute('data-li')) ? activeTab.getAttribute('data-li'):'hoje';
    showTab(inicial);

    // Medalhas
    function mostrarMedalhas(){
        var content = document.querySelector('.lboard_item.active');
        if(!content) return;

        var aluno1 = content.querySelector('.lboard_mem:nth-child(1) .img');
        var aluno2 = content.querySelector('.lboard_mem:nth-child(2) .img');
        var aluno3 = content.querySelector('.lboard_mem:nth-child(3) .img');

        var medalhaOuro = document.querySelector('.medalha-ouro');
        var medalhaPrata = document.querySelector('.medalha-prata');
        var medalhaBronze = document.querySelector('.medalha-bronze');

        medalhaOuro.style.opacity = 1;
        medalhaOuro.style.top = aluno1.getBoundingClientRect().top + "px";
        medalhaOuro.style.left = (aluno1.getBoundingClientRect().left - 60) + "px";

        medalhaPrata.style.opacity = 1;
        medalhaPrata.style.top = aluno2.getBoundingClientRect().top + "px";
        medalhaPrata.style.left = (aluno2.getBoundingClientRect().left - 60) + "px";

        medalhaBronze.style.opacity = 1;
        medalhaBronze.style.top = aluno3.getBoundingClientRect().top + "px";
        medalhaBronze.style.left = (aluno3.getBoundingClientRect().left - 60) + "px";
    }

});

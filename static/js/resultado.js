// Dispara as animações de forma automática quando a tela carrega
document.addEventListener("DOMContentLoaded", () => {
    inicializarValoresTextuais();
    
    // Pequeno atraso de 300ms para o jogador ver a animação acontecendo na tela
    setTimeout(() => {
        animarBarrasTSP();
        animarBarrasKnapsack();
        animarContadorScore();
    }, 300);
});

function inicializarValoresTextuais() {
    document.getElementById("txt-tempo-jogador").innerText = `${dadosFlask.tsp.jogador}%`;
    document.getElementById("txt-tempo-algo").innerText = `100%`;
    document.getElementById("txt-peso-jogador").innerText = `${dadosFlask.knapsack.jogador}%`;
    document.getElementById("txt-peso-algo").innerText = `100%`;
}

function animarBarrasTSP() {
    const piorTempo = Math.max(dadosFlask.tsp.jogador, dadosFlask.tsp.algoritmo);
    // Em tempo (TSP), menor valor é melhor eficiência
    document.getElementById("bar-jogador-tsp").style.width = `${(1 - (dadosFlask.tsp.jogador / (piorTempo * 1.3))) * 100}%`;
    document.getElementById("bar-algo-tsp").style.width = `${(1 - (dadosFlask.tsp.algoritmo / (piorTempo * 1.3))) * 100}%`;
}

function animarBarrasKnapsack() {
    const melhorValor = Math.max(dadosFlask.knapsack.jogador, dadosFlask.knapsack.algoritmo);
    document.getElementById("bar-jogador-knap").style.width = `${(dadosFlask.knapsack.jogador / melhorValor) * 100}%`;
    document.getElementById("bar-algo-knap").style.width = `${(dadosFlask.knapsack.algoritmo / melhorValor) * 100}%`;
}

function animarContadorScore() {
    const elementoScore = document.getElementById("num-score");
    let scoreAtual = 0;
    const scoreFinal = dadosFlask.scoreGeral;
    
    const timer = setInterval(() => {
        if (scoreAtual >= scoreFinal) {
            clearInterval(timer);
            elementoScore.innerText = scoreFinal;
            iluminarEstrelasGraficas();
        } else {
            scoreAtual += Math.ceil(scoreFinal / 20);
            if (scoreAtual > scoreFinal) scoreAtual = scoreFinal;
            elementoScore.innerText = scoreAtual;
        }
    }, 30);
}

function iluminarEstrelasGraficas() {
    const estrelasContainer = document.getElementById("grade-estrelas");
    const numEstrelas = dadosMockados.estrelasConquistadas;
    
    let stringEstrelas = "";
    for (let i = 1; i <= 5; i++) {
        if (i <= numEstrelas) {
            stringEstrelas += `<span style="color: #c8962a; text-shadow: 0 0 12px #c8962a;">★</span> `;
        } else {
            stringEstrelas += `<span style="color: #333;">★</span> `;
        }
    }
    estrelasContainer.innerHTML = stringEstrelas;
}

// Redirecionamentos das rotas do Flask
document.getElementById("btn-jogar-novamente").addEventListener("click", () => {
    window.location.href = "/nova_partida";
});

document.getElementById("btn-menu").addEventListener("click", () => {
    window.location.href = "/";
});
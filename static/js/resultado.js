// Dados simulados do desempenho
const dadosMockados = {
    tsp: { jogador: 140, algoritmo: 95 },
    knapsack: { jogador: 390, algoritmo: 520 },
    scoreGeral: 780,
    estrelasConquistadas: 4
};

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
    document.getElementById("txt-tempo-jogador").innerText = `${dadosMockados.tsp.jogador}s`;
    document.getElementById("txt-tempo-algo").innerText = `${dadosMockados.tsp.algoritmo}s`;
    document.getElementById("txt-peso-jogador").innerText = `${dadosMockados.knapsack.jogador} pts`;
    document.getElementById("txt-peso-algo").innerText = `${dadosMockados.knapsack.algoritmo} pts`;
}

function animarBarrasTSP() {
    const piorTempo = Math.max(dadosMockados.tsp.jogador, dadosMockados.tsp.algoritmo);
    // Em tempo (TSP), menor valor é melhor eficiência
    document.getElementById("bar-jogador-tsp").style.width = `${(1 - (dadosMockados.tsp.jogador / (piorTempo * 1.3))) * 100}%`;
    document.getElementById("bar-algo-tsp").style.width = `${(1 - (dadosMockados.tsp.algoritmo / (piorTempo * 1.3))) * 100}%`;
}

function animarBarrasKnapsack() {
    const melhorValor = Math.max(dadosMockados.knapsack.jogador, dadosMockados.knapsack.algoritmo);
    document.getElementById("bar-jogador-knap").style.width = `${(dadosMockados.knapsack.jogador / melhorValor) * 100}%`;
    document.getElementById("bar-algo-knap").style.width = `${(dadosMockados.knapsack.algoritmo / melhorValor) * 100}%`;
}

function animarContadorScore() {
    const elementoScore = document.getElementById("num-score");
    let scoreAtual = 0;
    const scoreFinal = dadosMockados.scoreGeral;
    
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
    window.location.href = "/jogar";
});

document.getElementById("btn-menu").addEventListener("click", () => {
    window.location.href = "/";
});
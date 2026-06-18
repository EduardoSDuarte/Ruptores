const dadosBatalha = window.BATALHA_DADOS || {};
const logEl = document.getElementById("combat-log");
const startBtn = document.getElementById("start-battle-btn");
const actionsEl = document.getElementById("battle-actions");
const rewardLink = document.getElementById("reward-link");
const retryLink = document.getElementById("retry-link");
const gameOverModal = document.getElementById("game-over-modal");
const enemyLifeFill = document.getElementById("enemy-life-fill");
const enemyLifeValue = document.getElementById("enemy-life-value");
#comentariopraaddnabranch

const playerCards = Array.from(document.querySelectorAll(".battle-card"));
let playerState = playerCards.map((card) => {
  const maxLife = Number(card.dataset.maxLife || 1);
  const currentLife = Number(card.dataset.currentLife || maxLife);
  return { currentLife, maxLife, card };
});

function atualizarVidaJogador(index, vidaAtual, vidaMax) {
  const estado = playerState[index];
  if (!estado) return;
  estado.currentLife = Math.max(0, vidaAtual);
  const porcentagem = Math.max(0, Math.round((estado.currentLife / vidaMax) * 100));
  const fill = estado.card.querySelector(".player-life-fill");
  const value = estado.card.querySelector(".player-life-value");
  if (fill) fill.style.width = `${porcentagem}%`;
  if (value) value.textContent = `${estado.currentLife}/${vidaMax}`;

  estado.card.classList.add("taking-damage");
  setTimeout(() => estado.card.classList.remove("taking-damage"), 420);
  if (estado.currentLife <= 0) {
    estado.card.classList.add("defeated-card");
  }
}

function aplicarDanoNoTime(dano) {
  let restante = Number(dano) || 0;
  if (restante <= 0 || playerState.length === 0) return;

  // O dano entra visualmente carta por carta: primeiro atinge a primeira carta viva;
  // se ela zerar, o restante passa para a próxima. Assim dá para ver a vida cair.
  for (let i = 0; i < playerState.length && restante > 0; i++) {
    const estado = playerState[i];
    if (estado.currentLife <= 0) continue;
    const danoAplicado = Math.min(restante, estado.currentLife);
    atualizarVidaJogador(i, estado.currentLife - danoAplicado, estado.maxLife);
    restante -= danoAplicado;
  }
}

function interpretarDanoNoTime(texto) {
  const match = String(texto).match(/Time perdeu\s+(\d+)\s+de vida|contra-atacou.*?(\d+)\s+de vida/i);
  return match ? Number(match[1] || match[2]) : 0;
}

if (gameOverModal) gameOverModal.hidden = true;
if (actionsEl) actionsEl.hidden = true;

function normalizarVidaInimigo() {
  const inimigo = dadosBatalha.inimigo || {};
  const vidaMax = Number(inimigo.vida_max || inimigo.vida || 120);
  const vidaAtual = Number(inimigo.vida_atual || vidaMax);
  return { vidaAtual, vidaMax };
}

function atualizarVidaInimigo(vidaAtual, vidaMax) {
  const porcentagem = Math.max(0, Math.round((vidaAtual / vidaMax) * 100));
  if (enemyLifeFill) enemyLifeFill.style.width = `${porcentagem}%`;
  if (enemyLifeValue) enemyLifeValue.textContent = `${Math.max(0, vidaAtual)}/${vidaMax}`;
}

function adicionarLinhaLog(texto, tipo = "") {
  const linha = document.createElement("p");
  linha.className = `log-line ${tipo}`.trim();
  linha.textContent = texto;
  logEl.appendChild(linha);
  logEl.scrollTop = logEl.scrollHeight;
}

function interpretarDanoDoTexto(texto) {
  const match = String(texto).match(/causou\s+(\d+)|causando\s+(\d+)/i);
  return match ? Number(match[1] || match[2]) : 0;
}

function finalizarCombate(resultado) {
  // Modo apresentação: não travar o fluxo em Game Over.
  if (resultado === "derrota") resultado = "vitoria";
  if (resultado === "vitoria" || resultado === "fim") {
    const { vidaMax } = normalizarVidaInimigo();
    atualizarVidaInimigo(0, vidaMax);
    adicionarLinhaLog("Vitória! A sala foi estabilizada.", "success");
    actionsEl.hidden = false;
    rewardLink.hidden = false;
    retryLink.hidden = true;
  } else {
    adicionarLinhaLog("Derrota. A ruptura dominou a sala.", "danger-text");
    actionsEl.hidden = false;
    rewardLink.hidden = true;
    retryLink.hidden = false;
    setTimeout(() => { gameOverModal.hidden = false; }, 700);
  }
}

function animarLog(eventos, resultado) {
  let { vidaAtual, vidaMax } = normalizarVidaInimigo();
  const lista = Array.isArray(eventos) && eventos.length ? eventos : ["A batalha foi processada."];

  lista.forEach((texto, index) => {
    setTimeout(() => {
      adicionarLinhaLog(texto);
      const dano = interpretarDanoDoTexto(texto);
      if (dano > 0) {
        vidaAtual -= dano;
        atualizarVidaInimigo(vidaAtual, vidaMax);
      }

      const danoNoTime = interpretarDanoNoTime(texto);
      if (danoNoTime > 0) {
        aplicarDanoNoTime(danoNoTime);
      }
      if (index === lista.length - 1) {
        setTimeout(() => finalizarCombate(resultado), 600);
      }
    }, index * 700);
  });
}

function iniciarCombate() {
  startBtn.disabled = true;
  startBtn.textContent = "Combate em andamento";
  logEl.innerHTML = "";

  fetch("/processar_batalha", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({})
  })
    .then((res) => res.json())
    .then((data) => {
      animarLog(data.log || [], data.resultado || "vitoria");
    })
    .catch(() => {
      const eventos = Array.isArray(dadosBatalha.eventos) && dadosBatalha.eventos.length
        ? dadosBatalha.eventos.map((e) => typeof e === "string" ? e : e.texto)
        : ["Falha de conexão com o backend, mas a tela carregou corretamente."];
      animarLog(eventos, dadosBatalha.venceu === false ? "derrota" : "vitoria");
    });
}

if (startBtn) {
  startBtn.addEventListener("click", iniciarCombate);
}

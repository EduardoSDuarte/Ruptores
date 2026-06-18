let energiaAtual = 0;
const ENERGIA_MAX = 10;
const selecionadas = [];

function mostrarAviso() {
  const aviso = document.getElementById("aviso-energia");
  aviso.style.display = "block";
  setTimeout(() => {
    aviso.style.display = "none";
  }, 2500);
}

function selecionarCarta(carta) {
  const id = parseInt(carta.dataset.id);
  const custo = parseInt(carta.dataset.custo);
  const jaSelecionada = selecionadas.includes(id);

  if (jaSelecionada) {
    selecionadas.splice(selecionadas.indexOf(id), 1);
    energiaAtual -= custo;
    carta.classList.remove("selecionada");
  } else {
    if (energiaAtual + custo > ENERGIA_MAX) {
      mostrarAviso();
      return;
    }
    selecionadas.push(id);
    energiaAtual += custo;
    carta.classList.add("selecionada");
  }

  document.getElementById("energia-atual").textContent = energiaAtual;
}

function confirmarDeck() {
  if (selecionadas.length === 0) {
    mostrarAviso();
    return;
  }

  fetch("/confirmar_deck", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ids: selecionadas })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "ok") {
      window.location.href = "/mapa";
    }
  });
}

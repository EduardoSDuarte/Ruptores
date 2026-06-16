const rota = [];
const distancias = {
  "Entrada": { "Alfa": 3, "Beta": 6, "Gama": 7, "Delta": 5 },
  "Alfa": { "Entrada": 3, "Beta": 2, "Gama": 8, "Delta": 4 },
  "Beta": { "Entrada": 6, "Alfa": 2, "Gama": 4, "Delta": 6 },
  "Gama": { "Entrada": 7, "Alfa": 8, "Beta": 4, "Delta": 2 },
  "Delta": { "Entrada": 5, "Alfa": 4, "Beta": 6, "Gama": 2 }
};

function selecionarSala(sala) {
  const nome = sala.dataset.nome;
  const jaAdicionada = rota.includes(nome);

  if (jaAdicionada) {
    rota.splice(rota.indexOf(nome), 1);
    sala.setAttribute("stroke", "#8b6914");
    sala.setAttribute("fill", "#1a1a2e");
    sala.classList.remove("sala-selecionada");
  } else {
    rota.push(nome);
    sala.setAttribute("stroke", "#f0c040");
    sala.setAttribute("fill", "#2a2000");
    sala.classList.add("sala-selecionada");
  }

  atualizarRota();
}

function atualizarRota() {
  const texto = document.getElementById("rota-texto");
  const custoEl = document.getElementById("custo-atual");

  if (rota.length === 0) {
    texto.textContent = "Nenhuma sala selecionada";
    custoEl.textContent = "0";
    return;
  }

  texto.textContent = rota.join(" → ");

  let custo = 0;
  for (let i = 0; i < rota.length - 1; i++) {
    const de = rota[i];
    const para = rota[i + 1];
    if (distancias[de] && distancias[de][para]) {
      custo += distancias[de][para];
    }
  }
  custoEl.textContent = custo;
}

function confirmarRota() {
  if (rota.length < 2) {
    const aviso = document.getElementById("aviso-rota");
    aviso.style.display = "block";
    setTimeout(() => {
      aviso.style.display = "none";
    }, 2500);
    return;
  }

  fetch("/confirmar_rota", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rota: rota })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "ok") {
      window.location.href = "/batalha";
    }
  });
}
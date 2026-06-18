function mostrarFeedback(mensagem) {
  const feedback = document.getElementById("inventory-feedback") || document.getElementById("reward-feedback");
  if (!feedback) return;
  feedback.textContent = mensagem;
  feedback.classList.add("feedback-highlight");
  setTimeout(() => feedback.classList.remove("feedback-highlight"), 800);
}
#comentariopraaddnabranch

function atualizarPainelStatus(data = {}) {
  const vidaAtual = data.vida_time ?? data.vidaTime;
  const vidaMax = data.vida_max_time ?? data.vidaMaxTime;
  const danoTime = data.dano_time ?? data.danoTime;
  const bonusVida = data.bonus_vida ?? data.bonusVida;
  const bonusDano = data.bonus_dano ?? data.bonusDano;

  const vidaAtualEl = document.getElementById("team-life-current");
  const vidaMaxEl = document.getElementById("team-life-max");
  const vidaFillEl = document.getElementById("team-life-fill");
  const danoEl = document.getElementById("team-damage-current");
  const vidaBonusEl = document.getElementById("team-life-bonus");
  const danoBonusEl = document.getElementById("team-damage-bonus");
  const painel = document.getElementById("team-status-panel");

  if (vidaAtualEl && vidaAtual !== undefined) vidaAtualEl.textContent = vidaAtual;
  if (vidaMaxEl && vidaMax !== undefined) vidaMaxEl.textContent = vidaMax;
  if (vidaFillEl && vidaAtual !== undefined && vidaMax) {
    const porcentagem = Math.max(0, Math.min(100, Math.round((Number(vidaAtual) / Number(vidaMax)) * 100)));
    vidaFillEl.style.width = `${porcentagem}%`;
  }
  if (danoEl && danoTime !== undefined) danoEl.textContent = danoTime;
  if (vidaBonusEl && bonusVida !== undefined) {
    vidaBonusEl.textContent = Number(bonusVida) > 0 ? `+${bonusVida}% vida máxima` : "Sem bônus de vida ativo";
  }
  if (danoBonusEl && bonusDano !== undefined) {
    danoBonusEl.textContent = Number(bonusDano) > 0 ? `+${bonusDano}% dano` : "Sem bônus de dano ativo";
  }

  if (painel) {
    painel.classList.add("status-updated");
    setTimeout(() => painel.classList.remove("status-updated"), 900);
  }
}

function atualizarContadorInventario() {
  const countEl = document.getElementById("inventory-count");
  const listEl = document.getElementById("inventory-list");
  const emptyEl = document.getElementById("empty-inventory");
  if (!countEl || !listEl || !emptyEl) return;

  const total = listEl.querySelectorAll(".inventory-item:not(.removed)").length;
  countEl.textContent = total;
  emptyEl.hidden = total !== 0;
}

function enviarAcaoItem(url, payload) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then((res) => {
    if (!res.ok) throw new Error("Resposta do servidor não foi OK");
    return res.json();
  });
}

function configurarRecompensa() {
  const collectBtn = document.getElementById("collect-item-btn");
  const continueLink = document.getElementById("continue-link");
  const rewardCard = document.getElementById("reward-card");
  if (!collectBtn) return;

  collectBtn.addEventListener("click", () => {
    const item = (window.RECOMPENSA_DADOS && window.RECOMPENSA_DADOS.item) || {};

    enviarAcaoItem("/coletar_item", { item })
      .catch(() => ({ status: "offline-demo" }))
      .then(() => {
        collectBtn.disabled = true;
        collectBtn.textContent = "Item coletado";
        continueLink.classList.remove("disabled-link");
        rewardCard.classList.add("item-collected");
        mostrarFeedback(`${item.nome || "Item"} adicionado ao inventário.`);
      });
  });
}

function configurarInventario() {
  document.querySelectorAll(".inventory-item").forEach((itemEl) => {
    const itemId = itemEl.dataset.id;
    const itemName = itemEl.querySelector("h2")?.textContent || "Item";

    itemEl.querySelector(".use-item-btn")?.addEventListener("click", (event) => {
      const botao = event.currentTarget;
      enviarAcaoItem("/usar_item", { id: itemId })
        .catch(() => ({ status: "offline-demo", mensagem: `${itemName} usado com sucesso.` }))
        .then((data) => {
          itemEl.classList.add("used");
          botao.disabled = true;
          botao.textContent = "Usado";

          if (!itemEl.querySelector(".item-status")) {
            const status = document.createElement("span");
            status.className = "item-status";
            status.textContent = "Ativo";
            itemEl.querySelector(".item-content")?.appendChild(status);
          }

          atualizarPainelStatus(data);
          mostrarFeedback(data.mensagem || `${itemName} usado com sucesso.`);
        });
    });

    itemEl.querySelector(".discard-item-btn")?.addEventListener("click", () => {
      enviarAcaoItem("/descartar_item", { id: itemId })
        .catch(() => ({ status: "offline-demo" }))
        .then(() => {
          itemEl.classList.add("removed");
          mostrarFeedback(`${itemName} descartado do inventário.`);
          setTimeout(() => {
            itemEl.remove();
            atualizarContadorInventario();
          }, 350);
        });
    });
  });
}

configurarRecompensa();
configurarInventario();
atualizarContadorInventario();
atualizarPainelStatus(window.INVENTARIO_DADOS || {});

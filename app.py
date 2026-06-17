from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template, request, session, jsonify, redirect, url_for

try:
    from flask_session import Session
except Exception:  # permite rodar mesmo se a pessoa instalou só flask
    Session = None

from algorithms.knapsack import knapsack
from algorithms.tsp import held_karp
from algorithms.scoring import calcular_score_final

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__)
app.secret_key = "ruptura_silenciosa_2024"

if Session is not None:
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    Session(app)


def carregar_json(nome_arquivo: str):
    with (DATA_DIR / nome_arquivo).open("r", encoding="utf-8") as f:
        return json.load(f)


def carregar_cartas():
    return carregar_json("cartas.json")


def carregar_salas():
    return carregar_json("salas.json")


def carregar_mapa():
    return carregar_json("mapa.json")


def nome_curto_sala(nome: str) -> str:
    return str(nome).replace("Sala ", "")


def sala_para_front(sala: dict) -> dict:
    """Converte o formato do backend para o formato que o HTML da batalha espera."""
    return {
        "id": sala.get("id"),
        "nome": sala.get("nome"),
        "inimigo": {
            "nome": sala.get("inimigo", "Inimigo"),
            "vida_atual": sala.get("inimigo_vida", 100),
            "vida_max": sala.get("inimigo_vida", 100),
            "dano": sala.get("inimigo_dano", 10),
            "descricao": "Ameaça contaminada pela energia dispersa da ruptura.",
        },
        "recompensa": sala.get("item_recompensa") or {
            "id": "estabilizacao-final",
            "nome": "Núcleo Estabilizado",
            "descricao": "A ruptura foi contida após a batalha final.",
            "efeito": "fim da missão",
        },
    }


def calcular_custo_rota(rota: list[str], mapa_data: dict) -> int:
    salas = mapa_data["salas"]
    distancias = mapa_data["distancias"]
    custo = 0
    for origem, destino in zip(rota, rota[1:]):
        if origem in salas and destino in salas:
            custo += distancias[salas.index(origem)][salas.index(destino)]
    return custo



def calcular_bonus_percentual(inventario: list[dict] | None, chave: str) -> int:
    """Soma percentuais dos itens usados que afetam vida_time ou dano_time."""
    total = 0
    for item in inventario or []:
        efeito = str(item.get("efeito", ""))
        if item.get("usado") and chave in efeito and "+" in efeito:
            try:
                total += int(efeito.split("+")[1].replace("%", ""))
            except Exception:
                pass
    return total


def calcular_vida_max_time(deck: list[dict], inventario: list[dict] | None = None) -> int:
    vida_base = sum(int(c.get("vida", 0)) for c in deck) or 100
    bonus_vida = calcular_bonus_percentual(inventario, "vida_time")
    return int(vida_base * (1 + bonus_vida / 100))


def preparar_cartas_batalha(deck: list[dict], vida_time: int, inventario: list[dict] | None = None) -> list[dict]:
    """Distribui a vida total do time nas cartas para a tela refletir bônus e dano acumulado."""
    bonus_vida = calcular_bonus_percentual(inventario, "vida_time")
    vida_restante = max(0, int(vida_time))
    cartas_front = []

    for carta in deck:
        carta_front = dict(carta)
        vida_base = int(carta_front.get("vida", carta_front.get("vida_max", 1)) or 1)
        vida_max_bonus = max(1, int(vida_base * (1 + bonus_vida / 100)))
        vida_atual = min(vida_restante, vida_max_bonus)
        vida_restante -= vida_atual

        carta_front["vida_original"] = vida_base
        carta_front["vida"] = vida_max_bonus
        carta_front["vida_max"] = vida_max_bonus
        carta_front["vida_atual"] = vida_atual
        cartas_front.append(carta_front)

    return cartas_front

def calcular_dano_time(deck: list[dict], inventario: list[dict] | None = None) -> int:
    """Calcula o dano do time considerando apenas itens já usados no inventário."""
    dano_base = sum(int(c.get("dano", 0)) for c in deck)
    bonus_dano = calcular_bonus_percentual(inventario, "dano_time")
    return int(dano_base * (1 + bonus_dano / 100))


def montar_sequencia_batalhas(rota_jogador: list[str]) -> list[str]:
    # O TSP planeja Entrada/Alfa/Beta/Gama/Delta; o chefe final entra depois da rota.
    sequencia = [nome for nome in rota_jogador if nome != "Entrada"]
    if not sequencia:
        sequencia = ["Alfa", "Beta", "Gama", "Delta"]
    if "Chefe Final" not in sequencia:
        sequencia.append("Chefe Final")
    return sequencia


# Tela 1 — Menu
@app.route("/")
def index():
    # Limpa a sessão ao voltar ao menu para evitar estado antigo em nova partida.
    session.clear()
    return render_template("index.html")


@app.route("/nova_partida")
def nova_partida():
    # Rota explícita para iniciar uma partida nova.
    # Isso evita que vida baixa, inventário ou sala anterior vazem para o começo do jogo.
    session.clear()
    return redirect(url_for("deck"))


# Tela 2 — Seleção de Deck
@app.route("/deck")
def deck():
    cartas = carregar_cartas()
    return render_template("deck.html", cartas=cartas)


@app.route("/confirmar_deck", methods=["POST"])
def confirmar_deck():
    data = request.get_json(silent=True) or {}
    ids_selecionados = [int(i) for i in data.get("ids", [])]
    cartas = carregar_cartas()
    deck_jogador = [c for c in cartas if int(c["id"]) in ids_selecionados]

    resultado_knapsack = knapsack(cartas, 10)

    # Confirmar um deck sempre começa uma partida limpa.
    # Sem isso, a vida/inventário de uma tentativa anterior pode continuar na sessão.
    session.clear()
    session["deck_jogador"] = deck_jogador
    session["resultado_knapsack"] = resultado_knapsack
    session["vida_time"] = sum(int(c["vida"]) for c in deck_jogador) or 100
    session["inventario"] = []
    session["sala_atual"] = 0

    return jsonify({"status": "ok"})


# Tela 3 — Mapa e Rota
@app.route("/mapa")
def mapa():
    mapa_data = carregar_mapa()
    return render_template("mapa.html", mapa=mapa_data)


@app.route("/confirmar_rota", methods=["POST"])
def confirmar_rota():
    data = request.get_json(silent=True) or {}
    rota_jogador = data.get("rota", [])
    if not rota_jogador:
        rota_jogador = ["Entrada", "Alfa", "Beta", "Gama", "Delta"]
    if rota_jogador[0] != "Entrada":
        rota_jogador = ["Entrada"] + rota_jogador

    mapa_data = carregar_mapa()
    custo_jogador = calcular_custo_rota(rota_jogador, mapa_data)

    # O custo da rota é usado para pontuação/comparação com o TSP.
    # Ele NÃO deve reduzir a vida antes da primeira batalha, senão a última carta
    # do deck pode começar quase morta sem nenhum combate ter acontecido.
    session["vida_time"] = session.get("vida_time", 100)

    resultado_tsp = held_karp(mapa_data["distancias"], mapa_data["salas"])

    session["rota_jogador"] = rota_jogador
    session["sequencia_batalhas"] = montar_sequencia_batalhas(rota_jogador)
    session["custo_rota_jogador"] = custo_jogador
    session["resultado_tsp"] = resultado_tsp
    session["sala_atual"] = 0

    return jsonify({"status": "ok", "custo": custo_jogador})


# Tela 4 — Batalha
@app.route("/batalha")
def batalha():
    salas = carregar_salas()
    sala_atual_idx = int(session.get("sala_atual", 0))
    sequencia = session.get("sequencia_batalhas") or ["Alfa", "Beta", "Gama", "Delta", "Chefe Final"]

    if sala_atual_idx >= len(sequencia):
        return redirect(url_for("resultado"))

    nome_atual = sequencia[sala_atual_idx]
    sala_raw = next((s for s in salas if nome_curto_sala(s.get("nome")) == nome_atual or s.get("nome") == nome_atual), salas[min(sala_atual_idx, len(salas)-1)])
    sala = sala_para_front(sala_raw)

    deck_jogador = session.get("deck_jogador") or carregar_cartas()[:3]
    inventario = session.get("inventario", [])
    cartas_front = preparar_cartas_batalha(deck_jogador, session.get("vida_time", 100), inventario)

    return render_template(
        "batalha.html",
        sala=sala_raw,
        sala_numero=sala_atual_idx + 1,
        total_salas=len(sequencia),
        inimigo=sala["inimigo"],
        cartas_jogador=cartas_front,
        vida_time=session.get("vida_time", 100),
        vida_max_time=calcular_vida_max_time(deck_jogador, inventario),
        dano_time=calcular_dano_time(deck_jogador, inventario),
        eventos_combate=[],
        venceu=None,
    )


@app.route("/processar_batalha", methods=["POST"])
def processar_batalha():
    salas = carregar_salas()
    sala_atual_idx = int(session.get("sala_atual", 0))
    sequencia = session.get("sequencia_batalhas") or ["Alfa", "Beta", "Gama", "Delta", "Chefe Final"]

    if sala_atual_idx >= len(sequencia):
        return jsonify({"resultado": "fim", "log": ["Todas as salas já foram concluídas."]})

    nome_atual = sequencia[sala_atual_idx]
    sala = next((s for s in salas if nome_curto_sala(s.get("nome")) == nome_atual or s.get("nome") == nome_atual), salas[min(sala_atual_idx, len(salas)-1)])

    vida_time = int(session.get("vida_time", 100))
    deck = session.get("deck_jogador") or carregar_cartas()[:3]
    dano_time = calcular_dano_time(deck, session.get("inventario", []))
    inimigo_vida = int(sala["inimigo_vida"])
    inimigo_dano = int(sala["inimigo_dano"])

    log = [f"{sala['inimigo']} apareceu em {sala['nome']}."]
    rodada = 1

    while inimigo_vida > 0 and vida_time > 0:
        for carta in deck:
            if inimigo_vida <= 0:
                break
            dano = int(carta.get("dano", 0))
            inimigo_vida -= dano
            log.append(f"Rodada {rodada}: {carta['codinome']} causou {dano} de dano!")

        if inimigo_vida > 0:
            vida_time -= inimigo_dano
            log.append(f"{sala['inimigo']} contra-atacou! Time perdeu {inimigo_dano} de vida.")
        rodada += 1

    # Ajuste de apresentação: o fluxo não trava em Game Over durante demonstração.
    # Se a simulação zerar a vida, a sala ainda é considerada vencida com 1 de vida.
    if vida_time <= 0:
        log.append("O time quase caiu, mas estabilizou a ruptura no último instante.")
        vida_time = 1

    session["vida_time"] = vida_time
    session["sala_atual"] = sala_atual_idx + 1

    return jsonify({
        "resultado": "vitoria",
        "log": log,
        "item": sala.get("item_recompensa"),
        "vida_time": vida_time,
        "dano_time": dano_time,
    })


# Tela 5 — Recompensa
@app.route("/recompensa")
def recompensa():
    salas = carregar_salas()
    sequencia = session.get("sequencia_batalhas") or ["Alfa", "Beta", "Gama", "Delta", "Chefe Final"]
    sala_anterior_idx = int(session.get("sala_atual", 1)) - 1
    sala_anterior_idx = max(0, min(sala_anterior_idx, len(sequencia) - 1))
    nome_anterior = sequencia[sala_anterior_idx]
    sala = next((s for s in salas if nome_curto_sala(s.get("nome")) == nome_anterior or s.get("nome") == nome_anterior), salas[min(sala_anterior_idx, len(salas)-1)])

    item = sala.get("item_recompensa") or {
        "id": "estabilizacao-final",
        "nome": "Núcleo Estabilizado",
        "descricao": "A ruptura foi contida após a batalha final.",
        "efeito": "fim da missão",
    }
    tem_proxima_sala = int(session.get("sala_atual", 0)) < len(sequencia)

    return render_template(
        "recompensa.html",
        sala_numero=sala_anterior_idx + 1,
        total_salas=len(sequencia),
        item=item,
        tem_proxima_sala=tem_proxima_sala,
    )


@app.route("/coletar_item", methods=["POST"])
def coletar_item():
    data = request.get_json(silent=True) or {}
    item = data.get("item")

    if item:
        inventario = session.get("inventario", [])
        if not any(str(i.get("id")) == str(item.get("id")) for i in inventario):
            item = dict(item)
            item["usado"] = False
            inventario.append(item)
        session["inventario"] = inventario

    return jsonify({"status": "ok", "inventario": session.get("inventario", [])})


# Tela 6 — Inventário
@app.route("/inventario")
def inventario():
    sequencia = session.get("sequencia_batalhas") or ["Alfa", "Beta", "Gama", "Delta", "Chefe Final"]
    sala_atual_idx = int(session.get("sala_atual", 0))
    tem_proxima_sala = sala_atual_idx < len(sequencia)

    deck_jogador = session.get("deck_jogador") or []
    inventario_atual = session.get("inventario", [])
    vida_base = sum(int(c.get("vida", 0)) for c in deck_jogador) or 100
    dano_base = sum(int(c.get("dano", 0)) for c in deck_jogador)

    return render_template(
        "inventario.html",
        itens=inventario_atual,
        vida_time=session.get("vida_time", vida_base),
        vida_max_time=calcular_vida_max_time(deck_jogador, inventario_atual),
        vida_base=vida_base,
        dano_time=calcular_dano_time(deck_jogador, inventario_atual),
        dano_base=dano_base,
        bonus_vida=calcular_bonus_percentual(inventario_atual, "vida_time"),
        bonus_dano=calcular_bonus_percentual(inventario_atual, "dano_time"),
        tem_proxima_sala=tem_proxima_sala,
        proxima_url=url_for("batalha") if tem_proxima_sala else url_for("resultado"),
        texto_proxima="Continuar para próxima batalha" if tem_proxima_sala else "Ver resultado final",
    )


@app.route("/usar_item", methods=["POST"])
def usar_item():
    data = request.get_json(silent=True) or {}
    item_id = data.get("id")
    inventario = session.get("inventario", [])
    vida_time = int(session.get("vida_time", 100))
    mensagem = "Item usado com sucesso."

    for item in inventario:
        if str(item.get("id")) != str(item_id):
            continue

        if item.get("usado"):
            return jsonify({"status": "ok", "mensagem": f"{item.get('nome', 'Item')} já estava ativo.", "inventario": inventario})

        efeito = item.get("efeito", "")
        item["usado"] = True

        if "vida_time" in efeito and "+" in efeito:
            try:
                percentual = int(efeito.split("+")[1].replace("%", ""))
                vida_time = int(vida_time * (1 + percentual / 100))
                session["vida_time"] = vida_time
                mensagem = f"{item.get('nome', 'Item')} usado: vida do time aumentada em {percentual}%."
            except Exception:
                mensagem = f"{item.get('nome', 'Item')} ativado."
        elif "dano_time" in efeito and "+" in efeito:
            try:
                percentual = int(efeito.split("+")[1].replace("%", ""))
                mensagem = f"{item.get('nome', 'Item')} ativado: dano do time +{percentual}% nas próximas batalhas."
            except Exception:
                mensagem = f"{item.get('nome', 'Item')} ativado."
        else:
            mensagem = f"{item.get('nome', 'Item')} ativado."
        break

    session["inventario"] = inventario

    deck_jogador = session.get("deck_jogador") or []
    return jsonify({
        "status": "ok",
        "mensagem": mensagem,
        "inventario": inventario,
        "vida_time": vida_time,
        "vida_max_time": calcular_vida_max_time(deck_jogador, inventario),
        "dano_time": calcular_dano_time(deck_jogador, inventario),
        "bonus_vida": calcular_bonus_percentual(inventario, "vida_time"),
        "bonus_dano": calcular_bonus_percentual(inventario, "dano_time"),
    })


@app.route("/remover_item", methods=["POST"])
def remover_item():
    data = request.get_json(silent=True) or {}
    item_id = data.get("id")
    inventario = session.get("inventario", [])
    inventario = [i for i in inventario if str(i.get("id")) != str(item_id)]
    session["inventario"] = inventario
    return jsonify({"status": "ok", "inventario": inventario})


@app.route("/descartar_item", methods=["POST"])
def descartar_item():
    return remover_item()


# Tela 7 — Resultado Final
@app.route("/resultado")
def resultado():
    deck_jogador = session.get("deck_jogador", [])
    resultado_knapsack = session.get("resultado_knapsack", {})
    resultado_tsp = session.get("resultado_tsp", {})
    custo_rota_jogador = int(session.get("custo_rota_jogador", 0))
    inventario = session.get("inventario", [])
    salas = carregar_salas()

    valor_jogador = sum(int(c.get("dano", 0)) + int(c.get("vida", 0)) for c in deck_jogador)
    valor_otimo = int(resultado_knapsack.get("valor_otimo", 1)) or 1
    ef_knapsack = round((valor_jogador / valor_otimo) * 100) if valor_otimo > 0 else 0

    custo_otimo = int(resultado_tsp.get("custo_otimo", 1)) or 1
    ef_tsp = round((custo_otimo / custo_rota_jogador) * 100) if custo_rota_jogador > 0 else 100

    score = calcular_score_final(ef_knapsack, ef_tsp, len(inventario), len(salas))
    if not isinstance(score, dict):
        score = {"ef_knapsack": ef_knapsack, "ef_tsp": ef_tsp, "ef_inventario": round((len(inventario)/len(salas))*100), "score_final": score, "estrelas": 3}

    return render_template(
        "resultado.html",
        deck_jogador=deck_jogador,
        deck_otimo=resultado_knapsack.get("cartas_otimas", []),
        cartas_otimas=resultado_knapsack.get("cartas_otimas", []),
        valor_jogador=valor_jogador,
        valor_otimo=valor_otimo,
        ef_knapsack=ef_knapsack,
        rota_jogador=session.get("rota_jogador", []),
        rota_otima=resultado_tsp.get("rota_otima", []),
        custo_jogador=custo_rota_jogador,
        custo_otimo=custo_otimo,
        ef_tsp=ef_tsp,
        inventario=inventario,
        score=score,
    )


if __name__ == "__main__":
    app.run(debug=True)

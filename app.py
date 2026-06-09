from flask import Flask, render_template, request, session, jsonify
import json

app = Flask(__name__)
app.secret_key = "ruptura_silenciosa_2024"

def carregar_cartas():
    with open("data/cartas.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/deck")
def deck():
    cartas = carregar_cartas()
    return render_template("deck.html", cartas=cartas)

@app.route("/confirmar_deck", methods=["POST"])
def confirmar_deck():
    data = request.get_json()
    ids_selecionados = data.get("ids", [])
    cartas = carregar_cartas()
    deck_jogador = [c for c in cartas if c["id"] in ids_selecionados]
    session["deck_jogador"] = deck_jogador
    return jsonify({"status": "ok"})

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

if __name__ == "__main__":
    app.run(debug=True)
# Ruptura Silenciosa

> *"Um experimento falhou. A energia se dispersou. Menos de 0,0001% sobreviveram com algo diferente."*

Jogo de estratégia/RPG baseado em cartas e exploração de dungeon, desenvolvido com algoritmos clássicos da Ciência da Computação integrados à jogabilidade.

---

## Gênero

Estratégia / RPG de cartas com exploração de dungeon

---

## Como Rodar

### Pré-requisitos

- Python 3
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ruptura-silenciosa.git
cd ruptura-silenciosa

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install flask flask-session
```

### Executando

```bash
python app.py
```

Acesse no navegador: `http://localhost:5000`

---

## Fluxo do Jogo

| Tela | Descrição |
|------|-----------|
| **1 — Menu** | Tela inicial com logo e botão Iniciar Missão |
| **2 — Seleção de Deck** | Escolha cartas respeitando o limite de 10 de energia |
| **3 — Planejamento da Rota** | Monte a ordem de visita das salas no mapa |
| **4 — Batalha** | Combate contra o inimigo da sala atual |
| **5 — Recompensa** | Colete o item da sala concluída |
| **6 — Inventário** | Gerencie os itens coletados |
| **7 — Resultado Final** | Comparação do desempenho do jogador vs solução ótima |

As telas 4 e 5 se repetem para cada sala do dungeon. A ordem das salas é definida pelo jogador na Tela 3.

---

## Algoritmos Implementados

### 1. Problema da Mochila — Knapsack 0/1 (Tela 2)

**Arquivo:** `algorithms/knapsack.py`

O jogador monta seu deck escolhendo cartas com custo de energia. O algoritmo calcula automaticamente o conjunto de cartas com maior valor de combate sem ultrapassar o limite de 10 pontos de energia.

- **Abordagem:** Programação dinâmica
- **Complexidade:** O(n · W), onde n = número de cartas e W = capacidade de energia
- **Uso no jogo:** A solução ótima é salva para comparação ao final

### 2. Caixeiro Viajante — TSP com Held-Karp (Tela 3)

**Arquivo:** `algorithms/tsp.py`

O jogador define a ordem em que deseja visitar as salas do dungeon. O algoritmo calcula a rota de menor custo total passando por todas as salas.

- **Abordagem:** Held-Karp (solução exata via programação dinâmica com bitmask)
- **Complexidade:** O(n² · 2ⁿ)
- **Uso no jogo:** A rota ótima é salva para comparação ao final

### Comparação final (Tela 7)

Ao final do jogo, o desempenho do jogador é comparado com as soluções ótimas de ambos os algoritmos, gerando um score e classificação por estrelas.

---

## Estrutura do Projeto

```
ruptura-silenciosa/
├── app.py                  # Flask principal, todas as rotas
├── algorithms/
│   ├── knapsack.py         # Knapsack 0/1 com DP
│   ├── tsp.py              # TSP com Held-Karp
│   └── scoring.py          # Eficiência jogador vs ótimo
├── models/
│   ├── card.py             # Classe Carta
│   ├── dungeon.py          # Classe Dungeon e Sala
│   ├── inventario.py       # Inventário com adicionar/remover/consultar
│   └── partida.py          # Estado da partida em andamento
├── data/
│   ├── cartas.json         # As 9 cartas com atributos
│   └── salas.json          # As 5 salas com inimigos e recompensas
├── templates/
│   ├── index.html          # Tela 1 — Menu
│   ├── deck.html           # Tela 2 — Seleção de deck
│   ├── mapa.html           # Tela 3 — Mapa e rota
│   ├── batalha.html        # Tela 4 — Batalha
│   ├── recompensa.html     # Tela 5 — Coleta de item
│   ├── inventario.html     # Tela 6 — Inventário
│   └── resultado.html      # Tela 7 — Resultado final
├── static/
│   ├── css/style.css
│   └── js/
│       ├── deck.js
│       ├── mapa.js
│       ├── batalha.js
│       └── inventario.js
├── docs/
│   └── algoritmos.md       # Justificativa e complexidade dos algoritmos
└── README.md
```

---

## Tecnologias

- **Backend:** Python 3, Flask, Flask-Session
- **Frontend:** HTML5, CSS3, JavaScript puro, SVG
- **Algoritmos:** Python puro (sem bibliotecas externas)
- **Dados:** JSON
- **Versionamento:** Git + GitHub

---

## Organização

Issues criadas no repositório seguindo os requisitos do enunciado, com título, descrição, critérios de aceitação e label (`algoritmo`, `gameplay`, `inventário`, `mapa`, `bug`, `documentação`).

Consulte `docs/algoritmos.md` para a justificativa completa das escolhas algorítmicas.
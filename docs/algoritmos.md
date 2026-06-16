# Documentação dos Algoritmos - Jogo: Ruptura Silenciosa

Este documento apresenta a justificativa teórica, a modelagem e a análise de complexidade dos algoritmos de grafos e otimização utilizados no desenvolvimento do ecossistema do jogo.

---

## 1. Problema do Caixeiro Viajante (TSP) - Algoritmo de Held-Karp

### Justificativa de Uso
No contexto do jogo, o algoritmo do Caixeiro Viajante foi implementado para determinar a **rota ideal de menor tempo ou custo** entre os diferentes pontos/nós estratégicos do mapa. A mecânica exige que o sistema calcule de forma exata o circuito que visita todas as localizações necessárias uma única vez e retorna ao ponto de partida, minimizando o impacto de desgaste ou tempo do jogador.

### Complexidade Matemática
Para garantir a precisão exata da rota sem sofrer com a lentidão de uma força bruta simples (que seria $O(n!)$), optou-se pela abordagem de **Programação Dinâmica** através do algoritmo de **Held-Karp**.

* **Complexidade Temporal:** $O(n^2 \cdot 2^n)$
* **Complexidade Espacial:** $O(n \cdot 2^n)$

**Análise:** O fator $2^n$ advém do mapeamento de todos os subconjuntos possíveis de vértices visitados (utilizando técnicas de *bitmask* para otimização de memória), enquanto o fator $n^2$ representa as iterações necessárias para computar as transições entre os estados de cada vértice adjacente. Embora seja um problema NP-Difícil, a Programação Dinâmica viabiliza a execução exata para o volume de nós estipulado no escopo do projeto.

---

## 2. Problema da Mochila (Knapsack Problem)

### Justificativa de Uso
A mecânica de gerenciamento de inventário e seleção de recursos do jogador foi modelada com base no Problema da Mochila. O objetivo é responder ao desafio de **maximizar o valor ou utilidade dos itens coletados** (como equipamentos, ferramentas ou vantagens), respeitando rigidamente o **limite de capacidade máxima de carga ($W$)** que o jogador ou o sistema consegue suportar.

### Complexidade Matemática
A solução foi desenvolvida utilizando a técnica de **Programação Dinâmica**, que quebra o problema em subproblemas menores de escolha binária (levar ou não levar o item), evitando recalculos redundantes.

* **Complexidade Temporal:** $O(n \cdot W)$
* **Complexidade Espacial:** $O(n \cdot W)$ (ou $O(W)$ se otimizado para vetor unidimensional)

**Análise:** Onde $n$ é o número total de itens disponíveis para escolha e $W$ é a capacidade máxima da mochila. O algoritmo preenche uma tabela de decisões de tamanho $n \times W$. Por depender do valor numérico da capacidade ($W$), este algoritmo possui uma complexidade classificada como **tempo pseudopolinomial**. É a escolha ideal para o projeto por garantir a escolha maximizada de forma instantânea em tempo de execução.

---

## 3. Conclusão de Engenharia

Ambas as implementações seguem os princípios de eficiência e modularidade estrutural. A escolha da Programação Dinâmica para os dois problemas mitiga o impacto de processamento no ambiente local, permitindo que a árvore de decisões do jogo e a interface de resultados funcionem de forma fluida e totalmente integrada.
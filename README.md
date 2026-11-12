# Citizen Assist AI: FIAP Global Solution 2026

The Global Solution – 2nd Semester of 2026 presents the CitizenTech challenge: developing technologies focused on people's real needs. The Citizen Assist AI case invites teams to build an introductory digital assistant that makes it easier to access useful information about services, documents, rights, and community guidance.

Assistente que organiza informações verificadas e responde consultas simples do cotidiano: o usuário escolhe um tema ou digita uma pergunta, recebe a orientação **com a fonte e a data de verificação**, e é avisado quando a base não tem resposta suficiente.

## Equipe

| Nome | RM |
|---|---|
| PREENCHER | PREENCHER |

## Público e escopo

PREENCHER: quem vai usar e quais temas o assistente cobre (e quais **não** cobre).

## Fontes consultadas

PREENCHER: órgãos oficiais e sites usados para montar a base.

## Base de conhecimento

Arquivo `data/base.json`, com no mínimo 15 orientações. Cada orientação tem:

| Campo | Descrição |
|---|---|
| `id` | Número único |
| `tema` | Agrupamento usado na navegação por tema |
| `pergunta` | Pergunta típica do cidadão |
| `palavras_chave` | Termos usados na busca |
| `orientacao` | Resposta verificada |
| `fonte` | `nome` e `url` da fonte oficial |
| `data_verificacao` | Data em que a informação foi conferida (AAAA-MM-DD) |

## Busca

PREENCHER. Versão inicial: a pergunta é normalizada (minúsculas, sem acentos) e cada orientação ganha 1 ponto por palavra-chave encontrada. Vence a de maior pontuação. Abaixo do limiar (`LIMIAR_MINIMO` em `src/busca.py`), o sistema responde que não há resposta suficiente.

## Rota até o atendimento (grafos e Dijkstra)

O arquivo `data/mapa.json` descreve bairros e postos de atendimento (os **nós**) e as ruas entre eles, com distâncias em km (as **arestas com peso**). O mapa atual é **fictício**. O `src/grafo.py` monta o grafo como lista de adjacência (`{local: {vizinho: distância}}`) e usa o **algoritmo de Dijkstra**, com fila de prioridade (`heapq`), para achar o posto mais próximo do bairro escolhido e o caminho até ele.

- As distâncias não podem ser negativas: o Dijkstra exige isso, e o programa confere ao carregar o mapa.
- Se nenhum posto for alcançável, o sistema avisa em vez de quebrar.
- Em caso de empate na distância, vale o primeiro posto da lista.

## Estratégias de resposta

PREENCHER: sempre citar fonte e data, aviso de resposta insuficiente e, opcionalmente, prompts para um LLM (`src/llm.py`).

## Estrutura do projeto

```text
├── data/
│   ├── base.json       # base de conhecimento
│   └── mapa.json       # bairros, postos e distâncias (grafo)
├── docs/               # relatorio.pdf, link_video.txt, uso_ia.md
├── src/
│   ├── main.py         # programa principal (menu)
│   ├── base.py         # leitura e validação da base
│   ├── busca.py        # busca por palavras-chave
│   ├── grafo.py        # grafo do mapa + Dijkstra
│   ├── avaliacao.py    # métricas de desempenho da busca
│   └── llm.py          # extensão opcional para LLM
└── tests/              # testes com pytest + perguntas_avaliacao.json
```

## Como rodar

Requer Python 3.13 (testado no Windows com PowerShell).

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows (PowerShell)
source .venv/bin/activate           # Linux / macOS / Git Bash

# 2. Instalar as dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Rodar o assistente
python src/main.py

# 4. Gerar as métricas da busca
python src/avaliacao.py
```

### Qualidade (rodar antes de cada commit)

```bash
black src tests                        # formatação
pylint --disable=R,C src               # lint
python -m pytest -v --cov=src tests    # testes + cobertura
```

> Use `python -m pytest` (e não só `pytest`), a partir da raiz do projeto, para o import de `src` funcionar.

## Testes e métricas

**Testes automatizados** (`python -m pytest -v --cov=src tests`): base, busca, grafo/Dijkstra, métricas e tratamento de entradas inválidas.

**Métricas da busca** (`python src/avaliacao.py`): roda as perguntas de `tests/perguntas_avaliacao.json`, cada uma com o `id` da orientação esperada (`null` quando o sistema **não** deve responder).

| Métrica | O que mede |
|---|---|
| Acurácia geral | % de casos em que o resultado foi o esperado |
| Acerto (com resposta) | % de perguntas respondíveis que trouxeram a orientação certa |
| Recusa correta | % de perguntas fora da base em que o sistema avisou que não há resposta |
| Respostas erradas | Quantas vezes respondeu algo errado (o pior erro, porque informa mal o cidadão) |
| Tempo médio por busca | Desempenho, em milissegundos |

PREENCHER: resultados finais com a base completa.

## Vídeo

PREENCHER (o mesmo link de `docs/link_video.txt`).

## Regras do projeto

- Toda orientação da base tem **fonte oficial e data de verificação**. Sem fonte, não entra.
- Toda função nova em `src/` ganha pelo menos um teste em `tests/`.
- Nova dependência → adicionar ao `requirements.txt`.
- Chaves de API ficam só no `.env` (modelo em `.env.example`), **nunca** no Git.
- Rodar formatação, lint e testes antes de cada commit.
- Uso de IA no desenvolvimento → registrar em `docs/uso_ia.md`.

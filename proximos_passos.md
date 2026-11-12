# Próximos passos: Citizen Assist AI

Atualizado em 2026-11-12. Nenhum commit feito ainda: todos os arquivos abaixo estão só no computador.

## O que já foi feito

### Estrutura (scaffold)
- Repositório `fiap-project-globalsolution2026` clonado em `C:\DEV\GitHub\fiap-project-globalsolution2026` (fora do repositório `fiap-project-aurorasiger`, para não haver um repositório Git dentro de outro).
- Ambiente virtual `.venv` criado (Python 3.13.7) e dependências instaladas. A `.venv` já é ignorada pelo `.gitignore`.
- Diferenças em relação ao roteiro padrão de scaffold:
  - Sem `notebooks/`, `models/`, `reports/`, `data/raw/` e `data/processed/`, porque a entrega não pede essas pastas.
  - Com `docs/`, porque a entrega exige.
  - Sem regras de dados no `.gitignore`, porque o `data/base.json` precisa ir para o GitHub.
- Comandos documentados só no README (sem Makefile, porque o `make` não está instalado no Windows). VS Code ainda não configurado.

### Arquivos criados

| Arquivo | O que faz | Situação |
|---|---|---|
| `README.md` | Todas as seções exigidas pela entrega | Estrutura pronta, com campos **PREENCHER** |
| `src/main.py` | Menu: tema, pergunta livre, posto mais próximo, entrada inválida | Funcionando |
| `src/base.py` | Lê `data/base.json` e confere os campos obrigatórios | Funcionando |
| `src/busca.py` | Normaliza o texto (sem acentos/maiúsculas) e pontua por palavra-chave, com limiar mínimo | Funcionando (versão simples) |
| `src/grafo.py` | Grafo do mapa + algoritmo de Dijkstra (posto mais próximo e caminho) | Funcionando |
| `src/avaliacao.py` | Métricas da busca: acurácia, acerto, recusa correta, respostas erradas, tempo médio | Funcionando |
| `src/llm.py` | Ponto de extensão opcional para um LLM | Só devolve o texto da base (sem API) |
| `data/base.json` | Base de conhecimento | **3 entradas de exemplo**, fonte fictícia |
| `data/mapa.json` | 5 bairros, 2 postos, 8 ruas com distâncias | **Fictício** |
| `tests/perguntas_avaliacao.json` | Perguntas com a resposta esperada | 6 casos de exemplo |
| `tests/test_*.py` | Testes de base, busca, grafo, avaliação e menu (main) | 25 testes passando |
| `docs/link_video.txt` | Link do vídeo | Placeholder |
| `docs/uso_ia.md` | Registro do uso de IA | Modelo a preencher |
| `.env.example` | Modelo da chave do LLM opcional | Pronto |
| `requirements.txt` | pytest, pytest-cov, black, pylint (o sistema usa só o Python padrão) | Pronto |

### Situação da qualidade (última execução)
- `black`: tudo formatado.
- `pylint --disable=R,C src`: nota 10/10.
- `python -m pytest -v --cov=src tests`: 25 testes passando, 71% de cobertura (o que falta é quase todo o menu interativo de `main.py`).
- `python src/avaliacao.py`: 100% de acerto nos 6 casos de exemplo, 0,03 ms por busca.

### Como rodar
```bash
.venv\Scripts\Activate.ps1
python src/main.py           # assistente
python src/avaliacao.py      # métricas
python -m pytest -v --cov=src tests
```

## Próximos passos

### Conteúdo (prioridade alta)
- [ ] Definir o **tema** e o **público** do assistente (preencher "Público e escopo" no README).
- [ ] Montar a base real: **mínimo 15 orientações** em `data/base.json`, cada uma com fonte oficial (`nome`, `url`) e `data_verificacao`. Apagar as 3 entradas de exemplo.
- [ ] Decidir o mapa: **locais reais** (postos de uma cidade, distâncias tiradas de um mapa) ou **mapa ilustrativo**. Se for ilustrativo, deixar isso escrito no README e no relatório.
- [ ] Ampliar `tests/perguntas_avaliacao.json`: pelo menos 2 perguntas por orientação, mais várias perguntas fora do escopo (`id_esperado: null`).

### Código
- [ ] **Melhorar a busca.** Hoje só reconhece palavras-chave exatas ("tirar RG de novo" falha). Ideias: comparar por palavras em comum com a pergunta, sinônimos, remover palavras sem valor ("de", "o", "como").
- [ ] **Comparar algoritmos de busca** com `src/avaliacao.py` (versão atual × versão melhorada), para o item "busca e comparação de algoritmos".
- [ ] Ajustar o `LIMIAR_MINIMO` com base nas métricas (equilíbrio entre responder errado e recusar demais).
- [ ] (Opcional) Integrar um LLM em `src/llm.py`: cadeia de prompts, saída estruturada em JSON e regra de usar **só** o conteúdo da base. Chave no `.env`.
- [ ] (Opcional) Aumentar a cobertura de testes do menu em `main.py`.

### Entrega
- [ ] README: equipe e RMs, fontes, estratégias de resposta, resultados finais das métricas, link do vídeo.
- [ ] `docs/relatorio.pdf` (4 a 8 páginas): problema, público, arquitetura, fontes, estratégias de prompts, resultados de testes, indicadores, limitações e impacto social.
- [ ] Gravar o vídeo e colocar o link em `docs/link_video.txt` e no README.
- [ ] `docs/uso_ia.md`: ferramentas, prompts testados e validação crítica das respostas.

### Git
- [ ] Primeiro commit e push ("Estrutura inicial do projeto (scaffold)").
- [ ] Conferir no GitHub que a `.venv` e o `.env` **não** subiram.
- [ ] Combinar com a equipe como cada um vai contribuir (branches ou commits direto na `main`).

### Para depois
- [ ] Configurar o VS Code (`.vscode/settings.json`: usar a `.venv`, black ao salvar, testes na aba de testes).
- [ ] Fixar as versões das dependências (`pip freeze > requirements.txt`).
- [ ] Integração contínua: rodar lint e testes no GitHub a cada push.

## Prompt para retomar no Claude Code

Copie o bloco abaixo e cole no Claude Code ao abrir a pasta do projeto:

````text
Estou retomando o projeto Citizen Assist AI (FIAP Global Solution 2026, trabalho em grupo).
Responda sempre em português. Se tiver qualquer dúvida, pergunte ANTES de criar ou alterar arquivos.
NÃO faça commits nem push sem eu pedir. NÃO configure o VS Code ainda.

## Contexto do desafio
Criar um assistente que organiza informações verificadas e responde consultas simples do cotidiano.
O usuário escolhe um tema ou digita uma pergunta; o sistema localiza a orientação na base de
conhecimento, cita a fonte associada e avisa quando não houver resposta suficiente.
Conteúdos da disciplina a contemplar: estruturas de dados (listas, tuplas, dicionários), arquivos
TXT/JSON, lógica booleana e De Morgan, grafos e Dijkstra, busca e comparação de algoritmos,
avaliação de desempenho e métricas, prompts inteligentes, cadeias de prompts e saídas estruturadas,
chatbots e assistentes virtuais, noções de regressão, limites e derivadas, mapas de Karnaugh.

## Entregáveis exigidos
- README.md: equipe e RMs; público e escopo; fontes consultadas; base de conhecimento; busca;
  estratégias de resposta; testes, métricas e instruções de execução; link do vídeo.
- src/main.py: programa funcional e comentado (consulta, referências, navegação, entradas inválidas).
- data/base.json: mínimo 15 orientações, com perguntas/palavras-chave, fontes e datas de verificação.
- docs/relatorio.pdf: 4 a 8 páginas (problema, público, arquitetura, fontes, estratégias de prompts,
  resultados de testes, indicadores, limitações, impacto social).
- docs/link_video.txt: link completo do vídeo no YouTube.
- docs/uso_ia.md: ferramentas de IA, prompts testados e validação crítica das respostas.

## Decisões já tomadas
- Pasta do projeto: C:\DEV\GitHub\fiap-project-globalsolution2026
  (repo https://github.com/renatolvalle/fiap-project-globalsolution2026), fora do repo aurorasiger.
- Python 3.13, ambiente virtual .venv dentro do projeto (já criado e com dependências instaladas).
- O sistema usa só a biblioteca padrão; requirements.txt tem só pytest, pytest-cov, black, pylint.
- Busca local na base JSON + LLM OPCIONAL (src/llm.py, chave no .env, provedor ainda não escolhido).
- Base com entradas genéricas de exemplo por enquanto; o tema real ainda não foi definido.
- Grafo/Dijkstra usado para a "rota até o posto de atendimento mais próximo" (data/mapa.json, fictício).
- Métricas da busca via perguntas com resposta esperada (tests/perguntas_avaliacao.json).
- Sem Makefile: comandos ficam só no README.
- Estrutura proporcional: sem notebooks/, models/, reports/, data/raw/ e data/processed/.

## O que já existe
- src/main.py: menu (1 tema, 2 pergunta livre, 3 posto mais próximo, 0 sair), ler_opcao valida entradas.
- src/base.py: carregar_base, validar_orientacao, listar_temas.
- src/busca.py: normalizar (sem acentos/minúsculas), pontuar por palavra-chave, buscar com LIMIAR_MINIMO,
  filtrar_por_tema.
- src/grafo.py: carregar_mapa (valida distâncias não negativas), montar_grafo, dijkstra (heapq),
  reconstruir_caminho, posto_mais_proximo.
- src/avaliacao.py: acurácia, acerto com resposta, recusa correta, respostas erradas, tempo médio.
- src/llm.py: stub (llm_disponivel, reformular devolve o texto da base).
- Testes: tests/test_base.py, test_busca.py, test_grafo.py, test_avaliacao.py, test_main.py
  (25 passando, 71% de cobertura, pylint 10/10).
- README.md com todas as seções (campos PREENCHER), docs/uso_ia.md e docs/link_video.txt como modelos,
  .env.example, proximos_passos.md (checklist completo).

## Comandos
- Rodar: python src/main.py   |   Métricas: python src/avaliacao.py
- Qualidade: black src tests ; pylint --disable=R,C src ; python -m pytest -v --cov=src tests
  (usar python -m pytest, não só pytest, por causa do import de src)

## Próximo passo
Leia proximos_passos.md e o README.md, rode os testes para confirmar que está tudo funcionando
e me pergunte por qual item do checklist quer começar.
````

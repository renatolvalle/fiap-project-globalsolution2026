"""Citizen Assist AI: programa principal (menu no terminal).

Como rodar, a partir da raiz do projeto:
    python src/main.py
"""

import sys
from pathlib import Path

# Permite rodar como script (python src/main.py) e ainda importar "src.xxx".
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.base import carregar_base, listar_temas
from src.busca import buscar, filtrar_por_tema
from src.grafo import carregar_mapa, montar_grafo, posto_mais_proximo
from src.llm import reformular

MSG_SEM_RESPOSTA = (
    "Não encontrei uma orientação suficiente para essa pergunta na base verificada. "
    "Procure o canal oficial do órgão responsável."
)


def formatar_resposta(orientacao: dict, pergunta: str = "") -> str:
    """Monta o texto da resposta sempre com a fonte e a data de verificação."""
    fonte = orientacao["fonte"]
    return (
        f"\n{reformular(pergunta, orientacao)}\n"
        f"Fonte: {fonte['nome']} ({fonte['url']})\n"
        f"Verificado em: {orientacao['data_verificacao']}\n"
    )


def ler_opcao(mensagem: str, opcoes_validas: range) -> int:
    """Pede um número até o usuário digitar uma opção válida."""
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit() and int(entrada) in opcoes_validas:
            return int(entrada)
        print("Opção inválida. Digite um dos números do menu.")


def menu_temas(orientacoes: list[dict]) -> None:
    """Navegação por tema: escolhe o tema e depois a pergunta."""
    temas = listar_temas(orientacoes)
    print("\nTemas disponíveis:")
    for i, tema in enumerate(temas, start=1):
        print(f"  {i}. {tema}")
    print("  0. Voltar")
    escolha = ler_opcao("Escolha um tema: ", range(0, len(temas) + 1))
    if escolha == 0:
        return

    itens = filtrar_por_tema(temas[escolha - 1], orientacoes)
    for i, item in enumerate(itens, start=1):
        print(f"  {i}. {item['pergunta']}")
    print("  0. Voltar")
    escolha = ler_opcao("Escolha uma pergunta: ", range(0, len(itens) + 1))
    if escolha != 0:
        print(formatar_resposta(itens[escolha - 1]))


def menu_pergunta(orientacoes: list[dict]) -> None:
    """Pergunta livre: busca por palavras-chave na base."""
    pergunta = input("\nDigite sua pergunta: ")
    resultado = buscar(pergunta, orientacoes)
    print(
        formatar_resposta(resultado, pergunta)
        if resultado
        else f"\n{MSG_SEM_RESPOSTA}\n"
    )


def menu_rota(mapa: dict) -> None:
    """Rota até o posto de atendimento mais próximo (Dijkstra)."""
    nomes = {local["id"]: local["nome"] for local in mapa["locais"]}
    bairros = [l["id"] for l in mapa["locais"] if l["tipo"] == "bairro"]
    postos = [l["id"] for l in mapa["locais"] if l["tipo"] == "posto"]

    print("\nOnde você está?")
    for i, bairro in enumerate(bairros, start=1):
        print(f"  {i}. {nomes[bairro]}")
    print("  0. Voltar")
    escolha = ler_opcao("Escolha o local: ", range(0, len(bairros) + 1))
    if escolha == 0:
        return

    resultado = posto_mais_proximo(montar_grafo(mapa), bairros[escolha - 1], postos)
    if resultado is None:
        print("\nNenhum posto de atendimento alcançável a partir desse local.\n")
        return
    posto, distancia, caminho = resultado
    print(f"\nPosto mais próximo: {nomes[posto]} ({distancia:.1f} {mapa['unidade']})")
    print("Caminho: " + " -> ".join(nomes[no] for no in caminho) + "\n")


def main() -> None:
    """Laço principal do menu."""
    orientacoes = carregar_base()
    mapa = carregar_mapa()
    print("=== Citizen Assist AI ===")
    while True:
        print(
            "1. Escolher um tema\n2. Fazer uma pergunta\n"
            "3. Posto de atendimento mais próximo\n0. Sair"
        )
        opcao = ler_opcao("Opção: ", range(0, 4))
        if opcao == 1:
            menu_temas(orientacoes)
        elif opcao == 2:
            menu_pergunta(orientacoes)
        elif opcao == 3:
            menu_rota(mapa)
        else:
            print("Até logo!")
            break


if __name__ == "__main__":
    main()

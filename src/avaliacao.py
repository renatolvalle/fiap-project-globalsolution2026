"""Avaliação de desempenho da busca: roda perguntas com resposta esperada e calcula métricas.

Como rodar, a partir da raiz do projeto:
    python src/avaliacao.py
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.base import carregar_base
from src.busca import buscar

CAMINHO_CASOS = (
    Path(__file__).resolve().parent.parent / "tests" / "perguntas_avaliacao.json"
)


def carregar_casos(caminho: Path = CAMINHO_CASOS) -> list[dict]:
    """Cada caso: {"pergunta": str, "id_esperado": int ou null (null = não deve responder)}."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)["casos"]


def avaliar(casos: list[dict], orientacoes: list[dict]) -> dict:
    """Calcula acurácia, acerto com resposta, recusa correta, respostas erradas e tempo médio."""
    acertos = respostas_erradas = 0
    com_resposta = acertos_com_resposta = 0
    sem_resposta = recusas_corretas = 0
    erros = []
    tempo_total = 0.0

    for caso in casos:
        inicio = time.perf_counter()
        resultado = buscar(caso["pergunta"], orientacoes)
        tempo_total += time.perf_counter() - inicio

        obtido = resultado["id"] if resultado else None
        esperado = caso["id_esperado"]
        acertou = obtido == esperado

        # Respondeu errado = respondeu algo E não era o esperado.
        # Por De Morgan, é o mesmo que: not (obtido is None or acertou).
        if obtido is not None and not acertou:
            respostas_erradas += 1

        if esperado is None:
            sem_resposta += 1
            recusas_corretas += acertou
        else:
            com_resposta += 1
            acertos_com_resposta += acertou

        acertos += acertou
        if not acertou:
            erros.append({**caso, "id_obtido": obtido})

    total = len(casos)
    return {
        "total": total,
        "acuracia": acertos / total if total else 0.0,
        "acerto_com_resposta": (
            acertos_com_resposta / com_resposta if com_resposta else 0.0
        ),
        "recusa_correta": recusas_corretas / sem_resposta if sem_resposta else 0.0,
        "respostas_erradas": respostas_erradas,
        "tempo_medio_ms": (tempo_total / total * 1000) if total else 0.0,
        "erros": erros,
    }


def imprimir_relatorio(metricas: dict) -> None:
    """Mostra as métricas no terminal."""
    print("=== Avaliação da busca ===")
    print(f"Casos avaliados:              {metricas['total']}")
    print(f"Acurácia geral:               {metricas['acuracia']:.0%}")
    print(f"Acerto (com resposta):        {metricas['acerto_com_resposta']:.0%}")
    print(f"Recusa correta (sem resposta): {metricas['recusa_correta']:.0%}")
    print(f"Respostas erradas:            {metricas['respostas_erradas']}")
    print(f"Tempo médio por busca:        {metricas['tempo_medio_ms']:.3f} ms")
    for erro in metricas["erros"]:
        print(
            f"  ERRO: '{erro['pergunta']}' esperado={erro['id_esperado']} obtido={erro['id_obtido']}"
        )


if __name__ == "__main__":
    imprimir_relatorio(avaliar(carregar_casos(), carregar_base()))

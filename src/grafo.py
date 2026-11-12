"""Mapa de atendimento como grafo e caminho mais curto com o algoritmo de Dijkstra."""

import heapq
import json
import math
from pathlib import Path

CAMINHO_MAPA = Path(__file__).resolve().parent.parent / "data" / "mapa.json"


def carregar_mapa(caminho: Path = CAMINHO_MAPA) -> dict:
    """Lê o mapa (locais e ligações) e confere se as distâncias são válidas."""
    with open(caminho, encoding="utf-8") as arquivo:
        mapa = json.load(arquivo)
    ids = {local["id"] for local in mapa["locais"]}
    for ligacao in mapa["ligacoes"]:
        if ligacao["de"] not in ids or ligacao["para"] not in ids:
            raise ValueError(f"Ligação com local inexistente: {ligacao}")
        # Dijkstra só funciona com pesos não negativos.
        if ligacao["distancia"] < 0:
            raise ValueError(f"Distância negativa: {ligacao}")
    return mapa


def montar_grafo(mapa: dict) -> dict[str, dict[str, float]]:
    """Lista de adjacência: {local: {vizinho: distancia}}. As ruas valem nos dois sentidos."""
    grafo = {local["id"]: {} for local in mapa["locais"]}
    for ligacao in mapa["ligacoes"]:
        grafo[ligacao["de"]][ligacao["para"]] = ligacao["distancia"]
        grafo[ligacao["para"]][ligacao["de"]] = ligacao["distancia"]
    return grafo


def dijkstra(grafo: dict, origem: str) -> tuple[dict, dict]:
    """Menor distância da origem até cada local, e o local anterior em cada caminho."""
    distancias = {no: math.inf for no in grafo}
    anteriores = {}
    distancias[origem] = 0
    fila = [(0, origem)]  # fila de prioridade: (distância acumulada, local)
    visitados = set()

    while fila:
        dist_atual, no = heapq.heappop(fila)
        if no in visitados:
            continue
        visitados.add(no)
        for vizinho, peso in grafo[no].items():
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                anteriores[vizinho] = no
                heapq.heappush(fila, (nova_dist, vizinho))
    return distancias, anteriores


def reconstruir_caminho(anteriores: dict, origem: str, destino: str) -> list[str]:
    """Volta pelos 'anteriores' do destino até a origem. Lista vazia se não há caminho."""
    if destino != origem and destino not in anteriores:
        return []
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anteriores[caminho[-1]])
    return caminho[::-1]


def posto_mais_proximo(grafo: dict, origem: str, postos: list[str]):
    """Devolve (posto, distancia, caminho) do posto mais próximo, ou None se nenhum for alcançável."""
    distancias, anteriores = dijkstra(grafo, origem)
    alcancaveis = [p for p in postos if distancias[p] != math.inf]
    if not alcancaveis:
        return None
    melhor = min(alcancaveis, key=lambda p: distancias[p])
    return melhor, distancias[melhor], reconstruir_caminho(anteriores, origem, melhor)

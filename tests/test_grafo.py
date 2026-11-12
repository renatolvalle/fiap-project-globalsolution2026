import math

import pytest

from src.grafo import (
    carregar_mapa,
    dijkstra,
    montar_grafo,
    posto_mais_proximo,
    reconstruir_caminho,
)

# A --1-- B --1-- C,  A --5-- C,  D isolado
GRAFO_TESTE = {
    "A": {"B": 1, "C": 5},
    "B": {"A": 1, "C": 1},
    "C": {"A": 5, "B": 1},
    "D": {},
}


def test_dijkstra_prefere_caminho_mais_curto_com_mais_paradas():
    distancias, anteriores = dijkstra(GRAFO_TESTE, "A")
    assert distancias["C"] == 2
    assert reconstruir_caminho(anteriores, "A", "C") == ["A", "B", "C"]


def test_local_inalcancavel():
    distancias, anteriores = dijkstra(GRAFO_TESTE, "A")
    assert distancias["D"] == math.inf
    assert reconstruir_caminho(anteriores, "A", "D") == []


def test_caminho_para_a_propria_origem():
    _, anteriores = dijkstra(GRAFO_TESTE, "A")
    assert reconstruir_caminho(anteriores, "A", "A") == ["A"]


def test_posto_mais_proximo():
    assert posto_mais_proximo(GRAFO_TESTE, "A", ["C", "D"]) == ("C", 2, ["A", "B", "C"])


def test_nenhum_posto_alcancavel():
    assert posto_mais_proximo(GRAFO_TESTE, "A", ["D"]) is None


def test_mapa_real_carrega_e_grafo_e_simetrico():
    grafo = montar_grafo(carregar_mapa())
    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            assert grafo[vizinho][no] == peso


def test_mapa_com_distancia_negativa(tmp_path):
    arquivo = tmp_path / "mapa.json"
    arquivo.write_text(
        '{"locais": [{"id": "a"}, {"id": "b"}],'
        ' "ligacoes": [{"de": "a", "para": "b", "distancia": -1}]}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        carregar_mapa(arquivo)

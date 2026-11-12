import pytest

from src.busca import buscar, filtrar_por_tema, normalizar

BASE_TESTE = [
    {"id": 1, "tema": "Docs", "palavras_chave": ["segunda via", "documento"]},
    {"id": 2, "tema": "Saúde", "palavras_chave": ["vacina", "posto"]},
]


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("  Vacinação  ", "vacinacao"),
        ("SEGUNDA Via", "segunda via"),
        ("", ""),
    ],
)
def test_normalizar(entrada, esperado):
    assert normalizar(entrada) == esperado


def test_buscar_encontra_melhor_orientacao():
    assert buscar("Como tiro a segunda via do documento?", BASE_TESTE)["id"] == 1


def test_buscar_ignora_acentos_e_maiusculas():
    assert buscar("Onde fica o POSTO de VACINA?", BASE_TESTE)["id"] == 2


@pytest.mark.parametrize("pergunta", ["", "   ", "qual a previsão do tempo?"])
def test_buscar_sem_resposta_suficiente(pergunta):
    assert buscar(pergunta, BASE_TESTE) is None


def test_filtrar_por_tema():
    assert [item["id"] for item in filtrar_por_tema("Saúde", BASE_TESTE)] == [2]

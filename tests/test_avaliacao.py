from src.avaliacao import avaliar, carregar_casos
from src.base import carregar_base

BASE_TESTE = [
    {"id": 1, "palavras_chave": ["vacina"]},
    {"id": 2, "palavras_chave": ["documento"]},
]


def test_metricas_casos_mistos():
    casos = [
        {"pergunta": "onde tomo vacina?", "id_esperado": 1},  # acerto
        {"pergunta": "vacina", "id_esperado": 2},  # resposta errada
        {"pergunta": "previsão do tempo", "id_esperado": None},  # recusa correta
        {"pergunta": "documento", "id_esperado": None},  # deveria recusar
    ]
    metricas = avaliar(casos, BASE_TESTE)
    assert metricas["total"] == 4
    assert metricas["acuracia"] == 0.5
    assert metricas["acerto_com_resposta"] == 0.5
    assert metricas["recusa_correta"] == 0.5
    assert metricas["respostas_erradas"] == 2
    assert len(metricas["erros"]) == 2


def test_lista_vazia_nao_quebra():
    assert avaliar([], BASE_TESTE)["acuracia"] == 0.0


def test_casos_apontam_para_ids_da_base():
    ids = {item["id"] for item in carregar_base()}
    for caso in carregar_casos():
        assert caso["id_esperado"] is None or caso["id_esperado"] in ids

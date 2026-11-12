import pytest

from src.base import carregar_base, listar_temas, validar_orientacao


def test_base_carrega_e_tem_campos():
    orientacoes = carregar_base()
    assert len(orientacoes) > 0


def test_ids_unicos():
    ids = [item["id"] for item in carregar_base()]
    assert len(ids) == len(set(ids))


def test_validar_orientacao_incompleta():
    with pytest.raises(ValueError):
        validar_orientacao({"id": 99, "tema": "X"})


def test_listar_temas_sem_repeticao():
    orientacoes = [{"tema": "B"}, {"tema": "A"}, {"tema": "B"}]
    assert listar_temas(orientacoes) == ["A", "B"]

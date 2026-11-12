"""Leitura e validação da base de conhecimento (data/base.json)."""

import json
from pathlib import Path

# Caminho padrão da base, calculado a partir deste arquivo (funciona de qualquer pasta).
CAMINHO_BASE = Path(__file__).resolve().parent.parent / "data" / "base.json"

# Campos que toda orientação precisa ter.
CAMPOS_OBRIGATORIOS = (
    "id",
    "tema",
    "pergunta",
    "palavras_chave",
    "orientacao",
    "fonte",
    "data_verificacao",
)


def carregar_base(caminho: Path = CAMINHO_BASE) -> list[dict]:
    """Lê o JSON e devolve a lista de orientações já validada."""
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    orientacoes = dados["orientacoes"]
    for item in orientacoes:
        validar_orientacao(item)
    return orientacoes


def validar_orientacao(item: dict) -> None:
    """Levanta ValueError se faltar algum campo obrigatório."""
    faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in item]
    if faltando:
        raise ValueError(f"Orientação {item.get('id', '?')} sem os campos: {faltando}")


def listar_temas(orientacoes: list[dict]) -> list[str]:
    """Devolve os temas sem repetição, em ordem alfabética."""
    return sorted({item["tema"] for item in orientacoes})

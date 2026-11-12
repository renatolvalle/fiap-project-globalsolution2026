"""Busca de orientações na base por palavras-chave."""

import unicodedata

# Pontuação mínima para considerar que existe resposta suficiente.
LIMIAR_MINIMO = 1


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos e sem espaços extras."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return " ".join(sem_acento.lower().split())


def pontuar(pergunta: str, item: dict) -> int:
    """Conta quantas palavras-chave da orientação aparecem na pergunta."""
    pergunta_norm = normalizar(pergunta)
    return sum(
        1 for chave in item["palavras_chave"] if normalizar(chave) in pergunta_norm
    )


def buscar(pergunta: str, orientacoes: list[dict]) -> dict | None:
    """Devolve a orientação com maior pontuação, ou None se nenhuma atingir o limiar."""
    if not pergunta.strip():
        return None
    melhor = max(orientacoes, key=lambda item: pontuar(pergunta, item), default=None)
    if melhor is None or pontuar(pergunta, melhor) < LIMIAR_MINIMO:
        return None
    return melhor


def filtrar_por_tema(tema: str, orientacoes: list[dict]) -> list[dict]:
    """Devolve as orientações de um tema."""
    return [item for item in orientacoes if item["tema"] == tema]

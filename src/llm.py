"""Ponto de extensão OPCIONAL para um modelo de linguagem (LLM).

Por enquanto não chama nenhuma API: o sistema funciona só com a busca local.
Quando a equipe escolher um provedor, a chave fica no arquivo .env (nunca no Git).
"""

import os


def llm_disponivel() -> bool:
    """True se houver uma chave de API configurada no ambiente."""
    return bool(os.getenv("LLM_API_KEY"))


def reformular(pergunta: str, orientacao: dict) -> str:
    """Devolve o texto da orientação. Futuro: pedir ao LLM uma resposta mais natural,
    usando SOMENTE o conteúdo da orientação (para não inventar informação)."""
    _ = pergunta  # será usada no prompt quando o LLM for integrado
    return orientacao["orientacao"]

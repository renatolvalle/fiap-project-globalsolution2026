from src.main import formatar_resposta, ler_opcao

ORIENTACAO = {
    "orientacao": "Texto da orientação.",
    "fonte": {"nome": "Órgão X", "url": "https://x.gov.br"},
    "data_verificacao": "2026-11-12",
}


def test_resposta_sempre_cita_fonte_e_data():
    texto = formatar_resposta(ORIENTACAO)
    assert "Órgão X" in texto and "https://x.gov.br" in texto and "2026-11-12" in texto


def test_ler_opcao_repete_ate_entrada_valida(monkeypatch, capsys):
    entradas = iter(["abc", "9", "", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    assert ler_opcao("Opção: ", range(0, 3)) == 2
    assert capsys.readouterr().out.count("Opção inválida") == 3

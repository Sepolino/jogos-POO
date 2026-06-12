import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.core import Jogador, Jogada, Tabuleiro
from src.core.regra import (
    RegraDestinoDentroDoTabuleiro,
    RegraDestinoDentroDoTabuleiroVazio,
    ConjuntoDeRegras,
)


# ------------------------------------------------------------------
# Tabuleiro
# ------------------------------------------------------------------

class TestTabuleiro:
    def test_criacao(self):
        t = Tabuleiro(3, 3)
        assert t.linhas == 3
        assert t.colunas == 3

    def test_celula_inicial_vazia(self):
        t = Tabuleiro(3, 3)
        assert t.celula_vazia(0, 0)
        assert t.obter_celula(1, 1) is None

    def test_definir_e_obter_celula(self):
        t = Tabuleiro(3, 3)
        t.definir_celula(0, 0, "X")
        assert t.obter_celula(0, 0) == "X"
        assert not t.celula_vazia(0, 0)

    def test_posicao_invalida_levanta_excecao(self):
        t = Tabuleiro(3, 3)
        with pytest.raises(ValueError):
            t.obter_celula(5, 5)

    def test_posicao_valida(self):
        t = Tabuleiro(3, 3)
        assert t.posicao_valida(0, 0)
        assert t.posicao_valida(2, 2)
        assert not t.posicao_valida(-1, 0)
        assert not t.posicao_valida(3, 3)

    def test_esta_cheio(self):
        t = Tabuleiro(2, 2)
        assert not t.esta_cheio()
        t.definir_celula(0, 0, "X")
        t.definir_celula(0, 1, "O")
        t.definir_celula(1, 0, "X")
        t.definir_celula(1, 1, "O")
        assert t.esta_cheio()

    def test_limpar(self):
        t = Tabuleiro(3, 3)
        t.definir_celula(0, 0, "X")
        t.limpar()
        assert t.celula_vazia(0, 0)

    def test_diagonal_principal(self):
        t = Tabuleiro(3, 3)
        t.definir_celula(0, 0, "X")
        t.definir_celula(1, 1, "X")
        t.definir_celula(2, 2, "X")
        diag = t.obter_diagonal_principal()
        assert diag == ["X", "X", "X"]

    def test_diagonal_secundaria(self):
        t = Tabuleiro(3, 3)
        t.definir_celula(0, 2, "O")
        t.definir_celula(1, 1, "O")
        t.definir_celula(2, 0, "O")
        diag = t.obter_diagonal_secundaria()
        assert diag == ["O", "O", "O"]

    def test_grade_retorna_copia(self):
        t = Tabuleiro(3, 3)
        t.definir_celula(0, 0, "X")
        grade = t.grade
        grade[0][0] = "MODIFICADO"
        assert t.obter_celula(0, 0) == "X"


# ------------------------------------------------------------------
# Jogador
# ------------------------------------------------------------------

class TestJogador:
    def test_criacao(self):
        j = Jogador("Alice", "X")
        assert j.nome == "Alice"
        assert j.simbolo == "X"

    def test_placar_inicial(self):
        j = Jogador("Bob", "O")
        assert j.vitorias == 0
        assert j.derrotas == 0
        assert j.empates == 0

    def test_registrar_vitoria(self):
        j = Jogador("Alice", "X")
        j.registrar_vitoria()
        j.registrar_vitoria()
        assert j.vitorias == 2

    def test_igualdade(self):
        j1 = Jogador("Alice", "X")
        j2 = Jogador("Alice", "X")
        j3 = Jogador("Bob", "O")
        assert j1 == j2
        assert j1 != j3


# ------------------------------------------------------------------
# Regras
# ------------------------------------------------------------------

class TestRegras:
    def setup_method(self):
        self.tabuleiro = Tabuleiro(3, 3)
        self.jogador = Jogador("A", "X")

    def test_regra_dentro_do_tabuleiro_valida(self):
        regra = RegraDestinoDentroDoTabuleiro()
        jogada = Jogada(jogador=self.jogador, linha_destino=1, coluna_destino=1)
        valido, _ = regra.validar(jogada, self.tabuleiro)
        assert valido

    def test_regra_fora_do_tabuleiro_invalida(self):
        regra = RegraDestinoDentroDoTabuleiro()
        jogada = Jogada(jogador=self.jogador, linha_destino=5, coluna_destino=5)
        valido, motivo = regra.validar(jogada, self.tabuleiro)
        assert not valido
        assert motivo != ""

    def test_regra_celula_vazia_invalida_quando_ocupada(self):
        self.tabuleiro.definir_celula(0, 0, "X")
        regra = RegraDestinoDentroDoTabuleiroVazio()
        jogada = Jogada(jogador=self.jogador, linha_destino=0, coluna_destino=0)
        valido, _ = regra.validar(jogada, self.tabuleiro)
        assert not valido

    def test_conjunto_de_regras_para_no_primeiro_erro(self):
        conjunto = ConjuntoDeRegras([
            RegraDestinoDentroDoTabuleiro(),
            RegraDestinoDentroDoTabuleiroVazio(),
        ])
        jogada = Jogada(jogador=self.jogador, linha_destino=99, coluna_destino=99)
        valido, _ = conjunto.validar_todas(jogada, self.tabuleiro)
        assert not valido

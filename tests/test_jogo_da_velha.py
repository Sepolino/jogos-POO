import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.core import Jogador, Jogada
from src.jogos import JogoDaVelha


def criar_jogo():
    j1 = Jogador("Alice", "X")
    j2 = Jogador("Bob", "O")
    jogo = JogoDaVelha(j1, j2)
    jogo.iniciar()
    return jogo, j1, j2


class TestJogoDaVelha:

    def test_inicio_tabuleiro_vazio(self):
        jogo, j1, j2 = criar_jogo()
        assert jogo.jogador_atual == j1
        assert not jogo.partida_encerrada

    def test_jogada_valida_aceita(self):
        jogo, j1, j2 = criar_jogo()
        jogada = Jogada(jogador=j1, linha_destino=0, coluna_destino=0)
        aceita = jogo.fazer_jogada(jogada)
        assert aceita

    def test_jogada_fora_do_tabuleiro_rejeitada(self):
        jogo, j1, j2 = criar_jogo()
        jogada = Jogada(jogador=j1, linha_destino=5, coluna_destino=5)
        aceita = jogo.fazer_jogada(jogada)
        assert not aceita

    def test_jogada_em_celula_ocupada_rejeitada(self):
        jogo, j1, j2 = criar_jogo()
        jogada1 = Jogada(jogador=j1, linha_destino=0, coluna_destino=0)
        jogo.fazer_jogada(jogada1)
        jogada2 = Jogada(jogador=j2, linha_destino=0, coluna_destino=0)
        aceita = jogo.fazer_jogada(jogada2)
        assert not aceita

    def test_turno_alterna_apos_jogada_valida(self):
        jogo, j1, j2 = criar_jogo()
        assert jogo.jogador_atual == j1
        jogo.fazer_jogada(Jogada(jogador=j1, linha_destino=0, coluna_destino=0))
        assert jogo.jogador_atual == j2

    def test_jogada_fora_do_turno_rejeitada(self):
        jogo, j1, j2 = criar_jogo()
        jogada = Jogada(jogador=j2, linha_destino=0, coluna_destino=0)
        aceita = jogo.fazer_jogada(jogada)
        assert not aceita

    def test_vitoria_por_linha(self):
        jogo, j1, j2 = criar_jogo()
        # X vence na linha 0
        moves = [
            (j1, 0, 0), (j2, 1, 0),
            (j1, 0, 1), (j2, 1, 1),
            (j1, 0, 2),  # vitória!
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        assert jogo.partida_encerrada
        assert jogo.vencedor == j1

    def test_vitoria_por_coluna(self):
        jogo, j1, j2 = criar_jogo()
        moves = [
            (j1, 0, 0), (j2, 0, 1),
            (j1, 1, 0), (j2, 1, 1),
            (j1, 2, 0),  # vitória coluna 0
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        assert jogo.vencedor == j1

    def test_vitoria_por_diagonal_principal(self):
        jogo, j1, j2 = criar_jogo()
        moves = [
            (j1, 0, 0), (j2, 0, 1),
            (j1, 1, 1), (j2, 0, 2),
            (j1, 2, 2),  # diagonal principal
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        assert jogo.vencedor == j1

    def test_vitoria_por_diagonal_secundaria(self):
        jogo, j1, j2 = criar_jogo()
        moves = [
            (j1, 0, 2), (j2, 0, 0),
            (j1, 1, 1), (j2, 1, 0),
            (j1, 2, 0),  # diagonal secundária
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        assert jogo.vencedor == j1

    def test_empate(self):
        jogo, j1, j2 = criar_jogo()
        # X O X
        # X X O
        # O X O  → empate
        moves = [
            (j1, 0, 0), (j2, 0, 1),
            (j1, 0, 2), (j2, 1, 2),
            (j1, 1, 0), (j2, 2, 0),
            (j1, 1, 1), (j2, 2, 2),
            (j1, 2, 1),
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        assert jogo.partida_encerrada
        assert jogo.vencedor is None

    def test_jogada_apos_fim_rejeitada(self):
        jogo, j1, j2 = criar_jogo()
        moves = [
            (j1, 0, 0), (j2, 1, 0),
            (j1, 0, 1), (j2, 1, 1),
            (j1, 0, 2),
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        # Jogo acabou; tentar jogar de novo
        extra = Jogada(jogador=j2, linha_destino=2, coluna_destino=2)
        aceita = jogo.fazer_jogada(extra)
        assert not aceita

    def test_historico_registra_jogadas(self):
        jogo, j1, j2 = criar_jogo()
        jogo.fazer_jogada(Jogada(jogador=j1, linha_destino=0, coluna_destino=0))
        jogo.fazer_jogada(Jogada(jogador=j2, linha_destino=1, coluna_destino=1))
        assert len(jogo.historico) == 2

    def test_placar_atualizado_apos_vitoria(self):
        jogo, j1, j2 = criar_jogo()
        moves = [
            (j1, 0, 0), (j2, 1, 0),
            (j1, 0, 1), (j2, 1, 1),
            (j1, 0, 2),
        ]
        for jogador, l, c in moves:
            jogo.fazer_jogada(Jogada(jogador=jogador, linha_destino=l, coluna_destino=c))
        assert j1.vitorias == 1
        assert j2.derrotas == 1

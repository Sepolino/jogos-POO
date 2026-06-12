import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.core import Jogador, Jogada
from src.jogos.xadrez_simplificado import XadrezSimplificado, Peao, Torre, Rei


def criar_jogo():
    branco = Jogador("Brancas", "B")
    preto = Jogador("Pretas", "P")
    jogo = XadrezSimplificado(branco, preto)
    jogo.iniciar()
    return jogo, branco, preto


class TestXadrezSimplificado:

    def test_tabuleiro_inicializado_corretamente(self):
        jogo, branco, preto = criar_jogo()
        # Peões brancos na linha 6
        from src.core.tabuleiro import Tabuleiro
        # Verifica via fazer_jogada que peão está na posição inicial
        # (linha 6, col 4 → e2)
        assert not jogo.partida_encerrada

    def test_jogada_valida_peao_branco(self):
        jogo, branco, preto = criar_jogo()
        # Peão em e2 (linha 6, col 4) → e3 (linha 5, col 4)
        jogada = Jogada(
            jogador=branco,
            linha_destino=5, coluna_destino=4,
            linha_origem=6, coluna_origem=4,
        )
        aceita = jogo.fazer_jogada(jogada)
        assert aceita

    def test_jogada_sem_peca_na_origem_rejeitada(self):
        jogo, branco, preto = criar_jogo()
        # Linha 3 está vazia no início
        jogada = Jogada(
            jogador=branco,
            linha_destino=4, coluna_destino=4,
            linha_origem=3, coluna_origem=4,
          
        )
        # Origem vazia → inválido
        jogada2 = Jogada(
            jogador=branco,
            linha_destino=4, coluna_destino=0,
            linha_origem=3, coluna_origem=0,
        )
        aceita = jogo.fazer_jogada(jogada2)
        assert not aceita

    def test_mover_peca_do_adversario_rejeitado(self):
        jogo, branco, preto = criar_jogo()
        # Brancas tentam mover peça preta (linha 1, col 0)
        jogada = Jogada(
            jogador=branco,
            linha_destino=2, coluna_destino=0,
            linha_origem=1, coluna_origem=0,
        )
        aceita = jogo.fazer_jogada(jogada)
        assert not aceita

    def test_jogada_sem_origem_rejeitada(self):
        jogo, branco, preto = criar_jogo()
        jogada = Jogada(jogador=branco, linha_destino=5, coluna_destino=4)
        aceita = jogo.fazer_jogada(jogada)
        assert not aceita

    def test_turno_alterna(self):
        jogo, branco, preto = criar_jogo()
        assert jogo.jogador_atual == branco
        jogada = Jogada(
            jogador=branco,
            linha_destino=5, coluna_destino=4,
            linha_origem=6, coluna_origem=4,
        )
        jogo.fazer_jogada(jogada)
        assert jogo.jogador_atual == preto

    def test_captura_rei_encerra_jogo(self):
        jogo, branco, preto = criar_jogo()
        # Colocar o rei preto em posição acessível e capturá-lo manualmente
        # Usamos acesso interno para montar cenário de teste
        from src.jogos.xadrez_simplificado import Rei as ReiPeca
        tabuleiro = jogo._tabuleiro
        # Limpa e coloca apenas os dois reis + uma torre branca perto
        tabuleiro.limpar()
        tabuleiro.definir_celula(7, 4, ReiPeca(branco))
        tabuleiro.definir_celula(0, 4, ReiPeca(preto))
        tabuleiro.definir_celula(1, 4, Torre(branco))

        # Torre branca captura rei preto
        jogada = Jogada(
            jogador=branco,
            linha_destino=0, coluna_destino=4,
            linha_origem=1, coluna_origem=4,
        )
        jogo.fazer_jogada(jogada)
        assert jogo.partida_encerrada
        assert jogo.vencedor == branco


class TestPecasXadrez:

    def setup_method(self):
        self.branco = Jogador("B", "B")
        self.preto = Jogador("P", "P")

    def test_peao_branco_move_para_cima(self):
        from src.core import Tabuleiro
        t = Tabuleiro(8, 8)
        peao = Peao(self.branco, branco=True)
        t.definir_celula(6, 4, peao)
        movs = peao.movimentos_validos(6, 4, t)
        assert (5, 4) in movs
        assert (7, 4) not in movs  # não volta

    def test_peao_preto_move_para_baixo(self):
        from src.core import Tabuleiro
        t = Tabuleiro(8, 8)
        peao = Peao(self.preto, branco=False)
        t.definir_celula(1, 4, peao)
        movs = peao.movimentos_validos(1, 4, t)
        assert (2, 4) in movs

    def test_torre_move_em_linha_reta(self):
        from src.core import Tabuleiro
        t = Tabuleiro(8, 8)
        torre = Torre(self.branco)
        t.definir_celula(4, 4, torre)
        movs = torre.movimentos_validos(4, 4, t)
        # Deve incluir todas as casas livres na mesma linha e coluna
        assert (4, 0) in movs
        assert (0, 4) in movs
        assert (4, 7) in movs
        assert (7, 4) in movs

    def test_rei_move_uma_casa(self):
        from src.core import Tabuleiro
        t = Tabuleiro(8, 8)
        rei = Rei(self.branco)
        t.definir_celula(4, 4, rei)
        movs = rei.movimentos_validos(4, 4, t)
        esperados = [
            (3, 3), (3, 4), (3, 5),
            (4, 3),         (4, 5),
            (5, 3), (5, 4), (5, 5),
        ]
        for pos in esperados:
            assert pos in movs
        assert len(movs) == 8

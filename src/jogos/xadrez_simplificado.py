from ..core import (
    JogoTabuleiro, Tabuleiro, Jogador, Jogada, Peca,
    Regra, ConjuntoDeRegras, RegraDestinoDentroDoTabuleiro,
)
from typing import Optional


# ======================================================================
# Peças do Xadrez Simplificado
# Cada peça herda de Peca e sobrescreve simbolo + movimentos_validos
# ======================================================================

class Peao(Peca):
    """Peão: move 1 casa para frente (sem captura diagonal, sem en passant)."""

    DIRECOES = {True: -1, False: 1}  # True = brancas (sobem), False = pretas (descem)

    def __init__(self, jogador: Jogador, branco: bool):
        super().__init__(jogador)
        self._branco = branco

    @property
    def simbolo(self) -> str:
        return "♙" if self._branco else "♟"

    def movimentos_validos(self, linha: int, coluna: int, tabuleiro: Tabuleiro) -> list[tuple[int, int]]:
        direcao = self.DIRECOES[self._branco]
        movimentos = []
        nova_linha = linha + direcao
        if tabuleiro.posicao_valida(nova_linha, coluna) and tabuleiro.celula_vazia(nova_linha, coluna):
            movimentos.append((nova_linha, coluna))
        # Capturas diagonais
        for dc in [-1, 1]:
            nova_col = coluna + dc
            if tabuleiro.posicao_valida(nova_linha, nova_col):
                peca_dest = tabuleiro.obter_celula(nova_linha, nova_col)
                if peca_dest is not None and peca_dest.jogador != self._jogador:
                    movimentos.append((nova_linha, nova_col))
        return movimentos


class Torre(Peca):
    """Torre: move em linha reta (horizontal ou vertical), sem saltar peças."""

    @property
    def simbolo(self) -> str:
        return "♖" if self._jogador.simbolo == "B" else "♜"

    def movimentos_validos(self, linha: int, coluna: int, tabuleiro: Tabuleiro) -> list[tuple[int, int]]:
        movimentos = []
        for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            l, c = linha + dl, coluna + dc
            while tabuleiro.posicao_valida(l, c):
                peca = tabuleiro.obter_celula(l, c)
                if peca is None:
                    movimentos.append((l, c))
                elif peca.jogador != self._jogador:
                    movimentos.append((l, c))
                    break
                else:
                    break
                l += dl
                c += dc
        return movimentos


class Rei(Peca):
    """Rei: move 1 casa em qualquer direção."""

    @property
    def simbolo(self) -> str:
        return "♔" if self._jogador.simbolo == "B" else "♚"

    def movimentos_validos(self, linha: int, coluna: int, tabuleiro: Tabuleiro) -> list[tuple[int, int]]:
        movimentos = []
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                l, c = linha + dl, coluna + dc
                if tabuleiro.posicao_valida(l, c):
                    peca = tabuleiro.obter_celula(l, c)
                    if peca is None or peca.jogador != self._jogador:
                        movimentos.append((l, c))
        return movimentos


# ======================================================================
# Regras específicas do Xadrez Simplificado
# ======================================================================

class RegraMovimentoValido(Regra):
    """Verifica se o destino está entre os movimentos válidos da peça."""

    def validar(self, jogada: Jogada, tabuleiro: Tabuleiro) -> tuple[bool, str]:
        if not jogada.tem_origem():
            return False, "Jogada de xadrez precisa de origem."

        peca = tabuleiro.obter_celula(jogada.linha_origem, jogada.coluna_origem)
        if peca is None:
            return False, "Não há peça na posição de origem."
        if peca.jogador != jogada.jogador:
            return False, "Essa peça não pertence a você."

        destinos = peca.movimentos_validos(jogada.linha_origem, jogada.coluna_origem, tabuleiro)
        if (jogada.linha_destino, jogada.coluna_destino) not in destinos:
            return False, "Movimento inválido para esta peça."

        return True, ""


# ======================================================================
# Jogo de Xadrez Simplificado (8x8, só Peões, Torres e Reis)
# ======================================================================

class XadrezSimplificado(JogoTabuleiro):
    """
    Xadrez Simplificado com Peões, Torres e Reis em tabuleiro 8x8.

    Herda de JogoTabuleiro e demonstra polimorfismo com diferentes
    subclasses de Peca, além de regras específicas do xadrez.
    """

    def __init__(self, jogador_branco: Jogador, jogador_preto: Jogador):
        super().__init__([jogador_branco, jogador_preto])
        self._branco = jogador_branco
        self._preto = jogador_preto
        self._tabuleiro = Tabuleiro(8, 8)
        self._regras = ConjuntoDeRegras([
            RegraDestinoDentroDoTabuleiro(),
            RegraMovimentoValido(),
        ])

    # ------------------------------------------------------------------
    # Implementação dos métodos abstratos
    # ------------------------------------------------------------------

    def inicializar_tabuleiro(self) -> None:
        self._tabuleiro.limpar()

        # Torres
        for col in [0, 7]:
            self._tabuleiro.definir_celula(0, col, Torre(self._preto))
            self._tabuleiro.definir_celula(7, col, Torre(self._branco))

        # Reis
        self._tabuleiro.definir_celula(0, 4, Rei(self._preto))
        self._tabuleiro.definir_celula(7, 4, Rei(self._branco))

        # Peões
        for col in range(8):
            self._tabuleiro.definir_celula(1, col, Peao(self._preto, branco=False))
            self._tabuleiro.definir_celula(6, col, Peao(self._branco, branco=True))

    def validar_jogada(self, jogada: Jogada) -> bool:
        valido, _motivo = self._regras.validar_todas(jogada, self._tabuleiro)
        return valido

    def aplicar_jogada(self, jogada: Jogada) -> None:
        peca = self._tabuleiro.obter_celula(jogada.linha_origem, jogada.coluna_origem)
        self._tabuleiro.definir_celula(jogada.linha_destino, jogada.coluna_destino, peca)
        self._tabuleiro.definir_celula(jogada.linha_origem, jogada.coluna_origem, None)

    def verificar_fim_de_jogo(self) -> bool:
        # Vitória: rei adversário foi capturado
        rei_branco_vivo = self._rei_existe(self._branco)
        rei_preto_vivo = self._rei_existe(self._preto)

        if not rei_branco_vivo:
            self._vencedor = self._preto
            self._preto.registrar_vitoria()
            self._branco.registrar_derrota()
            print(f"\n♚ {self._preto.nome} capturou o Rei branco e venceu!")
            return True

        if not rei_preto_vivo:
            self._vencedor = self._branco
            self._branco.registrar_vitoria()
            self._preto.registrar_derrota()
            print(f"\n♔ {self._branco.nome} capturou o Rei preto e venceu!")
            return True

        return False

    def exibir_tabuleiro(self) -> None:
        colunas = "  a b c d e f g h"
        print(f"\n{colunas}")
        for i in range(8):
            linha = [str(8 - i)]
            for j in range(8):
                peca = self._tabuleiro.obter_celula(i, j)
                if peca:
                    linha.append(peca.simbolo)
                else:
                    # Casas claras e escuras
                    linha.append("·" if (i + j) % 2 == 0 else "░")
            linha.append(str(8 - i))
            print(" ".join(linha))
        print(f"{colunas}\n")

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _rei_existe(self, jogador: Jogador) -> bool:
        for l in range(8):
            for c in range(8):
                peca = self._tabuleiro.obter_celula(l, c)
                if isinstance(peca, Rei) and peca.jogador == jogador:
                    return True
        return False

    def _encontrar_peca(self, linha: int, coluna: int) -> Optional[Peca]:
        return self._tabuleiro.obter_celula(linha, coluna)

    # ------------------------------------------------------------------
    # Loop de jogo no terminal
    # ------------------------------------------------------------------

    def jogar_terminal(self) -> None:
        """Loop principal para jogar no terminal."""
        print("=" * 40)
        print("   XADREZ SIMPLIFICADO (Peões, Torres, Reis)")
        print("=" * 40)
        print("Colunas: a-h  |  Linhas: 1-8")
        print("Exemplo de jogada: e2 e4\n")
        self.iniciar()

        while not self._partida_encerrada:
            self.exibir_tabuleiro()
            jogador = self.jogador_atual
            cor = "Brancas" if jogador == self._branco else "Pretas"
            print(f"Turno de {jogador.nome} ({cor})")

            try:
                entrada = input("  Jogada (ex: e2 e4): ").strip().lower().split()
                if len(entrada) != 2:
                    raise ValueError()
                orig = self._parse_posicao(entrada[0])
                dest = self._parse_posicao(entrada[1])
            except (ValueError, IndexError):
                print("  Formato inválido. Use: [coluna][linha] [coluna][linha] (ex: e2 e4)")
                continue

            jogada = Jogada(
                jogador=jogador,
                linha_destino=dest[0],
                coluna_destino=dest[1],
                linha_origem=orig[0],
                coluna_origem=orig[1],
            )
            self.fazer_jogada(jogada)

        self.exibir_tabuleiro()
        print("\nPlacar final:")
        for j in self._jogadores:
            print(f"  {j.placar()}")

    @staticmethod
    def _parse_posicao(texto: str) -> tuple[int, int]:
        """Converte notação 'e2' em (linha, coluna) do array."""
        col_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        coluna = col_map[texto[0]]
        linha = 8 - int(texto[1])
        return linha, coluna

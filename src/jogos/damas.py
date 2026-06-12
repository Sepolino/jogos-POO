from typing import Optional

from ..core import (
    JogoTabuleiro,
    Tabuleiro,
    Jogador,
    Jogada,
    Peca,
    Regra,
    ConjuntoDeRegras,
    RegraDestinoDentroDoTabuleiro,
    RegraDestinoDentroDoTabuleiroVazio,
)


class PecaDamas(Peca):
    """Peça de damas, com movimento diagonal e promoção a dama."""

    def __init__(self, jogador: Jogador, preto: bool, dama: bool = False):
        super().__init__(jogador)
        self._preto = preto
        self._dama = dama

    @property
    def simbolo(self) -> str:
        if self._preto:
            return "⛁" if not self._dama else "⛃"
        return "⛀" if not self._dama else "⛂"

    @property
    def dama(self) -> bool:
        return self._dama

    def movimentos_validos(
        self,
        linha: int,
        coluna: int,
        tabuleiro: Tabuleiro,
    ) -> list[tuple[int, int]]:
        movimentos: list[tuple[int, int]] = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dl, dc in direcoes:
            if not self._dama:
                if self._preto and dl == -1:
                    continue
                if not self._preto and dl == 1:
                    continue

            destino_linha = linha + dl
            destino_coluna = coluna + dc
            if tabuleiro.posicao_valida(destino_linha, destino_coluna):
                if tabuleiro.celula_vazia(destino_linha, destino_coluna):
                    movimentos.append((destino_linha, destino_coluna))
                else:
                    captura_linha = linha + 2 * dl
                    captura_coluna = coluna + 2 * dc
                    if tabuleiro.posicao_valida(captura_linha, captura_coluna):
                        celula_meio = tabuleiro.obter_celula(destino_linha, destino_coluna)
                        if celula_meio is not None and celula_meio.jogador != self._jogador:
                            if tabuleiro.celula_vazia(captura_linha, captura_coluna):
                                movimentos.append((captura_linha, captura_coluna))
        return movimentos


class RegraMovimentoDamas(Regra):
    """Valida movimentação e captura de damas."""

    def validar(self, jogada: Jogada, tabuleiro: Tabuleiro) -> tuple[bool, str]:
        if not jogada.tem_origem():
            return False, "Jogada de damas precisa de origem."

        if not tabuleiro.posicao_valida(jogada.linha_origem, jogada.coluna_origem):
            return False, "Origem fora do tabuleiro."
        if not tabuleiro.posicao_valida(jogada.linha_destino, jogada.coluna_destino):
            return False, "Destino fora do tabuleiro."

        peca = tabuleiro.obter_celula(jogada.linha_origem, jogada.coluna_origem)
        if peca is None:
            return False, "Não há peça na posição de origem."
        if peca.jogador != jogada.jogador:
            return False, "Essa peça não pertence a você."
        if not tabuleiro.celula_vazia(jogada.linha_destino, jogada.coluna_destino):
            return False, "Destino deve estar vazio."

        dl = jogada.linha_destino - jogada.linha_origem
        dc = jogada.coluna_destino - jogada.coluna_origem
        abs_dl = abs(dl)
        abs_dc = abs(dc)

        if abs_dl == 1 and abs_dc == 1:
            if peca.dama:
                return True, ""
            if peca._preto and dl == 1:
                return True, ""
            if not peca._preto and dl == -1:
                return True, ""
            return False, "Peça não pode se mover nessa direção."

        if abs_dl == 2 and abs_dc == 2:
            meio_linha = (jogada.linha_origem + jogada.linha_destino) // 2
            meio_coluna = (jogada.coluna_origem + jogada.coluna_destino) // 2
            meio_peca = tabuleiro.obter_celula(meio_linha, meio_coluna)
            if meio_peca is None or meio_peca.jogador == jogada.jogador:
                return False, "Captura inválida."
            if peca.dama:
                return True, ""
            if peca._preto and dl == 2:
                return True, ""
            if not peca._preto and dl == -2:
                return True, ""
            return False, "Peça não pode capturar nessa direção."

        return False, "Movimento inválido para damas."


class JogoDamas(JogoTabuleiro):
    """Implementação simplificada de Damas com movimentação diagonal e captura."""

    def __init__(self, jogador_preto: Jogador, jogador_branco: Jogador):
        super().__init__([jogador_preto, jogador_branco])
        self._preto = jogador_preto
        self._branco = jogador_branco
        self._tabuleiro = Tabuleiro(8, 8)
        self._regras = ConjuntoDeRegras([
            RegraDestinoDentroDoTabuleiro(),
            RegraDestinoDentroDoTabuleiroVazio(),
            RegraMovimentoDamas(),
        ])

    def inicializar_tabuleiro(self) -> None:
        self._tabuleiro.limpar()
        for linha in range(3):
            for coluna in range(8):
                if (linha + coluna) % 2 == 1:
                    self._tabuleiro.definir_celula(linha, coluna, PecaDamas(self._preto, preto=True))
        for linha in range(5, 8):
            for coluna in range(8):
                if (linha + coluna) % 2 == 1:
                    self._tabuleiro.definir_celula(linha, coluna, PecaDamas(self._branco, preto=False))

    def validar_jogada(self, jogada: Jogada) -> bool:
        valido, _motivo = self._regras.validar_todas(jogada, self._tabuleiro)
        return valido

    def aplicar_jogada(self, jogada: Jogada) -> None:
        peca = self._tabuleiro.obter_celula(jogada.linha_origem, jogada.coluna_origem)
        dl = jogada.linha_destino - jogada.linha_origem
        dc = jogada.coluna_destino - jogada.coluna_origem
        if abs(dl) == 2 and abs(dc) == 2:
            meio_linha = (jogada.linha_origem + jogada.linha_destino) // 2
            meio_coluna = (jogada.coluna_origem + jogada.coluna_destino) // 2
            self._tabuleiro.definir_celula(meio_linha, meio_coluna, None)

        self._tabuleiro.definir_celula(jogada.linha_destino, jogada.coluna_destino, peca)
        self._tabuleiro.definir_celula(jogada.linha_origem, jogada.coluna_origem, None)

        if isinstance(peca, PecaDamas) and not peca.dama:
            if peca._preto and jogada.linha_destino == 7:
                self._tabuleiro.definir_celula(jogada.linha_destino, jogada.coluna_destino, PecaDamas(self._preto, preto=True, dama=True))
            elif not peca._preto and jogada.linha_destino == 0:
                self._tabuleiro.definir_celula(jogada.linha_destino, jogada.coluna_destino, PecaDamas(self._branco, preto=False, dama=True))

    def verificar_fim_de_jogo(self) -> bool:
        preto_pieces = self._quantidade_pecas(self._preto)
        branco_pieces = self._quantidade_pecas(self._branco)

        if preto_pieces == 0:
            self._vencedor = self._branco
            self._branco.registrar_vitoria()
            self._preto.registrar_derrota()
            print(f"\n⛀ {self._branco.nome} venceu por eliminação!")
            return True
        if branco_pieces == 0:
            self._vencedor = self._preto
            self._preto.registrar_vitoria()
            self._branco.registrar_derrota()
            print(f"\n⛁ {self._preto.nome} venceu por eliminação!")
            return True

        if not self._ha_movimentos_validos(self.jogador_atual):
            vencedor = self._preto if self.jogador_atual == self._branco else self._branco
            self._vencedor = vencedor
            vencedor.registrar_vitoria()
            (self._branco if vencedor == self._preto else self._preto).registrar_derrota()
            print(f"\n⛀ {vencedor.nome} venceu por bloqueio do adversário!")
            return True

        return False

    def exibir_tabuleiro(self) -> None:
        linhas = []
        for linha in range(8):
            linha_texto = []
            for coluna in range(8):
                celula = self._tabuleiro.obter_celula(linha, coluna)
                linha_texto.append(celula.simbolo if celula else " .")
            linhas.append(" ".join(linha_texto))
        print("\n" + "\n".join(linhas))

    def obter_estado_tabuleiro(self) -> list[list[str]]:
        estado: list[list[str]] = []
        for linha in range(8):
            valores: list[str] = []
            for coluna in range(8):
                celula = self._tabuleiro.obter_celula(linha, coluna)
                valores.append(celula.simbolo if celula else "")
            estado.append(valores)
        return estado

    def obter_placar(self) -> list[dict[str, int | str]]:
        return [
            {
                "nome": jogador.nome,
                "simbolo": jogador.simbolo,
                "vitorias": jogador.vitorias,
                "derrotas": jogador.derrotas,
                "empates": jogador.empates,
            }
            for jogador in self._jogadores
        ]

    def is_valid_origin(self, row: int, column: int) -> bool:
        if not self._tabuleiro.posicao_valida(row, column):
            return False
        peca = self._tabuleiro.obter_celula(row, column)
        return peca is not None and peca.jogador == self.jogador_atual

    def realizar_jogada_posicao(
        self,
        linha_destino: int,
        coluna_destino: int,
        linha_origem: Optional[int] = None,
        coluna_origem: Optional[int] = None,
    ) -> bool:
        if linha_origem is None or coluna_origem is None:
            raise RuntimeError("Selecione origem e destino para a jogada de damas.")

        jogada = Jogada(
            jogador=self.jogador_atual,
            linha_destino=linha_destino,
            coluna_destino=coluna_destino,
            linha_origem=linha_origem,
            coluna_origem=coluna_origem,
        )
        return self.fazer_jogada(jogada)

    def _quantidade_pecas(self, jogador: Jogador) -> int:
        contador = 0
        for linha in range(8):
            for coluna in range(8):
                peca = self._tabuleiro.obter_celula(linha, coluna)
                if peca is not None and peca.jogador == jogador:
                    contador += 1
        return contador

    def _ha_movimentos_validos(self, jogador: Jogador) -> bool:
        for linha in range(8):
            for coluna in range(8):
                peca = self._tabuleiro.obter_celula(linha, coluna)
                if peca is not None and peca.jogador == jogador:
                    if peca.movimentos_validos(linha, coluna, self._tabuleiro):
                        return True
        return False

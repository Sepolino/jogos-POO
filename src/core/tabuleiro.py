from typing import Optional, Any


class Tabuleiro:
    """
    Representa o tabuleiro genérico de um jogo.

    Armazena apenas o ESTADO (grade de células), sem conhecer regras.
    Regras pertencem ao JogoTabuleiro, não ao Tabuleiro.

    Relação: Composição com JogoTabuleiro.
    """

    def __init__(self, linhas: int, colunas: int):
        self._linhas = linhas
        self._colunas = colunas
        self._grade: list[list[Any]] = self._criar_grade()

    def _criar_grade(self) -> list[list[Any]]:
        return [[None for _ in range(self._colunas)] for _ in range(self._linhas)]

    def limpar(self) -> None:
        """Reseta todas as células para None."""
        self._grade = self._criar_grade()

    def obter_celula(self, linha: int, coluna: int) -> Any:
        self._validar_posicao(linha, coluna)
        return self._grade[linha][coluna]

    def definir_celula(self, linha: int, coluna: int, valor: Any) -> None:
        self._validar_posicao(linha, coluna)
        self._grade[linha][coluna] = valor

    def celula_vazia(self, linha: int, coluna: int) -> bool:
        return self.obter_celula(linha, coluna) is None

    def posicao_valida(self, linha: int, coluna: int) -> bool:
        return 0 <= linha < self._linhas and 0 <= coluna < self._colunas

    def _validar_posicao(self, linha: int, coluna: int) -> None:
        if not self.posicao_valida(linha, coluna):
            raise ValueError(
                f"Posição ({linha}, {coluna}) fora dos limites "
                f"({self._linhas}x{self._colunas})."
            )

    def obter_linha(self, linha: int) -> list[Any]:
        self._validar_posicao(linha, 0)
        return list(self._grade[linha])

    def obter_coluna(self, coluna: int) -> list[Any]:
        self._validar_posicao(0, coluna)
        return [self._grade[l][coluna] for l in range(self._linhas)]

    def obter_diagonal_principal(self) -> list[Any]:
        """Diagonal de (0,0) até (min-1, min-1)."""
        tamanho = min(self._linhas, self._colunas)
        return [self._grade[i][i] for i in range(tamanho)]

    def obter_diagonal_secundaria(self) -> list[Any]:
        """Diagonal de (0, max_col-1) até (min-1, max_col-min)."""
        tamanho = min(self._linhas, self._colunas)
        return [self._grade[i][self._colunas - 1 - i] for i in range(tamanho)]

    def esta_cheio(self) -> bool:
        return all(
            self._grade[l][c] is not None
            for l in range(self._linhas)
            for c in range(self._colunas)
        )

    @property
    def linhas(self) -> int:
        return self._linhas

    @property
    def colunas(self) -> int:
        return self._colunas

    @property
    def grade(self) -> list[list[Any]]:
        """Retorna cópia da grade (encapsulamento)."""
        return [list(linha) for linha in self._grade]

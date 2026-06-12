from abc import ABC, abstractmethod
from .jogador import Jogador


class Peca(ABC):
    """
    Classe base abstrata para peças de jogos de tabuleiro.

    Cada jogo concreto define suas próprias subclasses de Peca,
    sobrescrevendo o símbolo e os movimentos válidos.

    Relação: Associação com Jogador (a peça pertence a um jogador).
    """

    def __init__(self, jogador: Jogador):
        self._jogador = jogador

    @property
    def jogador(self) -> Jogador:
        return self._jogador

    @property
    @abstractmethod
    def simbolo(self) -> str:
        """Retorna a representação visual da peça."""
        pass

    @abstractmethod
    def movimentos_validos(self, linha: int, coluna: int, tabuleiro) -> list[tuple[int, int]]:
        """
        Retorna lista de posições (linha, coluna) para onde a peça pode se mover
        a partir da posição atual.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(jogador={self._jogador.nome!r})"

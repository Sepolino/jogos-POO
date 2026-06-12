from dataclasses import dataclass, field
from typing import Optional, Any
from .jogador import Jogador


@dataclass
class Jogada:
    """
    Representa uma jogada realizada por um jogador.

    Armazena a origem, o destino e metadados opcionais.
    Imutável após criação (frozen=True garante isso).

    Relação: Associação com Jogador; usada por JogoTabuleiro.
    """
    jogador: Jogador
    linha_destino: int
    coluna_destino: int
    linha_origem: Optional[int] = None
    coluna_origem: Optional[int] = None
    metadados: dict = field(default_factory=dict)

    def tem_origem(self) -> bool:
        """True se a jogada envolve mover uma peça de um lugar para outro."""
        return self.linha_origem is not None and self.coluna_origem is not None

    def __repr__(self) -> str:
        if self.tem_origem():
            return (
                f"Jogada({self.jogador.nome}: "
                f"({self.linha_origem},{self.coluna_origem}) → "
                f"({self.linha_destino},{self.coluna_destino}))"
            )
        return (
            f"Jogada({self.jogador.nome}: "
            f"→ ({self.linha_destino},{self.coluna_destino}))"
        )

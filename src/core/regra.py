from abc import ABC, abstractmethod
from .jogada import Jogada
from .tabuleiro import Tabuleiro


class Regra(ABC):
    """
    Classe base abstrata para regras de validação de jogadas.

    Permite compor múltiplas regras independentes usando o padrão
    Chain of Responsibility / Strategy.

    Extensibilidade: basta criar uma subclasse e adicionar ao jogo.
    """

    @abstractmethod
    def validar(self, jogada: Jogada, tabuleiro: Tabuleiro) -> tuple[bool, str]:
        """
        Valida uma jogada contra esta regra.

        Returns:
            (True, "") se válida
            (False, "motivo") se inválida
        """
        pass


class RegraDestinoDentroDoTabuleiro(Regra):
    """Garante que o destino da jogada está dentro dos limites do tabuleiro."""

    def validar(self, jogada: Jogada, tabuleiro: Tabuleiro) -> tuple[bool, str]:
        if not tabuleiro.posicao_valida(jogada.linha_destino, jogada.coluna_destino):
            return False, "Posição fora do tabuleiro."
        return True, ""


class RegraDestinoDentroDoTabuleiroVazio(Regra):
    """Garante que a célula de destino está vazia."""

    def validar(self, jogada: Jogada, tabuleiro: Tabuleiro) -> tuple[bool, str]:
        if not tabuleiro.celula_vazia(jogada.linha_destino, jogada.coluna_destino):
            return False, "Célula já ocupada."
        return True, ""


class ConjuntoDeRegras:
    """
    Agrega múltiplas Regras e as aplica em sequência.

    Uso de composição: o jogo possui um ConjuntoDeRegras que contém Regras.
    """

    def __init__(self, regras: list[Regra] = None):
        self._regras: list[Regra] = regras or []

    def adicionar(self, regra: Regra) -> None:
        self._regras.append(regra)

    def validar_todas(self, jogada: Jogada, tabuleiro: Tabuleiro) -> tuple[bool, str]:
        """Executa todas as regras; retorna o primeiro erro encontrado."""
        for regra in self._regras:
            valido, motivo = regra.validar(jogada, tabuleiro)
            if not valido:
                return False, motivo
        return True, ""

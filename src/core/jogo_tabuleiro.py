from abc import ABC, abstractmethod
from typing import Optional
from .jogador import Jogador
from .jogada import Jogada


class JogoTabuleiro(ABC):
    """
    Classe base abstrata para todos os jogos de tabuleiro.

    Define o contrato (interface) que todo jogo deve seguir,
    garantindo extensibilidade e polimorfismo.

    Relações:
        - Composição com Tabuleiro (cada jogo TEM um tabuleiro)
        - Agregação com Jogador (jogadores existem fora do jogo)
    """

    def __init__(self, jogadores: list[Jogador]):
        if len(jogadores) < 2:
            raise ValueError("Um jogo precisa de pelo menos 2 jogadores.")
        self._jogadores = jogadores
        self._turno_atual: int = 0
        self._partida_encerrada: bool = False
        self._vencedor: Optional[Jogador] = None
        self._historico: list[Jogada] = []

    # ------------------------------------------------------------------
    # Métodos abstratos — cada jogo concreto DEVE implementar
    # ------------------------------------------------------------------

    @abstractmethod
    def inicializar_tabuleiro(self) -> None:
        """Configura o estado inicial do tabuleiro para este jogo."""
        pass

    @abstractmethod
    def validar_jogada(self, jogada: Jogada) -> bool:
        """Retorna True se a jogada é permitida pelas regras do jogo."""
        pass

    @abstractmethod
    def aplicar_jogada(self, jogada: Jogada) -> None:
        """Aplica a jogada ao estado do tabuleiro."""
        pass

    @abstractmethod
    def verificar_fim_de_jogo(self) -> bool:
        """Verifica se o jogo chegou ao fim (vitória, empate etc.)."""
        pass

    @abstractmethod
    def exibir_tabuleiro(self) -> None:
        """Exibe o estado atual do tabuleiro na interface."""
        pass

    # ------------------------------------------------------------------
    # Métodos concretos — lógica compartilhada por todos os jogos
    # ------------------------------------------------------------------

    def iniciar(self) -> None:
        """Inicializa o tabuleiro e começa a partida."""
        self.inicializar_tabuleiro()
        self._partida_encerrada = False
        self._vencedor = None
        self._historico = []
        self._turno_atual = 0

    def fazer_jogada(self, jogada: Jogada) -> bool:
        """
        Tenta realizar uma jogada para o jogador do turno atual.

        Returns:
            True se a jogada foi aceita, False caso contrário.
        """
        if self._partida_encerrada:
            print("A partida já foi encerrada.")
            return False

        if jogada.jogador != self.jogador_atual:
            print(f"Não é o turno de {jogada.jogador.nome}.")
            return False

        if not self.validar_jogada(jogada):
            print("Jogada inválida.")
            return False

        self.aplicar_jogada(jogada)
        self._historico.append(jogada)

        if self.verificar_fim_de_jogo():
            self._partida_encerrada = True
        else:
            self._avancar_turno()

        return True

    def _avancar_turno(self) -> None:
        """Passa o turno para o próximo jogador."""
        self._turno_atual = (self._turno_atual + 1) % len(self._jogadores)


    @property
    def jogador_atual(self) -> Jogador:
        return self._jogadores[self._turno_atual]

    @property
    def vencedor(self) -> Optional[Jogador]:
        return self._vencedor

    @property
    def partida_encerrada(self) -> bool:
        return self._partida_encerrada

    @property
    def historico(self) -> list[Jogada]:
        return list(self._historico)

    @property
    def jogadores(self) -> list[Jogador]:
        return list(self._jogadores)

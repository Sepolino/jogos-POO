class Jogador:
    """
    Representa um jogador humano ou computador.

    Relação: Agregação com JogoTabuleiro (jogadores podem participar
    de múltiplos jogos).
    """

    def __init__(self, nome: str, simbolo: str):
        self._nome = nome
        self._simbolo = simbolo
        self._vitorias: int = 0
        self._derrotas: int = 0
        self._empates: int = 0

    def registrar_vitoria(self) -> None:
        self._vitorias += 1

    def registrar_derrota(self) -> None:
        self._derrotas += 1

    def registrar_empate(self) -> None:
        self._empates += 1

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @property
    def vitorias(self) -> int:
        return self._vitorias

    @property
    def derrotas(self) -> int:
        return self._derrotas

    @property
    def empates(self) -> int:
        return self._empates

    def placar(self) -> str:
        return (
            f"{self._nome} | V:{self._vitorias} "
            f"D:{self._derrotas} E:{self._empates}"
        )

    def __repr__(self) -> str:
        return f"Jogador(nome={self._nome!r}, simbolo={self._simbolo!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Jogador):
            return NotImplemented
        return self._nome == other._nome and self._simbolo == other._simbolo

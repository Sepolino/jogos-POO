"""Model da partida, independente da interface grafica."""

from src.core import Jogador
from src.jogos import JogoDaVelha


class GameModel:
    """
    Model do MVC.

    Encapsula a logica do JogoDaVelha e expoe apenas metodos publicos para o
    Controller. A View nunca acessa diretamente este objeto.
    """

    def __init__(self) -> None:
        self._player_names = ["Jogador 1", "Jogador 2"]
        self._game: JogoDaVelha | None = None

    def configure_players(self, names: list[str]) -> None:
        """Configura os nomes dos jogadores da proxima partida."""
        cleaned_names = [
            name.strip() or f"Jogador {index + 1}"
            for index, name in enumerate(names[:2])
        ]
        while len(cleaned_names) < 2:
            cleaned_names.append(f"Jogador {len(cleaned_names) + 1}")
        self._player_names = cleaned_names

    def start_new_match(self) -> None:
        """Cria e inicia uma nova partida mantendo os jogadores configurados."""
        player_one = Jogador(self._player_names[0], "X")
        player_two = Jogador(self._player_names[1], "O")
        self._game = JogoDaVelha(player_one, player_two)
        self._game.iniciar()

    def play_turn(self, row: int, column: int) -> bool:
        """Executa a jogada do jogador atual na posicao informada."""
        self._ensure_game()
        return self._game.realizar_jogada_posicao(row, column)

    def get_board(self) -> list[list[str]]:
        """Retorna o estado atual do tabuleiro."""
        self._ensure_game()
        return self._game.obter_estado_tabuleiro()

    def get_current_player_text(self) -> str:
        """Retorna o texto do jogador da vez."""
        self._ensure_game()
        player = self._game.jogador_atual
        return f"{player.nome} ({player.simbolo})"

    def get_scoreboard(self) -> list[dict[str, int | str]]:
        """Retorna o placar atual em formato estruturado."""
        self._ensure_game()
        return self._game.obter_placar()

    def is_finished(self) -> bool:
        """Indica se a partida atual terminou."""
        self._ensure_game()
        return self._game.partida_encerrada

    def get_result(self) -> dict[str, str | int | list[dict[str, int | str]]]:
        """Retorna vencedor, estatisticas e dados finais da partida."""
        self._ensure_game()
        winner = self._game.vencedor
        return {
            "winner": f"{winner.nome} ({winner.simbolo})" if winner else "Empate",
            "moves": len(self._game.historico),
            "scoreboard": self._game.obter_placar(),
            "status": "Vitoria" if winner else "Empate",
        }

    def _ensure_game(self) -> None:
        if self._game is None:
            raise RuntimeError("Nenhuma partida foi iniciada.")

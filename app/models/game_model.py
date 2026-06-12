"""Model da partida, independente da interface grafica."""

from src.core import Jogador
from src.jogos import JogoDaVelha, JogoDamas


class GameModel:
    """
    Model do MVC.

    Encapsula a partida atual e expõe apenas métodos públicos para o
    Controller. A View nunca acessa diretamente este objeto.
    """

    def __init__(self) -> None:
        self._player_names = ["Jogador 1", "Jogador 2"]
        self._game_mode = "velha"
        self._game: JogoDaVelha | JogoDamas | None = None
        self._selected_origin: tuple[int, int] | None = None

    def configure_players(self, names: list[str]) -> None:
        """Configura os nomes dos jogadores da próxima partida."""
        cleaned_names = [
            name.strip() or f"Jogador {index + 1}"
            for index, name in enumerate(names[:2])
        ]
        while len(cleaned_names) < 2:
            cleaned_names.append(f"Jogador {len(cleaned_names) + 1}")
        self._player_names = cleaned_names

    def configure_game_mode(self, game_mode: str) -> None:
        """Configura o modo de jogo a ser usado na próxima partida."""
        self._game_mode = "damas" if game_mode == "damas" else "velha"
        self._selected_origin = None

    def start_new_match(self) -> None:
        """Cria e inicia uma nova partida mantendo os jogadores configurados."""
        if self._game_mode == "damas":
            player_one = Jogador(self._player_names[0], "B")
            player_two = Jogador(self._player_names[1], "P")
            self._game = JogoDamas(player_one, player_two)
        else:
            player_one = Jogador(self._player_names[0], "X")
            player_two = Jogador(self._player_names[1], "O")
            self._game = JogoDaVelha(player_one, player_two)

        self._selected_origin = None
        self._game.iniciar()

    def play_turn(
        self,
        row: int,
        column: int,
        row_origin: int | None = None,
        column_origin: int | None = None,
    ) -> bool:
        """Executa a jogada do jogador atual na posição informada."""
        self._ensure_game()

        if self._game_mode == "damas":
            if row_origin is not None and column_origin is not None:
                return self._game.realizar_jogada_posicao(
                    row,
                    column,
                    row_origin,
                    column_origin,
                )
            if self._selected_origin is None:
                if not self._game.is_valid_origin(row, column):
                    return False
                self._selected_origin = (row, column)
                return True
            origin_row, origin_column = self._selected_origin
            accepted = self._game.realizar_jogada_posicao(
                row,
                column,
                origin_row,
                origin_column,
            )
            if accepted:
                self._selected_origin = None
            return accepted

        return self._game.realizar_jogada_posicao(row, column)

    def clear_selected_origin(self) -> None:
        self._selected_origin = None

    def is_game_mode_damas(self) -> bool:
        """Retorna True se o jogo atual for Damas."""
        return self._game_mode == "damas"

    def get_selected_origin_text(self) -> str:
        if self._selected_origin is None:
            return ""
        return f"Origem: {self._selected_origin}"

    def is_valid_origin(self, row: int, column: int) -> bool:
        """Verifica se a posição selecionada é uma peça válida do jogador atual."""
        if self._game_mode != "damas":
            return False
        return self._game.is_valid_origin(row, column)

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

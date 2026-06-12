"""Controller que orquestra fluxo entre Model e Views."""

from kivymd.app import MDApp

from app.models.game_model import GameModel


class GameController:
    """
    Controller do MVC.

    Recebe eventos da View, chama metodos publicos do Model e decide quando
    atualizar telas ou navegar. Regras do jogo permanecem fora da interface.
    """

    def __init__(self, screen_manager) -> None:
        self._screen_manager = screen_manager
        self._model = GameModel()

    def show_menu(self) -> None:
        """Mostra o menu principal."""
        self._screen_manager.current = "menu"

    def show_config(self) -> None:
        """Mostra a tela de configuracao da partida."""
        self._screen_manager.current = "config"

    def start_match(self, player_names: list[str]) -> None:
        """Configura jogadores, inicia partida e abre o tabuleiro."""
        self._model.configure_players(player_names)
        self._model.start_new_match()
        self._screen_manager.current = "board"
        self.current_screen.refresh()

    def restart_match(self) -> None:
        """Reinicia a partida atual sem fechar o aplicativo."""
        self._model.start_new_match()
        self._screen_manager.current = "board"
        self.current_screen.refresh()

    def play_cell(self, row: int, column: int) -> bool:
        """Tenta executar uma jogada e atualiza a interface."""
        try:
            accepted = self._model.play_turn(row, column)
        except RuntimeError as error:
            self.current_screen.show_error(str(error))
            return False

        board_screen = self._screen_manager.get_screen("board")
        board_screen.refresh()

        if accepted and self._model.is_finished():
            result_screen = self._screen_manager.get_screen("result")
            result_screen.refresh()
            self._screen_manager.current = "result"
        elif not accepted:
            board_screen.show_error("Jogada invalida. Escolha uma casa vazia.")
        return accepted

    def get_board(self) -> list[list[str]]:
        """Retorna o tabuleiro da partida."""
        return self._model.get_board()

    def get_current_player_text(self) -> str:
        """Retorna o jogador da vez."""
        return self._model.get_current_player_text()

    def get_scoreboard_text(self) -> str:
        """Retorna o placar formatado para exibicao."""
        lines = []
        for player in self._model.get_scoreboard():
            lines.append(
                f"{player['nome']} ({player['simbolo']})  "
                f"V:{player['vitorias']} D:{player['derrotas']} E:{player['empates']}"
            )
        return "\n".join(lines)

    def get_result(self) -> dict[str, str | int | list[dict[str, int | str]]]:
        """Retorna o resumo final da partida."""
        return self._model.get_result()

    def exit_app(self) -> None:
        """Fecha o aplicativo de forma controlada."""
        MDApp.get_running_app().stop()

    @property
    def current_screen(self):
        """Retorna a tela atual do ScreenManager."""
        return self._screen_manager.current_screen

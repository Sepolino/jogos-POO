"""Tela do tabuleiro."""

from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton

from app.views.base_screen import BaseScreen


class BoardScreen(BaseScreen):
    """View responsavel por renderizar tabuleiro, turno e placar."""

    def on_pre_enter(self, *args) -> None:
        """Atualiza a tela sempre que ela for aberta."""
        self.refresh()

    def refresh(self) -> None:
        """Reconstroi os botoes do tabuleiro com o estado mais recente."""
        if not self.ids:
            return

        board = self.controller.get_board()
        self.ids.turn_label.text = f"Vez de: {self.controller.get_current_player_text()}"
        self.ids.score_label.text = self.controller.get_scoreboard_text()
        self.ids.board_grid.clear_widgets()

        for row_index, row in enumerate(board):
            for column_index, symbol in enumerate(row):
                button = MDRaisedButton(
                    text=symbol or " ",
                    font_size="36sp",
                    size_hint=(1, 1),
                    md_bg_color=(0.95, 0.98, 0.98, 1),
                    text_color=(0.02, 0.2, 0.2, 1),
                )
                button.bind(
                    on_release=lambda _btn, row=row_index, col=column_index:
                    self.controller.play_cell(row, col)
                )
                self.ids.board_grid.add_widget(button)

        self.ids.board_grid.spacing = dp(8)

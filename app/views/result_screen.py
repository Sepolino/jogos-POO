"""Tela de resultado final."""

from app.views.base_screen import BaseScreen


class ResultScreen(BaseScreen):
    """View que apresenta vencedor e estatisticas finais."""

    def on_pre_enter(self, *args) -> None:
        """Atualiza resultado antes de mostrar a tela."""
        self.refresh()

    def refresh(self) -> None:
        """Preenche os campos de resultado com dados do Controller."""
        result = self.controller.get_result()
        self.ids.winner_label.text = f"Resultado: {result['winner']}"
        self.ids.stats_label.text = (
            f"Status: {result['status']}\n"
            f"Jogadas realizadas: {result['moves']}\n\n"
            f"{self.controller.get_scoreboard_text()}"
        )

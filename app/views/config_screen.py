"""Tela de configuracao da partida."""

from app.views.base_screen import BaseScreen


class ConfigScreen(BaseScreen):
    """View para definir quantidade e nomes dos jogadores."""

    def start_match(self) -> None:
        """Envia nomes configurados para o Controller iniciar a partida."""
        names = [
            self.ids.player_one.text,
            self.ids.player_two.text,
        ]
        self.controller.start_match(names)

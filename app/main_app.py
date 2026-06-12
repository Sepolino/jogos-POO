"""Aplicacao KivyMD do jogo de tabuleiro."""

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from app.controllers.game_controller import GameController
from app.views.board_screen import BoardScreen
from app.views.config_screen import ConfigScreen
from app.views.menu_screen import MenuScreen
from app.views.result_screen import ResultScreen


class BoardGameApp(MDApp):
    """
    Aplicacao principal.

    No MVC, esta classe monta as Views e injeta o Controller. Ela nao contem
    regras do jogo; apenas inicializa tema, KV e navegacao.
    """

    def build(self) -> ScreenManager:
        """Constroi o gerenciador de telas e configura o tema Material."""
        self.title = "Jogo da Velha MVC"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"

        Builder.load_file("app/views/screens.kv")

        manager = ScreenManager()
        self.controller = GameController(manager)

        manager.add_widget(MenuScreen(name="menu", controller=self.controller))
        manager.add_widget(ConfigScreen(name="config", controller=self.controller))
        manager.add_widget(BoardScreen(name="board", controller=self.controller))
        manager.add_widget(ResultScreen(name="result", controller=self.controller))

        self.controller.show_menu()
        return manager

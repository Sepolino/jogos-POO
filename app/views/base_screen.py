"""Tela base compartilhada pelas Views."""

from kivymd.uix.screen import MDScreen

from app.components.dialogs import DialogService


class BaseScreen(MDScreen):
    """Classe base com suporte ao Controller e dialogos de erro."""

    def __init__(self, controller, **kwargs) -> None:
        super().__init__(**kwargs)
        self.controller = controller

    def refresh(self) -> None:
        """Atualiza dados visuais da tela."""

    def show_error(self, message: str) -> None:
        """Exibe uma mensagem de erro sem encerrar o aplicativo."""
        DialogService.show_message("Atencao", message)

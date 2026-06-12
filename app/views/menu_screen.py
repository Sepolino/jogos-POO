"""Tela de menu principal."""

from app.views.base_screen import BaseScreen
from app.components.dialogs import DialogService
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp


class MenuScreen(BaseScreen):
    """View do menu principal."""

    def open_settings(self) -> None:
        """Abre um diálogo de configurações com opções úteis.

        Alterna tema ou mostra informações sobre o app sem abrir a tela
        de configuração de partida (evita duplicar a ação de 'Nova Partida').
        """

        def _toggle_theme(*_args) -> None:
            app = MDApp.get_running_app()
            app.theme_cls.theme_style = (
                "Dark" if app.theme_cls.theme_style == "Light" else "Light"
            )
            dialog.dismiss()

        def _show_about(*_args) -> None:
            dialog.dismiss()
            DialogService.show_message(
                "Sobre",
                "Jogo da Velha\nVersão 1.0\nAutor:\nCarlos Chen\nFelipe Savegnago Pires\nMarcus Vinícius Milan da Silva",
            )

        dialog = MDDialog(
            title="Configurações",
            text="Escolha uma opção:",
            buttons=[
                MDRaisedButton(text="Alternar Tema", on_release=_toggle_theme),
                MDRaisedButton(text="Sobre", on_release=_show_about),
                MDRaisedButton(text="Fechar", on_release=lambda *_: dialog.dismiss()),
            ],
        )
        dialog.open()

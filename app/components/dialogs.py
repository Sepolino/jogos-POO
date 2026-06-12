"""Dialogos reutilizaveis da interface."""

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog


class DialogService:
    """Servico simples para exibir mensagens Material Design."""

    @staticmethod
    def show_message(title: str, text: str) -> None:
        """Abre um dialogo informativo com botao OK."""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda *_: dialog.dismiss(),
                )
            ],
        )
        dialog.open()

"""Dobles de prueba del módulo de clientes."""

from clientes.notificaciones import Notificador


class NotificadorEspia(Notificador):
    """Registra los mensajes en lugar de enviarlos."""

    def __init__(self) -> None:
        self.enviados: list[tuple[str, str, str]] = []

    def enviar(self, destinatario: str, asunto: str, mensaje: str) -> None:
        self.enviados.append((destinatario, asunto, mensaje))

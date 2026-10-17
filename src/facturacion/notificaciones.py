"""Envío de notificaciones al cliente (ISP + DIP)."""

from __future__ import annotations

import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage


class Notificador(ABC):
    @abstractmethod
    def notificar(self, destinatario: str, asunto: str, mensaje: str) -> None: ...


class NotificadorEmail(Notificador):
    """Las credenciales llegan desde la configuración, nunca escritas en el código."""

    def __init__(
        self, servidor: str, puerto: int, usuario: str, clave: str, remitente: str
    ) -> None:
        self._servidor = servidor
        self._puerto = puerto
        self._usuario = usuario
        self._clave = clave
        self._remitente = remitente

    def notificar(self, destinatario: str, asunto: str, mensaje: str) -> None:
        correo = EmailMessage()
        correo["From"] = self._remitente
        correo["To"] = destinatario
        correo["Subject"] = asunto
        correo.set_content(mensaje)

        with smtplib.SMTP(self._servidor, self._puerto) as smtp:
            smtp.starttls()
            smtp.login(self._usuario, self._clave)
            smtp.send_message(correo)

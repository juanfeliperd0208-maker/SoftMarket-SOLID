"""Notificaciones al cliente (ISP, DIP, OCP).

Notificador tiene un único método: quien solo necesita avisar al cliente no
depende de nada más. Un canal nuevo (SMS, WhatsApp) es otra clase.
"""

from __future__ import annotations

import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage


class Notificador(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, asunto: str, mensaje: str) -> None: ...


class NotificadorConsola(Notificador):
    """Útil en desarrollo: muestra el mensaje en lugar de enviarlo."""

    def enviar(self, destinatario: str, asunto: str, mensaje: str) -> None:
        print(f"Para: {destinatario} | {asunto}\n{mensaje}")


class NotificadorEmail(Notificador):
    """Servidor y credenciales llegan por constructor, nunca escritos en el código."""

    def __init__(self, servidor: str, puerto: int, usuario: str, clave: str) -> None:
        self._servidor = servidor
        self._puerto = puerto
        self._usuario = usuario
        self._clave = clave

    def enviar(self, destinatario: str, asunto: str, mensaje: str) -> None:
        correo = EmailMessage()
        correo["From"] = self._usuario
        correo["To"] = destinatario
        correo["Subject"] = asunto
        correo.set_content(mensaje)
        with smtplib.SMTP(self._servidor, self._puerto) as smtp:
            smtp.starttls()
            smtp.login(self._usuario, self._clave)
            smtp.send_message(correo)

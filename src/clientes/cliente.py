"""Entidad Cliente: solo datos y reglas propias del cliente (SRP).

Ya no sabe guardarse, enviar correos ni generar reportes; esas tareas
pasaron a clases separadas.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    id: str
    nombre: str
    email: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("El cliente debe tener un identificador")
        if not self.nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío")
        if "@" not in self.email or self.email.startswith("@") or self.email.endswith("@"):
            raise ValueError(f"Correo inválido: {self.email!r}")

    def mostrar(self) -> str:
        return self.nombre

"""Persistencia de facturas detrás de una abstracción (DIP).

El servicio solo conoce RepositorioFacturas; la base de datos concreta
(SQLite, PostgreSQL, una API externa) se decide al componer la aplicación.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from facturacion.modelos import Factura


class RepositorioFacturas(ABC):
    @abstractmethod
    def guardar(self, factura: Factura) -> None: ...

    @abstractmethod
    def obtener(self, numero: str) -> Factura | None: ...


class RepositorioEnMemoria(RepositorioFacturas):
    def __init__(self) -> None:
        self._facturas: dict[str, Factura] = {}

    def guardar(self, factura: Factura) -> None:
        if factura.numero in self._facturas:
            raise ValueError(f"La factura {factura.numero} ya existe")
        self._facturas[factura.numero] = factura

    def obtener(self, numero: str) -> Factura | None:
        return self._facturas.get(numero)

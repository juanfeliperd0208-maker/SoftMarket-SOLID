"""Políticas de descuento (patrón Strategy).

OCP: un descuento nuevo es una clase nueva; las existentes no se modifican.
LSP: toda política devuelve un monto en el rango [0, subtotal], de modo que
cualquier implementación puede sustituir a otra sin romper la calculadora.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal

from facturacion.modelos import Cliente, TipoCliente

CERO = Decimal("0")


class PoliticaDescuento(ABC):
    @abstractmethod
    def calcular(self, cliente: Cliente, subtotal: Decimal) -> Decimal:
        """Devuelve el monto a descontar, siempre entre 0 y el subtotal."""


class SinDescuento(PoliticaDescuento):
    def calcular(self, cliente: Cliente, subtotal: Decimal) -> Decimal:
        return CERO


class DescuentoPorcentual(PoliticaDescuento):
    def __init__(self, porcentaje: Decimal) -> None:
        if not CERO <= porcentaje <= Decimal("100"):
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        self._porcentaje = porcentaje

    def calcular(self, cliente: Cliente, subtotal: Decimal) -> Decimal:
        return subtotal * self._porcentaje / Decimal("100")


class DescuentoPorVolumen(PoliticaDescuento):
    """Monto fijo cuando el subtotal alcanza un umbral; nunca supera el subtotal."""

    def __init__(self, umbral: Decimal, monto: Decimal) -> None:
        self._umbral = umbral
        self._monto = monto

    def calcular(self, cliente: Cliente, subtotal: Decimal) -> Decimal:
        if subtotal < self._umbral:
            return CERO
        return min(self._monto, subtotal)


class DescuentoPorTipoCliente(PoliticaDescuento):
    """Elige la política según el tipo de cliente (reemplaza la cadena de if/elif)."""

    def __init__(
        self,
        politicas: dict[TipoCliente, PoliticaDescuento],
        por_defecto: PoliticaDescuento | None = None,
    ) -> None:
        self._politicas = dict(politicas)
        self._por_defecto = por_defecto or SinDescuento()

    def calcular(self, cliente: Cliente, subtotal: Decimal) -> Decimal:
        politica = self._politicas.get(cliente.tipo, self._por_defecto)
        return politica.calcular(cliente, subtotal)

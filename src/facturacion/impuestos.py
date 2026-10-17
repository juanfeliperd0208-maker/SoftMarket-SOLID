"""Cálculo de impuestos.

La tasa deja de estar copiada en varios módulos: se configura en un único lugar
(la composición de la aplicación) y se inyecta donde se necesita.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal


class CalculadoraImpuesto(ABC):
    @abstractmethod
    def calcular(self, base_imponible: Decimal) -> Decimal:
        """Devuelve el impuesto correspondiente a la base imponible."""


class IVA(CalculadoraImpuesto):
    def __init__(self, tasa: Decimal) -> None:
        if not Decimal("0") <= tasa < Decimal("1"):
            raise ValueError("La tasa debe expresarse como fracción, por ejemplo 0.19")
        self._tasa = tasa

    def calcular(self, base_imponible: Decimal) -> Decimal:
        return base_imponible * self._tasa


class Exento(CalculadoraImpuesto):
    def calcular(self, base_imponible: Decimal) -> Decimal:
        return Decimal("0")

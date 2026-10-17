"""Entidades del dominio de facturación.

Solo contienen datos y reglas propias del dominio: no saben guardarse,
imprimirse ni enviarse (SRP).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum


class TipoCliente(Enum):
    REGULAR = "regular"
    FRECUENTE = "frecuente"
    MAYORISTA = "mayorista"


@dataclass(frozen=True)
class Cliente:
    id: str
    nombre: str
    email: str
    tipo: TipoCliente = TipoCliente.REGULAR


@dataclass(frozen=True)
class ItemFactura:
    descripcion: str
    cantidad: int
    precio_unitario: Decimal

    def __post_init__(self) -> None:
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        if self.precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo")

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad


@dataclass
class Factura:
    numero: str
    cliente: Cliente
    items: list[ItemFactura]
    fecha: date = field(default_factory=date.today)
    subtotal: Decimal = Decimal("0")
    descuento: Decimal = Decimal("0")
    impuesto: Decimal = Decimal("0")

    @property
    def total(self) -> Decimal:
        return self.subtotal - self.descuento + self.impuesto

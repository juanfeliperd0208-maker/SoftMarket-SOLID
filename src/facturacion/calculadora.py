"""Cálculo de los montos de una factura (única responsabilidad: SRP)."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from facturacion.descuentos import PoliticaDescuento
from facturacion.impuestos import CalculadoraImpuesto
from facturacion.modelos import Factura

DOS_DECIMALES = Decimal("0.01")


def redondear(monto: Decimal) -> Decimal:
    return monto.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)


class CalculadoraFactura:
    def __init__(
        self,
        politica_descuento: PoliticaDescuento,
        calculadora_impuesto: CalculadoraImpuesto,
    ) -> None:
        self._politica_descuento = politica_descuento
        self._calculadora_impuesto = calculadora_impuesto

    def calcular(self, factura: Factura) -> Factura:
        subtotal = sum((item.subtotal for item in factura.items), Decimal("0"))
        descuento = self._politica_descuento.calcular(factura.cliente, subtotal)
        impuesto = self._calculadora_impuesto.calcular(subtotal - descuento)

        factura.subtotal = redondear(subtotal)
        factura.descuento = redondear(descuento)
        factura.impuesto = redondear(impuesto)
        return factura

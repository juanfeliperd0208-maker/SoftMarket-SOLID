from decimal import Decimal

import pytest

from facturacion.calculadora import CalculadoraFactura
from facturacion.descuentos import DescuentoPorcentual, SinDescuento
from facturacion.impuestos import IVA, Exento
from facturacion.modelos import Cliente, Factura, ItemFactura

CLIENTE = Cliente("C1", "Ana", "ana@correo.com")


def factura_con(*items):
    return Factura(numero="FAC-000001", cliente=CLIENTE, items=list(items))


def test_calcula_subtotal_descuento_e_impuesto():
    calculadora = CalculadoraFactura(DescuentoPorcentual(Decimal("10")), IVA(Decimal("0.19")))
    factura = factura_con(
        ItemFactura("Licencia", 2, Decimal("100.00")), ItemFactura("Soporte", 1, Decimal("50.00"))
    )

    calculadora.calcular(factura)

    assert (factura.subtotal, factura.descuento, factura.impuesto, factura.total) == (
        Decimal("250.00"),
        Decimal("25.00"),
        Decimal("42.75"),
        Decimal("267.75"),
    )


def test_redondea_a_dos_decimales_hacia_arriba_en_la_mitad():
    factura = factura_con(ItemFactura("Módulo", 1, Decimal("10.50")))

    CalculadoraFactura(SinDescuento(), IVA(Decimal("0.19"))).calcular(factura)

    assert factura.impuesto == Decimal("2.00")  # 1.995 -> 2.00


def test_las_estrategias_son_intercambiables():
    factura = factura_con(ItemFactura("Licencia", 1, Decimal("80")))

    CalculadoraFactura(SinDescuento(), Exento()).calcular(factura)

    assert factura.total == Decimal("80.00")


def test_iva_rechaza_tasas_expresadas_como_porcentaje():
    with pytest.raises(ValueError):
        IVA(Decimal("19"))

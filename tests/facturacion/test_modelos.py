from decimal import Decimal

import pytest

from facturacion.modelos import Cliente, Factura, ItemFactura


def test_subtotal_del_item_es_precio_por_cantidad():
    assert ItemFactura("Licencia anual", 3, Decimal("150.00")).subtotal == Decimal("450.00")


@pytest.mark.parametrize("cantidad", [0, -1])
def test_rechaza_cantidades_no_positivas(cantidad):
    with pytest.raises(ValueError):
        ItemFactura("Soporte", cantidad, Decimal("10"))


def test_rechaza_precio_negativo():
    with pytest.raises(ValueError):
        ItemFactura("Soporte", 1, Decimal("-1"))


def test_total_resta_descuento_y_suma_impuesto():
    factura = Factura(
        numero="FAC-000001",
        cliente=Cliente("C1", "Ana", "ana@correo.com"),
        items=[],
        subtotal=Decimal("100"),
        descuento=Decimal("10"),
        impuesto=Decimal("17.10"),
    )

    assert factura.total == Decimal("107.10")

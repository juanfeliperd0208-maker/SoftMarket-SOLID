from decimal import Decimal

import pytest

from facturacion.descuentos import (
    DescuentoPorcentual,
    DescuentoPorTipoCliente,
    DescuentoPorVolumen,
    SinDescuento,
)
from facturacion.modelos import Cliente, TipoCliente

REGULAR = Cliente("C1", "Ana", "ana@correo.com", TipoCliente.REGULAR)
MAYORISTA = Cliente("C2", "Distribuidora Sur", "compras@sur.com", TipoCliente.MAYORISTA)


def test_descuento_porcentual_aplica_el_porcentaje():
    assert DescuentoPorcentual(Decimal("12")).calcular(REGULAR, Decimal("1000")) == Decimal("120")


def test_descuento_porcentual_rechaza_valores_fuera_de_rango():
    with pytest.raises(ValueError):
        DescuentoPorcentual(Decimal("120"))


@pytest.mark.parametrize(
    ("subtotal", "esperado"), [(Decimal("499"), Decimal("0")), (Decimal("500"), Decimal("50"))]
)
def test_descuento_por_volumen_solo_desde_el_umbral(subtotal, esperado):
    politica = DescuentoPorVolumen(umbral=Decimal("500"), monto=Decimal("50"))

    assert politica.calcular(REGULAR, subtotal) == esperado


def test_descuento_por_tipo_usa_la_politica_del_tipo_de_cliente():
    politica = DescuentoPorTipoCliente({TipoCliente.MAYORISTA: DescuentoPorcentual(Decimal("12"))})

    assert politica.calcular(MAYORISTA, Decimal("100")) == Decimal("12")
    assert politica.calcular(REGULAR, Decimal("100")) == Decimal("0")


# LSP: cualquier política debe cumplir 0 <= descuento <= subtotal.
POLITICAS = [
    SinDescuento(),
    DescuentoPorcentual(Decimal("0")),
    DescuentoPorcentual(Decimal("100")),
    DescuentoPorVolumen(umbral=Decimal("10"), monto=Decimal("1000")),
    DescuentoPorTipoCliente({TipoCliente.REGULAR: DescuentoPorcentual(Decimal("30"))}),
]


@pytest.mark.parametrize("politica", POLITICAS, ids=lambda p: type(p).__name__)
@pytest.mark.parametrize("subtotal", [Decimal("0"), Decimal("9.99"), Decimal("250.50")])
def test_toda_politica_respeta_el_contrato(politica, subtotal):
    descuento = politica.calcular(REGULAR, subtotal)

    assert Decimal("0") <= descuento <= subtotal

"""El caso de uso completo se prueba con dobles, sin base de datos ni correo (DIP)."""

from decimal import Decimal

import pytest

from facturacion.calculadora import CalculadoraFactura
from facturacion.descuentos import DescuentoPorcentual, DescuentoPorTipoCliente
from facturacion.exportadores import ExportadorTexto
from facturacion.impuestos import IVA
from facturacion.modelos import Cliente, ItemFactura, TipoCliente
from facturacion.notificaciones import Notificador
from facturacion.repositorio import RepositorioEnMemoria
from facturacion.servicio import GeneradorNumeroConsecutivo, ServicioFacturacion

MAYORISTA = Cliente("C2", "Distribuidora Sur", "compras@sur.com", TipoCliente.MAYORISTA)


class NotificadorEspia(Notificador):
    def __init__(self):
        self.enviados = []

    def notificar(self, destinatario, asunto, mensaje):
        self.enviados.append((destinatario, asunto, mensaje))


@pytest.fixture
def repositorio():
    return RepositorioEnMemoria()


@pytest.fixture
def notificador():
    return NotificadorEspia()


@pytest.fixture
def servicio(repositorio, notificador):
    descuentos = DescuentoPorTipoCliente(
        {TipoCliente.MAYORISTA: DescuentoPorcentual(Decimal("12"))}
    )
    return ServicioFacturacion(
        calculadora=CalculadoraFactura(descuentos, IVA(Decimal("0.19"))),
        repositorio=repositorio,
        exportador=ExportadorTexto(),
        notificador=notificador,
        generar_numero=GeneradorNumeroConsecutivo(),
    )


def test_emitir_calcula_guarda_y_notifica(servicio, repositorio, notificador):
    factura = servicio.emitir(MAYORISTA, [ItemFactura("Licencia", 10, Decimal("100"))])

    assert factura.total == Decimal("1047.20")
    assert repositorio.obtener("FAC-000001") is factura
    destinatario, asunto, mensaje = notificador.enviados[0]
    assert (destinatario, asunto) == ("compras@sur.com", "Factura FAC-000001")
    assert "TOTAL:     1047.20" in mensaje


def test_los_numeros_de_factura_son_consecutivos(servicio):
    primera = servicio.emitir(MAYORISTA, [ItemFactura("A", 1, Decimal("1"))])
    segunda = servicio.emitir(MAYORISTA, [ItemFactura("B", 1, Decimal("1"))])

    assert (primera.numero, segunda.numero) == ("FAC-000001", "FAC-000002")


def test_no_emite_ni_notifica_facturas_sin_items(servicio, notificador):
    with pytest.raises(ValueError):
        servicio.emitir(MAYORISTA, [])

    assert notificador.enviados == []


def test_el_repositorio_rechaza_numeros_repetidos(repositorio, servicio):
    factura = servicio.emitir(MAYORISTA, [ItemFactura("A", 1, Decimal("1"))])

    with pytest.raises(ValueError):
        repositorio.guardar(factura)

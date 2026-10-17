"""Pruebas del servicio con dobles: sin base de datos ni servidor de correo (DIP)."""

import pytest

from clientes.cliente import Cliente
from clientes.reportes import ReporteTexto
from clientes.repositorio import ClienteDuplicadoError, RepositorioClientesEnMemoria
from clientes.servicio import ServicioClientes
from tests.clientes.dobles import NotificadorEspia


@pytest.fixture
def repositorio():
    return RepositorioClientesEnMemoria()


@pytest.fixture
def notificador():
    return NotificadorEspia()


@pytest.fixture
def servicio(repositorio, notificador):
    return ServicioClientes(repositorio, notificador, ReporteTexto())


def test_registrar_guarda_al_cliente_y_le_da_la_bienvenida(servicio, repositorio, notificador):
    ana = Cliente("C1", "Ana", "ana@correo.com")

    servicio.registrar(ana)

    assert repositorio.buscar("C1") == ana
    assert notificador.enviados == [
        ("ana@correo.com", "Bienvenido a SoftMarket", "Hola Ana, tu registro fue exitoso.")
    ]


def test_no_notifica_si_el_cliente_ya_existe(servicio, notificador):
    servicio.registrar(Cliente("C1", "Ana", "ana@correo.com"))

    with pytest.raises(ClienteDuplicadoError):
        servicio.registrar(Cliente("C1", "Ana", "ana@correo.com"))

    assert len(notificador.enviados) == 1


def test_el_reporte_usa_el_generador_inyectado(servicio):
    servicio.registrar(Cliente("C1", "Ana", "ana@correo.com"))

    assert servicio.reporte() == "Clientes registrados: 1\n- C1: Ana <ana@correo.com>"

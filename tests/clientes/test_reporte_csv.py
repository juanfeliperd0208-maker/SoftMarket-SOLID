import csv
import io

from clientes.cliente import Cliente
from clientes.reporte_csv import ReporteCSV
from clientes.repositorio import RepositorioClientesEnMemoria
from clientes.servicio import ServicioClientes
from tests.clientes.dobles import NotificadorEspia


def test_genera_encabezado_y_una_fila_por_cliente():
    clientes = [Cliente("C1", "Ana Gómez", "ana@correo.com"), Cliente("C2", "Luis", "l@c.com")]

    filas = list(csv.reader(io.StringIO(ReporteCSV().generar(clientes))))

    assert filas == [
        ["id", "nombre", "email"],
        ["C1", "Ana Gómez", "ana@correo.com"],
        ["C2", "Luis", "l@c.com"],
    ]


def test_escapa_nombres_con_comas():
    texto = ReporteCSV().generar([Cliente("C1", "Pérez, Ana", "ana@correo.com")])

    assert list(csv.reader(io.StringIO(texto)))[1] == ["C1", "Pérez, Ana", "ana@correo.com"]


def test_el_servicio_usa_el_nuevo_formato_sin_modificarse():
    servicio = ServicioClientes(RepositorioClientesEnMemoria(), NotificadorEspia(), ReporteCSV())
    servicio.registrar(Cliente("C1", "Ana", "ana@correo.com"))

    assert servicio.reporte().splitlines() == ["id,nombre,email", "C1,Ana,ana@correo.com"]

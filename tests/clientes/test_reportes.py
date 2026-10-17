from clientes.cliente import Cliente
from clientes.reportes import ReporteTexto


def test_reporte_de_texto_lista_cada_cliente():
    clientes = [Cliente("C1", "Ana", "ana@correo.com"), Cliente("C2", "Luis", "luis@correo.com")]

    assert ReporteTexto().generar(clientes) == (
        "Clientes registrados: 2\n- C1: Ana <ana@correo.com>\n- C2: Luis <luis@correo.com>"
    )


def test_reporte_de_texto_sin_clientes():
    assert ReporteTexto().generar([]) == "No hay clientes registrados."

import pytest

from clientes.cliente import Cliente


def test_crea_cliente_valido_y_lo_muestra_por_nombre():
    cliente = Cliente("C1", "Ana Gómez", "ana@correo.com")

    assert cliente.mostrar() == "Ana Gómez"


@pytest.mark.parametrize("nombre", ["", "   "])
def test_rechaza_nombre_vacio(nombre):
    with pytest.raises(ValueError, match="nombre"):
        Cliente("C1", nombre, "ana@correo.com")


@pytest.mark.parametrize("email", ["ana.correo.com", "@correo.com", "ana@"])
def test_rechaza_correo_invalido(email):
    with pytest.raises(ValueError, match="Correo"):
        Cliente("C1", "Ana", email)


def test_rechaza_identificador_vacio():
    with pytest.raises(ValueError, match="identificador"):
        Cliente(" ", "Ana", "ana@correo.com")


def test_es_inmutable():
    cliente = Cliente("C1", "Ana", "ana@correo.com")

    with pytest.raises(AttributeError):
        cliente.nombre = "Otra"

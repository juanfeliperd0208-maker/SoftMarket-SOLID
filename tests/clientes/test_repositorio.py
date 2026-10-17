"""Prueba de contrato (LSP): todas las implementaciones se comportan igual."""

import pytest

from clientes.cliente import Cliente
from clientes.repositorio import (
    ClienteDuplicadoError,
    RepositorioClientesEnMemoria,
    RepositorioClientesJSON,
)

ANA = Cliente("C1", "Ana", "ana@correo.com")
LUIS = Cliente("C2", "Luis", "luis@correo.com")


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        return RepositorioClientesEnMemoria()
    return RepositorioClientesJSON(tmp_path / "clientes.json")


def test_guarda_y_busca_por_id(repositorio):
    repositorio.guardar(ANA)

    assert repositorio.buscar("C1") == ANA


def test_buscar_un_id_inexistente_devuelve_none(repositorio):
    assert repositorio.buscar("NO-EXISTE") is None


def test_lista_en_orden_de_registro(repositorio):
    repositorio.guardar(ANA)
    repositorio.guardar(LUIS)

    assert repositorio.listar() == [ANA, LUIS]


def test_rechaza_ids_duplicados(repositorio):
    repositorio.guardar(ANA)

    with pytest.raises(ClienteDuplicadoError):
        repositorio.guardar(Cliente("C1", "Otra persona", "otra@correo.com"))


def test_el_repositorio_json_conserva_los_datos_entre_instancias(tmp_path):
    ruta = tmp_path / "clientes.json"
    RepositorioClientesJSON(ruta).guardar(ANA)

    assert RepositorioClientesJSON(ruta).listar() == [ANA]

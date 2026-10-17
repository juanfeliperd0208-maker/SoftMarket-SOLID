"""Casos de uso de gestión de clientes.

ServicioClientes coordina, pero no guarda, no envía y no formatea: recibe
esas capacidades como abstracciones por su constructor (DIP). Por eso se
prueba sin base de datos ni servidor de correo.
"""

from __future__ import annotations

from clientes.cliente import Cliente
from clientes.notificaciones import Notificador
from clientes.reportes import GeneradorReporte
from clientes.repositorio import RepositorioClientes


class ServicioClientes:
    def __init__(
        self,
        repositorio: RepositorioClientes,
        notificador: Notificador,
        reporte: GeneradorReporte,
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador
        self._reporte = reporte

    def registrar(self, cliente: Cliente) -> None:
        self._repositorio.guardar(cliente)
        self._notificador.enviar(
            cliente.email,
            "Bienvenido a SoftMarket",
            f"Hola {cliente.nombre}, tu registro fue exitoso.",
        )

    def reporte(self) -> str:
        return self._reporte.generar(self._repositorio.listar())

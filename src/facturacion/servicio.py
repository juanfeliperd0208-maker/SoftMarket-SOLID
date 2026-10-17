"""Caso de uso «emitir factura».

El servicio coordina los pasos pero no implementa ninguno: depende solo de
abstracciones recibidas por el constructor (DIP), por eso se prueba sin base
de datos ni servidor de correo.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

from facturacion.calculadora import CalculadoraFactura
from facturacion.exportadores import ExportadorFactura
from facturacion.modelos import Cliente, Factura, ItemFactura
from facturacion.notificaciones import Notificador
from facturacion.repositorio import RepositorioFacturas


class GeneradorNumeroConsecutivo:
    def __init__(self, prefijo: str = "FAC", inicio: int = 1) -> None:
        self._prefijo = prefijo
        self._siguiente = inicio

    def __call__(self) -> str:
        numero = f"{self._prefijo}-{self._siguiente:06d}"
        self._siguiente += 1
        return numero


class ServicioFacturacion:
    def __init__(
        self,
        calculadora: CalculadoraFactura,
        repositorio: RepositorioFacturas,
        exportador: ExportadorFactura,
        notificador: Notificador,
        generar_numero: Callable[[], str],
    ) -> None:
        self._calculadora = calculadora
        self._repositorio = repositorio
        self._exportador = exportador
        self._notificador = notificador
        self._generar_numero = generar_numero

    def emitir(self, cliente: Cliente, items: Iterable[ItemFactura]) -> Factura:
        items = list(items)
        if not items:
            raise ValueError("Una factura debe tener al menos un ítem")

        factura = Factura(numero=self._generar_numero(), cliente=cliente, items=items)
        self._calculadora.calcular(factura)
        self._repositorio.guardar(factura)

        documento = self._exportador.exportar(factura)
        self._notificador.notificar(cliente.email, f"Factura {factura.numero}", documento)
        return factura

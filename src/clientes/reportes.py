"""Reportes de clientes (patrón Strategy: OCP).

Un formato nuevo se agrega como una clase nueva que implementa
GeneradorReporte; ni el servicio ni los otros formatos se modifican.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from clientes.cliente import Cliente


class GeneradorReporte(ABC):
    @abstractmethod
    def generar(self, clientes: list[Cliente]) -> str: ...


class ReporteTexto(GeneradorReporte):
    def generar(self, clientes: list[Cliente]) -> str:
        if not clientes:
            return "No hay clientes registrados."
        lineas = [f"Clientes registrados: {len(clientes)}"]
        lineas += [f"- {c.id}: {c.nombre} <{c.email}>" for c in clientes]
        return "\n".join(lineas)

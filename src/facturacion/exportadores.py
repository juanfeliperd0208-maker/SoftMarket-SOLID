"""Representaciones de una factura para el cliente (ISP + OCP)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from facturacion.modelos import Factura


class ExportadorFactura(ABC):
    @abstractmethod
    def exportar(self, factura: Factura) -> str:
        """Devuelve el documento de la factura listo para enviarse o guardarse."""


class ExportadorTexto(ExportadorFactura):
    def exportar(self, factura: Factura) -> str:
        lineas = [
            f"FACTURA {factura.numero}",
            f"Fecha: {factura.fecha.isoformat()}",
            f"Cliente: {factura.cliente.nombre}",
            "",
        ]
        for item in factura.items:
            lineas.append(f"{item.cantidad} x {item.descripcion}: {item.subtotal:.2f}")
        lineas += [
            "",
            f"Subtotal:  {factura.subtotal:.2f}",
            f"Descuento: {factura.descuento:.2f}",
            f"Impuesto:  {factura.impuesto:.2f}",
            f"TOTAL:     {factura.total:.2f}",
        ]
        return "\n".join(lineas)

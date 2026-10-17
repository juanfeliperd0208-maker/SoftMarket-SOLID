"""Reporte CSV: formato nuevo agregado sin modificar el código existente (OCP)."""

from __future__ import annotations

import csv
import io

from clientes.cliente import Cliente
from clientes.reportes import GeneradorReporte


class ReporteCSV(GeneradorReporte):
    def generar(self, clientes: list[Cliente]) -> str:
        salida = io.StringIO()
        escritor = csv.writer(salida, lineterminator="\n")
        escritor.writerow(["id", "nombre", "email"])
        escritor.writerows([c.id, c.nombre, c.email] for c in clientes)
        return salida.getvalue()

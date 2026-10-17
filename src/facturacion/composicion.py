"""Raíz de composición: el único lugar donde se eligen las clases concretas."""

from __future__ import annotations

import os
from decimal import Decimal

from facturacion.calculadora import CalculadoraFactura
from facturacion.descuentos import DescuentoPorcentual, DescuentoPorTipoCliente
from facturacion.exportadores import ExportadorTexto
from facturacion.impuestos import IVA
from facturacion.modelos import TipoCliente
from facturacion.notificaciones import NotificadorEmail
from facturacion.repositorio import RepositorioEnMemoria
from facturacion.servicio import GeneradorNumeroConsecutivo, ServicioFacturacion


def crear_servicio_facturacion() -> ServicioFacturacion:
    descuentos = DescuentoPorTipoCliente(
        {
            TipoCliente.FRECUENTE: DescuentoPorcentual(Decimal("5")),
            TipoCliente.MAYORISTA: DescuentoPorcentual(Decimal("12")),
        }
    )
    tasa_iva = Decimal(os.environ.get("SOFTMARKET_TASA_IVA", "0.19"))
    notificador = NotificadorEmail(
        servidor=os.environ["SOFTMARKET_SMTP_SERVIDOR"],
        puerto=int(os.environ.get("SOFTMARKET_SMTP_PUERTO", "587")),
        usuario=os.environ["SOFTMARKET_SMTP_USUARIO"],
        clave=os.environ["SOFTMARKET_SMTP_CLAVE"],
        remitente=os.environ["SOFTMARKET_SMTP_REMITENTE"],
    )
    return ServicioFacturacion(
        calculadora=CalculadoraFactura(descuentos, IVA(tasa_iva)),
        repositorio=RepositorioEnMemoria(),
        exportador=ExportadorTexto(),
        notificador=notificador,
        generar_numero=GeneradorNumeroConsecutivo(),
    )

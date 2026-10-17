"""Persistencia de clientes detrás de una abstracción (DIP, LSP).

Contrato que toda implementación debe cumplir (LSP):
- guardar() rechaza un id repetido con ClienteDuplicadoError;
- buscar() devuelve el cliente guardado o None si no existe;
- listar() devuelve los clientes en el orden en que se guardaron.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path

from clientes.cliente import Cliente


class ClienteDuplicadoError(Exception):
    pass


class RepositorioClientes(ABC):
    @abstractmethod
    def guardar(self, cliente: Cliente) -> None: ...

    @abstractmethod
    def buscar(self, id_cliente: str) -> Cliente | None: ...

    @abstractmethod
    def listar(self) -> list[Cliente]: ...


class RepositorioClientesEnMemoria(RepositorioClientes):
    def __init__(self) -> None:
        self._clientes: dict[str, Cliente] = {}

    def guardar(self, cliente: Cliente) -> None:
        if cliente.id in self._clientes:
            raise ClienteDuplicadoError(cliente.id)
        self._clientes[cliente.id] = cliente

    def buscar(self, id_cliente: str) -> Cliente | None:
        return self._clientes.get(id_cliente)

    def listar(self) -> list[Cliente]:
        return list(self._clientes.values())


class RepositorioClientesJSON(RepositorioClientes):
    """Guarda los clientes en un archivo JSON; sobrevive al cierre del programa."""

    def __init__(self, ruta: Path) -> None:
        self._ruta = Path(ruta)

    def _leer(self) -> list[dict[str, str]]:
        if not self._ruta.exists():
            return []
        return json.loads(self._ruta.read_text(encoding="utf-8"))

    def guardar(self, cliente: Cliente) -> None:
        datos = self._leer()
        if any(d["id"] == cliente.id for d in datos):
            raise ClienteDuplicadoError(cliente.id)
        datos.append({"id": cliente.id, "nombre": cliente.nombre, "email": cliente.email})
        self._ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    def buscar(self, id_cliente: str) -> Cliente | None:
        return next((c for c in self.listar() if c.id == id_cliente), None)

    def listar(self) -> list[Cliente]:
        return [Cliente(**d) for d in self._leer()]

# SoftMarket-SOLID

Proyecto académico de **Buenas Prácticas de Desarrollo de Software** (Parcial 2:
«Refactorizando el Caos en SoftMarket»). Implementa los módulos de gestión de
clientes y facturación aplicando los principios SOLID, Conventional Commits,
Git Flow simplificado, pruebas unitarias e integración continua.

## Estructura

```
src/
  clientes/       Entidad Cliente, repositorios, notificaciones, reportes y servicio
  facturacion/    Descuentos, impuestos, calculadora, repositorio, exportador y servicio
tests/
  clientes/       Pruebas de la entidad, contrato de repositorios, reportes y servicio
  facturacion/    Pruebas de modelos, descuentos, calculadora y servicio
.github/
  workflows/ci.yml           Pruebas y estilo en cada pull request
  pull_request_template.md   Lista de verificación de cada PR
```

## Ejecutar en local

```bash
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt

pytest -v --cov                   # pruebas con cobertura (mínimo 80 %)
ruff check . && ruff format --check .
```

## Flujo de trabajo

- `main`: versiones estables, etiquetadas (`v1.0.0`).
- `develop`: integración de funcionalidades.
- `feature/<nombre>`: una funcionalidad por rama; se integra en `develop` por pull request.

Cada pull request debe pasar el CI (ruff + pytest) y tener al menos una
aprobación de otro integrante antes de fusionarse. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

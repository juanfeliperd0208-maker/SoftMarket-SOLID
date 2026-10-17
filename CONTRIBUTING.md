# Guía de contribución

## Ramas (Git Flow simplificado)

| Rama               | Sale de   | Se integra en | Regla                                        |
|--------------------|-----------|---------------|----------------------------------------------|
| `main`             | —         | —             | Solo versiones estables; cada versión lleva tag |
| `develop`          | `main`    | `main`        | Integración; protegida                       |
| `feature/<nombre>` | `develop` | `develop`     | Una funcionalidad; vida corta                |

Nadie hace push directo a `main` ni a `develop`: todo entra por pull request.

## Commits (Conventional Commits)

```
<tipo>(<alcance>): <descripción en imperativo>
```

Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `ci`, `chore`.
Ejemplo: `feat(clientes): validar el correo del cliente`.

## Pull requests

1. Actualizar la rama: `git pull origin develop` (o `git rebase origin/develop`).
2. Ejecutar `pytest` y `ruff check .` en local.
3. Abrir el PR hacia `develop` completando la plantilla.
4. Esperar el CI en verde y la aprobación de otro integrante.
5. Fusionar con *Create a merge commit* y borrar la rama.

## Conflictos

Quien abre el PR resuelve el conflicto en su rama: `git pull origin develop`,
editar los archivos marcados, ejecutar las pruebas, `git add` y `git commit`.
Nunca se usa `git push --force` sobre `main` o `develop`.

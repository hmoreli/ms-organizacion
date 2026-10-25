# ms-organizacion

Microservicio de Localización y Organización. Catálogos compartidos: países, departamentos, ciudades, barrios, sectores, cargos (con salario base) y tipos de contrato.

Implementa el contrato [`contrato/openapi.yaml`](contrato/openapi.yaml) con FastAPI, SQLAlchemy 2 y Alembic sobre PostgreSQL (schema `organizacion`).

## Respecto al contrato

- `Pais` suma `codigo_iso` y `gentilicio` (opcionales), que estaban en el ScriptBD.sql.
- Los listados aceptan `?limit=&offset=` y filtros por el padre (`/cargos?sector_id=`, `/departamentos?pais_id=`, etc.).
- No se puede borrar un registro en uso (por ejemplo un país con departamentos): responde 409.

## Desarrollo

Este repo usa `rrhh-common`, que tiene que estar clonado al lado:

```
rrhh/
├── rrhh-common/
├── rrhh-plataforma/
└── ms-organizacion/
```

```bash
python -m venv .venv && . .venv/bin/activate
pip install "../rrhh-common[db]" -e ".[dev]"
pytest              # usa SQLite en memoria, no necesita la plataforma
ruff check app tests && ruff format --check app tests
```

## Levantar con la plataforma

```bash
cd ../rrhh-plataforma && docker compose up -d
cd ../ms-organizacion && docker compose up -d --build
```

Al arrancar, el contenedor aplica las migraciones (`alembic upgrade head`) en el schema `organizacion`. Queda accesible solo por Kong en `http://localhost:8000/api/organizacion/...` con un token de Keycloak. La documentación interactiva está en `/api/organizacion/docs` (también detrás del gateway).

## Migraciones

```bash
export DATABASE_URL=postgresql+psycopg://ms_organizacion:servicio-dev@localhost:5432/rrhh
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head
```

## Roles

Lectura: `rrhh-operador`, `nomina-liquidador`, `consulta`. Escritura: `rrhh-operador`. `rrhh-admin` puede todo.

## CI

GitHub Actions corre ruff y pytest. Como `rrhh-common` es privado, el repo necesita el secreto **`RRHH_COMMON_TOKEN`**: un token *fine-grained* con permiso `Contents: read` sobre `hmoreli/rrhh-common`.

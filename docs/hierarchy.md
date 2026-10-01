# File and Directory Hierarchy

## Backend (Python/FastAPI - Hexagonal)
- `src/`
  - `domain/`: Modelos de negocio, entidades y excepciones core.
  - `application/`: Casos de uso, puertos de entrada/salida (interfaces).
  - `infrastructure/`
    - `adapters/`: Implementaciones de persistencia (SQLAlchemy), mensajería (Meta, Telegram, Email) y clientes externos.
    - `web/`: Controladores FastAPI, routers, esquemas Pydantic (DTOs).
    - `config/`: Gestión de variables de entorno y settings por ambiente.
- `migrations/`: Archivos de migración de base de datos (Alembic).
- `tests/`: Suite de pruebas unitarias, integración y funcionales.

## Frontend (TypeScript/React)
- `src/`
  - `api/`: Clientes y hooks de comunicación con el backend (React Query).
  - `components/`
    - `presentational/`: UI pura, átomos y moléculas.
    - `containers/`: Orquestación de lógica y estado de pantallas.
  - `hooks/`: Lógica compartida de UI.
  - `store/`: Estado global si aplica.
  - `types/`: Definiciones TypeScript compartidas.
- `public/`: Assets estáticos.

## Root
- `docs/`: Memoria del proyecto.
- `.env.example`: Plantilla de variables de entorno.
- `docker-compose.yml`: Configuración de servicios locales (DB, Redis, App).

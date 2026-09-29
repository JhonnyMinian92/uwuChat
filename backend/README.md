# uwuChat Backend

Backend desarrollado con Python 3.12 y FastAPI siguiendo los principios de Arquitectura Hexagonal.

## Estructura de Carpetas

- `src/domain`: Entidades de negocio y reglas de dominio puras.
- `src/application`: Casos de uso de la aplicación.
- `src/ports`: Interfaces (contratos) para adaptadores de entrada y salida.
- `src/adapters/inbound`: Controladores REST, WebSockets, CLI.
- `src/adapters/outbound`: Implementaciones de persistencia, clientes de APIs externas (Meta, Telegram, etc).

## Desarrollo

Requisitos: Docker y Docker Compose.

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

# File and Directory Hierarchy

## Backend (FastAPI)
- `app/` 
  - `domain/`: Entidades de negocio (Message, Conversation, Customer) y lógica pura.
  - `application/`: Casos de uso (SendMessage, RouteMessage, MergeCustomers).
  - `ports/`: Definición de interfaces (RepositoryInterface, ChannelAdapterInterface).
  - `adapters/` 
    - `inbound/`: Controladores REST, Webhooks y sus validadores de firma.
    - `outbound/`: Implementación de base de datos (SQLAlchemy/Tortoise) y clientes de APIs (Meta, Telegram).
  - `workers/`: Tareas de Celery para sondeo IMAP y envío asíncrono.
  - `core/`: Configuración, seguridad (JWT), cifrado y middleware de tenant.

## Frontend (React + TS)
- `src/` 
  - `api/`: Cliente de servicios y configuración de WebSockets.
  - `components/` 
    - `layout/`: Estructura general de la bandeja.
    - `chat/`: Burbujas de mensaje, input, lista de conversaciones.
    - `admin/`: Paneles de configuración de canales y métricas.
  - `hooks/`: Gestión de estado local y suscripciones a tiempo real.
  - `types/`: Definiciones TypeScript compartidas.

# Gemini Initial Plan

Análisis inicial completado para uwuChat. Se ha estructurado el plan de implementación basado en arquitectura hexagonal, FastAPI para el backend, React 18 para el frontend, y adaptadores para la unificación de canales de mensajería (WhatsApp, Messenger, Instagram, Telegram, Discord, Email).

## Changes

- Uso de FastAPI (Python 3.12) para la API REST, manejo de webhooks e integración con canales.
- Uso de React 18 con TypeScript para la interfaz web unificada.
- Implementación de arquitectura hexagonal y patrones de repositorio, adaptador y estrategia.

## Tasks

- **T1** Configuración del proyecto backend con FastAPI y estructura hexagonal
  - Historia: Infraestructura Base Backend
  - Inicializar el repositorio backend con Python 3.12 y FastAPI, configurando la estructura de carpetas siguiendo la arquitectura hexagonal (domain, application, ports, adapters/inbound, adapters/outbound). Configurar dependencias, linter y tipado estricto.
  - [ ] El servidor levanta correctamente con Uvicorn.
  - [ ] La estructura de directorios respeta los principios de arquitectura hexagonal.
  - [ ] El entorno de desarrollo está completamente documentado y funcional.
- **T2** Diseño y migración de base de datos multi-tenant (depende de: T1)
  - Historia: Gestión de Datos y Tenants
  - Configurar la conexión a la base de datos con gestión de transacciones explícitas (Explicit Transaction Boundary) y concurrencia optimista (Optimistic Concurrency). Definir los modelos de datos para Empresas, Usuarios, Canales, Contactos, Conversaciones y Mensajes asegurando el aislamiento estricto de datos entre tenants.
  - [ ] Los modelos reflejan las relaciones requeridas sin fugas de datos entre empresas.
  - [ ] Se implementan migraciones de base de datos automatizadas.
  - [ ] Se aplican restricciones de aislamiento por tenant en las consultas.
- **T3** Implementación del módulo de autenticación y autorización JWT (depende de: T2)
  - Historia: Seguridad y Accesos
  - Crear el sistema de autenticación basado en JWT con control de acceso basado en roles (RBAC) para administrador de empresa, supervisor y agente de atención, aplicando el principio de defensa en profundidad.
  - [ ] Endpoints de login y emisión de tokens seguros.
  - [ ] Middleware de validación de roles y aislamiento por empresa operativo.
  - [ ] Pruebas unitarias para los flujos de autenticación.
- **T4** Desarrollo del motor de adaptadores de canales de mensajería (depende de: T3)
  - Historia: Integración de Canales
  - Implementar el patrón Strategy y Adapter para unificar la recepción y envío de mensajes de WhatsApp Cloud API, Facebook Messenger, Instagram Messaging, Telegram Bot API, Discord bot y correo IMAP/SMTP mediante una interfaz común.
  - [ ] Normalización correcta de mensajes entrantes de cada canal a un modelo común.
  - [ ] Cifrado seguro de credenciales de canales en la base de datos.
  - [ ] Manejo de webhooks verificados por firma criptográfica.
- **T5** Construcción de la bandeja unificada en React 18 (depende de: T3)
  - Historia: Frontend y Bandeja Unificada
  - Desarrollar la interfaz web en React 18 con TypeScript utilizando componentes contenedores y presentacionales. Incluir lista de conversaciones, filtros avanzados (modern filters), buscador con debounce y comunicación en tiempo real mediante WebSockets.
  - [ ] Renderizado fluido de la bandeja con WebSockets integrados para mensajes en tiempo real.
  - [ ] Filtros combinables y buscador operativos con manejo de estado vacío.
  - [ ] Uso correcto de Skeleton loading para la carga de datos.
- **T6** Panel de administración y métricas por empresa (depende de: T4, T5)
  - Historia: Administración y Métricas
  - Implementar las vistas y endpoints para la gestión de canales, agentes, horarios de atención, respuestas rápidas y el tablero de métricas de rendimiento (tiempo de primera respuesta, resolución, volumen).
  - [ ] CRUD completo de configuración empresarial y agentes desde la UI.
  - [ ] Cálculo preciso de métricas por empresa, canal y agente.
  - [ ] Pruebas de integración para los flujos administrativos.

## Tests

- Pruebas unitarias de dominio para validar la lógica de enrutamiento y normalización de mensajes.
- Pruebas de integración para verificar el aislamiento estricto de datos entre tenants en la base de datos.
- Pruebas de seguridad para validar la verificación de firmas en webhooks de Meta y Telegram.
- Pruebas end-to-end de la bandeja de chat en tiempo real con WebSockets.

## Rationale

- Se ha validado la viabilidad técnica utilizando FastAPI para la concurrencia asíncrona requerida por los webhooks y React 18 para la interfaz de usuario en tiempo real.
- La arquitectura hexagonal garantiza el desacoplamiento de los proveedores de mensajería externos.

## Assumptions

- Se asume que las credenciales de acceso a las APIs de Meta, Telegram y Discord serán provistas mediante variables de entorno o configuración cifrada por empresa.

## Memory changes

- Aplicado: architecture/hierarchy.md — Definición completa de la jerarquía de archivos y estructura del proyecto para FastAPI y React.

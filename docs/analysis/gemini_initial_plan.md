# Gemini Initial Plan

Análisis inicial completado y validado. El mapa de producto cubre todos los requisitos funcionales, de seguridad, arquitectura hexagonal y perfiles de producción requeridos para uwuChat, incorporando la política de retención de 72 horas con logs permanentes y la gestión de plantillas HSM.

## Changes

- Alineación formal del esquema de base de datos multi-tenant para reflejar la tabla audit_logs permanente y hsm_templates.
- Definición de módulos de construcción estructurados para abarcar cimientos, adaptadores de canales, bandeja web y características de producción.

## Mapa del producto

Mnemosine planifica todas las tareas de cada módulo después de este análisis (analysis/product_plan.md).

- **M1** Cimientos y Esqueleto del Proyecto (foundation)
  - Establecer la estructura de repositorios con arquitectura hexagonal, configuración por ambiente, tests automatizados básicos y arranque de salud.
  - Requisitos de producción: PRD-QA-01, PRD-SEC-01, PRD-DEP-04, PRD-DEP-05
- **M2** Capa de Datos Transaccionales y Autenticación (foundation)
  - Configurar la base de datos PostgreSQL local con migraciones versionadas, aislamiento multi-tenant y autenticación JWT con roles.
  - Requisitos de producción: PRD-DATA-01, PRD-DATA-05, WEB-SEC-02, API-02
- **M3** Motor de Canales de Mensajería y Webhooks (feature)
  - Implementar el patrón Strategy y Adapter para unificar la recepción y envío de mensajes vía WhatsApp, Messenger, Instagram, Telegram y Discord.
  - Requisitos de producción: PRD-SEC-03, API-01
- **M4** Procesamiento Asíncrono y Correo IMAP/SMTP (feature)
  - Configurar Celery y Redis para el sondeo periódico de buzones IMAP y envíos SMTP, asegurando la retención de mensajes por 72 horas y logs permanentes.
  - Requisitos de producción: PRD-OPS-01
- **M5** Bandeja Unificada y WebSocket en Tiempo Real (feature)
  - Desarrollar la interfaz en React 18 con WebSocket para la atención de clientes en tiempo real, aplicando filtros avanzados, buscadores y skeleton loading.
  - Requisitos de producción: WEB-UX-01, WEB-UX-03, WEB-PERF-01
- **M6** Fusión de Identidades y Gestión de Contactos (feature)
  - Permitir la unificación de identidades técnicas de un mismo cliente en múltiples canales hacia un único perfil de Customer.
  - Requisitos de producción: API-04
- **M7** Panel de Administración y Métricas de Negocio (feature)
  - Construir el panel para gestión de horarios, respuestas rápidas, canales cifrados y el tablero de métricas de rendimiento por agente y canal.
  - Requisitos de producción: PRD-SEC-01
- **M8** Endurecimiento de Producción y Operaciones (production)
  - Asegurar la preparación final para producción mediante cabeceras de seguridad, despliegue reproducible, respaldos probados y documentación completa.
  - Requisitos de producción: PRD-QA-02, PRD-SEC-02, PRD-DATA-03, PRD-DEP-01, PRD-DEP-02, PRD-DEP-03, PRD-DEP-06, WEB-SEC-01

## Tasks

- Se planifican por módulo.

## Tests

- Pruebas de aislamiento multi-tenant: Verificar que usuarios de Empresa A no pueden acceder a datos, mensajes ni conversaciones de Empresa B vía API o WebSockets.
- Pruebas de retención y purgado (72h): Verificar que la tarea de limpieza elimina mensajes y adjuntos activos tras 72 horas y que estos pueden reconstruirse desde audit_logs.
- Pruebas de verificación criptográfica: Comprobar rechazo de webhooks con firma HMAC inválida para Meta y token erróneo en Telegram.
- Pruebas de plantillas WhatsApp (HSM): Validar el bloqueo de mensajes libres fuera de las 24 horas y permitir el despacho exitoso mediante plantilla aprobada.
- Pruebas de concurrencia y asignación: Validar la asignación de conversaciones usando Optimistic Concurrency para prevenir sobrescrituras entre agentes.

## Rationale

- El mapa de producto se ha desglosado en 8 módulos coherentes que van desde los cimientos y la base de datos hasta la bandeja unificada, la gestión de identidades y el endurecimiento para producción.
- Todas las tareas pendientes actuales se alinean perfectamente con los módulos planificados sin duplicidades.
- No quedan preguntas pendientes ni bloqueantes.

## Assumptions

- Se asume que el despliegue local y de desarrollo utilizará contenedores Docker con PostgreSQL y Redis.

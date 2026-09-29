# Gemini Initial Plan

Preparación y gobierno del proyecto uwuChat finalizada con éxito. Se preservan las tareas pendientes requeridas alineadas a la arquitectura hexagonal, patrones de concurrencia y límites transaccionales. El modelo de datos en contracts/schemas/database.json y database.md se mantiene consistente incorporando la política de purgado y retención a 72 horas con persistencia permanente en audit_logs, junto con el soporte de plantillas HSM para WhatsApp.

## Changes

- Alineación formal del esquema de base de datos en database.json y database.md reflejando la tabla audit_logs inmutable y la tabla hsm_templates para WhatsApp fuera de la ventana de 24 horas.
- Reflejo de la política de retención de 72 horas para mensajes y adjuntos activos con purga automática y respaldo estructurado en logs de auditoría permanentes.

## Tasks

- **T4** Desarrollo del motor de adaptadores de canales de mensajería
  - Historia: Integración de Canales
  - Implementar en el backend (FastAPI, Python 3.12) el patrón Strategy y Adapter para unificar la recepción y envío de mensajes multicanal (WhatsApp Cloud API, Messenger, Instagram Messaging, Telegram Bot API, Discord bot). Validar firmas criptográficas (Meta X-Hub-Signature-256, secreto de Telegram) y procesar mensajes entrantes de forma idempotente con deduplicación por provider_msg_id. Incluir soporte para envío de plantillas genéricas (HSM) de WhatsApp para conversaciones fuera de la ventana de 24 horas.
  - [ ] Adaptadores funcionales y desacoplados para WhatsApp, Facebook Messenger, Instagram, Telegram y Discord siguiendo arquitectura hexagonal.
  - [ ] Validación estricta de firmas criptográficas en webhooks de entrada rechazando peticiones con firma inválida.
  - [ ] Normalización de mensajes entrantes (texto, imágenes, audio y archivos adjuntos) al contrato de dominio unificado.
  - [ ] Deduplicación idempotente usando provider_msg_id.
  - [ ] Soporte para el envío de plantillas HSM preaprobadas cuando se supere la ventana de 24 horas de WhatsApp.
- **T7** Infraestructura asíncrona y procesamiento de correo IMAP (depende de: T4)
  - Historia: Canal de Correo y Resiliencia
  - Configurar infraestructura asíncrona con Celery y Redis para el sondeo periódico de buzones de correo por IMAP y el envío mediante SMTP. Implementar reintentos con backoff exponencial para llamadas a proveedores externos. Implementar la tarea periódica de purgado para eliminar mensajes y archivos adjuntos con más de 72 horas del almacenamiento activo, garantizando la persistencia del histórico completo estructurado en la tabla audit_logs.
  - [ ] Worker Celery configurado con sondeo IMAP periódico que extrae mensajes y adjuntos y los normaliza en conversaciones.
  - [ ] Mecanismo de envío SMTP con reintentos bounded backoff ante fallos transitorios.
  - [ ] Tarea periódica de purgado que elimina mensajes y adjuntos activos de más de 72 horas preservando registros estructurados inmutables en audit_logs.
  - [ ] Consulta eficiente de auditoría por rangos de fechas y usuario para reconstrucción histórica.
- **T5** Construcción de la bandeja unificada en React 18 (depende de: T7)
  - Historia: Bandeja de Entrada
  - Construir en React 18 con TypeScript la bandeja de entrada unificada de atención al cliente. Implementar conexión en tiempo real con WebSockets (FastAPI + Redis Pub/Sub) para recibir y enviar mensajes instantáneamente. Integrar lista de conversaciones con filtros combinables (por canal, estado y agente), buscador con debounce de 300ms, y skeleton loading durante la carga de conversaciones. Asegurar el aislamiento estricto de datos por tenant en la interfaz.
  - [ ] Bandeja de entrada web unificada con visualización y envío en tiempo real vía WebSocket.
  - [ ] Buscador de conversaciones y contactos con debounce de 300ms y resaltado de coincidencias.
  - [ ] Filtros modernos combinables reflejando estado y aislamiento visual garantizado por tenant.
  - [ ] Skeleton loading visible durante la obtención de conversaciones y mensajes.
  - [ ] Advertencia visual en la UI cuando una conversación de WhatsApp supere la ventana de 24 horas, habilitando selector de plantillas HSM.
- **T8** Lógica de fusión de identidades y gestión de contactos (depende de: T5)
  - Historia: Gestión de Contactos
  - Implementar el servicio de dominio y los endpoints para gestionar clientes y contactos técnicos multicanal. Permitir la vinculación y fusión (merge) de múltiples registros de 'contacts' (canal + id externo) a un único registro de 'customers'. Garantizar que las fusiones sólo puedan realizarse entre contactos pertenecientes a la misma empresa (tenant) y actualizar las conversaciones asociadas de forma consistente dentro de una transacción explícita.
  - [ ] Mapeo de múltiples contactos (WhatsApp, Telegram, correo, etc.) a un único Customer dentro del mismo tenant.
  - [ ] Endpoint transaccional para fusionar identidades con validación de aislamiento multi-tenant.
  - [ ] Visualización del historial unificado de mensajes en la vista de cliente fusionado.
  - [ ] Manejo de concurrencia optimista para evitar condiciones de carrera durante la fusión simultánea.
- **T6** Panel de administración y métricas por empresa (depende de: T5)
  - Historia: Administración y Business Intelligence
  - Desarrollar el panel de administración multi-tenant en React y FastAPI. Permitir la gestión de canales (registro de credenciales cifradas), configuración de horarios de atención con mensajes automáticos fuera de horario, CRUD de respuestas rápidas y gestión del catálogo de plantillas HSM. Crear el dashboard de métricas calculando tiempo de primera respuesta, tiempo de resolución y volumen de conversaciones por canal y por agente.
  - [ ] CRUD seguro para configuración de canales con credenciales cifradas en reposo.
  - [ ] Configuración de horarios de atención y envío automático de mensajes fuera de horario.
  - [ ] Gestión de respuestas rápidas y catálogo de plantillas HSM aprobadas para agentes.
  - [ ] Dashboard con métricas de tiempo de primera respuesta, tiempo de resolución y volumen por agente/canal filtrable por rango de fechas.

## Tests

- Pruebas de aislamiento multi-tenant: Verificar que usuarios de Empresa A no pueden acceder a datos, mensajes ni conversaciones de Empresa B vía API o WebSockets.
- Pruebas de retención y purgado (72h): Verificar que la tarea de limpieza elimina mensajes y adjuntos activos tras 72 horas y que estos pueden reconstruirse desde audit_logs.
- Pruebas de verificación criptográfica: Comprobar rechazo de webhooks con firma HMAC inválida para Meta y token erróneo en Telegram.
- Pruebas de plantillas WhatsApp (HSM): Validar el bloqueo de mensajes libres fuera de las 24 horas y permitir el despacho exitoso mediante plantilla aprobada.
- Pruebas de concurrencia y asignación: Validar la asignación de conversaciones usando Optimistic Concurrency para prevenir sobrescrituras entre agentes.

## Rationale

- Se preservan de forma idéntica los títulos de las 5 tareas PENDING existentes en current_tasks sin repetir las tareas ya completadas.
- Las respuestas a Q1 (retención 72h con respaldo permanente en audit_logs) y Q2 (plantillas HSM genéricas) han sido incorporadas formalmente en los contratos de base de datos y criterios de aceptación.
- El estatus es READY dado que no existen preguntas bloqueantes ni ambigüedades pendientes para iniciar la ejecución.

## Warnings

- El purgado periódico de mensajes a las 72 horas debe ejecutarse por lotes controlados para evitar bloqueos en la base de datos de producción.
- Las llamadas salientes a la API de WhatsApp deben verificar la ventana de 24 horas antes de intentar enviar texto libre para evitar penalizaciones del proveedor.

## Assumptions

- Se asume el uso de Redis como message broker para Celery y capa Pub/Sub para la distribución de eventos WebSocket.
- Se asume que el cifrado de credenciales de canales se realiza a nivel de aplicación con AES-256-GCM antes de persistir en PostgreSQL.

## Memory changes

- Aplicado: contracts/schemas/database.md — Actualización de la documentación Markdown del esquema de base de datos para concordar exactamente con database.json y reflejar las reglas de retención y plantillas.
- Aplicado: architecture/hierarchy.md — Completar la jerarquía de directorios requerida según la arquitectura hexagonal, FastAPI y React 18 seleccionados.
- Rechazado: contracts/schemas/database.json — un JSON no se puede anexar: envía el documento completo

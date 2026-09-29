# Gemini Final Plan

Proyecto reanalizado tras incorporar las respuestas del usuario sobre la política de retención de mensajes y archivos adjuntos (72 horas con respaldo permanente en logs estructurados) y la generación y aprobación de plantillas (HSM) para WhatsApp. Se actualizan las tareas pendientes y el esquema de base de datos.

## Changes

- Se incorpora formalmente la política de retención de 72 horas para adjuntos y mensajes con persistencia de logs de auditoría estructurados.
- Se añade el flujo de gestión y envío de plantillas genéricas (HSM) para WhatsApp fuera de la ventana de 24 horas.

## Tasks

- **T4** Desarrollo del motor de adaptadores de canales de mensajería
  - Historia: Integración de Canales
  - Implementar el patrón Strategy y Adapter en el backend para unificar la recepción y envío de mensajes. Incluir validadores de firma para Meta y Telegram, normalización de adjuntos y soporte para envío de plantillas genéricas (HSM) de WhatsApp para la gestión fuera de la ventana de 24 horas.
  - [ ] Adaptadores funcionales para WhatsApp, Telegram y Discord.
  - [ ] Validación de firmas criptográficas en webhooks de entrada.
  - [ ] Normalización de adjuntos a estructura común.
  - [ ] Gestión de envío de plantillas de WhatsApp (HSM) para flujos fuera de la ventana de 24 horas.
- **T7** Infraestructura asíncrona y procesamiento de correo IMAP (depende de: T4)
  - Historia: Canal de Correo y Resiliencia
  - Configurar Celery con Redis para el sondeo periódico de buzones IMAP y envío SMTP. Incluir lógica de reintentos con backoff exponencial y el registro estructurado de logs que garantice la trazabilidad permanente sin purgar metadatos históricos.
  - [ ] Sondeo IMAP funcional recuperando correos no leídos.
  - [ ] Cola de tareas para envío saliente con reintentos robustos.
  - [ ] Estructura de logs permanente para auditoría y recuperación por rangos de fecha y usuario.
- **T5** Construcción de la bandeja unificada en React 18 (depende de: T7)
  - Historia: Bandeja de Entrada
  - Desarrollar la interfaz de chat en tiempo real utilizando WebSockets (FastAPI + Redis Pub/Sub). Implementar componentes de lista de conversaciones, buscador con debounce y filtros avanzados según los patrones de diseño seleccionados, aplicando purgado automático de datos efímeros según la regla de 72 horas.
  - [ ] Mensajes entrantes aparecen instantáneamente sin refrescar.
  - [ ] Buscador filtra contactos y mensajes con debounce de 300ms.
  - [ ] Skeleton loading aplicado durante la carga inicial.
  - [ ] Aislamiento estricto de datos entre tenants.
- **T8** Lógica de fusión de identidades y gestión de contactos (depende de: T5)
  - Historia: Gestión de Contactos
  - Implementar el servicio de dominio para vincular múltiples 'Contactos' a un único 'Cliente' (Customer) mediante reglas de negocio o intervención manual, permitiendo unificar identidades en múltiples canales.
  - [ ] Posibilidad de unir un contacto de WhatsApp y uno de Telegram en un mismo perfil.
  - [ ] Historial unificado de mensajes en la vista de cliente fusionado.
  - [ ] Validación de pertenencia al mismo tenant.
- **T6** Panel de administración y métricas por empresa (depende de: T5)
  - Historia: Administración y Business Intelligence
  - Crear el dashboard de métricas calculando tiempos de respuesta y volúmenes. Implementar la configuración de empresa: horarios, respuestas rápidas y gestión del catálogo de plantillas HSM.
  - [ ] Gráficos de volumen de mensajes por canal/agente.
  - [ ] Configuración de horario de atención y respuestas automáticas.
  - [ ] Gestión de respuestas rápidas y plantillas en la bandeja.

## Tests

- Pruebas de aislamiento de base de datos: Verificar que el usuario de una empresa no puede leer datos de otra.
- Pruebas de retención y purgado: Comprobar que los mensajes y adjuntos superadas las 72 horas son eliminados del almacenamiento activo pero persisten en los logs estructurados de auditoría.
- Pruebas de plantillas WhatsApp (HSM): Validar el comportamiento de envío fuera de la ventana de 24 horas usando plantillas genéricas.
- Pruebas de concurrencia y conflictos en la asignación de conversaciones.

## Rationale

- Todas las preguntas pendientes han sido respondidas satisfactoriamente, por lo que no quedan bloqueos para la activación.
- Se incorpora la política de retención de 72 horas junto con una tabla de logs de auditoría persistentes que garantizan la recuperabilidad requerida.
- Se incluye el soporte y la gestión para la aprobación y uso de plantillas HSM.

## Warnings

- Asegurar que la tarea de purgado automático de mensajes a las 72 horas esté configurada correctamente en background para evitar saturación.

## Assumptions

- Se asume que los logs estructurados permanentes se almacenarán de forma segura en la base de datos o en un almacén de logs asociado al tenant.

## Memory changes

- Aplicado: contracts/schemas/database.json — Actualización del esquema de base de datos para incorporar la tabla de logs permanentes de auditoría y la gestión de plantillas HSM.

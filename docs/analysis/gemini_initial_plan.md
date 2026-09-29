# Gemini Initial Plan

Análisis de preparación para uwuChat completado. Se han mantenido las tareas pendientes prioritarias y se han añadido tareas críticas para la infraestructura de tiempo real (WebSockets) y el procesamiento asíncrono necesario para el sondeo de correos y reintentos de webhooks. Se define el esquema de base de datos multi-tenant detallado para asegurar el aislamiento estricto.

## Changes

- Incorporación de Redis como broker para Celery (procesamiento de correos IMAP y reintentos) y como Pub/Sub para WebSockets.
- Definición explícita del modelo de fusión de identidades (Customer vs Contact) en la base de datos.
- Refuerzo del esquema de seguridad para el cifrado de credenciales de canales (Requirement 3).

## Tasks

- **T4** Desarrollo del motor de adaptadores de canales de mensajería
  - Historia: Integración de Canales
  - Implementar el patrón Strategy y Adapter en el backend para unificar la recepción y envío de mensajes. Debe incluir validadores de firma para Meta (X-Hub-Signature-256) y Telegram. Los adaptadores deben normalizar los payloads a un esquema de mensaje interno común.
  - [ ] Adaptadores funcionales para WhatsApp, Telegram y Discord.
  - [ ] Validación de firmas criptográficas en webhooks de entrada.
  - [ ] Normalización de adjuntos (imágenes, audio) a una estructura común.
  - [ ] Uso de Idempotency Key basada en el ID de mensaje del proveedor externo.
- **T7** Infraestructura asíncrona y procesamiento de correo IMAP (depende de: T4)
  - Historia: Canal de Correo y Resiliencia
  - Configurar Celery con Redis para el sondeo periódico de buzones IMAP y el envío SMTP. Implementar lógica de reintentos con backoff exponencial para fallos en las APIs de los proveedores.
  - [ ] Sondeo IMAP funcional recuperando correos no leídos.
  - [ ] Cola de tareas para envío de mensajes salientes.
  - [ ] Mecanismo de reintento observable en logs ante fallos de red con proveedores.
- **T5** Construcción de la bandeja unificada en React 18 (depende de: T7)
  - Historia: Bandeja de Entrada
  - Desarrollar la interfaz de chat en tiempo real utilizando WebSockets (FastAPI + Redis Pub/Sub). Implementar componentes de lista de conversaciones, buscador con debounce y filtros avanzados según los patrones de diseño seleccionados.
  - [ ] Mensajes entrantes aparecen instantáneamente sin refrescar.
  - [ ] Buscador filtra contactos y mensajes con debounce de 300ms.
  - [ ] Skeleton loading aplicado durante la carga inicial de conversaciones.
  - [ ] Aislamiento visual: un agente solo ve datos de su propia empresa.
- **T8** Lógica de fusión de identidades y gestión de contactos (depende de: T5)
  - Historia: Gestión de Contactos
  - Implementar el servicio de dominio para vincular múltiples 'Contactos' (canal+id) a un único 'Cliente' (Customer) mediante reglas de negocio o intervención manual del agente.
  - [ ] Posibilidad de unir un contacto de WhatsApp y uno de Telegram en un mismo perfil.
  - [ ] Historial unificado de mensajes en la vista de cliente fusionado.
  - [ ] Validación de que ambos contactos pertenecen a la misma empresa (tenant).
- **T6** Panel de administración y métricas por empresa (depende de: T5)
  - Historia: Administración y Business Intelligence
  - Crear el dashboard de métricas calculando tiempos de respuesta y volúmenes. Implementar la gestión de configuración de empresa: horarios, respuestas rápidas y roles de usuario.
  - [ ] Gráficos de volumen de mensajes por canal/agente.
  - [ ] Configuración de horario de atención reflejada en mensajes automáticos.
  - [ ] CRUD de respuestas rápidas funcional en la bandeja de chat.

## Tests

- Pruebas de aislamiento de base de datos: Verificar que el usuario A de Empresa 1 no puede leer mensajes de Empresa 2 mediante manipulación de IDs.
- Pruebas de firma de Webhooks: Simular payloads de Meta con firmas correctas e incorrectas.
- Pruebas de concurrencia: Dos agentes intentando asignar la misma conversación simultáneamente (Optimistic Concurrency).
- Pruebas de integración IMAP: Verificar que correos con adjuntos pesados se procesan y normalizan correctamente.

## Rationale

- Se mantienen las tareas PENDING originales pero se detallan para incluir los patrones de diseño seleccionados (Adapter, Strategy).
- La inclusión de Redis es necesaria tanto para la escalabilidad de WebSockets como para la gestión de tareas asíncronas de IMAP.
- El esquema de base de datos separa 'Contact' de 'Customer' para satisfacer el Requirement 5 de fusión de identidades.
- Se omite la creación de tareas completadas (T1, T2, T3) para centrar el esfuerzo en lo restante.

## Warnings

- La ventana de 24h de WhatsApp requiere un manejo de errores específico para notificar al agente que no puede responder sin plantillas.
- El sondeo IMAP puede ser ineficiente si no se gestionan bien los flags de 'leído/no leído' en buzones con mucho tráfico.

## Assumptions

- Se asume el uso de Redis para colas y WebSockets dada la naturaleza en tiempo real del proyecto.
- Se asume que el cifrado de credenciales se realizará a nivel de aplicación antes de persistir en la DB.

## Memory changes

- Aplicado: contracts/schemas/database.json — Definición del esquema de base de datos requerido para el desarrollo de la lógica multi-tenant y de fusión de identidades.
- Aplicado: architecture/hierarchy.md — Ampliación de la jerarquía para incluir workers y una estructura de carpetas más granular según la arquitectura hexagonal.

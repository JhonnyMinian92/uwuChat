# Tareas — uwuChat

Plan de implementación generado por Mnemosine. El estado vivo de cada tarea está en Mnemosine;
este archivo es una foto del plan en el momento de la última publicación.

## Infraestructura Base Backend

- [x] **Configuración del proyecto backend con FastAPI y estructura hexagonal** (completada)
  - Criterio: El servidor levanta correctamente con Uvicorn.
  - Criterio: La estructura de directorios respeta los principios de arquitectura hexagonal.
  - Criterio: El entorno de desarrollo está completamente documentado y funcional.
  - Bug: Los tests del backend no se pueden ejecutar (completada)

## Integración de Canales

- [ ] **Desarrollo del motor de adaptadores de canales de mensajería** (pendiente)
  - Criterio: Adaptadores funcionales y desacoplados para WhatsApp, Facebook Messenger, Instagram, Telegram y Discord siguiendo arquitectura hexagonal.
  - Criterio: Validación estricta de firmas criptográficas en webhooks de entrada rechazando peticiones con firma inválida.
  - Criterio: Normalización de mensajes entrantes (texto, imágenes, audio y archivos adjuntos) al contrato de dominio unificado.
  - Criterio: Deduplicación idempotente usando provider_msg_id.
  - Criterio: Soporte para el envío de plantillas HSM preaprobadas cuando se supere la ventana de 24 horas de WhatsApp.

## Gestión de Datos y Tenants

- [x] **Diseño y migración de base de datos multi-tenant** (completada)
  - Depende de: Configuración del proyecto backend con FastAPI y estructura hexagonal
  - Criterio: Los modelos reflejan las relaciones requeridas sin fugas de datos entre empresas.
  - Criterio: Se implementan migraciones de base de datos automatizadas.
  - Criterio: Se aplican restricciones de aislamiento por tenant en las consultas.

## Canal de Correo y Resiliencia

- [ ] **Infraestructura asíncrona y procesamiento de correo IMAP** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: Worker Celery configurado con sondeo IMAP periódico que extrae mensajes y adjuntos y los normaliza en conversaciones.
  - Criterio: Mecanismo de envío SMTP con reintentos bounded backoff ante fallos transitorios.
  - Criterio: Tarea periódica de purgado que elimina mensajes y adjuntos activos de más de 72 horas preservando registros estructurados inmutables en audit_logs.
  - Criterio: Consulta eficiente de auditoría por rangos de fechas y usuario para reconstrucción histórica.

## Bandeja de Entrada

- [ ] **Construcción de la bandeja unificada en React 18** (pendiente)
  - Depende de: Infraestructura asíncrona y procesamiento de correo IMAP
  - Criterio: Bandeja de entrada web unificada con visualización y envío en tiempo real vía WebSocket.
  - Criterio: Buscador de conversaciones y contactos con debounce de 300ms y resaltado de coincidencias.
  - Criterio: Filtros modernos combinables reflejando estado y aislamiento visual garantizado por tenant.
  - Criterio: Skeleton loading visible durante la obtención de conversaciones y mensajes.
  - Criterio: Advertencia visual en la UI cuando una conversación de WhatsApp supere la ventana de 24 horas, habilitando selector de plantillas HSM.

## Seguridad y Accesos

- [x] **Implementación del módulo de autenticación y autorización JWT** (completada)
  - Depende de: Diseño y migración de base de datos multi-tenant
  - Criterio: Endpoints de login y emisión de tokens seguros.
  - Criterio: Middleware de validación de roles y aislamiento por empresa operativo.
  - Criterio: Pruebas unitarias para los flujos de autenticación.

## Gestión de Contactos

- [ ] **Lógica de fusión de identidades y gestión de contactos** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18
  - Criterio: Mapeo de múltiples contactos (WhatsApp, Telegram, correo, etc.) a un único Customer dentro del mismo tenant.
  - Criterio: Endpoint transaccional para fusionar identidades con validación de aislamiento multi-tenant.
  - Criterio: Visualización del historial unificado de mensajes en la vista de cliente fusionado.
  - Criterio: Manejo de concurrencia optimista para evitar condiciones de carrera durante la fusión simultánea.

## Administración y Business Intelligence

- [ ] **Panel de administración y métricas por empresa** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18
  - Criterio: CRUD seguro para configuración de canales con credenciales cifradas en reposo.
  - Criterio: Configuración de horarios de atención y envío automático de mensajes fuera de horario.
  - Criterio: Gestión de respuestas rápidas y catálogo de plantillas HSM aprobadas para agentes.
  - Criterio: Dashboard con métricas de tiempo de primera respuesta, tiempo de resolución y volumen por agente/canal filtrable por rango de fechas.

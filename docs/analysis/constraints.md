# Constraints

Record mandatory technical, business, security, compatibility and operational constraints.

## Gemini proposed changes

- Uso de FastAPI (Python 3.12) para la API REST, manejo de webhooks e integración con canales.
- Uso de React 18 con TypeScript para la interfaz web unificada.
- Implementación de arquitectura hexagonal y patrones de repositorio, adaptador y estrategia.

## Gemini proposed changes

- Incorporación de Redis como broker para Celery (procesamiento de correos IMAP y reintentos) y como Pub/Sub para WebSockets.
- Definición explícita del modelo de fusión de identidades (Customer vs Contact) en la base de datos.
- Refuerzo del esquema de seguridad para el cifrado de credenciales de canales (Requirement 3).

## Gemini proposed changes

- Se incorpora formalmente la política de retención de 72 horas para adjuntos y mensajes con persistencia de logs de auditoría estructurados.
- Se añade el flujo de gestión y envío de plantillas genéricas (HSM) para WhatsApp fuera de la ventana de 24 horas.

## Gemini proposed changes

- Alineación formal del esquema de base de datos en database.json y database.md reflejando la tabla audit_logs inmutable y la tabla hsm_templates para WhatsApp fuera de la ventana de 24 horas.
- Reflejo de la política de retención de 72 horas para mensajes y adjuntos activos con purga automática y respaldo estructurado en logs de auditoría permanentes.

## Gemini proposed changes

- Alineación formal del esquema de base de datos multi-tenant para reflejar la tabla audit_logs permanente y hsm_templates.
- Definición de módulos de construcción estructurados para abarcar cimientos, adaptadores de canales, bandeja web y características de producción.


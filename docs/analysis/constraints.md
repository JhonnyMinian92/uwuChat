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


# Requirements and Business Logic

1. Empresas (tenants): alta de empresa, plan, datos de contacto; aislamiento estricto de datos entre empresas.
2. Usuarios de la empresa con roles: administrador de empresa, supervisor y agente de atención.
3. Canales: cada empresa conecta uno o varios canales (WhatsApp Cloud API, Messenger, Instagram Messaging, Telegram Bot API, Discord bot, correo IMAP/SMTP). Las credenciales de cada canal se guardan cifradas.
4. Recepción: webhooks verificados por firma (Meta X-Hub-Signature-256, token secreto de Telegram) e idempotentes por id de mensaje externo; el correo se sondea por IMAP.
5. Contactos: un cliente se identifica por canal + id externo; se pueden fusionar identidades del mismo cliente en varios canales.
6. Conversaciones: abiertas, asignadas, en espera, resueltas; asignación manual o automática round-robin entre agentes disponibles; transferencia entre agentes.
7. Mensajes: texto, imágenes, audio y archivos adjuntos; estado enviado/entregado/leído cuando el canal lo informa.
8. Respuestas: el agente responde desde la bandeja y el mensaje sale por el canal original respetando las reglas del canal (ventana de 24 h de WhatsApp: fuera de ella solo plantillas aprobadas).
9. Respuestas rápidas, etiquetas y notas internas por conversación.
10. Horario de atención y mensaje automático fuera de horario.
11. Métricas por empresa: tiempo de primera respuesta, tiempo de resolución, volumen por canal y por agente.
12. Auditoría de accesos y cambios de configuración.

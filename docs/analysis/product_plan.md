# Plan del producto — uwuChat

Mapa del producto final por módulos, con sus tareas en orden y los códigos de sus criterios de aceptación. El estado vivo de cada tarea está en Mnemosine.

## M1 · Cimientos y Esqueleto del Proyecto

Establecer la estructura de repositorios con arquitectura hexagonal, configuración por ambiente, tests automatizados básicos y arranque de salud.

- **T11** Implementación del endpoint de salud /health y configuración de entornos en FastAPI (pending)
  - T11-C1: La petición GET /health retorna código HTTP 200 con cuerpo JSON {'status': 'ok', 'database': 'connected'} cuando la base de datos está disponible.
  - T11-C2: La petición GET /health retorna código HTTP 503 cuando la base de datos no está disponible, sin exponer contraseñas ni stack traces.
  - T11-C3: La configuración carga las variables desde el entorno y falla de forma temprana si faltan parámetros obligatorios.
- **T10** Configuración del proyecto frontend con React 18, TypeScript y Vite (pending)
  - T10-C1: Vitest ejecuta con éxito el test unitario de renderizado del componente principal en frontend/src/App.test.tsx.
  - T10-C2: La compilación estricta de tipos con tsc --noEmit finaliza con cero errores.
  - T10-C3: El empaquetado de producción genera los artefactos en frontend/dist de forma limpia.
- **T12** Configuración del pipeline de Integración Continua (CI) y comprobaciones de calidad (pending)
  - T12-C1: El archivo de workflow .github/workflows/ci.yml cuenta con una estructura YAML válida con etapas para backend y frontend.
  - T12-C2: El repositorio cuenta con archivos .env.example en la raíz y en backend/ y frontend/, y los archivos .env se encuentran bloqueados en .gitignore.
  - T12-C3: El conjunto de pruebas automatizadas del proyecto se ejecuta en el pipeline y finaliza en verde.

## M2 · Capa de Datos Transaccionales y Autenticación

Configurar la base de datos PostgreSQL local con migraciones versionadas, aislamiento multi-tenant y autenticación JWT con roles.

- **T13** Configuración de persistencia asíncrona y sistema de semillas de datos (pending)
  - T13-C1: La aplicación se conecta a la base de datos PostgreSQL usando el driver asíncrono asyncpg.
  - T13-C2: El script de seeds crea 2 empresas y 4 usuarios (admin, supervisor, agente) sin errores.
  - T13-C3: La configuración de base de datos no contiene secretos hardcodeados, lee todo de .env.
- **T14** Implementación de Inyección de Contexto de Tenant y Aislamiento (pending)
  - T14-C1: La dependencia 'get_current_tenant' devuelve el ID de empresa correcto del token JWT.
  - T14-C2: Toda consulta a la base de datos de una entidad multi-tenant incluye 'WHERE company_id = ...'.
- **T15** Refuerzo de Seguridad: RBAC y Hashing de Credenciales (pending)
  - T15-C1: Las contraseñas en la base de datos se almacenan como hashes bcrypt no reversibles.
  - T15-C2: Los endpoints marcados para ADMIN devuelven 403 Forbidden si el token pertenece a un AGENT.
- **T16** Endpoints de Gestión de Perfil y Usuarios (CRUD Básico) (pending)
  - T16-C1: El listado de usuarios devuelve una respuesta paginada con metadatos (total, página, tamaño).
  - T16-C2: Es imposible crear un usuario asignándolo a una empresa distinta a la del administrador autenticado.
- **T17** Pruebas de Integración de Aislamiento y Seguridad Multi-tenant (pending)
  - T17-C1: Test 'test_cross_tenant_data_leak' confirma que el Tenant A no puede ver registros del Tenant B.
  - T17-C2: La eliminación de una empresa mediante script borra todos sus usuarios asociados en cascada.

## M3 · Motor de Canales de Mensajería y Webhooks

Implementar el patrón Strategy y Adapter para unificar la recepción y envío de mensajes vía WhatsApp, Messenger, Instagram, Telegram y Discord.

- **T4** Desarrollo del motor de adaptadores de canales de mensajería (pending)
  - T4-C6: M3-T1-C1: Definida clase abstracta BaseChannelAdapter con firma de métodos obligatorios.
  - T4-C7: M3-T1-C2: AdapterFactory devuelve la instancia correcta según el enum de proveedores.
- **T18** Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram (pending)
  - T18-C1: M3-T2-C1: Rechazo de webhooks con firma HMAC inválida para WhatsApp.
  - T18-C2: M3-T2-C2: Conversión correcta de adjuntos (imágenes/audio) desde el JSON de Meta al modelo interno de mensajes.
- **T19** Adaptadores para Telegram Bot y Discord Bot (pending)
  - T19-C1: M3-T3-C1: Verificación de token de Telegram en la cabecera X-Telegram-Bot-Api-Secret-Token.
  - T19-C2: M3-T3-C2: Mensajes de Discord normalizados incluyendo el discriminador del usuario y contenido.
- **T20** Controlador Unificado de Webhooks e Idempotencia (pending)
  - T20-C1: M3-T4-C1: Mensajes duplicados con el mismo provider_msg_id son ignorados (idempotencia).
  - T20-C2: M3-T4-C2: Todo mensaje recibido genera un registro en audit_logs de forma inmutable.
- **T21** Gestión de Salida y Restricción de Ventana 24h (WhatsApp HSM) (pending)
  - T21-C1: M3-T5-C1: Bloqueo de envío de texto libre en WhatsApp si han pasado > 24h desde el último mensaje del cliente.
  - T21-C2: M3-T5-C2: Envío exitoso mediante plantilla aprobada (HSM) fuera de la ventana de 24 horas.

## M4 · Procesamiento Asíncrono y Correo IMAP/SMTP

Configurar Celery y Redis para el sondeo periódico de buzones IMAP y envíos SMTP, asegurando la retención de mensajes por 72 horas y logs permanentes.

- **T8** Infraestructura asíncrona y procesamiento de correo IMAP (pending)
  - T8-C5: La instancia de Celery inicializa y establece conexión verificable con Redis en entorno de pruebas.
  - T8-C6: El decorador de reintentos con backoff exponencial reprograma la tarea ante excepciones transitorias respetando el factor de espera.
  - T8-C7: El registro de errores de Celery almacena metadatos y código de error en formato estructurado sin filtrar credenciales ni datos sensibles.
- **T22** Adaptador de Correo Electrónico: Ingesta periódica IMAP y Despacho SMTP (pending)
  - T22-C1: La tarea de sondeo IMAP descarga correos no leídos y los normaliza correctamente en conversaciones y mensajes activos asignados a la empresa correspondiente.
  - T22-C2: El despacho de correos salientes vía SMTP envía los datos al servidor configurado y marca el mensaje con estado de entrega o error.
  - T22-C3: Los fallos transitorios de red durante el envío SMTP disparan reintentos automáticos sin generar duplicados en la base de datos.
- **T23** Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs (pending)
  - T23-C1: Los mensajes con antigüedad superior a 72 horas son eliminados de la tabla messages de forma segura y en lotes transaccionales.
  - T23-C2: Los mensajes con antigüedad inferior o igual a 72 horas permanecen intactos en la tabla messages tras la ejecución del purgado.
  - T23-C3: Cada mensaje purgado cuenta con un registro correspondiente en audit_logs que contiene el payload completo y el company_id para su reconstrucción histórica.
- **T24** Pruebas de integración de tareas asíncronas, resiliencia y purgado de datos (72h) (pending)
  - T24-C1: La suite de integración valida que los mensajes procesados y purgados después de 72h pueden reconstruirse fielmente desde audit_logs sin pérdida de información.
  - T24-C2: Las tareas Celery concurrentes de diferentes empresas procesan colas manteniendo aislamiento absoluto de datos y credenciales por tenant.
  - T24-C3: Los errores no recuperables en canales de correo quedan asentados en el registro de auditoría con código descriptivo y sin propagar excepciones no controladas.

## M5 · Bandeja Unificada y WebSocket en Tiempo Real

Desarrollar la interfaz en React 18 con WebSocket para la atención de clientes en tiempo real, aplicando filtros avanzados, buscadores y skeleton loading.

- **T25** Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant (pending)
  - T25-C1: Rechazar conexiones WebSocket que no envíen token JWT válido o cuyo token haya expirado con código de cierre 4401.
  - T25-C2: Garantizar aislamiento estricto impidiendo que los mensajes emitidos por el tenant A lleguen a los WebSockets conectados del tenant B.
  - T25-C3: Difundir eventos estructurados de asignación y cambio de estado de conversación a todos los agentes activos de la misma empresa.
- **T5** Construcción de la bandeja unificada en React 18 (pending)
  - T5-C6: Renderizar la lista de conversaciones y el panel de detalle de chat con badges específicos para cada canal soportado.
  - T5-C7: Permitir la selección de conversación cambiando activamente el historial del chat mostrado.
  - T5-C8: Adaptar la vista a pantallas de 360px permitiendo alternar entre lista y chat sin desbordamiento horizontal.
- **T26** Buscador con debounce y filtros modernos combinables (pending)
  - T26-C1: Retardar la ejecución del filtrado durante 300 ms mientras el usuario teclea en el buscador.
  - T26-C2: Reflejar las facetas activas de canal, estado y agente en los parámetros query de la URL del navegador.
  - T26-C3: Mostrar coincidencia resaltada o estado vacío específico si ningún chat coincide con el texto buscado.
- **T27** Cliente WebSocket en React con reconexión exponencial y sincronización en tiempo real (pending)
  - T27-C1: Reintentar la conexión con retraso creciente (backoff exponencial) tras una pérdida abrupta de socket.
  - T27-C2: Añadir mensajes entrantes recibidos por WebSocket en el hilo de la conversación activa sin requerir recargar la página.
  - T27-C3: Mostrar indicador visual del estado de conectividad en tiempo real (en línea / reconectando).
- **T28** Skeleton loaders, estados vacíos/error accesibles y optimización de rendimiento (pending)
  - T28-C1: Mostrar esqueletos de carga animados con la silueta de la lista y mensajes mientras se cargan los datos iniciales.
  - T28-C2: Proveer botón de reintento funcional en la pantalla de error ante fallos de conexión HTTP o WebSocket.
  - T28-C3: Verificar ausencia de violaciones de accesibilidad (axe-core) en la lista de conversaciones y controles de interacción.
  - T28-C4: Comprobar que las rutas no existentes despliegan la página 404 estructurada con enlace a la bandeja.
- **T29** Pruebas de integración E2E de la bandeja unificada y verificación de rendimiento (pending)
  - T29-C1: Completar el ciclo de lectura, filtrado y envío de respuesta en tiempo real simulado de extremo a extremo sin recargar la página.
  - T29-C2: Desconectar y limpiar adecuadamente las suscripciones WebSocket al desmontar el componente de chat sin dejar listeners colgados.
  - T29-C3: Validar que el bundle de la aplicación en producción divide adecuadamente los chunks principales sin exceder presupuestos de tamaño.

## M6 · Fusión de Identidades y Gestión de Contactos

Permitir la unificación de identidades técnicas de un mismo cliente en múltiples canales hacia un único perfil de Customer.

- **T9** Lógica de fusión de identidades y gestión de contactos (pending)
  - T9-C5: La fusión de dos clientes se ejecuta en una única transacción de base de datos.
  - T9-C6: Se prohíbe la fusión de clientes que pertenecen a diferentes empresas (tenants).
  - T9-C7: Todas las conversaciones del cliente origen son transferidas íntegramente al cliente destino.
- **T30** Endpoints de la API para gestión de identidades y contactos (pending)
  - T30-C1: El endpoint de fusión devuelve un error 400 con un mensaje claro si los clientes no pertenecen a la misma empresa.
  - T30-C2: El detalle del cliente incluye la lista de canales/contactos asociados (ej. su WhatsApp ID y su Telegram handle).
  - T30-C3: Las respuestas de error siguen el formato estándar definido en el proyecto.
- **T31** Interfaz de usuario para el perfil del cliente y fusión de identidades (pending)
  - T31-C1: El buscador de clientes para fusión aplica un debounce para evitar peticiones excesivas.
  - T31-C2 (manual): Se muestra un diálogo de confirmación antes de proceder con la fusión, advirtiendo que es irreversible.
  - T31-C3: La interfaz es totalmente accesible mediante teclado y cumple contrastes WCAG AA.
- **T32** Pruebas de integridad y aislamiento para la fusión de clientes (pending)
  - T32-C1: La tabla audit_logs contiene un registro detallado del evento de fusión con los IDs involucrados.
  - T32-C2: Un agente de la Empresa A no puede listar ni fusionar clientes de la Empresa B aunque conozca sus IDs.

## M7 · Panel de Administración y Métricas de Negocio

Construir el panel para gestión de horarios, respuestas rápidas, canales cifrados y el tablero de métricas de rendimiento por agente y canal.

- **T33** Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant (pending)
  - T33-C1: Las credenciales de los canales se persisten cifradas en base de datos y no se exponen valores en texto claro al consultar la tabla directamente.
  - T33-C2: Los endpoints GET de canales devuelven las credenciales enmascaradas y rechazan solicitudes de agentes que no posean rol de administrador.
  - T33-C3: Aislamiento multi-tenant estricto en la administración de canales.
- **T34** Configuración de horarios de atención y despacho de respuestas automáticas fuera de horario (pending)
  - T34-C1: El servicio evalúa con precisión si una conversación entra dentro o fuera del horario comercial según la zona horaria IANA de la empresa.
  - T34-C2: Se despacha el mensaje automático fuera de horario solo una vez por conversación entrante fuera de turno.
  - T34-C3: Endpoint REST para actualizar horario y mensaje fuera de oficina valida formato y esquema.
- **T35** Gestión de respuestas rápidas y categorización por etiquetas (pending)
  - T35-C1: CRUD completo de respuestas rápidas con validación de atajo único por empresa.
  - T35-C2: Permisos RBAC diferenciados para administración y consulta de respuestas rápidas.
  - T35-C3: Asignación y remoción de etiquetas en conversaciones con persistencia transaccional.
- **T36** Motor de agregación de métricas de rendimiento y tablero analítico (pending)
  - T36-C1: Cálculo preciso del Tiempo de Primera Respuesta (FRT) y Tiempo de Resolución (TTR).
  - T36-C2: Agregación por canal y agente con filtros de rango de fechas.
  - T36-C3: Protección de datos y aislamiento tenant en las métricas.
- **T6** Panel de administración y métricas por empresa (pending)
  - T6-C5: La ruta /admin restringe el acceso según rol y redirige a la bandeja a usuarios con rol agente.
  - T6-C6: El formulario de conexión de canales permite configurar credenciales de forma segura sin mostrarlas en claro.
  - T6-C7: El tablero de métricas renderiza KPIs y gráficos de volumen con selector de rango temporal.
  - T6-C8 (manual): Verificación manual de la configuración de horarios de atención y mensajes de ausencia.
- **T37** Pruebas de integración E2E del panel de administración, métricas y seguridad de credenciales cifradas (pending)
  - T37-C1: Flujo E2E completo de alta de canal, configuración de horario y visualización de métricas.
  - T37-C2: Verificación automatizada de no fuga de secretos en respuestas HTTP ni registros de logs.
  - T37-C3: Aislamiento multi-tenant validado en todas las operaciones del panel administrativo.

## M8 · Endurecimiento de Producción y Operaciones

Asegurar la preparación final para producción mediante cabeceras de seguridad, despliegue reproducible, respaldos probados y documentación completa.

- **T38** Configuración de cabeceras de seguridad y middleware HTTPS (pending)
  - T38-C1: La respuesta del backend incluye la cabecera Strict-Transport-Security con max-age de al menos un año.
  - T38-C2: La cabecera Content-Security-Policy (CSP) está presente y restringe orígenes no deseados.
  - T38-C3 (manual): Las peticiones HTTP son redirigidas automáticamente a HTTPS.
- **T39** Auditoría de vulnerabilidades y fijación de dependencias (pending)
  - T39-C1: El comando 'pip-audit' devuelve 0 vulnerabilidades críticas o altas en el entorno virtual del backend.
  - T39-C2: El comando 'npm audit' en la carpeta frontend no reporta vulnerabilidades de nivel 'high' o superior.
- **T40** Empaquetado reproducible con Docker y Docker Compose (pending)
  - T40-C1: Las imágenes de Docker se construyen sin errores y pesan menos de 500MB cada una.
  - T40-C2 (manual): El comando 'docker compose up' levanta todos los servicios y la aplicación responde en localhost.
- **T41** Suite de pruebas E2E de flujos críticos (pending)
  - T41-C1: El test de 'flujo completo de atención' termina con éxito simulando un cliente real.
  - T41-C2: Los tests comprueban que no se filtran datos de otras empresas (aislamiento multi-tenant) durante el flujo visual.
- **T42** Manual de despliegue y documentación del proyecto (pending)
  - T42-C1 (manual): El archivo README.md incluye todas las secciones requeridas por PRD-DOC-01.
  - T42-C2 (manual): DEPLOY.md describe cómo realizar una actualización (rollback incluido) sin pérdida de datos.
- **T43** Scripts de copia de seguridad y restauración de base de datos (pending)
  - T43-C1: El script backup.sh genera un archivo .sql.gz válido en la carpeta de backups.
  - T43-C2 (manual): Una base de datos vacía puede ser restaurada al estado del backup usando restore.sh.
- **T44** Limpieza de código muerto y verificación final de salud (pending)
  - T44-C1: Las herramientas de análisis de código muerto no reportan hallazgos significativos.
  - T44-C2: El endpoint /health devuelve 503 si la base de datos está caída y 200 si todo es funcional.

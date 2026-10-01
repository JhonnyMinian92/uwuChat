# Plan del producto — uwuChat

Mapa del producto final por módulos, con sus tareas en orden y los códigos de sus criterios de aceptación. El estado vivo de cada tarea está en Mnemosine.

## M1 · Cimientos y Esqueleto de Comunicación

Estructura base del repositorio, configuración de entornos y primer test de punta a punta con endpoint de salud.

- **T11** Implementación del endpoint de salud /health y configuración de entornos en FastAPI (pending)
  - T11-C4: El endpoint GET /health responde con código 200 y estado OK cuando la aplicación está operativa.
  - T11-C5: La configuración por ambiente carga correctamente desde las variables de entorno mediante settings.
- **T10** Configuración del proyecto frontend con React 18, TypeScript y Vite (pending)
  - T10-C4: El proyecto frontend compila correctamente en TypeScript con strict mode activado.
  - T10-C5: La estructura de carpetas y componentes cumple con la jerarquía definida y los tests corren en verde.
- **T12** Configuración del pipeline de Integración Continua (CI) y comprobaciones de calidad (pending)
  - T12-C4: El pipeline de CI ejecuta con éxito la suite de pruebas del backend y del frontend en cada ejecución.
  - T12-C5 (manual): El repositorio incluye el archivo README.md con instrucciones claras de instalación, ejecución y pruebas.

## M2 · Persistencia Multi-tenant y Autenticación

Base de datos PostgreSQL configurada con migraciones y sistema de autenticación JWT con aislamiento por empresa.

- **T13** Configuración de persistencia asíncrona y sistema de semillas de datos (pending)
  - T13-C4: M2.T1-C1: Las migraciones de Alembic se aplican exitosamente sobre la base de datos PostgreSQL creando todas las tablas requeridas por el modelo multi-tenant.
  - T13-C5: M2.T1-C2: El script de semillas de datos inserta registros de prueba válidos sin incluir datos reales ni comprometer entornos de producción.
- **T14** Implementación de Inyección de Contexto de Tenant y Aislamiento (pending)
  - T14-C3: M2.T2-C1: Las consultas a nivel de repositorio aplican automáticamente el filtro por company_id según el contexto de la sesión.
  - T14-C4: M2.T2-C2: Las peticiones sin contexto de tenant válido son rechazadas inmediatamente con código HTTP 401 o 403.
- **T15** Refuerzo de Seguridad: RBAC y Hashing de Credenciales (pending)
  - T15-C3: M2.T3-C1: Las contraseñas se almacenan empleando un hash fuerte y nunca en texto plano.
  - T15-C4: M2.T3-C2: Un usuario con rol agent recibe un error HTTP 403 al intentar acceder a rutas protegidas exclusivamente para roles admin o supervisor.
- **T16** Endpoints de Gestión de Perfil y Usuarios (CRUD Básico) (pending)
  - T16-C3: M2.T4-C1: El endpoint de creación de usuario valida correctamente los campos de entrada y rechaza correos malformados o faltantes.
  - T16-C4: M2.T4-C2: Los listados de usuarios devuelven únicamente los registros asociados a la empresa del usuario autenticado y de forma paginada.
- **T17** Pruebas de Integración de Aislamiento y Seguridad Multi-tenant (pending)
  - T17-C3: M2.T5-C1: Los usuarios de la Empresa A no pueden acceder a datos, perfiles ni recursos de la Empresa B mediante manipulación de parámetros de la API.
  - T17-C4: M2.T5-C2: La verificación de tokens JWT expirados o alterados rechaza el acceso de forma inequívoca en todos los endpoints protegidos.

## M3 · Motor de Adaptadores y Webhooks

Implementación de la interfaz común para canales de mensajería y recepción de eventos de Meta y Telegram.

- **T4** Desarrollo del motor de adaptadores de canales de mensajería (pending)
  - T4-C8: La interfaz BaseChannelAdapter y la clase de datos NormalizedMessage están definidas correctamente y forzadas con tipos estrictos.
  - T4-C9: La normalización de un payload de entrada produce un objeto NormalizedMessage válido según el esquema definido.
- **T18** Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram (pending)
  - T18-C3: El adaptador de Meta puede deserializar y normalizar correctamente un webhook de mensaje entrante de WhatsApp, Messenger e Instagram.
  - T18-C4: El método de envío de mensajes realiza una llamada POST HTTP autorizada hacia la Graph API de Meta.
- **T19** Adaptadores para Telegram Bot y Discord Bot (pending)
  - T19-C3: Los adaptadores de Telegram y Discord normalizan correctamente los formatos de mensajes entrantes de cada API.
  - T19-C4: El despacho de mensajes salientes para Telegram y Discord se realiza de manera segura y controlando respuestas del API.
- **T20** Controlador Unificado de Webhooks e Idempotencia (pending)
  - T20-C3: Se rechazan las peticiones a webhooks que no tengan firmas o tokens de verificación válidos.
  - T20-C4: El endpoint de webhooks procesa el payload de manera idempotente usando el external_id del mensaje.
- **T21** Gestión de Salida y Restricción de Ventana 24h (WhatsApp HSM) (pending)
  - T21-C3: Se bloquea el envío de un mensaje de texto libre si han transcurrido más de 24 horas desde la última interacción entrante de WhatsApp.
  - T21-C4: Se permite el envío exitoso de un mensaje de plantilla autorizada (HSM) aun superando la ventana de 24 horas.

## M4 · Procesamiento Asíncrono y Retención de Datos

Gestión de colas para correo IMAP/SMTP y cumplimiento de la política de purgado de 72 horas.

- **T8** Infraestructura asíncrona y procesamiento de correo IMAP (pending)
  - T8-C8: M4.T1-C1: El sistema de tareas asíncronas reintenta operaciones fallidas de red utilizando backoff exponencial.
  - T8-C9: M4.T1-C2: Los errores de conexión de correo se registran adecuadamente sin exponer credenciales ni datos sensibles.
- **T22** Adaptador de Correo Electrónico: Ingesta periódica IMAP y Despacho SMTP (pending)
  - T22-C4: M4.T2-C1: El lector IMAP sondea periódicamente y normaliza los mensajes entrantes al modelo común.
  - T22-C5: M4.T2-C2: El servicio SMTP despacha correctamente las respuestas de los agentes al buzón original del cliente.
- **T23** Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs (pending)
  - T23-C4: M4.T3-C1: La tarea de purgado identifica y elimina mensajes y adjuntos activos superadas las 72 horas.
  - T23-C5: M4.T3-C2: Se genera un registro inmutable en audit_logs por cada mensaje purgado que permite su reconstrucción histórica.
- **T24** Pruebas de integración de tareas asíncronas, resiliencia y purgado de datos (72h) (pending)
  - T24-C4: M4.T4-C1: Las pruebas de retención y purgado (72h) comprueban que los mensajes eliminados de la tabla activa persisten en audit_logs.
  - T24-C5: M4.T4-C2: Las respuestas de error en operaciones asíncronas y de red siguen un formato estándar y comprensible.

## M5 · Bandeja Unificada y Tiempo Real

Interfaz web para agentes con actualizaciones en tiempo real mediante WebSockets.

- **T25** Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant (pending)
  - T25-C4: M5.T1-C1: Rechazar conexiones WebSocket sin token JWT válido o con un token de otra empresa.
  - T25-C5: M5.T1-C2: Publicar y recibir mensajes correctamente a través de los canales de Redis pub/sub.
- **T5** Construcción de la bandeja unificada en React 18 (pending)
  - T5-C9: M5.T2-C1: Mostrar la lista de conversaciones estructurada por canal y estado con diseño responsive.
  - T5-C10: M5.T2-C2: Enviar un mensaje de texto operativo que se añade inmediatamente a la vista.
- **T26** Buscador con debounce y filtros modernos combinables (pending)
  - T26-C4: M5.T3-C1: Ejecutar la búsqueda de conversaciones aplicando un debounce de 300ms sobre el input de texto.
  - T26-C5: M5.T3-C2: Reflejar los estados de los filtros combinados directamente en los query params de la URL.
- **T27** Cliente WebSocket en React con reconexión exponencial y sincronización en tiempo real (pending)
  - T27-C4: M5.T4-C1: Reconectar automáticamente con backoff exponencial cuando la conexión WebSocket se interrumpe.
  - T27-C5: M5.T4-C2: Actualizar el listado de conversaciones y el chat activo al recibir un mensaje entrante por el socket.
- **T28** Skeleton loaders, estados vacíos/error accesibles y optimización de rendimiento (pending)
  - T28-C5: M5.T5-C1: Mostrar skeleton loaders con la forma exacta del layout mientras cargan los datos de las conversaciones.
  - T28-C6: M5.T5-C2: Superar la auditoría de accesibilidad automática asegurando contraste y etiquetas correctas en todos los estados.
- **T29** Pruebas de integración E2E de la bandeja unificada y verificación de rendimiento (pending)
  - T29-C4: M5.T6-C1: Completar el flujo E2E de login de agente, selección de conversación y respuesta en tiempo real sin errores.
  - T29-C5: M5.T6-C2: Obtener una puntuación de rendimiento de Lighthouse superior o igual a 80 en la vista móvil de la bandeja.

## M6 · Gestión de Contactos y Fusión de Identidades

Capacidad de unificar clientes que escriben desde diferentes canales en una sola ficha.

- **T9** Lógica de fusión de identidades y gestión de contactos (pending)
  - T9-C8: M6.T1-C1: Un cliente nuevo se crea automáticamente al registrar un contacto no existente en el canal.
  - T9-C9: M6.T1-C2: La fusión de dos customers transfiere correctamente todos los contactos y conversaciones al customer principal.
  - T9-C10: M6.T1-C3: Se rechaza e impide la fusión de customers que pertenecen a distintas empresas (tenants).
- **T30** Endpoints de la API para gestión de identidades y contactos (pending)
  - T30-C4: M6.T2-C1: El listado de customers devuelve resultados paginados correctamente.
  - T30-C5: M6.T2-C2: El endpoint de fusión requiere privilegios de supervisor o administrador y valida los IDs de entrada.
  - T30-C6: M6.T2-C3: Se documenta correctamente la especificación OpenAPI para los nuevos endpoints de contactos.
- **T31** Interfaz de usuario para el perfil del cliente y fusión de identidades (pending)
  - T31-C4: M6.T3-C1: La pantalla de perfil muestra claramente todos los canales y contactos asociados al cliente.
  - T31-C5: M6.T3-C2: El modal de fusión permite buscar el cliente secundario y muestra una confirmación antes de ejecutar la acción.
  - T31-C6: M6.T3-C3: Las interfaces cumplen con los criterios de accesibilidad básica WCAG 2.1 AA.
- **T32** Pruebas de integridad y aislamiento para la fusión de clientes (pending)
  - T32-C3: M6.T4-C1: Los usuarios de una empresa jamás pueden consultar o fusionar clientes pertenecientes a otra empresa.
  - T32-C4: M6.T4-C2: La suite de pruebas de integración de M6 se ejecuta y pasa exitosamente en el pipeline de CI.

## M7 · Administración, Horarios y Plantillas HSM

Panel de control para la empresa, configuración de canales y gestión de plantillas de WhatsApp.

- **T33** Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant (pending)
  - T33-C4: M7.T1-C1: Las credenciales se almacenan completamente cifradas en la base de datos sin texto plano.
  - T33-C5: M7.T1-C2: Solo los usuarios con rol de administrador de la misma empresa pueden gestionar sus canales.
  - T33-C6: M7.T1-C3: Los campos de entrada de credenciales se validan estrictamente mediante esquemas Pydantic rechazando payloads malformados.
- **T34** Configuración de horarios de atención y despacho de respuestas automáticas fuera de horario (pending)
  - T34-C4: M7.T2-C1: Los mensajes entrantes fuera del horario configurado generan una respuesta automática inmediata.
  - T34-C5: M7.T2-C2: Los administradores pueden configurar y actualizar sus horarios de atención mediante la API REST.
- **T35** Gestión de respuestas rápidas y categorización por etiquetas (pending)
  - T35-C4: M7.T3-C1: Los usuarios de una empresa solo pueden visualizar y utilizar las respuestas rápidas y etiquetas creadas dentro de su propio tenant.
  - T35-C5: M7.T3-C2: Las respuestas rápidas y etiquetas cuentan con validación de campos obligatorios y límites de longitud.
- **T36** Motor de agregación de métricas de rendimiento y tablero analítico (pending)
  - T36-C4: M7.T4-C1: El tablero de métricas calcula correctamente los tiempos de respuesta y resolución en base al historial de conversaciones.
  - T36-C5: M7.T4-C2: Las métricas están estrictamente aisladas por tenant y solo son accesibles por roles de supervisor y administrador.
- **T6** Panel de administración y métricas por empresa (pending)
  - T6-C9: M7.T5-C1: El panel de administración se adapta correctamente a pantallas desde 360px de ancho sin desbordes.
  - T6-C10: M7.T5-C2: Las rutas del panel de administración redirigen o bloquean a usuarios sin privilegios administrativos.
- **T37** Pruebas de integración E2E del panel de administración, métricas y seguridad de credenciales cifradas (pending)
  - T37-C4: M7.T6-C1: El flujo completo de administración y métricas funciona de extremo a extremo contra una base de datos real en el entorno de CI.
  - T37-C5: M7.T6-C2: Ningún dato ni configuración de una empresa puede ser accedido o modificado por otra empresa bajo ninguna circunstancia de prueba.

## M8 · Operaciones y Endurecimiento

Preparación final para producción con seguridad, monitoreo y despliegue automatizado.

- **T38** Configuración de cabeceras de seguridad y middleware HTTPS (pending)
  - T38-C4: Las respuestas del backend FastAPI devuelven las cabeceras HSTS, X-Content-Type-Options, Referrer-Policy y Content-Security-Policy (CSP) validadas por un cliente HTTP de pruebas.
  - T38-C5: Cualquier solicitud HTTP entrante a rutas protegidas o públicas redirige con código 301/307 hacia su contraparte segura HTTPS.
  - T38-C6: La aplicación no puede ser incrustada en iframes externos mediante validación estricta de frame-ancestors o X-Frame-Options.
- **T39** Auditoría de vulnerabilidades y fijación de dependencias (pending)
  - T39-C3: El escaneo de vulnerabilidades del backend con pip-audit retorna cero vulnerabilidades de criticidad alta o crítica.
  - T39-C4: El escaneo de dependencias npm audit en el frontend finaliza con código de salida cero y libre de incidencias de riesgo alto.
  - T39-C5: El proyecto cuenta con sus archivos de bloqueo (lockfiles) integrados en el repositorio de control de versiones.
- **T45** Empaquetado reproducible con Docker and Docker Compose (pending)
  - T45-C1: La compilación de las imágenes Docker se ejecuta exitosamente sin requerir o instalar dependencias de desarrollo locales.
  - T45-C2: El comando docker-compose up inicializa correctamente los servicios de DB, Redis, API y Frontend y permite interactuar con la interfaz en el puerto configurado.
  - T45-C3: El contenedor de backend rechaza arrancar si faltan variables de entorno críticas necesarias para su ejecución.
- **T43** Scripts de copia de seguridad y restauración de base de datos (pending)
  - T43-C3: El script de copia de seguridad genera un archivo dump válido con extensión SQL o binaria comprimida que contiene los esquemas multi-tenant completos.
  - T43-C4: El script de restauración reconstruye de forma idéntica todas las tablas de persistencia en un contenedor PostgreSQL recién inicializado, validado mediante comparación de esquemas.
  - T43-C5 (manual): Procedimiento de restauración de desastres verificado por un operador humano a partir de la documentación proporcionada.
- **T41** Suite de pruebas E2E de flujos críticos (pending)
  - T41-C3: El test de extremo a extremo simula con éxito la interacción del flujo crítico, cubriendo inicio de sesión, asignación de chat y respuesta sin provocar excepciones en el navegador ni en el servidor.
  - T41-C4: La suite de pruebas contiene aserciones explícitas que intentan acceder de forma no autorizada a datos de un tenant ajeno, resultando en rechazo automático por parte de la API.
- **T42** Manual de despliegue y documentación del proyecto (pending)
  - T42-C3: El archivo DEPLOY.md describe adecuadamente todas y cada una de las variables presentes en el archivo .env.example del proyecto.
  - T42-C4 (manual): La documentación de despliegue detalla los comandos requeridos, la configuración de HTTPS, dominios, variables y cómo volver a una versión previa.
  - T42-C5: La cabecera HTML del frontend de React expone títulos, meta descripciones de contenido, favicon institucional y metadatos básicos en formato Open Graph.
- **T44** Limpieza de código muerto y verificación final de salud (pending)
  - T44-C3: El analizador de código huérfano e imports confirma que el proyecto está limpio de referencias no utilizadas y dependencias sin declarar.
  - T44-C4: El endpoint de salud /health retorna un código de respuesta HTTP 200 conteniendo el estado del backend, conexión de persistencia y cola de caché Redis, sin filtrar secretos.
  - T44-C5: La suite de pruebas completa del repositorio (unitarias, integración y extremo a extremo) culmina exitosamente en un entorno limpio sin fallos.

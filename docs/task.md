# Tareas — uwuChat

Plan de implementación generado por Mnemosine. El estado vivo de cada tarea está en Mnemosine;
este archivo es una foto del plan en el momento de la última publicación.

## Infraestructura Base Backend

- [x] **Configuración del proyecto backend con FastAPI y estructura hexagonal** (completada)
  - Criterio: El servidor levanta correctamente con Uvicorn.
  - Criterio: La estructura de directorios respeta los principios de arquitectura hexagonal.
  - Criterio: El entorno de desarrollo está completamente documentado y funcional.
  - Bug: Los tests del backend no se pueden ejecutar (completada)

## Gestión de Datos y Tenants

- [x] **Diseño y migración de base de datos multi-tenant** (completada)
  - Depende de: Configuración del proyecto backend con FastAPI y estructura hexagonal
  - Criterio: Los modelos reflejan las relaciones requeridas sin fugas de datos entre empresas.
  - Criterio: Se implementan migraciones de base de datos automatizadas.
  - Criterio: Se aplican restricciones de aislamiento por tenant en las consultas.

## Seguridad y Accesos

- [x] **Implementación del módulo de autenticación y autorización JWT** (completada)
  - Depende de: Diseño y migración de base de datos multi-tenant
  - Criterio: Endpoints de login y emisión de tokens seguros.
  - Criterio: Middleware de validación de roles y aislamiento por empresa operativo.
  - Criterio: Pruebas unitarias para los flujos de autenticación.

## Panel de Administración

- [ ] **Panel de administración y métricas por empresa** (pendiente)
  - Depende de: Motor de agregación de métricas de rendimiento y tablero analítico
  - Criterio: M7.T5-C1: El panel de administración se adapta correctamente a pantallas desde 360px de ancho sin desbordes.
  - Criterio: M7.T5-C2: Las rutas del panel de administración redirigen o bloquean a usuarios sin privilegios administrativos.

## Como arquitecto del chat, quiero una interfaz común de puerto para adaptadores de mensajería para desacoplar el dominio de las APIs externas.

- [ ] **Desarrollo del motor de adaptadores de canales de mensajería** (pendiente)
  - Depende de: Pruebas de Integración de Aislamiento y Seguridad Multi-tenant
  - Criterio: La interfaz BaseChannelAdapter y la clase de datos NormalizedMessage están definidas correctamente y forzadas con tipos estrictos.
  - Criterio: La normalización de un payload de entrada produce un objeto NormalizedMessage válido según el esquema definido.

## Interfaz de Usuario de la Bandeja

- [ ] **Construcción de la bandeja unificada en React 18** (pendiente)
  - Depende de: Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant
  - Criterio: M5.T2-C1: Mostrar la lista de conversaciones estructurada por canal y estado con diseño responsive.
  - Criterio: M5.T2-C2: Enviar un mensaje de texto operativo que se añade inmediatamente a la vista.

## Procesamiento Asíncrono IMAP/SMTP

- [ ] **Infraestructura asíncrona y procesamiento de correo IMAP** (pendiente)
  - Depende de: Controlador Unificado de Webhooks e Idempotencia
  - Criterio: M4.T1-C1: El sistema de tareas asíncronas reintenta operaciones fallidas de red utilizando backoff exponencial.
  - Criterio: M4.T1-C2: Los errores de conexión de correo se registran adecuadamente sin exponer credenciales ni datos sensibles.
- [ ] **Adaptador de Correo Electrónico: Ingesta periódica IMAP y Despacho SMTP** (pendiente)
  - Depende de: Infraestructura asíncrona y procesamiento de correo IMAP
  - Criterio: M4.T2-C1: El lector IMAP sondea periódicamente y normaliza los mensajes entrantes al modelo común.
  - Criterio: M4.T2-C2: El servicio SMTP despacha correctamente las respuestas de los agentes al buzón original del cliente.

## Gestión de Contactos y Fusión de Identidades

- [ ] **Lógica de fusión de identidades y gestión de contactos** (pendiente)
  - Depende de: Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant
  - Criterio: M6.T1-C1: Un cliente nuevo se crea automáticamente al registrar un contacto no existente en el canal.
  - Criterio: M6.T1-C2: La fusión de dos customers transfiere correctamente todos los contactos y conversaciones al customer principal.
  - Criterio: M6.T1-C3: Se rechaza e impide la fusión de customers que pertenecen a distintas empresas (tenants).
- [ ] **Interfaz de usuario para el perfil del cliente y fusión de identidades** (pendiente)
  - Depende de: Endpoints de la API para gestión de identidades y contactos
  - Criterio: M6.T3-C1: La pantalla de perfil muestra claramente todos los canales y contactos asociados al cliente.
  - Criterio: M6.T3-C2: El modal de fusión permite buscar el cliente secundario y muestra una confirmación antes de ejecutar la acción.
  - Criterio: M6.T3-C3: Las interfaces cumplen con los criterios de accesibilidad básica WCAG 2.1 AA.
- [ ] **Endpoints de la API para gestión de identidades y contactos** (pendiente)
  - Depende de: Lógica de fusión de identidades y gestión de contactos
  - Criterio: M6.T2-C1: El listado de customers devuelve resultados paginados correctamente.
  - Criterio: M6.T2-C2: El endpoint de fusión requiere privilegios de supervisor o administrador y valida los IDs de entrada.
  - Criterio: M6.T2-C3: Se documenta correctamente la especificación OpenAPI para los nuevos endpoints de contactos.
- [ ] **Pruebas de integridad y aislamiento para la fusión de clientes** (pendiente)
  - Depende de: Interfaz de usuario para el perfil del cliente y fusión de identidades
  - Criterio: M6.T4-C1: Los usuarios de una empresa jamás pueden consultar o fusionar clientes pertenecientes a otra empresa.
  - Criterio: M6.T4-C2: La suite de pruebas de integración de M6 se ejecuta y pasa exitosamente en el pipeline de CI.

## Cimientos y Esqueleto de Comunicación

- [ ] **Configuración del pipeline de Integración Continua (CI) y comprobaciones de calidad** (pendiente)
  - Depende de: Implementación del endpoint de salud /health y configuración de entornos en FastAPI, Configuración del proyecto frontend con React 18, TypeScript y Vite
  - Criterio: El pipeline de CI ejecuta con éxito la suite de pruebas del backend y del frontend en cada ejecución.
  - Criterio: El repositorio incluye el archivo README.md con instrucciones claras de instalación, ejecución y pruebas.
- [ ] **Implementación del endpoint de salud /health y configuración de entornos en FastAPI** (pendiente)
  - Criterio: El endpoint GET /health responde con código 200 y estado OK cuando la aplicación está operativa.
  - Criterio: La configuración por ambiente carga correctamente desde las variables de entorno mediante settings.
- [ ] **Configuración del proyecto frontend con React 18, TypeScript y Vite** (pendiente)
  - Criterio: El proyecto frontend compila correctamente en TypeScript con strict mode activado.
  - Criterio: La estructura de carpetas y componentes cumple con la jerarquía definida y los tests corren en verde.

## Seguridad y Autenticación

- [ ] **Refuerzo de Seguridad: RBAC y Hashing de Credenciales** (pendiente)
  - Depende de: Implementación de Inyección de Contexto de Tenant y Aislamiento
  - Criterio: M2.T3-C1: Las contraseñas se almacenan empleando un hash fuerte y nunca en texto plano.
  - Criterio: M2.T3-C2: Un usuario con rol agent recibe un error HTTP 403 al intentar acceder a rutas protegidas exclusivamente para roles admin o supervisor.

## Calidad y Pruebas

- [ ] **Pruebas de Integración de Aislamiento y Seguridad Multi-tenant** (pendiente)
  - Depende de: Endpoints de Gestión de Perfil y Usuarios (CRUD Básico)
  - Criterio: M2.T5-C1: Los usuarios de la Empresa A no pueden acceder a datos, perfiles ni recursos de la Empresa B mediante manipulación de parámetros de la API.
  - Criterio: M2.T5-C2: La verificación de tokens JWT expirados o alterados rechaza el acceso de forma inequívoca en todos los endpoints protegidos.

## Persistencia y Configuración de Base de Datos

- [ ] **Configuración de persistencia asíncrona y sistema de semillas de datos** (pendiente)
  - Depende de: Implementación del endpoint de salud /health y configuración de entornos en FastAPI
  - Criterio: M2.T1-C1: Las migraciones de Alembic se aplican exitosamente sobre la base de datos PostgreSQL creando todas las tablas requeridas por el modelo multi-tenant.
  - Criterio: M2.T1-C2: El script de semillas de datos inserta registros de prueba válidos sin incluir datos reales ni comprometer entornos de producción.

## Aislamiento Multi-tenant

- [ ] **Implementación de Inyección de Contexto de Tenant y Aislamiento** (pendiente)
  - Depende de: Configuración de persistencia asíncrona y sistema de semillas de datos
  - Criterio: M2.T2-C1: Las consultas a nivel de repositorio aplican automáticamente el filtro por company_id según el contexto de la sesión.
  - Criterio: M2.T2-C2: Las peticiones sin contexto de tenant válido son rechazadas inmediatamente con código HTTP 401 o 403.

## Gestión de Usuarios

- [ ] **Endpoints de Gestión de Perfil y Usuarios (CRUD Básico)** (pendiente)
  - Depende de: Refuerzo de Seguridad: RBAC y Hashing de Credenciales
  - Criterio: M2.T4-C1: El endpoint de creación de usuario valida correctamente los campos de entrada y rechaza correos malformados o faltantes.
  - Criterio: M2.T4-C2: Los listados de usuarios devuelven únicamente los registros asociados a la empresa del usuario autenticado y de forma paginada.

## Como cliente de la empresa, quiero comunicarme vía Telegram o Discord y que mis mensajes lleguen a la bandeja unificada sin alteraciones.

- [ ] **Adaptadores para Telegram Bot y Discord Bot** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: Los adaptadores de Telegram y Discord normalizan correctamente los formatos de mensajes entrantes de cada API.
  - Criterio: El despacho de mensajes salientes para Telegram y Discord se realiza de manera segura y controlando respuestas del API.

## Como agente de atención al cliente, quiero recibir y responder mensajes desde WhatsApp, Facebook Messenger e Instagram de forma unificada.

- [ ] **Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: El adaptador de Meta puede deserializar y normalizar correctamente un webhook de mensaje entrante de WhatsApp, Messenger e Instagram.
  - Criterio: El método de envío de mensajes realiza una llamada POST HTTP autorizada hacia la Graph API de Meta.

## Como administrador del sistema, quiero asegurar que las solicitudes entrantes de webhooks sean auténticas y que los reintentos de red del proveedor no dupliquen los mensajes.

- [ ] **Controlador Unificado de Webhooks e Idempotencia** (pendiente)
  - Depende de: Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram, Adaptadores para Telegram Bot y Discord Bot
  - Criterio: Se rechazan las peticiones a webhooks que no tengan firmas o tokens de verificación válidos.
  - Criterio: El endpoint de webhooks procesa el payload de manera idempotente usando el external_id del mensaje.

## Como administrador de canales de Meta, quiero garantizar el cumplimiento de las políticas de WhatsApp (ventana de 24h) para evitar penalizaciones en el número de teléfono.

- [ ] **Gestión de Salida y Restricción de Ventana 24h (WhatsApp HSM)** (pendiente)
  - Depende de: Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram, Controlador Unificado de Webhooks e Idempotencia
  - Criterio: Se bloquea el envío de un mensaje de texto libre si han transcurrido más de 24 horas desde la última interacción entrante de WhatsApp.
  - Criterio: Se permite el envío exitoso de un mensaje de plantilla autorizada (HSM) aun superando la ventana de 24 horas.

## Validación y Calidad del Módulo M4

- [ ] **Pruebas de integración de tareas asíncronas, resiliencia y purgado de datos (72h)** (pendiente)
  - Depende de: Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs
  - Criterio: M4.T4-C1: Las pruebas de retención y purgado (72h) comprueban que los mensajes eliminados de la tabla activa persisten en audit_logs.
  - Criterio: M4.T4-C2: Las respuestas de error en operaciones asíncronas y de red siguen un formato estándar y comprensible.

## Retención y Purgado de Datos

- [ ] **Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs** (pendiente)
  - Depende de: Adaptador de Correo Electrónico: Ingesta periódica IMAP y Despacho SMTP
  - Criterio: M4.T3-C1: La tarea de purgado identifica y elimina mensajes y adjuntos activos superadas las 72 horas.
  - Criterio: M4.T3-C2: Se genera un registro inmutable en audit_logs por cada mensaje purgado que permite su reconstrucción histórica.

## Sincronización en Tiempo Real Frontend

- [ ] **Cliente WebSocket en React con reconexión exponencial y sincronización en tiempo real** (pendiente)
  - Depende de: Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant, Construcción de la bandeja unificada en React 18
  - Criterio: M5.T4-C1: Reconectar automáticamente con backoff exponencial cuando la conexión WebSocket se interrumpe.
  - Criterio: M5.T4-C2: Actualizar el listado de conversaciones y el chat activo al recibir un mensaje entrante por el socket.

## Pruebas y Calidad de la Bandeja

- [ ] **Pruebas de integración E2E de la bandeja unificada y verificación de rendimiento** (pendiente)
  - Depende de: Cliente WebSocket en React con reconexión exponencial y sincronización en tiempo real, Skeleton loaders, estados vacíos/error accesibles y optimización de rendimiento
  - Criterio: M5.T6-C1: Completar el flujo E2E de login de agente, selección de conversación y respuesta en tiempo real sin errores.
  - Criterio: M5.T6-C2: Obtener una puntuación de rendimiento de Lighthouse superior o igual a 80 en la vista móvil de la bandeja.

## Experiencia de Usuario y Accesibilidad

- [ ] **Skeleton loaders, estados vacíos/error accesibles y optimización de rendimiento** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18, Buscador con debounce y filtros modernos combinables
  - Criterio: M5.T5-C1: Mostrar skeleton loaders con la forma exacta del layout mientras cargan los datos de las conversaciones.
  - Criterio: M5.T5-C2: Superar la auditoría de accesibilidad automática asegurando contraste y etiquetas correctas en todos los estados.

## Infraestructura de Tiempo Real

- [ ] **Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant** (pendiente)
  - Depende de: Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs
  - Criterio: M5.T1-C1: Rechazar conexiones WebSocket sin token JWT válido o con un token de otra empresa.
  - Criterio: M5.T1-C2: Publicar y recibir mensajes correctamente a través de los canales de Redis pub/sub.

## Filtros y Búsqueda en Bandeja

- [ ] **Buscador con debounce y filtros modernos combinables** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18
  - Criterio: M5.T3-C1: Ejecutar la búsqueda de conversaciones aplicando un debounce de 300ms sobre el input de texto.
  - Criterio: M5.T3-C2: Reflejar los estados de los filtros combinados directamente en los query params de la URL.

## Productividad de Agentes

- [ ] **Gestión de respuestas rápidas y categorización por etiquetas** (pendiente)
  - Depende de: Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant
  - Criterio: M7.T3-C1: Los usuarios de una empresa solo pueden visualizar y utilizar las respuestas rápidas y etiquetas creadas dentro de su propio tenant.
  - Criterio: M7.T3-C2: Las respuestas rápidas y etiquetas cuentan con validación de campos obligatorios y límites de longitud.

## Gestión de Canales y Cifrado

- [ ] **Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant** (pendiente)
  - Depende de: Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant
  - Criterio: M7.T1-C1: Las credenciales se almacenan completamente cifradas en la base de datos sin texto plano.
  - Criterio: M7.T1-C2: Solo los usuarios con rol de administrador de la misma empresa pueden gestionar sus canales.
  - Criterio: M7.T1-C3: Los campos de entrada de credenciales se validan estrictamente mediante esquemas Pydantic rechazando payloads malformados.

## Horarios y Respuestas Automáticas

- [ ] **Configuración de horarios de atención y despacho de respuestas automáticas fuera de horario** (pendiente)
  - Depende de: Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant
  - Criterio: M7.T2-C1: Los mensajes entrantes fuera del horario configurado generan una respuesta automática inmediata.
  - Criterio: M7.T2-C2: Los administradores pueden configurar y actualizar sus horarios de atención mediante la API REST.

## Analítica y Métricas

- [ ] **Motor de agregación de métricas de rendimiento y tablero analítico** (pendiente)
  - Depende de: Configuración de horarios de atención y despacho de respuestas automáticas fuera de horario, Gestión de respuestas rápidas y categorización por etiquetas
  - Criterio: M7.T4-C1: El tablero de métricas calcula correctamente los tiempos de respuesta y resolución en base al historial de conversaciones.
  - Criterio: M7.T4-C2: Las métricas están estrictamente aisladas por tenant y solo son accesibles por roles de supervisor y administrador.

## Aseguramiento de Calidad y Pruebas E2E

- [ ] **Pruebas de integración E2E del panel de administración, métricas y seguridad de credenciales cifradas** (pendiente)
  - Depende de: Panel de administración y métricas por empresa
  - Criterio: M7.T6-C1: El flujo completo de administración y métricas funciona de extremo a extremo contra una base de datos real en el entorno de CI.
  - Criterio: M7.T6-C2: Ningún dato ni configuración de una empresa puede ser accedido o modificado por otra empresa bajo ninguna circunstancia de prueba.

## Gestión de dependencias seguras para el despliegue a producción de uwuChat.

- [ ] **Auditoría de vulnerabilidades y fijación de dependencias** (pendiente)
  - Depende de: Configuración de cabeceras de seguridad y middleware HTTPS
  - Criterio: El escaneo de vulnerabilidades del backend con pip-audit retorna cero vulnerabilidades de criticidad alta o crítica.
  - Criterio: El escaneo de dependencias npm audit en el frontend finaliza con código de salida cero y libre de incidencias de riesgo alto.
  - Criterio: El proyecto cuenta con sus archivos de bloqueo (lockfiles) integrados en el repositorio de control de versiones.

## Control de calidad final, depuración de código muerto y monitorización del endpoint de salud.

- [ ] **Limpieza de código muerto y verificación final de salud** (pendiente)
  - Depende de: Manual de despliegue y documentación del proyecto
  - Criterio: El analizador de código huérfano e imports confirma que el proyecto está limpio de referencias no utilizadas y dependencias sin declarar.
  - Criterio: El endpoint de salud /health retorna un código de respuesta HTTP 200 conteniendo el estado del backend, conexión de persistencia y cola de caché Redis, sin filtrar secretos.
  - Criterio: La suite de pruebas completa del repositorio (unitarias, integración y extremo a extremo) culmina exitosamente en un entorno limpio sin fallos.

## Integridad de datos, respaldo periódico y mitigación ante fallos graves de persistencia.

- [ ] **Scripts de copia de seguridad y restauración de base de datos** (pendiente)
  - Depende de: Empaquetado reproducible con Docker and Docker Compose
  - Criterio: El script de copia de seguridad genera un archivo dump válido con extensión SQL o binaria comprimida que contiene los esquemas multi-tenant completos.
  - Criterio: El script de restauración reconstruye de forma idéntica todas las tablas de persistencia en un contenedor PostgreSQL recién inicializado, validado mediante comparación de esquemas.
  - Criterio: Procedimiento de restauración de desastres verificado por un operador humano a partir de la documentación proporcionada.

## Establecimiento de las guías de despliegue, variables de producción y metadatos SEO mínimos.

- [ ] **Manual de despliegue y documentación del proyecto** (pendiente)
  - Depende de: Suite de pruebas E2E de flujos críticos
  - Criterio: El archivo DEPLOY.md describe adecuadamente todas y cada una de las variables presentes en el archivo .env.example del proyecto.
  - Criterio: La documentación de despliegue detalla los comandos requeridos, la configuración de HTTPS, dominios, variables y cómo volver a una versión previa.
  - Criterio: La cabecera HTML del frontend de React expone títulos, meta descripciones de contenido, favicon institucional y metadatos básicos en formato Open Graph.

## Aseguramiento de flujos principales y aislamiento multi-tenant a nivel de producción.

- [ ] **Suite de pruebas E2E de flujos críticos** (pendiente)
  - Depende de: Scripts de copia de seguridad y restauración de base de datos
  - Criterio: El test de extremo a extremo simula con éxito la interacción del flujo crítico, cubriendo inicio de sesión, asignación de chat y respuesta sin provocar excepciones en el navegador ni en el servidor.
  - Criterio: La suite de pruebas contiene aserciones explícitas que intentan acceder de forma no autorizada a datos de un tenant ajeno, resultando en rechazo automático por parte de la API.

## Configuración de seguridad a nivel de red y transporte para todo el entorno del tenant.

- [ ] **Configuración de cabeceras de seguridad y middleware HTTPS** (pendiente)
  - Depende de: Pruebas de integración E2E del panel de administración, métricas y seguridad de credenciales cifradas
  - Criterio: Las respuestas del backend FastAPI devuelven las cabeceras HSTS, X-Content-Type-Options, Referrer-Policy y Content-Security-Policy (CSP) validadas por un cliente HTTP de pruebas.
  - Criterio: Cualquier solicitud HTTP entrante a rutas protegidas o públicas redirige con código 301/307 hacia su contraparte segura HTTPS.
  - Criterio: La aplicación no puede ser incrustada en iframes externos mediante validación estricta de frame-ancestors o X-Frame-Options.

## Estandarización de contenedores para desarrollo y producción mediante empaquetamiento seguro.

- [ ] **Empaquetado reproducible con Docker and Docker Compose** (pendiente)
  - Depende de: Auditoría de vulnerabilidades y fijación de dependencias
  - Criterio: La compilación de las imágenes Docker se ejecuta exitosamente sin requerir o instalar dependencias de desarrollo locales.
  - Criterio: El comando docker-compose up inicializa correctamente los servicios de DB, Redis, API y Frontend y permite interactuar con la interfaz en el puerto configurado.
  - Criterio: El contenedor de backend rechaza arrancar si faltan variables de entorno críticas necesarias para su ejecución.

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

## Como administrador de empresa, quiero una interfaz web amigable para administrar canales, horarios, respuestas rápidas y consultar el rendimiento de atención.

- [ ] **Panel de administración y métricas por empresa** (pendiente)
  - Depende de: Configuración de horarios de atención y despacho de respuestas automáticas fuera de horario, Gestión de respuestas rápidas y categorización por etiquetas, Motor de agregación de métricas de rendimiento y tablero analítico
  - Criterio: La ruta /admin restringe el acceso según rol y redirige a la bandeja a usuarios con rol agente.
  - Criterio: El formulario de conexión de canales permite configurar credenciales de forma segura sin mostrarlas en claro.
  - Criterio: El tablero de métricas renderiza KPIs y gráficos de volumen con selector de rango temporal.
  - Criterio: Verificación manual de la configuración de horarios de atención y mensajes de ausencia.

## Bandeja unificada de atención

- [ ] **Construcción de la bandeja unificada en React 18** (pendiente)
  - Depende de: Configuración del proyecto frontend con React 18, TypeScript y Vite, Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant
  - Criterio: T2-C1: Renderizar la lista de conversaciones y el panel de detalle de chat con badges específicos para cada canal soportado.
  - Criterio: T2-C2: Permitir la selección de conversación cambiando activamente el historial del chat mostrado.
  - Criterio: T2-C3: Adaptar la vista a pantallas de 360px permitiendo alternar entre lista y chat sin desbordamiento horizontal.

## Como arquitecto, quiero una interfaz común para todos los canales para poder añadir nuevos proveedores sin tocar la lógica de negocio central.

- [ ] **Desarrollo del motor de adaptadores de canales de mensajería** (pendiente)
  - Depende de: Pruebas de Integración de Aislamiento y Seguridad Multi-tenant
  - Criterio: M3-T1-C1: Definida clase abstracta BaseChannelAdapter con firma de métodos obligatorios.
  - Criterio: M3-T1-C2: AdapterFactory devuelve la instancia correcta según el enum de proveedores.

## Como administrador de soporte, quiero unificar los perfiles de un cliente que me escribe por distintos canales para tener su historial centralizado.

- [ ] **Lógica de fusión de identidades y gestión de contactos** (pendiente)
  - Depende de: Configuración de persistencia asíncrona y sistema de semillas de datos, Implementación de Inyección de Contexto de Tenant y Aislamiento
  - Criterio: La fusión de dos clientes se ejecuta en una única transacción de base de datos.
  - Criterio: Se prohíbe la fusión de clientes que pertenecen a diferentes empresas (tenants).
  - Criterio: Todas las conversaciones del cliente origen son transferidas íntegramente al cliente destino.

## Infraestructura asíncrona base para mensajería y tareas periódicas

- [ ] **Infraestructura asíncrona y procesamiento de correo IMAP** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería, Controlador Unificado de Webhooks e Idempotencia
  - Criterio: La instancia de Celery inicializa y establece conexión verificable con Redis en entorno de pruebas.
  - Criterio: El decorador de reintentos con backoff exponencial reprograma la tarea ante excepciones transitorias respetando el factor de espera.
  - Criterio: El registro de errores de Celery almacena metadatos y código de error en formato estructurado sin filtrar credenciales ni datos sensibles.

## Cimientos de la plataforma

- [ ] **Configuración del proyecto frontend con React 18, TypeScript y Vite** (pendiente)
  - Criterio: Vitest ejecuta con éxito el test unitario de renderizado del componente principal en frontend/src/App.test.tsx.
  - Criterio: La compilación estricta de tipos con tsc --noEmit finaliza con cero errores.
  - Criterio: El empaquetado de producción genera los artefactos en frontend/dist de forma limpia.
- [ ] **Configuración del pipeline de Integración Continua (CI) y comprobaciones de calidad** (pendiente)
  - Depende de: Configuración del proyecto frontend con React 18, TypeScript y Vite, Implementación del endpoint de salud /health y configuración de entornos en FastAPI
  - Criterio: El archivo de workflow .github/workflows/ci.yml cuenta con una estructura YAML válida con etapas para backend y frontend.
  - Criterio: El repositorio cuenta con archivos .env.example en la raíz y en backend/ y frontend/, y los archivos .env se encuentran bloqueados en .gitignore.
  - Criterio: El conjunto de pruebas automatizadas del proyecto se ejecuta en el pipeline y finaliza en verde.
- [ ] **Implementación del endpoint de salud /health y configuración de entornos en FastAPI** (pendiente)
  - Criterio: La petición GET /health retorna código HTTP 200 con cuerpo JSON {'status': 'ok', 'database': 'connected'} cuando la base de datos está disponible.
  - Criterio: La petición GET /health retorna código HTTP 503 cuando la base de datos no está disponible, sin exponer contraseñas ni stack traces.
  - Criterio: La configuración carga las variables desde el entorno y falla de forma temprana si faltan parámetros obligatorios.

## Como responsable de calidad, quiero asegurar que el aislamiento de datos es impenetrable antes de pasar a la integración con canales externos.

- [ ] **Pruebas de Integración de Aislamiento y Seguridad Multi-tenant** (pendiente)
  - Depende de: Endpoints de Gestión de Perfil y Usuarios (CRUD Básico)
  - Criterio: Test 'test_cross_tenant_data_leak' confirma que el Tenant A no puede ver registros del Tenant B.
  - Criterio: La eliminación de una empresa mediante script borra todos sus usuarios asociados en cascada.

## Como empresa, necesito que mis datos estén estrictamente aislados de los datos de otras empresas para cumplir con la privacidad.

- [ ] **Implementación de Inyección de Contexto de Tenant y Aislamiento** (pendiente)
  - Depende de: Configuración de persistencia asíncrona y sistema de semillas de datos
  - Criterio: La dependencia 'get_current_tenant' devuelve el ID de empresa correcto del token JWT.
  - Criterio: Toda consulta a la base de datos de una entidad multi-tenant incluye 'WHERE company_id = ...'.

## Como desarrollador, necesito un entorno de base de datos poblado y configurado correctamente para trabajar en las funcionalidades de negocio.

- [ ] **Configuración de persistencia asíncrona y sistema de semillas de datos** (pendiente)
  - Depende de: Implementación del endpoint de salud /health y configuración de entornos en FastAPI
  - Criterio: La aplicación se conecta a la base de datos PostgreSQL usando el driver asíncrono asyncpg.
  - Criterio: El script de seeds crea 2 empresas y 4 usuarios (admin, supervisor, agente) sin errores.
  - Criterio: La configuración de base de datos no contiene secretos hardcodeados, lee todo de .env.

## Como administrador de seguridad, necesito que el sistema use hashes fuertes y restrinja acciones según el rol del usuario.

- [ ] **Refuerzo de Seguridad: RBAC y Hashing de Credenciales** (pendiente)
  - Depende de: Implementación de Inyección de Contexto de Tenant y Aislamiento
  - Criterio: Las contraseñas en la base de datos se almacenan como hashes bcrypt no reversibles.
  - Criterio: Los endpoints marcados para ADMIN devuelven 403 Forbidden si el token pertenece a un AGENT.

## Como administrador de empresa, quiero poder gestionar a mis agentes para que puedan empezar a atender clientes.

- [ ] **Endpoints de Gestión de Perfil y Usuarios (CRUD Básico)** (pendiente)
  - Depende de: Refuerzo de Seguridad: RBAC y Hashing de Credenciales
  - Criterio: El listado de usuarios devuelve una respuesta paginada con metadatos (total, página, tamaño).
  - Criterio: Es imposible crear un usuario asignándolo a una empresa distinta a la del administrador autenticado.

## Como administrador, quiero cumplir con las políticas de WhatsApp para evitar el baneo del número de la empresa.

- [ ] **Gestión de Salida y Restricción de Ventana 24h (WhatsApp HSM)** (pendiente)
  - Depende de: Controlador Unificado de Webhooks e Idempotencia
  - Criterio: M3-T5-C1: Bloqueo de envío de texto libre en WhatsApp si han pasado > 24h desde el último mensaje del cliente.
  - Criterio: M3-T5-C2: Envío exitoso mediante plantilla aprobada (HSM) fuera de la ventana de 24 horas.

## Como empresa, quiero recibir mensajes de mis clientes de WhatsApp, Facebook e Instagram en un solo lugar.

- [ ] **Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: M3-T2-C1: Rechazo de webhooks con firma HMAC inválida para WhatsApp.
  - Criterio: M3-T2-C2: Conversión correcta de adjuntos (imágenes/audio) desde el JSON de Meta al modelo interno de mensajes.

## Como empresa tecnológica, quiero atender a mis comunidades de Telegram y Discord desde la misma plataforma.

- [ ] **Adaptadores para Telegram Bot y Discord Bot** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: M3-T3-C1: Verificación de token de Telegram en la cabecera X-Telegram-Bot-Api-Secret-Token.
  - Criterio: M3-T3-C2: Mensajes de Discord normalizados incluyendo el discriminador del usuario y contenido.

## Como operador del sistema, quiero garantizar que ningún mensaje se procese dos veces y que todos queden auditados.

- [ ] **Controlador Unificado de Webhooks e Idempotencia** (pendiente)
  - Depende de: Adaptadores de Redes Meta: WhatsApp, Messenger e Instagram, Adaptadores para Telegram Bot y Discord Bot
  - Criterio: M3-T4-C1: Mensajes duplicados con el mismo provider_msg_id son ignorados (idempotencia).
  - Criterio: M3-T4-C2: Todo mensaje recibido genera un registro en audit_logs de forma inmutable.

## Integración de canal de correo electrónico bidireccional

- [ ] **Adaptador de Correo Electrónico: Ingesta periódica IMAP y Despacho SMTP** (pendiente)
  - Depende de: Infraestructura asíncrona y procesamiento de correo IMAP, Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: La tarea de sondeo IMAP descarga correos no leídos y los normaliza correctamente en conversaciones y mensajes activos asignados a la empresa correspondiente.
  - Criterio: El despacho de correos salientes vía SMTP envía los datos al servidor configurado y marca el mensaje con estado de entrega o error.
  - Criterio: Los fallos transitorios de red durante el envío SMTP disparan reintentos automáticos sin generar duplicados en la base de datos.

## Cumplimiento de políticas de retención de datos efímeros y auditoría inmutable

- [ ] **Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs** (pendiente)
  - Depende de: Infraestructura asíncrona y procesamiento de correo IMAP
  - Criterio: Los mensajes con antigüedad superior a 72 horas son eliminados de la tabla messages de forma segura y en lotes transaccionales.
  - Criterio: Los mensajes con antigüedad inferior o igual a 72 horas permanecen intactos en la tabla messages tras la ejecución del purgado.
  - Criterio: Cada mensaje purgado cuenta con un registro correspondiente en audit_logs que contiene el payload completo y el company_id para su reconstrucción histórica.

## Validación de integración y resiliencia del sistema de mensajería asíncrona

- [ ] **Pruebas de integración de tareas asíncronas, resiliencia y purgado de datos (72h)** (pendiente)
  - Depende de: Adaptador de Correo Electrónico: Ingesta periódica IMAP y Despacho SMTP, Tarea de purgado automático a las 72 horas y archivo inmutable en audit_logs
  - Criterio: La suite de integración valida que los mensajes procesados y purgados después de 72h pueden reconstruirse fielmente desde audit_logs sin pérdida de información.
  - Criterio: Las tareas Celery concurrentes de diferentes empresas procesan colas manteniendo aislamiento absoluto de datos y credenciales por tenant.
  - Criterio: Los errores no recuperables en canales de correo quedan asentados en el registro de auditoría con código descriptivo y sin propagar excepciones no controladas.

## Experiencia de usuario y rendimiento

- [ ] **Skeleton loaders, estados vacíos/error accesibles y optimización de rendimiento** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18, Buscador con debounce y filtros modernos combinables, Cliente WebSocket en React con reconexión exponencial y sincronización en tiempo real
  - Criterio: T5-C1: Mostrar esqueletos de carga animados con la silueta de la lista y mensajes mientras se cargan los datos iniciales.
  - Criterio: T5-C2: Proveer botón de reintento funcional en la pantalla de error ante fallos de conexión HTTP o WebSocket.
  - Criterio: T5-C3: Verificar ausencia de violaciones de accesibilidad (axe-core) en la lista de conversaciones y controles de interacción.
  - Criterio: T5-C4: Comprobar que las rutas no existentes despliegan la página 404 estructurada con enlace a la bandeja.

## Calidad y verificación integral

- [ ] **Pruebas de integración E2E de la bandeja unificada y verificación de rendimiento** (pendiente)
  - Depende de: Skeleton loaders, estados vacíos/error accesibles y optimización de rendimiento
  - Criterio: T6-C1: Completar el ciclo de lectura, filtrado y envío de respuesta en tiempo real simulado de extremo a extremo sin recargar la página.
  - Criterio: T6-C2: Desconectar y limpiar adecuadamente las suscripciones WebSocket al desmontar el componente de chat sin dejar listeners colgados.
  - Criterio: T6-C3: Validar que el bundle de la aplicación en producción divide adecuadamente los chunks principales sin exceder presupuestos de tamaño.

## Comunicación en tiempo real

- [ ] **Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant** (pendiente)
  - Depende de: Pruebas de integración de tareas asíncronas, resiliencia y purgado de datos (72h)
  - Criterio: T1-C1: Rechazar conexiones WebSocket que no envíen token JWT válido o cuyo token haya expirado con código de cierre 4401.
  - Criterio: T1-C2: Garantizar aislamiento estricto impidiendo que los mensajes emitidos por el tenant A lleguen a los WebSockets conectados del tenant B.
  - Criterio: T1-C3: Difundir eventos estructurados de asignación y cambio de estado de conversación a todos los agentes activos de la misma empresa.

## Buscador y filtros avanzados

- [ ] **Buscador con debounce y filtros modernos combinables** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18
  - Criterio: T3-C1: Retardar la ejecución del filtrado durante 300 ms mientras el usuario teclea en el buscador.
  - Criterio: T3-C2: Reflejar las facetas activas de canal, estado y agente en los parámetros query de la URL del navegador.
  - Criterio: T3-C3: Mostrar coincidencia resaltada o estado vacío específico si ningún chat coincide con el texto buscado.

## Sincronización en tiempo real

- [ ] **Cliente WebSocket en React con reconexión exponencial y sincronización en tiempo real** (pendiente)
  - Depende de: Endpoint WebSocket en FastAPI para eventos de chat y aislamiento de tenant, Construcción de la bandeja unificada en React 18
  - Criterio: T4-C1: Reintentar la conexión con retraso creciente (backoff exponencial) tras una pérdida abrupta de socket.
  - Criterio: T4-C2: Añadir mensajes entrantes recibidos por WebSocket en el hilo de la conversación activa sin requerir recargar la página.
  - Criterio: T4-C3: Mostrar indicador visual del estado de conectividad en tiempo real (en línea / reconectando).

## Como agente de atención, quiero poder ver rápidamente qué otros canales tiene vinculados el cliente y fusionarlo si detecto un duplicado.

- [ ] **Interfaz de usuario para el perfil del cliente y fusión de identidades** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18, Endpoints de la API para gestión de identidades y contactos
  - Criterio: El buscador de clientes para fusión aplica un debounce para evitar peticiones excesivas.
  - Criterio: Se muestra un diálogo de confirmación antes de proceder con la fusión, advirtiendo que es irreversible.
  - Criterio: La interfaz es totalmente accesible mediante teclado y cumple contrastes WCAG AA.

## Como responsable de seguridad, quiero garantizar que la fusión de identidades no rompa el aislamiento de datos entre empresas.

- [ ] **Pruebas de integridad y aislamiento para la fusión de clientes** (pendiente)
  - Depende de: Interfaz de usuario para el perfil del cliente y fusión de identidades
  - Criterio: La tabla audit_logs contiene un registro detallado del evento de fusión con los IDs involucrados.
  - Criterio: Un agente de la Empresa A no puede listar ni fusionar clientes de la Empresa B aunque conozca sus IDs.

## Como desarrollador, necesito una API segura para gestionar la relación entre contactos de canales y perfiles de cliente.

- [ ] **Endpoints de la API para gestión de identidades y contactos** (pendiente)
  - Depende de: Lógica de fusión de identidades y gestión de contactos
  - Criterio: El endpoint de fusión devuelve un error 400 con un mensaje claro si los clientes no pertenecen a la misma empresa.
  - Criterio: El detalle del cliente incluye la lista de canales/contactos asociados (ej. su WhatsApp ID y su Telegram handle).
  - Criterio: Las respuestas de error siguen el formato estándar definido en el proyecto.

## Como empresa, deseo configurar los horarios de atención y un mensaje automático de bienvenida o ausencia para que los clientes sepan cuándo serán atendidos.

- [ ] **Configuración de horarios de atención y despacho de respuestas automáticas fuera de horario** (pendiente)
  - Depende de: Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant
  - Criterio: El servicio evalúa con precisión si una conversación entra dentro o fuera del horario comercial según la zona horaria IANA de la empresa.
  - Criterio: Se despacha el mensaje automático fuera de horario solo una vez por conversación entrante fuera de turno.
  - Criterio: Endpoint REST para actualizar horario y mensaje fuera de oficina valida formato y esquema.

## Como administrador de empresa, quiero dar de alta y gestionar los canales de comunicación de forma segura sin exponer credenciales ni claves de acceso.

- [ ] **Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant** (pendiente)
  - Depende de: Pruebas de integración E2E de la bandeja unificada y verificación de rendimiento
  - Criterio: Las credenciales de los canales se persisten cifradas en base de datos y no se exponen valores en texto claro al consultar la tabla directamente.
  - Criterio: Los endpoints GET de canales devuelven las credenciales enmascaradas y rechazan solicitudes de agentes que no posean rol de administrador.
  - Criterio: Aislamiento multi-tenant estricto en la administración de canales.

## Como agente y supervisor, quiero disponer de respuestas rápidas y etiquetas para estandarizar la atención y categorizar los motivos de contacto.

- [ ] **Gestión de respuestas rápidas y categorización por etiquetas** (pendiente)
  - Depende de: Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant
  - Criterio: CRUD completo de respuestas rápidas con validación de atajo único por empresa.
  - Criterio: Permisos RBAC diferenciados para administración y consulta de respuestas rápidas.
  - Criterio: Asignación y remoción de etiquetas en conversaciones con persistencia transaccional.

## Como supervisor o administrador, quiero visualizar métricas de tiempos de respuesta, resolución y volúmenes para optimizar la productividad del equipo.

- [ ] **Motor de agregación de métricas de rendimiento y tablero analítico** (pendiente)
  - Depende de: Servicio de cifrado de credenciales y gestión CRUD de canales multi-tenant
  - Criterio: Cálculo preciso del Tiempo de Primera Respuesta (FRT) y Tiempo de Resolución (TTR).
  - Criterio: Agregación por canal y agente con filtros de rango de fechas.
  - Criterio: Protección de datos y aislamiento tenant en las métricas.

## Como equipo de calidad y seguridad, queremos garantizar la integridad de los datos de administración, la confidencialidad de las credenciales y la precisión de los reportes analíticos.

- [ ] **Pruebas de integración E2E del panel de administración, métricas y seguridad de credenciales cifradas** (pendiente)
  - Depende de: Panel de administración y métricas por empresa
  - Criterio: Flujo E2E completo de alta de canal, configuración de horario y visualización de métricas.
  - Criterio: Verificación automatizada de no fuga de secretos en respuestas HTTP ni registros de logs.
  - Criterio: Aislamiento multi-tenant validado en todas las operaciones del panel administrativo.

## Como administrador del sistema, quiero que la plataforma sea segura por defecto para proteger los datos de las empresas.

- [ ] **Configuración de cabeceras de seguridad y middleware HTTPS** (pendiente)
  - Depende de: Pruebas de integración E2E del panel de administración, métricas y seguridad de credenciales cifradas
  - Criterio: La respuesta del backend incluye la cabecera Strict-Transport-Security con max-age de al menos un año.
  - Criterio: La cabecera Content-Security-Policy (CSP) está presente y restringe orígenes no deseados.
  - Criterio: Las peticiones HTTP son redirigidas automáticamente a HTTPS.

## Como responsable de seguridad, quiero asegurar que no usamos librerías comprometidas en producción.

- [ ] **Auditoría de vulnerabilidades y fijación de dependencias** (pendiente)
  - Depende de: Configuración de cabeceras de seguridad y middleware HTTPS
  - Criterio: El comando 'pip-audit' devuelve 0 vulnerabilidades críticas o altas en el entorno virtual del backend.
  - Criterio: El comando 'npm audit' en la carpeta frontend no reporta vulnerabilidades de nivel 'high' o superior.

## Como DevOps, quiero un despliegue reproducible en cualquier entorno para evitar el 'en mi máquina funciona'.

- [ ] **Empaquetado reproducible con Docker y Docker Compose** (pendiente)
  - Depende de: Auditoría de vulnerabilidades y fijación de dependencias
  - Criterio: Las imágenes de Docker se construyen sin errores y pesan menos de 500MB cada una.
  - Criterio: El comando 'docker compose up' levanta todos los servicios y la aplicación responde en localhost.

## Como QA, quiero validar que las funcionalidades centrales no se rompan antes de cada despliegue.

- [ ] **Suite de pruebas E2E de flujos críticos** (pendiente)
  - Depende de: Empaquetado reproducible con Docker y Docker Compose
  - Criterio: El test de 'flujo completo de atención' termina con éxito simulando un cliente real.
  - Criterio: Los tests comprueban que no se filtran datos de otras empresas (aislamiento multi-tenant) durante el flujo visual.

## Como nuevo desarrollador o sysadmin, quiero poder poner en marcha el sistema sin ayuda externa.

- [ ] **Manual de despliegue y documentación del proyecto** (pendiente)
  - Depende de: Suite de pruebas E2E de flujos críticos
  - Criterio: El archivo README.md incluye todas las secciones requeridas por PRD-DOC-01.
  - Criterio: DEPLOY.md describe cómo realizar una actualización (rollback incluido) sin pérdida de datos.

## Como dueño del producto, quiero garantizar la recuperación de datos ante fallos catastróficos.

- [ ] **Scripts de copia de seguridad y restauración de base de datos** (pendiente)
  - Depende de: Empaquetado reproducible con Docker y Docker Compose
  - Criterio: El script backup.sh genera un archivo .sql.gz válido en la carpeta de backups.
  - Criterio: Una base de datos vacía puede ser restaurada al estado del backup usando restore.sh.

## Como equipo de operaciones, quiero un sistema limpio y fácil de monitorear en producción.

- [ ] **Limpieza de código muerto y verificación final de salud** (pendiente)
  - Depende de: Manual de despliegue y documentación del proyecto
  - Criterio: Las herramientas de análisis de código muerto no reportan hallazgos significativos.
  - Criterio: El endpoint /health devuelve 503 si la base de datos está caída y 200 si todo es funcional.

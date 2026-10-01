# Perfil de producción

Requisitos que esta aplicación web cumple para considerarse lista para producción (no un MVP). Mnemosine los comprueba en la pestaña Producción; el plan de tareas incluye trabajo para cada uno.

## Calidad

- **PRD-QA-01 — Pruebas automáticas en cada entrega.** La CI del repositorio instala, compila y ejecuta todos los tests en cada pull/merge request y en la rama del proyecto. Nada se fusiona con la CI en rojo.
- **PRD-QA-02 — Pruebas de los flujos principales de principio a fin.** Tests de integración o de extremo a extremo (E2E) que recorren los flujos principales como los usaría una persona: inicio de sesión si existe, las operaciones centrales del negocio y los errores más comunes, contra la base de datos real del proyecto levantada en la CI (nunca la de producción).
- **PRD-QA-03 — Sin código muerto ni duplicado.** Cuando algo se reemplaza dentro de la misma versión, lo anterior se elimina con sus referencias, imports, tests, configuración y dependencias. La versión termina con una revisión que quita funciones, archivos, código comentado y dependencias sin uso, con la herramienta de análisis del stack (por ejemplo knip, vulture, deadcode o el analizador del IDE) ejecutada en la CI.
- **API-04 — Errores consistentes y listados paginados.** Las respuestas de error tienen un formato estable y el código HTTP correcto; los listados están paginados.

## Seguridad

- **PRD-SEC-01 — Sin secretos en el código.** Claves, tokens y contraseñas solo en variables de entorno o en el gestor de secretos del hosting. El repositorio incluye un .env.example con los nombres de las variables y sin valores reales, y .env está en .gitignore.
- **PRD-SEC-02 — Dependencias sin vulnerabilidades conocidas.** Las dependencias están fijadas con su archivo de bloqueo (lockfile) y la CI ejecuta la auditoría del gestor de paquetes (npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, composer audit...) sin vulnerabilidades altas o críticas.
- **PRD-SEC-03 — Todas las entradas validadas.** Toda entrada externa (formularios, parámetros, archivos, mensajes, variables) se valida y se rechaza con un mensaje claro. Sin inyección SQL/NoSQL, XSS, rutas manipuladas ni ejecución de comandos.
- **PRD-DATA-05 — Acceso a datos con mínimos privilegios.** La aplicación usa un usuario de base de datos con solo los permisos que necesita y consultas parametrizadas; los datos de cada usuario o empresa solo los ve quien corresponde.
- **WEB-SEC-01 — HTTPS y cabeceras de seguridad.** Se sirve solo por HTTPS con HSTS, Content-Security-Policy, X-Content-Type-Options, Referrer-Policy y protección contra iframes (X-Frame-Options o frame-ancestors).
- **WEB-SEC-02 — Cuentas y sesiones seguras.** Si hay usuarios: contraseñas con hash fuerte (Argon2 o bcrypt), sesiones en cookies HttpOnly/Secure/SameSite o tokens con expiración, protección CSRF, límite de intentos y recuperación de cuenta segura.
- **API-02 — Autenticación y autorización en cada endpoint.** Cada endpoint protegido comprueba quién llama y qué puede hacer, incluido que nadie acceda a datos de otro usuario o empresa.
- **API-03 — Límite de peticiones y CORS restringido.** Límites por IP o por usuario en los endpoints sensibles (inicio de sesión, registro, envío de mensajes) y CORS solo para los orígenes conocidos.

## Datos

- **PRD-DATA-01 — Esquema versionado con migraciones.** Cada cambio del modelo de datos es una migración versionada que se aplica automáticamente al desplegar y puede revertirse. El modelo coincide con contracts/schemas/database.json de la memoria del proyecto.
- **PRD-DATA-03 — Copias de seguridad y restauración probadas.** Procedimiento documentado (y automatizado si el hosting lo permite) para respaldar la base de datos de producción y restaurarla. La restauración se probó al menos una vez.
- **PRD-DATA-04 — Datos de prueba separados de producción.** Semillas o fixtures para desarrollo y tests. Nunca datos reales en el repositorio ni en los tests.

## Operación

- **PRD-OPS-01 — Registro de errores y mensajes comprensibles.** Los errores se registran con el contexto necesario para diagnosticarlos, sin datos personales ni secretos. La persona usuaria ve mensajes comprensibles, nunca trazas internas.
- **PRD-DEP-04 — Endpoint de salud.** Una ruta /health (o equivalente) responde 200 cuando la aplicación y sus dependencias (por ejemplo la base de datos) están disponibles, sin exponer datos internos.

## Despliegue

- **PRD-DEP-01 — Configuración por ambiente.** La aplicación lee de variables de entorno todo lo que cambia entre local, desarrollo y producción (URLs, base de datos, claves, nivel de logs). Nada de eso está escrito en el código.
- **PRD-DEP-02 — Empaquetado reproducible.** Un Dockerfile/compose o el archivo del hosting (render.yaml, fly.toml, vercel.json, netlify.toml, firebase.json, Procfile...) construye y arranca la aplicación igual en cualquier máquina.
- **PRD-DEP-05 — Ambiente de desarrollo desplegado y respondiendo.** La rama del proyecto está desplegada en el ambiente de desarrollo y su URL responde. Ahí se prueba cada versión antes de publicarla.
- **PRD-DEP-06 — Producción desplegada y respondiendo.** Tras publicar la versión, producción ejecuta esa versión y su URL responde.

## Experiencia

- **WEB-UX-01 — Diseño adaptable a móvil, tableta y escritorio.** Todas las pantallas se usan bien desde 360 px de ancho hasta escritorio, sin desbordes ni textos cortados.
- **WEB-UX-02 — Accesibilidad básica (WCAG 2.1 AA).** Contraste suficiente, uso completo con teclado, etiquetas en formularios y textos alternativos, comprobado con una herramienta automática (axe o Lighthouse) en los tests.
- **WEB-UX-03 — Estados de carga, vacío y error; páginas 404 y 500.** Cada pantalla muestra qué está pasando mientras carga, cuando no hay datos y cuando algo falla, con una salida para la persona usuaria.
- **WEB-PERF-01 — Carga rápida.** Build de producción minificado, recursos comprimidos, imágenes optimizadas y carga diferida; objetivo Lighthouse Performance ≥ 80 en móvil.

## Documentación

- **PRD-DOC-01 — README para instalar, ejecutar y probar.** README en la raíz con: qué es, requisitos, instalación, variables de entorno, cómo ejecutarlo en local, cómo ejecutar los tests y cómo está organizado el código, escrito para alguien que empieza.
- **PRD-DEP-03 — Guía de despliegue paso a paso.** DEPLOY.md en la raíz explica, para alguien sin experiencia, cómo desplegar en cada ambiente: hosting recomendado, variables, base de datos, dominio y HTTPS, cómo actualizar y cómo volver a la versión anterior.
- **API-01 — Contrato de la API documentado (OpenAPI).** Cada endpoint documentado con su método, parámetros, respuestas y errores en una especificación OpenAPI publicada o generada por el framework.

## Distribución

- **WEB-SEO-01 — SEO básico y metadatos para compartir.** Título y descripción por página, favicon, metadatos Open Graph, robots.txt y sitemap si el sitio es público.

## Legal

- **WEB-LEG-01 — Privacidad y consentimiento de cookies.** Si recoge datos personales o usa cookies no esenciales: política de privacidad accesible y consentimiento.

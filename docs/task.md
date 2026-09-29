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
  - Criterio: Adaptadores funcionales para WhatsApp, Telegram y Discord.
  - Criterio: Validación de firmas criptográficas en webhooks de entrada.
  - Criterio: Normalización de adjuntos (imágenes, audio) a una estructura común.
  - Criterio: Uso de Idempotency Key basada en el ID de mensaje del proveedor externo.

## Gestión de Datos y Tenants

- [x] **Diseño y migración de base de datos multi-tenant** (completada)
  - Depende de: Configuración del proyecto backend con FastAPI y estructura hexagonal
  - Criterio: Los modelos reflejan las relaciones requeridas sin fugas de datos entre empresas.
  - Criterio: Se implementan migraciones de base de datos automatizadas.
  - Criterio: Se aplican restricciones de aislamiento por tenant en las consultas.

## Canal de Correo y Resiliencia

- [ ] **Infraestructura asíncrona y procesamiento de correo IMAP** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería
  - Criterio: Sondeo IMAP funcional recuperando correos no leídos.
  - Criterio: Cola de tareas para envío de mensajes salientes.
  - Criterio: Mecanismo de reintento observable en logs ante fallos de red con proveedores.

## Bandeja de Entrada

- [ ] **Construcción de la bandeja unificada en React 18** (pendiente)
  - Depende de: Infraestructura asíncrona y procesamiento de correo IMAP
  - Criterio: Mensajes entrantes aparecen instantáneamente sin refrescar.
  - Criterio: Buscador filtra contactos y mensajes con debounce de 300ms.
  - Criterio: Skeleton loading aplicado durante la carga inicial de conversaciones.
  - Criterio: Aislamiento visual: un agente solo ve datos de su propia empresa.

## Seguridad y Accesos

- [x] **Implementación del módulo de autenticación y autorización JWT** (completada)
  - Depende de: Diseño y migración de base de datos multi-tenant
  - Criterio: Endpoints de login y emisión de tokens seguros.
  - Criterio: Middleware de validación de roles y aislamiento por empresa operativo.
  - Criterio: Pruebas unitarias para los flujos de autenticación.

## Gestión de Contactos

- [ ] **Lógica de fusión de identidades y gestión de contactos** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18
  - Criterio: Posibilidad de unir un contacto de WhatsApp y uno de Telegram en un mismo perfil.
  - Criterio: Historial unificado de mensajes en la vista de cliente fusionado.
  - Criterio: Validación de que ambos contactos pertenecen a la misma empresa (tenant).

## Administración y Business Intelligence

- [ ] **Panel de administración y métricas por empresa** (pendiente)
  - Depende de: Construcción de la bandeja unificada en React 18
  - Criterio: Gráficos de volumen de mensajes por canal/agente.
  - Criterio: Configuración de horario de atención reflejada en mensajes automáticos.
  - Criterio: CRUD de respuestas rápidas funcional en la bandeja de chat.

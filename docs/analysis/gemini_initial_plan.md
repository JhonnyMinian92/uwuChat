# Gemini Initial Plan

Análisis inicial y plan de producto finalizados para uwuChat. Se ha diseñado una arquitectura hexagonal para gestionar la integración de múltiples canales de mensajería (Meta, Telegram, Discord, Email). Se ha integrado la lógica de retención efímera de 72 horas para mensajes y adjuntos en la base de datos transaccional, con persistencia inmutable en logs de auditoría estructurados para cumplimiento legal y recuperación. El plan de construcción prioriza la base multi-tenant y el esqueleto funcional antes de escalar a los adaptadores específicos.

## Changes

- Ajuste del esquema de base de datos para incluir la tabla 'hsm_templates' dentro de la lista de tablas principal.
- Refinamiento de la jerarquía de archivos para soportar una estructura hexagonal clara tanto en el dominio como en los adaptadores de infraestructura.
- Establecimiento de la política de nombres para tests basada en códigos de criterios de aceptación (ej. T1-C1).

## Mapa del producto

Mnemosine planifica todas las tareas de cada módulo después de este análisis (analysis/product_plan.md).

- **M1** Cimientos y Esqueleto de Comunicación (foundation)
  - Estructura base del repositorio, configuración de entornos y primer test de punta a punta con endpoint de salud.
  - Requisitos de producción: PRD-QA-01, PRD-SEC-01, PRD-DEP-04, PRD-DEP-05, PRD-DOC-01
- **M2** Persistencia Multi-tenant y Autenticación (foundation)
  - Base de datos PostgreSQL configurada con migraciones y sistema de autenticación JWT con aislamiento por empresa.
  - Requisitos de producción: PRD-DATA-01, PRD-DATA-04, PRD-DATA-05, API-02, WEB-SEC-02
- **M3** Motor de Adaptadores y Webhooks (feature)
  - Implementación de la interfaz común para canales de mensajería y recepción de eventos de Meta y Telegram.
  - Requisitos de producción: PRD-SEC-03, API-01, API-03
- **M4** Procesamiento Asíncrono y Retención de Datos (feature)
  - Gestión de colas para correo IMAP/SMTP y cumplimiento de la política de purgado de 72 horas.
  - Requisitos de producción: PRD-OPS-01, API-04
- **M5** Bandeja Unificada y Tiempo Real (feature)
  - Interfaz web para agentes con actualizaciones en tiempo real mediante WebSockets.
  - Requisitos de producción: WEB-UX-01, WEB-UX-03, WEB-PERF-01
- **M6** Gestión de Contactos y Fusión de Identidades (feature)
  - Capacidad de unificar clientes que escriben desde diferentes canales en una sola ficha.
  - Requisitos de producción: API-04
- **M7** Administración, Horarios y Plantillas HSM (feature)
  - Panel de control para la empresa, configuración de canales y gestión de plantillas de WhatsApp.
  - Requisitos de producción: PRD-SEC-01
- **M8** Operaciones y Endurecimiento (production)
  - Preparación final para producción con seguridad, monitoreo y despliegue automatizado.
  - Requisitos de producción: PRD-QA-02, PRD-SEC-02, PRD-DATA-03, PRD-DEP-01, PRD-DEP-02, PRD-DEP-03, WEB-SEC-01, WEB-SEO-01, WEB-LEG-01

## Tasks

- Se planifican por módulo.

## Tests

- No tests generated.

## Rationale

- Se ha validado que el product_map cubre el 100% de los requisitos funcionales, incluyendo el purgado de 72h y la gestión de plantillas HSM.
- Se ha elegido una arquitectura hexagonal para facilitar la adición de nuevos canales de mensajería (adaptadores) sin modificar la lógica de conversaciones central.
- La inclusión de Optimistic Concurrency en el esquema de base de datos responde a la necesidad de evitar conflictos en la asignación de agentes en un entorno SaaS concurrente.
- Se han incluido las reglas de Mnemosine para garantizar la trazabilidad de los tests con los criterios de aceptación desde el inicio.

## Warnings

- El purgado de mensajes a las 72 horas requiere una tarea en segundo plano (Celery) altamente confiable para no saturar la base de datos de auditoría durante picos de tráfico.
- La integración con Meta requiere que el ambiente de desarrollo sea accesible vía HTTPS para recibir webhooks reales (se sugiere ngrok o similar en la documentación de despliegue).

## Assumptions

- Se asume que el sistema de logs de auditoría no almacenará archivos binarios pesados (imágenes/audio), sino enlaces temporales o metadatos, delegando el almacenamiento binario a un bucket S3 con TTL si fuera necesario.

## Memory changes

- Aplicado: rules.md — Incorporación de reglas de calidad de Mnemosine y políticas de limpieza de código.
- Aplicado: architecture/hierarchy.md — Definición de la jerarquía de archivos para arquitectura hexagonal con FastAPI y React.
- Aplicado: contracts/schemas/database.json — Actualización del esquema de base de datos incluyendo hsm_templates y versionado para concurrencia optimista.
- Rechazado: analysis/constraints.md — Gemini no recibió el contenido completo de este archivo

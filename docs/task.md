# Tareas — uwuChat

Plan de implementación generado por Mnemosine. El estado vivo de cada tarea está en Mnemosine;
este archivo es una foto del plan en el momento de la última publicación.

## Infraestructura Base Backend

- [ ] **Configuración del proyecto backend con FastAPI y estructura hexagonal** (pendiente)
  - Criterio: El servidor levanta correctamente con Uvicorn.
  - Criterio: La estructura de directorios respeta los principios de arquitectura hexagonal.
  - Criterio: El entorno de desarrollo está completamente documentado y funcional.

## Gestión de Datos y Tenants

- [ ] **Diseño y migración de base de datos multi-tenant** (pendiente)
  - Depende de: Configuración del proyecto backend con FastAPI y estructura hexagonal
  - Criterio: Los modelos reflejan las relaciones requeridas sin fugas de datos entre empresas.
  - Criterio: Se implementan migraciones de base de datos automatizadas.
  - Criterio: Se aplican restricciones de aislamiento por tenant en las consultas.

## Seguridad y Accesos

- [ ] **Implementación del módulo de autenticación y autorización JWT** (pendiente)
  - Depende de: Diseño y migración de base de datos multi-tenant
  - Criterio: Endpoints de login y emisión de tokens seguros.
  - Criterio: Middleware de validación de roles y aislamiento por empresa operativo.
  - Criterio: Pruebas unitarias para los flujos de autenticación.

## Integración de Canales

- [ ] **Desarrollo del motor de adaptadores de canales de mensajería** (pendiente)
  - Depende de: Implementación del módulo de autenticación y autorización JWT
  - Criterio: Normalización correcta de mensajes entrantes de cada canal a un modelo común.
  - Criterio: Cifrado seguro de credenciales de canales en la base de datos.
  - Criterio: Manejo de webhooks verificados por firma criptográfica.

## Frontend y Bandeja Unificada

- [ ] **Construcción de la bandeja unificada en React 18** (pendiente)
  - Depende de: Implementación del módulo de autenticación y autorización JWT
  - Criterio: Renderizado fluido de la bandeja con WebSockets integrados para mensajes en tiempo real.
  - Criterio: Filtros combinables y buscador operativos con manejo de estado vacío.
  - Criterio: Uso correcto de Skeleton loading para la carga de datos.

## Administración y Métricas

- [ ] **Panel de administración y métricas por empresa** (pendiente)
  - Depende de: Desarrollo del motor de adaptadores de canales de mensajería, Construcción de la bandeja unificada en React 18
  - Criterio: CRUD completo de configuración empresarial y agentes desde la UI.
  - Criterio: Cálculo preciso de métricas por empresa, canal y agente.
  - Criterio: Pruebas de integración para los flujos administrativos.

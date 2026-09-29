# Test Strategy

- Define test requirements during Gemini analysis.

# Reused Testing from Central Memory


## testing/test_pyramid.md

# Test Pyramid

## Intent
Balance fast feedback and broad confidence by using many focused tests, fewer integration tests and a smaller set of end-to-end tests.

## Applicability
Use as a planning heuristic for automated verification of software where different test levels provide different cost, speed and isolation characteristics.

## Non-applicability
Do not treat the pyramid as a fixed percentage rule. Systems dominated by integration boundaries, distributed behavior or user journeys may require a different distribution based on risk.

## Structure / responsibilities
- **Unit tests:** verify small units in isolation.
- **Integration tests:** verify real interactions between components or infrastructure boundaries.
- **End-to-end tests:** verify critical user-visible workflows across the system.
- **Test strategy:** maps risk and requirements to the appropriate level.
- **Quality gate:** prevents release when required critical behavior is unverified.

## Implementation guidance
1. Identify critical business and security risks.
2. Cover deterministic business logic with fast unit tests.
3. Use integration tests for persistence, APIs, queues and important boundaries.
4. Reserve end-to-end tests for critical workflows that require system-level confidence.
5. Add regression tests for defects at the lowest level that reproduces the failure reliably.
6. Keep tests deterministic and independent.
7. Measure useful coverage and mutation/risk signals rather than chasing a percentage alone.

## Validation criteria
- Critical requirements map to explicit tests.
- Unit tests remain fast and isolated.
- Integration tests exercise important real boundaries.
- Critical user journeys have appropriate end-to-end coverage.
- Defects gain durable regression tests.

## Security considerations
Security-sensitive behavior must be tested at the boundary where controls actually operate. Include authentication, authorization, validation, injection resistance, sensitive-data handling and security regression tests according to risk.

## Trade-offs
More unit tests usually improve speed and diagnosis, while integration and end-to-end tests provide stronger boundary confidence at higher cost and fragility. The optimal distribution follows system risk rather than a universal ratio.

## Related skills and patterns
- `testing.test_strategy`
- `testing.unit_testing`
- `testing.integration_testing`
- `testing.e2e_testing`
- `testing.quality_gate`
- `testing.contract_testing`

## Example decision signals
- **Pure deterministic logic:** prioritize unit tests.
- **Database transaction behavior:** add integration coverage.
- **Critical login journey:** add end-to-end coverage.
- **API provider/consumer boundary:** add contract tests.

## Tests required by Gemini

- Pruebas de aislamiento de base de datos: Verificar que el usuario de una empresa no puede leer datos de otra.
- Pruebas de retención y purgado: Comprobar que los mensajes y adjuntos superadas las 72 horas son eliminados del almacenamiento activo pero persisten en los logs estructurados de auditoría.
- Pruebas de plantillas WhatsApp (HSM): Validar el comportamiento de envío fuera de la ventana de 24 horas usando plantillas genéricas.
- Pruebas de concurrencia y conflictos en la asignación de conversaciones.

## Tests required by Gemini

- Pruebas de aislamiento multi-tenant: Verificar que usuarios de Empresa A no pueden acceder a datos, mensajes ni conversaciones de Empresa B vía API o WebSockets.
- Pruebas de retención y purgado (72h): Verificar que la tarea de limpieza elimina mensajes y adjuntos activos tras 72 horas y que estos pueden reconstruirse desde audit_logs.
- Pruebas de verificación criptográfica: Comprobar rechazo de webhooks con firma HMAC inválida para Meta y token erróneo en Telegram.
- Pruebas de plantillas WhatsApp (HSM): Validar el bloqueo de mensajes libres fuera de las 24 horas y permitir el despacho exitoso mediante plantilla aprobada.
- Pruebas de concurrencia y asignación: Validar la asignación de conversaciones usando Optimistic Concurrency para prevenir sobrescrituras entre agentes.


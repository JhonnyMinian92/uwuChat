# Project and Agent Rules

- Nunca colocar credenciales, tokens o claves en código fuente, memoria, prompts o commits.
- Los contratos de API, esquemas de datos y restricciones documentadas son SSOT y no deben modificarse silenciosamente.
- Cada cambio relevante debe reflejarse en la memoria del proyecto (docs/constraints, decisiones, requisitos) antes de darse por completado.
- El agente no debe inventar información, APIs, archivos o resultados que no haya verificado.
- Cada criterio de aceptación automático se prueba con un test cuyo nombre lleva el código del criterio (ej: T12-C3).
- Nada de código muerto: lo que se reemplaza dentro de la misma versión se elimina con sus referencias, tests y dependencias.
- El software debe quedar configurado y documentado para ejecutarse en todos los ambientes definidos (local, development, production).

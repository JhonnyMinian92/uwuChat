# File and Directory Hierarchy

Pending Gemini analysis of architecture, patterns, frameworks, languages and application type.

# File and Directory Hierarchy

- `/backend`: API FastAPI, adaptadores y lógica de negocio.
  - `domain/`: Entidades y casos de uso principales.
  - `ports/`: Interfaces de entrada y salida.
  - `adapters/`: Implementaciones concretas (webhooks, base de datos, canales).
- `/frontend`: Aplicación web React 18 con TypeScript.
  - `components/`: Componentes presentacionales y contenedores.
  - `services/`: Comunicación con la API REST y WebSockets.

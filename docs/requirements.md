# Technical Requirements

Languages, versions and frameworks selected from Central Memory are listed below. Gemini may propose additions.

# Reused Language from Central Memory


## languages/python.md

# Python

## Use when
Backend services, data/ML pipelines, automation and scripting.

## Key considerations
- Use type hints and a static checker (mypy/pyright) for anything beyond a script.
- `pyproject.toml` for packaging; a virtual environment per project.
- Prefer the standard library and a small dependency set for services.

## Common pitfalls
- Mutable default arguments (`def f(x=[])`) are shared across calls.
- Mixing sync and async code (blocking calls inside `async def`) stalls the event loop.



## languages/typescript.md

# TypeScript

## Use when
Any JavaScript project that benefits from static typing: frontend apps, Node.js services, shared contracts between frontend and backend.

## Key considerations
- Enable `strict` mode in `tsconfig.json` from day one.
- Share types between frontend and backend when both live in the same repository.
- Prefer `interface`/`type` over `any`; treat `any` as a last resort with a comment explaining why.

## Common pitfalls
- Widespread use of `any` defeats the purpose of adopting TypeScript.
- Type-only imports mixed with runtime imports can break tree-shaking if not marked with `import type`.

# Reused Version from Central Memory


## versions/python-3.12.md

# Python 3.12

Applies to: `languages/python.md`

Current stable line with performance improvements and better error messages.



## versions/react-18.md

# React 18

Applies to: `frameworks/react.md`, `frameworks/nextjs.md`

Current stable major with concurrent rendering features.

# Reused Framework from Central Memory


## frameworks/fastapi.md

# FastAPI

## Language
Python

## Use when
High-performance async backend APIs with automatic OpenAPI documentation and request validation.

## Key considerations
- Use Pydantic models for request/response validation — they double as documentation.
- Prefer `async def` endpoints for I/O-bound work; use sync `def` only for CPU-bound handlers.
- Dependency injection (`Depends`) keeps auth/db-session wiring testable.

## Common pitfalls
- Calling blocking libraries inside `async def` endpoints stalls the event loop.
- Skipping response models lets internal fields leak into API responses.



## frameworks/react.md

# React

## Language
JavaScript / TypeScript

## Use when
Web and PWA frontends needing componentized, interactive UIs.

## Key considerations
- Keep components small and composable; lift shared state up rather than duplicating it.
- Use a dedicated data-fetching layer (React Query, SWR) instead of ad-hoc `useEffect` fetches.
- Memoize expensive renders (`useMemo`/`memo`) only after measuring, not preemptively.

## Common pitfalls
- Missing/incorrect dependency arrays in `useEffect` cause stale closures or infinite loops.
- Mutating state directly instead of creating a new reference breaks re-renders.


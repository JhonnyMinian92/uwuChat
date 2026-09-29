# Architecture decisions

ADR files are the SSOT for architectural decisions.

# Reused Design_Pattern from Central Memory


## patterns/backend/adapter.md

# Adapter

## Intent
Translate an external interface into the contract expected by the application.

## Applicability
Use when an external API, library, legacy component or provider differs from the internal contract.

## Non-applicability
Avoid adapters that merely rename methods without isolating a real external boundary.

## Structure
Expose the internal port/contract and implement translation in an adapter dedicated to the external system.

## Implementation guidance
Map data explicitly, normalize provider-specific errors and keep provider assumptions at the boundary.

## Validation
Test request/response mapping, failure translation and compatibility with the internal contract.

## Security
Validate external data, apply least privilege and never trust provider payloads as already-safe internal data.

## Trade-offs
Isolates integration changes but adds translation code.

## Related
Skill: `backend.design_patterns`. Commonly paired with Hexagonal Architecture and Anti-Corruption Layer.



## patterns/backend/repository.md

# Repository

## Intent
Encapsulate persistence access behind a stable application/domain-facing contract.

## Applicability
Use when persistence must be isolated, multiple storage implementations exist, or tests benefit from substituting storage behavior.

## Non-applicability
Avoid creating a repository abstraction that only mirrors a single CRUD API with no meaningful boundary.

## Structure
Define a focused interface around domain operations and implement it in infrastructure. Keep query/storage details outside business logic.

## Implementation guidance
Return domain-oriented results, centralize persistence rules, and make transaction boundaries explicit. Do not expose database-specific models unnecessarily.

## Validation
Verify persistence concerns are isolated, behavior is testable without the database, and the interface expresses real use cases.

## Security
Enforce authorization before protected operations, parameterize queries, validate identifiers and avoid exposing raw persistence errors.

## Trade-offs
Improves testability and storage isolation, but can become unnecessary indirection.

## Related
Skill: `backend.design_patterns`. Commonly paired with Hexagonal Architecture and Explicit Transaction Boundary.



## patterns/backend/strategy.md

# Strategy

## Intent
Select one algorithm or business policy behind a stable contract without changing the caller.

## Applicability
Use when behavior varies by policy, algorithm, provider or configuration and new variants are expected.

## Non-applicability
Avoid when there is only one stable behavior and no credible variation.

## Structure
Define a common strategy contract, implement independent strategies, and use explicit deterministic selection rules.

## Implementation guidance
Keep strategies cohesive and side effects explicit. Selection should be driven by validated configuration or domain rules.

## Validation
Test each strategy independently and verify deterministic selection for every supported condition.

## Security
Validate selection inputs and configuration; never allow untrusted input to instantiate arbitrary classes or execute arbitrary behavior.

## Trade-offs
Easy extension and isolated algorithms, with additional types and selection logic.

## Related
Skill: `backend.design_patterns`.



## patterns/api/idempotency_key.md

# Idempotency Key

## Intent
Make retryable state-changing requests safe to repeat without duplicating the logical operation.

## Applicability
Use for operations vulnerable to duplicate submission, especially payments, provisioning, job creation, or network-timeout retries.

## Non-applicability
Do not add idempotency where repetition is already harmless or where the operation cannot define a stable identity.

## Structure / responsibilities
- Client supplies a unique key for a logical operation.
- Server validates key format and scope.
- Server associates the key with the operation result and relevant request fingerprint.
- Repeated valid requests return the prior outcome instead of executing the operation again.

## Implementation guidance
Define key scope, retention, concurrent-request behavior, and mismatch handling. Persist the key atomically with the protected operation when required for correctness.

## Validation criteria
- Duplicate requests do not create duplicate side effects.
- Concurrent reuse is deterministic.
- Reuse with materially different request data is rejected.
- Expired keys follow documented semantics.

## Security considerations
Prevent key guessing, cross-tenant reuse, unbounded storage growth, and leakage of sensitive response data. Bind keys to the authenticated principal and operation scope where appropriate.

## Trade-offs
Improves retry safety but requires durable key storage, lifecycle management, and concurrency handling.

## Related skills and patterns
- `backend.idempotency`
- `security.api_security`

## Example decision signals
Choose when clients may retry after uncertain network outcomes and duplicate side effects would be harmful.



## patterns/api/pagination.md

# Stable Pagination

## Intent
Bound collection responses while providing deterministic navigation through a changing dataset.

## Applicability
Use for endpoints that return potentially large collections or where response size must remain bounded.

## Non-applicability
Avoid pagination for inherently tiny, bounded collections where it adds needless client complexity.

## Structure / responsibilities
- API defines page size limits.
- Ordering is explicit and stable.
- Cursor or offset semantics are documented.
- Response includes enough metadata for the client to continue safely.

## Implementation guidance
Prefer a stable unique ordering key. Cap client-requested page sizes. For mutable large datasets, cursor/keyset pagination is often safer than offsets for consistency and performance.

## Validation criteria
- Repeated requests with the same cursor semantics are deterministic within documented consistency guarantees.
- Page size cannot bypass server limits.
- Items are not unexpectedly duplicated or skipped under supported consistency semantics.

## Security considerations
Authorize access before pagination. Do not expose internal identifiers solely because they are used as cursors. Treat cursors as untrusted input and validate them.

## Trade-offs
Pagination protects performance and payload size but requires more client logic and explicit consistency semantics.

## Related skills and patterns
- `api.pagination`
- `performance.api_optimization`

## Example decision signals
Choose when collection size is unbounded or could grow beyond a safe single response.



## patterns/error_handling/retry_with_backoff.md

# Retry with Bounded Backoff

## Intent
Retry transient operations without creating an uncontrolled retry storm or hiding permanent failures.

## Applicability
Use when an operation can fail temporarily because of network interruption, service unavailability, throttling, or another explicitly classified transient condition. The operation must be safe to retry or protected by idempotency.

## Non-applicability
Do not retry validation failures, authentication/authorization failures that will not change, malformed requests, deterministic business-rule failures, or non-idempotent operations without an explicit duplicate-prevention mechanism.

## Structure / responsibilities
- **Classifier:** distinguishes transient from permanent failures.
- **Retry policy:** defines maximum attempts, delay and optional jitter.
- **Operation:** performs the work and exposes a clear success/failure result.
- **Telemetry:** records attempts, final outcome and reason without exposing secrets.
- **Boundary:** enforces an overall timeout/deadline.

## Implementation guidance
1. Classify the failure before retrying.
2. Set a small explicit maximum attempt count.
3. Use bounded exponential backoff rather than immediate repeated calls.
4. Add jitter when many clients may retry concurrently.
5. Respect server-provided retry guidance such as `Retry-After` when applicable.
6. Stop when the overall deadline is reached.
7. Preserve the original failure context for diagnosis.
8. For state-changing operations, require idempotency or another duplicate-prevention mechanism.

## Validation criteria
- Permanent errors are not retried.
- Attempt count cannot exceed the configured limit.
- Delay is bounded and deterministic under a fixed test configuration.
- Overall timeout is enforced.
- Retry attempts are observable.
- Repeated state-changing requests do not create unintended duplicate effects.

## Security considerations
Retry policy must not become a denial-of-service amplifier. Never retry rejected credentials indefinitely. Avoid logging authorization headers, tokens, request bodies containing secrets, or sensitive response data. Respect upstream rate limits and retry-after instructions.

## Trade-offs
Bounded retries improve resilience but increase latency and can amplify load when applied incorrectly. Jitter reduces synchronized retries but makes exact timing less predictable.

## Related skills and patterns
- `backend.design_patterns`
- `api.idempotency-key`
- `security.defense-in-depth`
- `error.fail-fast-validation`

## Example decision signals
- **Transient dependency outage:** use bounded retries.
- **HTTP 429 with retry guidance:** retry within the allowed deadline.
- **HTTP 400 caused by invalid input:** fail immediately.
- **Payment-like state change:** combine retry with idempotency protection.



## patterns/frontend/container_presentational.md

# Container and Presentational

## Intent
Separate data/state orchestration from visual presentation when that separation improves reuse and clarity.

## Applicability
Use for screens where fetching, state coordination, or workflow logic is materially more complex than rendering.

## Non-applicability
Do not split small components merely to follow the pattern mechanically.

## Structure / responsibilities
- Container/orchestrator handles state, data loading, and actions.
- Presentational component receives explicit data and callbacks.
- Contracts remain small and predictable.

## Implementation guidance
Keep business rules outside purely visual components. Avoid containers becoming unbounded service objects; extract cohesive logic when it grows.

## Validation criteria
- Presentation can be tested independently.
- State transitions are explicit.
- No hidden dependency on global mutable state is required.

## Security considerations
Client-side separation does not establish trust boundaries. Enforce authorization, validation, and output encoding on trusted server boundaries.

## Trade-offs
The pattern can improve testability and reuse, but unnecessary separation can fragment simple UI code.

## Related skills and patterns
- `frontend.design_patterns`
- Component Composition

## Example decision signals
Choose when the same presentation can consume different data sources or when orchestration is significantly more complex than rendering.


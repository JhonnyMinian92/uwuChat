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



## patterns/authentication/implementation.md

# Authentication Pattern — Implementation

## Intent
Establish who is making a request through a verifiable identity proof, before authorization or business logic executes, without coupling every service to one specific credential technology.

## Applicability
Use for any system boundary that must know the identity of the caller: a public API, a user-facing application, or a service-to-service boundary that isn't fully trusted by network location alone.

## Non-applicability
Do not use this pattern to make authorization decisions — authentication only establishes identity; authorization (what the identity is allowed to do) is a separate concern (`security.zero-trust-boundary`). Do not build a custom cryptographic primitive when a vetted standard (OAuth 2.0, OpenID Connect, WebAuthn, TOTP) covers the need.

## Structure / responsibilities
- **Credential verifier**: validates the presented credential (password hash, signed token, TOTP code, WebAuthn assertion) against a trusted source.
- **Session/token issuer**: issues a short-lived, verifiable proof of the authenticated identity (session cookie, JWT, opaque token) after successful verification.
- **Transport boundary**: enforces that credentials and tokens never travel or persist unencrypted (TLS in transit, hashed/encrypted at rest).
- **Second factor (when required)**: an independent verification step (TOTP, WebAuthn, push approval) that does not rely on the same secret as the first factor.
- **Revocation/expiry mechanism**: a way to invalidate a session or token before its natural expiry (logout, credential compromise, policy change).

## Implementation guidance
1. Never store plaintext passwords; use a memory-hard hash (Argon2id, scrypt, or bcrypt with an adequate cost factor).
2. Encrypt sensitive secrets end-to-end when the transport alone is not trusted enough for the data's sensitivity (e.g. client-side encryption before a password reaches the server).
3. Bind sessions/tokens to an expiry and, where applicable, to a client context, without breaking legitimate mobility.
4. When mandatory 2FA is required, enforce it at the authentication boundary itself — never as an optional client-side step that can be bypassed by calling the API directly.
5. Rate-limit and lock out credential verification attempts to blunt brute-force and credential-stuffing attacks.
6. Log authentication successes and failures (without secrets) for detection and audit; never log passwords, tokens, or TOTP secrets.
7. Provide an explicit, tested logout/revocation path that invalidates the session server-side, not just client-side.

## Validation criteria
- No plaintext credential exists in logs, databases, or transport payloads at rest.
- A session/token cannot be replayed after logout or expiry.
- 2FA, when mandatory, cannot be bypassed by calling an underlying endpoint directly.
- Failed-attempt rate limiting is verifiably enforced (tested, not assumed).
- Authentication failures return a generic error that does not reveal whether the username or the credential was wrong (prevents enumeration).

## Security considerations
Authentication is the highest-value target for attackers; treat every implementation detail as security-relevant. Apply `security.web_security_baseline` in full. Never roll a custom crypto primitive. Assume credential databases will eventually leak and design so a leak of hashes does not equal a leak of plaintext credentials. Coordinate any change to this pattern with `cyber_security` before merge.

## Trade-offs
Stronger authentication (mandatory 2FA, short-lived tokens, strict rate limiting) increases security but adds friction and support burden (lockouts, recovery flows). Session-based auth simplifies revocation but complicates horizontal scaling without shared session storage; token-based auth scales more easily but makes immediate revocation harder without an additional check.

## Related skills and patterns
- `security.web_security_baseline`
- `security.zero-trust-boundary`
- `security.defense-in-depth`
- `error.fail-fast-validation`

## Example decision signals
- **User-facing web application with sensitive data**: session-based auth with mandatory 2FA and short expiry.
- **Public third-party API**: OAuth 2.0 / OpenID Connect with scoped, short-lived access tokens.
- **Service-to-service inside a private network**: mutual TLS or signed service tokens; never rely on network location alone (`security.zero-trust-boundary`).
- **Password reset flow**: treat as an authentication event; require re-verification and invalidate all existing sessions after a successful reset.

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



## patterns/authentication/implementation.md

# Authentication Pattern — Implementation

## Intent
Establish who is making a request through a verifiable identity proof, before authorization or business logic executes, without coupling every service to one specific credential technology.

## Applicability
Use for any system boundary that must know the identity of the caller: a public API, a user-facing application, or a service-to-service boundary that isn't fully trusted by network location alone.

## Non-applicability
Do not use this pattern to make authorization decisions — authentication only establishes identity; authorization (what the identity is allowed to do) is a separate concern (`security.zero-trust-boundary`). Do not build a custom cryptographic primitive when a vetted standard (OAuth 2.0, OpenID Connect, WebAuthn, TOTP) covers the need.

## Structure / responsibilities
- **Credential verifier**: validates the presented credential (password hash, signed token, TOTP code, WebAuthn assertion) against a trusted source.
- **Session/token issuer**: issues a short-lived, verifiable proof of the authenticated identity (session cookie, JWT, opaque token) after successful verification.
- **Transport boundary**: enforces that credentials and tokens never travel or persist unencrypted (TLS in transit, hashed/encrypted at rest).
- **Second factor (when required)**: an independent verification step (TOTP, WebAuthn, push approval) that does not rely on the same secret as the first factor.
- **Revocation/expiry mechanism**: a way to invalidate a session or token before its natural expiry (logout, credential compromise, policy change).

## Implementation guidance
1. Never store plaintext passwords; use a memory-hard hash (Argon2id, scrypt, or bcrypt with an adequate cost factor).
2. Encrypt sensitive secrets end-to-end when the transport alone is not trusted enough for the data's sensitivity (e.g. client-side encryption before a password reaches the server).
3. Bind sessions/tokens to an expiry and, where applicable, to a client context, without breaking legitimate mobility.
4. When mandatory 2FA is required, enforce it at the authentication boundary itself — never as an optional client-side step that can be bypassed by calling the API directly.
5. Rate-limit and lock out credential verification attempts to blunt brute-force and credential-stuffing attacks.
6. Log authentication successes and failures (without secrets) for detection and audit; never log passwords, tokens, or TOTP secrets.
7. Provide an explicit, tested logout/revocation path that invalidates the session server-side, not just client-side.

## Validation criteria
- No plaintext credential exists in logs, databases, or transport payloads at rest.
- A session/token cannot be replayed after logout or expiry.
- 2FA, when mandatory, cannot be bypassed by calling an underlying endpoint directly.
- Failed-attempt rate limiting is verifiably enforced (tested, not assumed).
- Authentication failures return a generic error that does not reveal whether the username or the credential was wrong (prevents enumeration).

## Security considerations
Authentication is the highest-value target for attackers; treat every implementation detail as security-relevant. Apply `security.web_security_baseline` in full. Never roll a custom crypto primitive. Assume credential databases will eventually leak and design so a leak of hashes does not equal a leak of plaintext credentials. Coordinate any change to this pattern with `cyber_security` before merge.

## Trade-offs
Stronger authentication (mandatory 2FA, short-lived tokens, strict rate limiting) increases security but adds friction and support burden (lockouts, recovery flows). Session-based auth simplifies revocation but complicates horizontal scaling without shared session storage; token-based auth scales more easily but makes immediate revocation harder without an additional check.

## Related skills and patterns
- `security.web_security_baseline`
- `security.zero-trust-boundary`
- `security.defense-in-depth`
- `error.fail-fast-validation`

## Example decision signals
- **User-facing web application with sensitive data**: session-based auth with mandatory 2FA and short expiry.
- **Public third-party API**: OAuth 2.0 / OpenID Connect with scoped, short-lived access tokens.
- **Service-to-service inside a private network**: mutual TLS or signed service tokens; never rely on network location alone (`security.zero-trust-boundary`).
- **Password reset flow**: treat as an authentication event; require re-verification and invalidate all existing sessions after a successful reset.



## patterns/integration/anti_corruption_layer.md

# Anti-Corruption Layer

## Intent
Keep an external or legacy domain model from leaking into the internal domain model by translating concepts at the integration boundary.

## Applicability
Use when integrating legacy systems, third-party APIs, bounded contexts with incompatible models, or protocols whose terminology and invariants differ from the internal model.

## Non-applicability
Do not introduce a translation layer when the external contract is already the stable internal contract and no semantic mismatch exists.

## Structure / responsibilities
- **Internal domain:** owns its terminology, invariants, and contracts.
- **Translator / adapter:** maps external requests and responses into internal representations.
- **External client:** handles protocol-specific communication.
- **Boundary contract:** defines what data and errors may cross the integration boundary.

## Implementation guidance
1. Identify semantic differences, not just field-name differences.
2. Define an internal model that does not inherit accidental external constraints.
3. Translate commands, queries, values, errors, and identifiers explicitly.
4. Keep external protocol details out of domain logic.
5. Validate external data before it enters trusted internal state.
6. Test mappings, edge cases, unknown values, and compatibility behavior.
7. Document intentional lossy mappings and version assumptions.

## Validation criteria
- Internal domain objects do not require external DTOs or protocol-specific types.
- Mapping behavior is deterministic and tested.
- External failures are translated into safe internal error semantics.
- Changes in the external contract have a bounded impact on the internal domain.

## Security considerations
Treat external data as untrusted. Validate types, ranges, encodings, identifiers, and authorization context before creating internal state. Do not forward external secrets or opaque tokens unnecessarily.

## Trade-offs
The layer protects the internal model but adds mapping code, maintenance, and possible duplication of data structures.

## Related skills and patterns
- Skill: `backend.design_patterns`
- Pattern: `backend.adapter`

## Example decision signals
Prefer this pattern when an integration's vocabulary, lifecycle, or invariants conflict with those of the internal domain.


## patterns/integration/outbox.md

# Transactional Outbox

## Intent
Make a database change and the intent to publish an event durable in the same transaction, avoiding an unsafe dual write.

## Applicability
Use when a successful state change must reliably produce an asynchronous integration event and the database is the authoritative transactional store.

## Non-applicability
Do not use when event publication is intentionally best-effort or when the integration can be rebuilt safely from another durable source without transactional coupling.

## Structure / responsibilities
- **Business transaction:** changes domain state and inserts an outbox record atomically.
- **Outbox table/store:** holds pending event payload, type, aggregate identity, ordering data, and publication state.
- **Dispatcher:** claims pending records and publishes them to the broker or external system.
- **Consumer:** handles delivery duplicates safely and applies its own idempotency rules.

## Implementation guidance
1. Define the event contract and ownership before implementation.
2. Insert the outbox record in the same transaction as the business state change.
3. Keep payloads sufficient for the consumer while avoiding unnecessary sensitive data.
4. Dispatch asynchronously with bounded retries and observable failure states.
5. Claim work safely when multiple dispatchers run concurrently.
6. Expect at-least-once delivery unless the infrastructure proves stronger semantics.
7. Make consumers idempotent and define retention/cleanup rules.

## Validation criteria
- A committed business change always has its required outbox record.
- A rolled-back business change does not publish its event.
- Dispatcher retries do not silently lose events.
- Duplicate delivery is safe for supported consumers.
- Stale, failed, and successfully published records are observable.

## Security considerations
Protect the outbox like business data. Minimize sensitive payloads, encrypt data where required, restrict dispatcher access, and prevent event injection through unvalidated fields.

## Trade-offs
The pattern improves delivery reliability but introduces a dispatcher, durable event state, cleanup, retries, and eventual consistency.

## Related skills and patterns
- Pattern: `database.transaction-boundary`
- Pattern: `api.idempotency-key`
- Pattern: `error.retry-with-backoff`

## Example decision signals
Prefer this pattern when losing an integration event after a successful database commit would create a business inconsistency.

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



## patterns/authentication/implementation.md

# Authentication Pattern — Implementation

## Intent
Establish who is making a request through a verifiable identity proof, before authorization or business logic executes, without coupling every service to one specific credential technology.

## Applicability
Use for any system boundary that must know the identity of the caller: a public API, a user-facing application, or a service-to-service boundary that isn't fully trusted by network location alone.

## Non-applicability
Do not use this pattern to make authorization decisions — authentication only establishes identity; authorization (what the identity is allowed to do) is a separate concern (`security.zero-trust-boundary`). Do not build a custom cryptographic primitive when a vetted standard (OAuth 2.0, OpenID Connect, WebAuthn, TOTP) covers the need.

## Structure / responsibilities
- **Credential verifier**: validates the presented credential (password hash, signed token, TOTP code, WebAuthn assertion) against a trusted source.
- **Session/token issuer**: issues a short-lived, verifiable proof of the authenticated identity (session cookie, JWT, opaque token) after successful verification.
- **Transport boundary**: enforces that credentials and tokens never travel or persist unencrypted (TLS in transit, hashed/encrypted at rest).
- **Second factor (when required)**: an independent verification step (TOTP, WebAuthn, push approval) that does not rely on the same secret as the first factor.
- **Revocation/expiry mechanism**: a way to invalidate a session or token before its natural expiry (logout, credential compromise, policy change).

## Implementation guidance
1. Never store plaintext passwords; use a memory-hard hash (Argon2id, scrypt, or bcrypt with an adequate cost factor).
2. Encrypt sensitive secrets end-to-end when the transport alone is not trusted enough for the data's sensitivity (e.g. client-side encryption before a password reaches the server).
3. Bind sessions/tokens to an expiry and, where applicable, to a client context, without breaking legitimate mobility.
4. When mandatory 2FA is required, enforce it at the authentication boundary itself — never as an optional client-side step that can be bypassed by calling the API directly.
5. Rate-limit and lock out credential verification attempts to blunt brute-force and credential-stuffing attacks.
6. Log authentication successes and failures (without secrets) for detection and audit; never log passwords, tokens, or TOTP secrets.
7. Provide an explicit, tested logout/revocation path that invalidates the session server-side, not just client-side.

## Validation criteria
- No plaintext credential exists in logs, databases, or transport payloads at rest.
- A session/token cannot be replayed after logout or expiry.
- 2FA, when mandatory, cannot be bypassed by calling an underlying endpoint directly.
- Failed-attempt rate limiting is verifiably enforced (tested, not assumed).
- Authentication failures return a generic error that does not reveal whether the username or the credential was wrong (prevents enumeration).

## Security considerations
Authentication is the highest-value target for attackers; treat every implementation detail as security-relevant. Apply `security.web_security_baseline` in full. Never roll a custom crypto primitive. Assume credential databases will eventually leak and design so a leak of hashes does not equal a leak of plaintext credentials. Coordinate any change to this pattern with `cyber_security` before merge.

## Trade-offs
Stronger authentication (mandatory 2FA, short-lived tokens, strict rate limiting) increases security but adds friction and support burden (lockouts, recovery flows). Session-based auth simplifies revocation but complicates horizontal scaling without shared session storage; token-based auth scales more easily but makes immediate revocation harder without an additional check.

## Related skills and patterns
- `security.web_security_baseline`
- `security.zero-trust-boundary`
- `security.defense-in-depth`
- `error.fail-fast-validation`

## Example decision signals
- **User-facing web application with sensitive data**: session-based auth with mandatory 2FA and short expiry.
- **Public third-party API**: OAuth 2.0 / OpenID Connect with scoped, short-lived access tokens.
- **Service-to-service inside a private network**: mutual TLS or signed service tokens; never rely on network location alone (`security.zero-trust-boundary`).
- **Password reset flow**: treat as an authentication event; require re-verification and invalidate all existing sessions after a successful reset.



## patterns/integration/anti_corruption_layer.md

# Anti-Corruption Layer

## Intent
Keep an external or legacy domain model from leaking into the internal domain model by translating concepts at the integration boundary.

## Applicability
Use when integrating legacy systems, third-party APIs, bounded contexts with incompatible models, or protocols whose terminology and invariants differ from the internal model.

## Non-applicability
Do not introduce a translation layer when the external contract is already the stable internal contract and no semantic mismatch exists.

## Structure / responsibilities
- **Internal domain:** owns its terminology, invariants, and contracts.
- **Translator / adapter:** maps external requests and responses into internal representations.
- **External client:** handles protocol-specific communication.
- **Boundary contract:** defines what data and errors may cross the integration boundary.

## Implementation guidance
1. Identify semantic differences, not just field-name differences.
2. Define an internal model that does not inherit accidental external constraints.
3. Translate commands, queries, values, errors, and identifiers explicitly.
4. Keep external protocol details out of domain logic.
5. Validate external data before it enters trusted internal state.
6. Test mappings, edge cases, unknown values, and compatibility behavior.
7. Document intentional lossy mappings and version assumptions.

## Validation criteria
- Internal domain objects do not require external DTOs or protocol-specific types.
- Mapping behavior is deterministic and tested.
- External failures are translated into safe internal error semantics.
- Changes in the external contract have a bounded impact on the internal domain.

## Security considerations
Treat external data as untrusted. Validate types, ranges, encodings, identifiers, and authorization context before creating internal state. Do not forward external secrets or opaque tokens unnecessarily.

## Trade-offs
The layer protects the internal model but adds mapping code, maintenance, and possible duplication of data structures.

## Related skills and patterns
- Skill: `backend.design_patterns`
- Pattern: `backend.adapter`

## Example decision signals
Prefer this pattern when an integration's vocabulary, lifecycle, or invariants conflict with those of the internal domain.


## patterns/integration/outbox.md

# Transactional Outbox

## Intent
Make a database change and the intent to publish an event durable in the same transaction, avoiding an unsafe dual write.

## Applicability
Use when a successful state change must reliably produce an asynchronous integration event and the database is the authoritative transactional store.

## Non-applicability
Do not use when event publication is intentionally best-effort or when the integration can be rebuilt safely from another durable source without transactional coupling.

## Structure / responsibilities
- **Business transaction:** changes domain state and inserts an outbox record atomically.
- **Outbox table/store:** holds pending event payload, type, aggregate identity, ordering data, and publication state.
- **Dispatcher:** claims pending records and publishes them to the broker or external system.
- **Consumer:** handles delivery duplicates safely and applies its own idempotency rules.

## Implementation guidance
1. Define the event contract and ownership before implementation.
2. Insert the outbox record in the same transaction as the business state change.
3. Keep payloads sufficient for the consumer while avoiding unnecessary sensitive data.
4. Dispatch asynchronously with bounded retries and observable failure states.
5. Claim work safely when multiple dispatchers run concurrently.
6. Expect at-least-once delivery unless the infrastructure proves stronger semantics.
7. Make consumers idempotent and define retention/cleanup rules.

## Validation criteria
- A committed business change always has its required outbox record.
- A rolled-back business change does not publish its event.
- Dispatcher retries do not silently lose events.
- Duplicate delivery is safe for supported consumers.
- Stale, failed, and successfully published records are observable.

## Security considerations
Protect the outbox like business data. Minimize sensitive payloads, encrypt data where required, restrict dispatcher access, and prevent event injection through unvalidated fields.

## Trade-offs
The pattern improves delivery reliability but introduces a dispatcher, durable event state, cleanup, retries, and eventual consistency.

## Related skills and patterns
- Pattern: `database.transaction-boundary`
- Pattern: `api.idempotency-key`
- Pattern: `error.retry-with-backoff`

## Example decision signals
Prefer this pattern when losing an integration event after a successful database commit would create a business inconsistency.


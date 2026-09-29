# Database

# Reused Database from Central Memory


## databases/transaction_boundary.md

# Explicit Transaction Boundary

## Intent
Define the smallest coherent unit of database work that must succeed or fail together, making consistency guarantees explicit.

## Applicability
Use when multiple writes represent one business operation, invariants span records, or partial persistence would leave invalid state.

## Non-applicability
Do not use a large transaction merely to simplify orchestration. Avoid holding transactions across slow network calls, user interaction, or unrelated work.

## Structure / responsibilities
- **Application/service boundary:** starts and ends the transaction around one business operation.
- **Domain/application logic:** defines the invariants that must hold when the transaction commits.
- **Repositories/data access:** participate in the caller's transaction instead of silently creating independent transactions.
- **Database:** provides atomic commit/rollback and isolation appropriate to the invariant.

## Implementation guidance
1. Identify the invariant and all writes required to preserve it.
2. Start the transaction at the application boundary that owns the use case.
3. Validate inputs and authorization before expensive transactional work where safe.
4. Perform the minimum required reads and writes.
5. Commit only after all invariants are satisfied.
6. Roll back on expected failure and propagate a structured error.
7. Keep external calls outside the transaction; use an outbox or equivalent when atomic publication is required.

## Validation criteria
- Partial execution cannot leave the protected invariant broken.
- Rollback behavior is tested for every relevant failure path.
- Isolation level is documented when it affects correctness.
- Transaction duration is bounded and observable.

## Security considerations
Enforce authorization before mutation, avoid exposing transaction errors with sensitive database details, and use parameterized queries. Do not rely on transaction atomicity as a substitute for access control or validation.

## Trade-offs
Transactions provide strong consistency but can reduce throughput and increase lock contention when they are too broad or long-lived.

## Related skills and patterns
- Skill: `database.transactions`
- Pattern: `database.optimistic-concurrency`
- Pattern: `integration.outbox`

## Example decision signals
Prefer this pattern when a single business action changes several records and observers must never see an invalid intermediate state.


## databases/optimistic_concurrency.md

# Optimistic Concurrency

## Intent
Detect conflicting updates with a version or revision check instead of holding long-lived locks.

## Applicability
Use when records can be edited concurrently, transactions should remain short, and conflicts are uncommon enough to resolve explicitly.

## Non-applicability
Avoid it when conflicts are frequent and expensive to resolve, or when correctness requires serialization that the data store can enforce more directly.

## Structure / responsibilities
- **Record:** stores a monotonic version/revision (or equivalent concurrency token).
- **Writer:** reads the token and includes it in the conditional update.
- **Database:** updates only when the expected version still matches.
- **Application:** translates a conflict into a retry, merge, or explicit user-facing resolution.

## Implementation guidance
1. Read the record and its current version.
2. Apply the intended change in memory.
3. Update with a condition such as `version = expected_version`.
4. Increment the version atomically on success.
5. Treat zero affected rows as a concurrency conflict, not as success.
6. Retry only when the operation is safe and the retry policy is bounded.
7. Record conflict metrics when contention matters operationally.

## Validation criteria
- Concurrent writers cannot silently overwrite one another.
- Version increments are atomic and monotonic.
- Conflict handling is covered by tests using concurrent or simulated writers.
- Retries cannot duplicate side effects.

## Security considerations
Do not expose internal revision values as authorization evidence. Authorization must be checked independently, and conflict responses must not reveal sensitive record state to an unauthorized caller.

## Trade-offs
This approach avoids long locks and often improves throughput, but conflicts require explicit resolution and can complicate write flows.

## Related skills and patterns
- Skill: `database.concurrency`
- Pattern: `database.transaction-boundary`
- Pattern: `error.retry-with-backoff`

## Example decision signals
Prefer this pattern when edits are short-lived and conflicts are possible but relatively infrequent.


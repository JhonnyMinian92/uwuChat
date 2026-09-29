# Architecture overview

Describe the system boundaries, components, dependencies and integration points.

# Reused Architecture from Central Memory


## architectures/hexagonal.md

# Hexagonal Architecture

## Intent
Protect domain and application logic from infrastructure and external interfaces through ports and adapters.

## Applicability
Use when a system has multiple integrations, requires strong testability, or must preserve domain independence.

## Non-applicability
Avoid for disposable prototypes or trivial components where interfaces would add more complexity than value.

## Structure
Define ports for required/provided capabilities and adapters for HTTP, persistence, messaging and other external mechanisms.

## Implementation guidance
Keep domain code unaware of concrete adapters. Select adapters through composition/configuration rather than embedding infrastructure decisions in business logic.

## Validation
Verify dependency direction, replaceability of adapters, isolated domain tests and explicit integration boundaries.

## Security
Treat adapters as trust boundaries; validate input, enforce authorization and avoid leaking infrastructure errors into public contracts.

## Trade-offs
Strong boundaries and testability at the cost of more interfaces and indirection.

## Related
Skill: `architecture.system_design`. Often complements Repository and Adapter patterns.



## architectures/adr.md

# Architecture Decision Record

## Intent
Preserve the context, decision and consequences behind an important architectural choice.

## Applicability
Use when alternatives exist, the decision has durable consequences, or future agents need the rationale.

## Non-applicability
Do not create an ADR for routine implementation details with no meaningful architectural consequence.

## Structure
Record context, constraints, alternatives considered, decision, consequences, risks and status.

## Implementation guidance
Reference affected contracts, components and constraints. Keep the ADR immutable in intent; supersede it with a new decision when the architecture changes.

## Validation
A reviewer should be able to understand why the decision was made without reconstructing the original discussion.

## Security
Record relevant security implications and rejected alternatives when security is a material decision factor.

## Trade-offs
Preserves rationale and reduces repeated debate, but requires maintenance and disciplined updates.

## Related
Skill: `architecture.system_design`. Project SSOT for architectural decisions is `architecture/decisions/`.

# Reused Architecture from Central Memory


## architectures/hexagonal.md

# Hexagonal Architecture

## Intent
Protect domain and application logic from infrastructure and external interfaces through ports and adapters.

## Applicability
Use when a system has multiple integrations, requires strong testability, or must preserve domain independence.

## Non-applicability
Avoid for disposable prototypes or trivial components where interfaces would add more complexity than value.

## Structure
Define ports for required/provided capabilities and adapters for HTTP, persistence, messaging and other external mechanisms.

## Implementation guidance
Keep domain code unaware of concrete adapters. Select adapters through composition/configuration rather than embedding infrastructure decisions in business logic.

## Validation
Verify dependency direction, replaceability of adapters, isolated domain tests and explicit integration boundaries.

## Security
Treat adapters as trust boundaries; validate input, enforce authorization and avoid leaking infrastructure errors into public contracts.

## Trade-offs
Strong boundaries and testability at the cost of more interfaces and indirection.

## Related
Skill: `architecture.system_design`. Often complements Repository and Adapter patterns.



## architectures/adr.md

# Architecture Decision Record

## Intent
Preserve the context, decision and consequences behind an important architectural choice.

## Applicability
Use when alternatives exist, the decision has durable consequences, or future agents need the rationale.

## Non-applicability
Do not create an ADR for routine implementation details with no meaningful architectural consequence.

## Structure
Record context, constraints, alternatives considered, decision, consequences, risks and status.

## Implementation guidance
Reference affected contracts, components and constraints. Keep the ADR immutable in intent; supersede it with a new decision when the architecture changes.

## Validation
A reviewer should be able to understand why the decision was made without reconstructing the original discussion.

## Security
Record relevant security implications and rejected alternatives when security is a material decision factor.

## Trade-offs
Preserves rationale and reduces repeated debate, but requires maintenance and disciplined updates.

## Related
Skill: `architecture.system_design`. Project SSOT for architectural decisions is `architecture/decisions/`.

# Reused Architecture from Central Memory


## architectures/hexagonal.md

# Hexagonal Architecture

## Intent
Protect domain and application logic from infrastructure and external interfaces through ports and adapters.

## Applicability
Use when a system has multiple integrations, requires strong testability, or must preserve domain independence.

## Non-applicability
Avoid for disposable prototypes or trivial components where interfaces would add more complexity than value.

## Structure
Define ports for required/provided capabilities and adapters for HTTP, persistence, messaging and other external mechanisms.

## Implementation guidance
Keep domain code unaware of concrete adapters. Select adapters through composition/configuration rather than embedding infrastructure decisions in business logic.

## Validation
Verify dependency direction, replaceability of adapters, isolated domain tests and explicit integration boundaries.

## Security
Treat adapters as trust boundaries; validate input, enforce authorization and avoid leaking infrastructure errors into public contracts.

## Trade-offs
Strong boundaries and testability at the cost of more interfaces and indirection.

## Related
Skill: `architecture.system_design`. Often complements Repository and Adapter patterns.



## architectures/adr.md

# Architecture Decision Record

## Intent
Preserve the context, decision and consequences behind an important architectural choice.

## Applicability
Use when alternatives exist, the decision has durable consequences, or future agents need the rationale.

## Non-applicability
Do not create an ADR for routine implementation details with no meaningful architectural consequence.

## Structure
Record context, constraints, alternatives considered, decision, consequences, risks and status.

## Implementation guidance
Reference affected contracts, components and constraints. Keep the ADR immutable in intent; supersede it with a new decision when the architecture changes.

## Validation
A reviewer should be able to understand why the decision was made without reconstructing the original discussion.

## Security
Record relevant security implications and rejected alternatives when security is a material decision factor.

## Trade-offs
Preserves rationale and reduces repeated debate, but requires maintenance and disciplined updates.

## Related
Skill: `architecture.system_design`. Project SSOT for architectural decisions is `architecture/decisions/`.

# Reused Architecture from Central Memory


## architectures/hexagonal.md

# Hexagonal Architecture

## Intent
Protect domain and application logic from infrastructure and external interfaces through ports and adapters.

## Applicability
Use when a system has multiple integrations, requires strong testability, or must preserve domain independence.

## Non-applicability
Avoid for disposable prototypes or trivial components where interfaces would add more complexity than value.

## Structure
Define ports for required/provided capabilities and adapters for HTTP, persistence, messaging and other external mechanisms.

## Implementation guidance
Keep domain code unaware of concrete adapters. Select adapters through composition/configuration rather than embedding infrastructure decisions in business logic.

## Validation
Verify dependency direction, replaceability of adapters, isolated domain tests and explicit integration boundaries.

## Security
Treat adapters as trust boundaries; validate input, enforce authorization and avoid leaking infrastructure errors into public contracts.

## Trade-offs
Strong boundaries and testability at the cost of more interfaces and indirection.

## Related
Skill: `architecture.system_design`. Often complements Repository and Adapter patterns.



## architectures/adr.md

# Architecture Decision Record

## Intent
Preserve the context, decision and consequences behind an important architectural choice.

## Applicability
Use when alternatives exist, the decision has durable consequences, or future agents need the rationale.

## Non-applicability
Do not create an ADR for routine implementation details with no meaningful architectural consequence.

## Structure
Record context, constraints, alternatives considered, decision, consequences, risks and status.

## Implementation guidance
Reference affected contracts, components and constraints. Keep the ADR immutable in intent; supersede it with a new decision when the architecture changes.

## Validation
A reviewer should be able to understand why the decision was made without reconstructing the original discussion.

## Security
Record relevant security implications and rejected alternatives when security is a material decision factor.

## Trade-offs
Preserves rationale and reduces repeated debate, but requires maintenance and disciplined updates.

## Related
Skill: `architecture.system_design`. Project SSOT for architectural decisions is `architecture/decisions/`.


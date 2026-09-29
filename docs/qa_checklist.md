# QA Checklist

# Reused Qa from Central Memory


## qa/functional_testing_checklist.md

# Functional testing checklist

- Golden path covered end to end.
- Known edge cases covered (empty, boundary, invalid input).
- Error states show a usable message and do not crash the flow.



## qa/security_review_checklist.md

# Security review checklist

- Input validation and output encoding at trust boundaries.
- AuthN/AuthZ enforced server-side, not only in the UI.
- No secrets in logs, commits or client-visible responses.


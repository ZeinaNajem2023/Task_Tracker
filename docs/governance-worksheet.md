# Module 5 Governance Retrospective

## What I Shared With AI

| Item | Module | Risk level | Reason |
|---|---|---|---|
| Unauthenticated and unscoped task routes | Module 4 | Low | Authorized course toy-project code with no secrets, PII, production data, or proprietary logic. |
| Unbounded task inputs and collection growth | Module 4 | Low | General validation and capacity details from course code with no sensitive data. |
| Arbitrary task IDs echoed in error responses | Module 4 | Low | Ordinary course-project behavior shared without real task IDs or user records. |
| Local CORS configuration with broad permissions | Module 4 | Low | Localhost configuration contained no credentials, production domains, or external infrastructure details. |
| Hard-coded plaintext localhost API URL | Module 4 | Low | A localhost development URL is non-sensitive and does not identify a real deployed service. |
| Missing dependency integrity and vulnerability checks | Module 4 | Low | General dependency-management details involving public packages, with no tokens or private registries. |
| Mutable Docker and GitHub Actions references | Module 4 | Low | Public image and CI version references contained no secrets or private build configuration. |

## What I Received From AI

| Generated thing | Module | Do I understand it line by line? | Action I will take |
|---|---|---|---|
| Security review with seven findings and remediation suggestions | Module 5 | Yes | Verify each finding against the code, rewrite it in my own words, and document safer sharing practices. |

## Assumption

These Low ratings assume the repository is my authorized course project and that no real user data, credentials, private infrastructure, or production configuration was shared.

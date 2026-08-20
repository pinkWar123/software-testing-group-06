# API 1 Test Conditions and Design

## Test conditions

| Condition ID | Requirement / risk | Design technique | Covered by |
|---|---|---|---|
| C01 | Known user + correct password authenticates | EP, use case | LOGIN-001 |
| C02 | Admin + correct password authenticates with admin role | EP, schema | LOGIN-002 |
| C03 | Unknown account is rejected without enumeration | EP, security | LOGIN-004 |
| C04 | Wrong password is rejected | EP | LOGIN-003/005 |
| C05 | Required fields missing, null, empty, or whitespace | EP, BVA | LOGIN-006–012 |
| C06 | Email syntax and length partitions | EP, BVA | LOGIN-013–018 |
| C07 | Password partitions and hostile values | EP, BVA, error guessing | LOGIN-019–024 |
| C08 | Failed-attempt counter changes by exactly one | State transition | LOGIN-025/026 |
| C09 | Third consecutive failure locks account | BVA, state transition | LOGIN-027 |
| C10 | Locked account remains blocked and error is generic | State transition, security | LOGIN-028/029 |
| C11 | Successful login resets failure state | State transition | LOGIN-030 |
| C12 | JWT and response schema are correct and non-sensitive | Schema, security | LOGIN-031/039 |
| C13 | HTTP/auth/header protocol behavior is robust | EP, error guessing | LOGIN-032–040 |

## Decision table — authentication result

| Rule | Account exists | Password matches | Account locked | Expected |
|---|---|---|---|---|
| D1 | Yes | Yes | No | 200; JWT and user object |
| D2 | Yes | No | No | 401; generic invalid-credentials error; increment attempts by 1 |
| D3 | No | N/A | N/A | 401; generic invalid-credentials error; no account state change |
| D4 | Yes | N/A | Yes | 403; generic lockout error; no new password check |
| D5 | Yes | Yes | Yes | 403 until lock expires |

## State model

```text
UNLOCKED --wrong password--> FAILED(n)
FAILED(1) --wrong password--> FAILED(2)
FAILED(2) --wrong password--> LOCKED
LOCKED --before expiry--> LOCKED
LOCKED --expiry reached--> UNLOCKED
UNLOCKED/FAILED(n) --correct password--> AUTHENTICATED and failure state reset
```

## Coverage notes

- SEC-01–SEC-07 are represented by the assignment’s security examples: injection, IDOR/account enumeration, role/token handling, brute-force lockout, and schema/information-disclosure checks. The exact SEC wording should be copied from the course specification if it is supplied separately.
- Cases with stateful prerequisites must use a disposable account or database reseed so execution order does not create hidden dependencies.


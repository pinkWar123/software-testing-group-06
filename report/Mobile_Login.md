# Mobile — Login — Domain Testing & BVA

| Field | Value |
| --- | --- |
| Feature | Mobile Login (Đăng nhập trên app) |
| Pool / Platform | D / Mobile (Expo) |
| Spec source | EShop SRS §7 FR-20 + FR-02 login rules |
| Tester | 23127362 |

## Spec summary
- User enters Email + Password.
- Wrong login increments a counter by exactly 1.
- 3+ consecutive failures -> account locked 30s (demo). Generic error, no detail leak.
- Success returns JWT; sent as `Authorization: Bearer <token>`.
- Email field should validate format.

> Reminder: mobile talks to backend via `API_URL` in `App.js` line 16 — set to your LAN IP.

---

## Step 1 — Input inventory
| # | Input | Type | Valid domain | Notes |
| --- | --- | --- | --- | --- |
| I1 | Email | string | valid email format, registered | e.g. test@eshop.com |
| I2 | Password | string | matches account | |
| I3 | Failure counter | integer | 0..2 before lock | lock at 3 |

## Step 2 — Domain Testing (Equivalence Partitioning)
| EC-ID | Input | Valid/Invalid | Class | Representative |
| --- | --- | --- | --- | --- |
| EC1 | Email+Pwd | Valid | correct pair | test@eshop.com / Test1234! |
| EC2 | Email | Invalid | bad format | "test@" / "test" |
| EC3 | Email | Invalid | empty | "" |
| EC4 | Password | Invalid | wrong password | test@eshop.com / wrong |
| EC5 | Password | Invalid | empty | "" |
| EC6 | Email | Invalid | not registered | nobody@x.com |

## Step 3 — Boundary Value Analysis (on the lockout counter)
| BV-ID | Boundary | Value | Side | Expected |
| --- | --- | --- | --- | --- |
| BV1 | lock threshold = 3 | after 2 failures | below | still allowed to try |
| BV2 | lock threshold | 3rd failure | on | account locked 30s |
| BV3 | lock threshold | 4th attempt (during lock) | above | blocked |
| BV4 | after 30s | retry post-lock | boundary | allowed again |

## Step 4 — Test cases
| TC-ID | Technique | Title | Precondition | Test data / steps | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC01 | EP | Valid login | app open, backend up | enter valid pair, submit | logged in |  |  |

## Step 5 — AI gap analysis
- Missed:
- Why:

## Step 6 — Bugs found
| BUG-ID | Title | Severity | Steps | Expected | Actual | Issue link |
| --- | --- | --- | --- | --- | --- | --- |

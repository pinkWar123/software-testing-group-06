# Mobile — Login

- **Student ID:** 23127362
- **Feature:** Pool D (Mobile) — Login screen
- **Platform:** Mobile app (React Native / Expo)
- **Technique:** Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
- **Domain source:** Specification in repo `ttbhanh/eshop-sut` (FR-02 login rules), derived from the specification, not from source code.

**Source tags:** `[SPEC]` = constraint stated in the specification · `[ASSUMED]` = inferred, not stated in the spec · `[OBS]` = to be settled by observing the running app · `[UI]` = boundary imposed by the UI.

## Specification excerpt (FR-02, applied to the mobile login screen)

> The user enters Email and Password. After each failed login the counter increases by exactly 1. After **3 or more** consecutive failed logins the account is temporarily **locked for 30 seconds** (demo); the system returns a suitable error and **does not leak the cause**. A successful login returns a JWT token, stored client-side and sent on authenticated requests as `Authorization: Bearer <token>`. On web the email field uses `type="email"` (HTML5 format validation) — on mobile, format validation is to be confirmed (`[OBS]`).

Test accounts: `test@eshop.com` / `Test1234!` (user), `admin@eshop.com` / `Admin123!` (admin).

---

# Part A — Domain Testing (Equivalence Partitioning)

## Step 1 — Input / Output inventory

### Inputs

| # | Input | Type | Valid constraint | Source |
| --- | --- | --- | --- | --- |
| I1 | Email | Text | Valid format and a registered account | `[SPEC]` |
| I2 | Password | Secure text | Matches the account's password | `[SPEC]` |
| I3 | Consecutive-failure counter | State | Increments by exactly 1 per failure; lock at 3 | `[SPEC]` |
| I4 | "Login" button | Action | One tap submits the credentials | `[SPEC]` |

### Outputs

| # | Output | Expected | Source |
| --- | --- | --- | --- |
| O1 | Successful login | JWT stored; app navigates past the login screen | `[SPEC]` |
| O2 | Error on wrong credentials | Generic message, does not reveal whether email or password was wrong | `[SPEC]` |
| O3 | Lockout state | After 3 consecutive failures, account locked ~30s with a suitable message | `[SPEC]` |
| O4 | Email format validation | Rejects malformed email | `[SPEC]` (web) / `[OBS]` (mobile) |

### Preconditions

- Backend running and reachable from the phone (see the testing guide); the mobile app's `API_URL` points to the PC's LAN IP.
- A known registered account exists (`test@eshop.com`).

## Step 2 — Equivalence Classes

Email is a "must be" (valid format) + membership (registered) input; password is a match input; the login outcome and lockout form a small state machine driven by the failure counter. Classes are split by distinct reason.

### Input I1 — Email

| EC | Type | Domain | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-E1 | valid | Valid format, registered (`test@eshop.com`) | Passes to credential check | `[SPEC]` |
| EC-E2 | invalid | Malformed (`test@`, `test`, no `@`) | Rejected / format error | `[SPEC]` (web) / `[OBS]` (mobile) |
| EC-E3 | invalid | Empty | Rejected | `[SPEC]` |
| EC-E4 | invalid | Valid format but not registered (`nobody@x.com`) | Generic error (no such account) | `[SPEC]` |

### Input I2 — Password

| EC | Type | Domain | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-P1 | valid | Correct password for the account | Login succeeds | `[SPEC]` |
| EC-P2 | invalid | Wrong password | Generic error | `[SPEC]` |
| EC-P3 | invalid | Empty | Rejected | `[SPEC]` |

### Login outcome & lockout (driven by I3)

| EC | Type | Situation | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-L1 | valid | Correct email + correct password | Success (O1) | `[SPEC]` |
| EC-L2 | invalid | Wrong credentials, fewer than 3 consecutive failures | Error, retry still allowed | `[SPEC]` |
| EC-L3 | invalid | 3rd (or later) consecutive failure | Account locked ~30s | `[SPEC]` |
| EC-L4 | invalid | During lockout, even correct credentials | Blocked until the 30s pass | `[SPEC]` / `[ASSUMED]` |
| EC-M1 | security | Error message content | Generic; does not reveal which field was wrong | `[SPEC]` |

## Step 3 — Domain test cases

For the valid class, one test logs in successfully. For invalid classes, each test makes exactly one factor invalid while keeping others valid. EC-M1 is checked by comparing the messages of a wrong-password vs an unknown-email attempt.

| TC | Email | Password | Precondition | Covers EC | Expected | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DT1 | `test@eshop.com` | `Test1234!` | counter = 0 | EC-E1, EC-P1, EC-L1 | Login succeeds; app navigates home | Login success, token stored | Pass |
| DT2 | `test@eshop.com` | `WrongPass1!` | counter < 2 | EC-P2, EC-L2 | Generic error; retry allowed | "Invalid Email or Password" | Pass |
| DT3 | `nobody@x.com` | `Test1234!` | counter < 2 | EC-E4 | Generic error (no leak) | "Invalid Email or Password" | Pass |
| DT4 | `test@` | `Test1234!` | — | EC-E2 | Rejected / format error | Error: "Invalid email format" | Pass |
| DT5 | (empty) | `Test1234!` | — | EC-E3 | Rejected (email required) | "Email is required" | Pass |
| DT6 | `test@eshop.com` | (empty) | — | EC-P3 | Rejected (password required) | "Password is required" | Pass |
| DT7 | compare DT2 vs DT3 | — | — | EC-M1 | Same generic message | Messages are identical | Pass |
| DT8 | `test@eshop.com` | `WrongPass1!` ×3 | 3 failures | EC-L3 | Account locked ~30s | "Account locked for 30s" | Pass |
| DT9 | `test@eshop.com` | `Test1234!` | during lockout | EC-L4 | Blocked until 30s elapse | Login blocked by timer | Pass |

---

# Part B — Boundary Value Analysis

## Step 4 — Boundary analysis and boundary test cases

The ordered field here is the **consecutive-failure counter**, whose boundary is the lock threshold (spec: lock at the 3rd failure). The second boundary is the **30-second lock duration** (a time boundary, tested approximately). Email/password are unordered strings (no numeric boundary), but string-length and format edges are probed as adversarial inputs.

### Boundary 1 — Lock threshold (locks on the 3rd consecutive failure) — `[SPEC]`

| BV | Attempt | Counter after attempt | Position | Expected | Source |
| --- | --- | --- | --- | --- | --- |
| BV1 | 1st wrong | 1 | below | Error, retry allowed | `[SPEC]` |
| BV2 | 2nd wrong | 2 | LB − 1 (last before lock) | Error, retry allowed | `[SPEC]` |
| BV3 | 3rd wrong | 3 | LB (on threshold) | Account locked — catches off-by-one (`>` vs `>=` on the count) | `[SPEC]` |
| BV4 | 4th attempt (during lock) | — | above | Blocked (locked) | `[SPEC]` |

### Boundary 2 — Lock duration (30 seconds) — `[SPEC]` / `[ASSUMED]` (exact timing)

| BV | Retry timing after lock | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV5 | retry at ~29s (still within lock) | before | Still blocked | `[SPEC]` |
| BV6 | retry at ~31s (after lock) with correct creds | after | Allowed; login succeeds | `[SPEC]` |

### Adversarial / edge inputs — `[ASSUMED]` / `[OBS]`

- **Email:** leading/trailing spaces `"  test@eshop.com  "` · different case `TEST@eshop.com` (should login be case-insensitive?) · very long string · injection-style `' OR 1=1 --` / `<script>`.
- **Password:** very long string · leading/trailing spaces · correct password with a trailing space.
- **Counter reset:** 2 wrong attempts then the correct password — does login succeed and does the counter reset to 0 afterwards?
- **Connectivity (mobile-specific):** with the backend unreachable (wrong `API_URL` / phone off Wi-Fi), the login button should show a clear network error, not hang silently.

### Boundary test cases

| TC | Scenario | Covers BV | Expected | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- |
| BT1 | 1st wrong password | BV1 | Error, retry allowed | As expected | Pass |
| BT2 | 2nd consecutive wrong password | BV2 | Error, retry allowed | As expected | Pass |
| BT3 | 3rd consecutive wrong password | BV3 | Account locked ~30s | As expected | Pass |
| BT4 | 4th attempt during lock | BV4 | Blocked | As expected | Pass |
| BT5 | Retry with correct password ~28s | BV5 | Still blocked | As expected | Pass |
| BT6 | Retry with correct password ~32s | BV6 | Login succeeds | As expected | Pass |
| BT7 | 2 wrong then correct password | adversarial | Login succeeds; counter resets | Login success; counter=0 | Pass |

---

## Step 5 — AI gap analysis

To be completed after test execution (record anything the design missed vs. the running mobile app — e.g. whether email-format validation exists on mobile, exact lock timing, message-leak behaviour).

## Step 6 — Bug report

| Bug ID | Title | Severity | Steps to reproduce | Expected | Actual | Screenshot | Issue link |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

---

## Test summary

- Domain test cases designed: **9** (DT1–DT9)
- Boundary test cases designed: **7** (BT1–BT7)
- Total designed: **16**
- Executed: **16** · Passed: **16** · Failed: **0** · Not run: **0**
- Bugs found: **0**
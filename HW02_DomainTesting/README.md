# HW02 – Domain Testing

HW02 – Domain Testing on EShop

Exercise ID: HW02-AI
Duration: 10 hours
Form: Individual Assignment

## 1. Self-Assessment Table

| Criterion | Weight | Self-Assessed Grade |
|---|---:|---:|
| Feature A — FR-01 (Domain + Boundary) | 25 | |
| Feature B — FR-08 (Domain + Boundary) | 25 | |
| Feature C — FR-19 (Domain + Boundary) | 25 | |
| Feature D — FR-20 (Mobile Domain + Boundary) | 15 | |
| Agent Skills (domain-testing-bva-skill) | 10 | |
| **Total** | 100 | |

> Leave the `Self-Assessed Grade` column blank for the student to fill.

## 2. Test Summary Report (current state)

- Number of features with any executed tests: 2 (FR-01, FR-19)
- Features in scope: FR-01 (A), FR-08 (B), FR-19 (C), FR-20 (D)

Per-feature summary (Domain Testing)

| Feature | Domain TCs designed | Executed | Passed | Failed | Not executed |
|---|---:|---:|---:|---:|---:|
| FR-01 (Account Registration) | 13 | 13 | 2 | 11 | 0 |
| FR-08 (Checkout) | 0 | 0 | 0 | 0 | 0 |
| FR-19 (User Management) | 6 | 4 | 2 | 2 | 2 |
| FR-20 (Mobile Profile) | 0 | 0 | 0 | 0 | 0 |

Per-feature summary (Boundary Value Analysis)

| Feature | BVA TCs designed | Executed | Passed | Failed | Not executed |
|---|---:|---:|---:|---:|---:|
| FR-01 (Account Registration) | 4 | 4 | 2 | 2 | 0 |
| FR-08 (Checkout) | 0 | 0 | 0 | 0 | 0 |
| FR-19 (User Management) | 4 | 1 | 0 | 1 | 3 |
| FR-20 (Mobile Profile) | 0 | 0 | 0 | 0 | 0 |

Overall test-case totals (both techniques)

- Domain TCs designed: 19
- Domain TCs executed: 17
- Domain TCs passed: 4
- Domain TCs failed: 13
- Domain TCs not-yet-executed: 2

- BVA TCs designed: 8
- BVA TCs executed: 5
- BVA TCs passed: 2
- BVA TCs failed: 3
- BVA TCs not-yet-executed: 3

## 3. Bug Summary

- Total bug entries recorded: 15
	- Critical: 2 (authorization bypass on admin endpoints; password exposure in login responses)
	- High: 13 (registration and BVA failures documented for FR-01)

Bug report files: `bug-reports/bug_report.md` (contains all current bug entries and steps-to-reproduce).

## 4. Demo / Agent Skill Links

- Agent Skill: `agent-skills/domain-testing-bva-skill/SKILL.md` (not yet implemented)
- Demo video (placeholder): <YouTube link placeholder — record demo and paste URL here>

## 5. Notes & Next Steps

- FR-01 and FR-19 have been exercised with dual-channel checks; FR-08 and FR-20 remain to be designed and executed.
- Blocking item for completing FR-19 admin verifications: a working admin bearer token is required (documented admin credentials returned 401 in black-box runs). Provide a valid admin token or allow further allowed black-box recovery attempts to complete admin-only checks (self-delete, password-field absence in admin list).
- I can (a) continue with FR-08 extraction and TC design now, or (b) complete FR-19 admin checks if you supply an admin token. Which do you prefer?

----
Generated from the current report files in `HW02_DomainTesting/reports/` and `HW02_DomainTesting/bug-reports/`.

# HW02 Domain Testing Workspace

This workspace contains the assignment artifacts for the EShop black-box test plan.

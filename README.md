# HW02 — Domain Testing & Boundary Value Analysis on EShop

| Field | Value |
| --- | --- |
| Student ID | 23127362 |
| Course | CS423 / CSC13003 — Software Testing |
| Group repo | software-testing-group-06 |
| Branch | `week_2/23127362` |
| SUT | EShop — https://github.com/ttbhanh/eshop-sut |

## Selected Features (one per pool, no duplicate with teammates)

| Pool | Feature | Platform | Report |
| --- | --- | --- | --- |
| A | FR-06 — Product Detail (Quantity input) | Web (`localhost:5173`) | `report/FR-06_ProductDetail.md` |
| B | FR-09 — Discount Coupon | Web checkout | `report/FR-09_Coupon.md` |
| C | FR-15 — Product Management (CRUD) | Web Admin (`localhost:5174`) | `report/FR-15_ProductCRUD.md` |
| D | Mobile — Login | Mobile / Expo | `report/Mobile_Login.md` |

## Self-Assessment

| No. | Criteria | Max | Self-Assessed |
| --- | --- | --- | --- |
| 1 | Feature A — FR-06 (Domain + Boundary) | 25 |  |
| 2 | Feature B — FR-09 (Domain + Boundary) | 25 |  |
| 3 | Feature C — FR-15 (Domain + Boundary) | 25 |  |
| 4 | Feature D — Mobile Login (Domain + Boundary) | 15 |  |
| 5 | Agent Skills | 10 |  |
|  | **Total** | **100** |  |

> The 3-digit self-assessed total also goes in the zip filename:
> `23127362_HW02_AI_DomainTesting_<grade>.zip`

## Test Summary

| Metric | Count |
| --- | --- |
| Features tested | 4 |
| Test cases designed |  |
| Test cases executed |  |
| Passed |  |
| Failed |  |
| Not yet executed |  |
| Bugs found (GitHub Issues) |  |

## Demo Videos

- Agent Skill (Domain + BVA) end-to-end demo: `<YouTube link>`

## Repository Layout

```
report/       # one Markdown report per feature (Domain Testing + BVA, 6 steps each)
bugs/         # consolidated bug report (also mirrored to GitHub Issues)
ai/           # prompt_log.md, ai-audit-report.md, ai-critique.md
skills/       # domain-bva-testing Agent Skill
screenshots/  # bug + evidence screenshots
SETUP.md      # how to run the EShop SUT (backend, web, admin, mobile)
TODO.md       # step-by-step checklist from now until submission
```

## How to run the SUT

See **SETUP.md**. Default accounts: admin `admin@eshop.com` / `Admin123!`,
user `test@eshop.com` / `Test1234!`.

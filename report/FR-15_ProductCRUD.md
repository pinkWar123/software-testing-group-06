# FR-15 — Product Management (CRUD) — Domain Testing & BVA

| Field | Value |
| --- | --- |
| Feature | FR-15 — Quản lý Sản phẩm |
| Pool / Platform | C / Web Admin (`localhost:5174`) |
| Spec source | EShop SRS §6, FR-15 |
| Tester | 23127362 |

## Spec summary — Add / View / Edit / Delete product
- Name: required, max 255 chars.
- Price: required, positive number ( > 0 ).
- Category: required, must be chosen from existing list.
- Editing one product must not change others.

---

## Step 1 — Input inventory
| # | Input | Type | Valid domain | Notes |
| --- | --- | --- | --- | --- |
| I1 | Name | string | required, 1..255 chars | non-empty |
| I2 | Price | number | > 0 | positive |
| I3 | Category | enum | from existing list | required |

## Step 2 — Domain Testing (Equivalence Partitioning)
| EC-ID | Input | Valid/Invalid | Class | Representative |
| --- | --- | --- | --- | --- |
| EC1 | Name | Valid | normal length | "Áo thun" |
| EC2 | Name | Invalid | empty | "" |
| EC3 | Name | Invalid | over 255 chars | 256-char string |
| EC4 | Name | Invalid/security | HTML/script | `<script>alert(1)</script>` |
| EC5 | Price | Valid | positive | 100000 |
| EC6 | Price | Invalid | zero / negative | 0 / -1 |
| EC7 | Price | Invalid | non-numeric | "abc" |
| EC8 | Category | Invalid | none selected | (empty) |

## Step 3 — Boundary Value Analysis
| BV-ID | Input | Boundary | Value | Side | Expected |
| --- | --- | --- | --- | --- | --- |
| BV1 | Name length | max=255 | 255 chars | on | accept |
| BV2 | Name length | max=255 | 256 chars | above | reject |
| BV3 | Name length | min=1 | 0 (empty) | below | reject |
| BV4 | Price | min ( >0 ) | 0 | on | reject |
| BV5 | Price | min | 0.01 / 1 | above | accept |
| BV6 | Price | min | -1 | below | reject |

## Step 4 — Test cases
| TC-ID | Technique | Title | Precondition | Test data / steps | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC01 | EP | Create valid product | logged in as admin | fill valid name/price/category, save | created |  |  |

## Step 5 — AI gap analysis
- Missed:
- Why:

## Step 6 — Bugs found
| BUG-ID | Title | Severity | Steps | Expected | Actual | Issue link |
| --- | --- | --- | --- | --- | --- | --- |

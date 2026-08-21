# API 2 Test Strategy — `POST /api/checkout`

## Basis and objective

- **Feature:** FR-08 Checkout, with the related FR-07 cart and FR-10 order lifecycle.
- **Endpoint:** `POST http://localhost:3000/api/checkout`.
- **Authentication:** `Authorization: Bearer <JWT>` and `X-Student-Id: 22127345`.
- **Request:** `{ "total_amount": 200000, "shipping_address": "123 Le Loi, TP.HCM" }`.
- **Success oracle:** HTTP 200, JSON `{ message: "Checkout successful", orderId: <positive integer> }`; the created order is owned by the authenticated user, starts as `pending`, uses the server-calculated cart total, and the cart is cleared.
- **Negative oracle:** controlled 4xx JSON response; no order is created and no unrelated user's cart/order is affected.

The specification requires the backend to recalculate the total from the authenticated user's cart and not trust `total_amount`. The test basis also includes the README security requirements SEC-01–SEC-07. The final expected status/message must be reconciled with the observed API contract during human audit.

## Scope

In scope: authentication, request/body validation, total integrity, shipping-address handling, empty and populated carts, order creation, cart clearing, response schema, ownership/IDOR, injection, role boundaries, malformed input, unsupported methods, and Student-ID header evidence.

Out of scope for this stage: UI checkout rendering, payment-gateway integration, load testing, human audit labels, execution results, and GitHub defect filing.

## ISTQB test design

| Technique | Application |
|---|---|
| Equivalence partitioning | Valid/invalid JWT; populated/empty cart; correct/tampered/missing/null/negative/non-numeric totals; valid/empty/oversized/hostile addresses. |
| Boundary value analysis | Total `0`, `0.01`, maximum practical amount, negative minimum; address empty, one character, maximum allowed length, and over-limit input; cart quantity `1` and boundary values. |
| Decision table | Authentication × cart state × total integrity × address validity determines acceptance, rejection, and side effects. |
| State transition | `cart populated → checkout accepted → order pending + cart empty`; rejected checkout leaves both states unchanged; order lifecycle starts at `pending`. |
| Experience-based/error guessing | SQL/XSS payloads, duplicate fields, wrong JSON types, prototype-like keys, IDOR attempts, stale/forged JWTs, unsupported methods. |

## Risk and priority

| Risk | Impact | Priority | Mitigation/test focus |
|---|---|---|---|
| Client total is trusted | Financial integrity | Critical | API2-004–008, API2-021 |
| Missing/weak JWT or ownership check | Unauthorized order creation/data access | Critical | API2-009–014, API2-025–028 |
| Cart/order state is inconsistent | Duplicate or lost orders | High | API2-001–003, API2-015–020 |
| Input injection or unsafe error handling | Data compromise/crash | High | API2-029–034 |
| Response contract leaks or changes | Client integration failure | High | API2-035–037 |

## Environment and data

- Node.js backend from `../eshop-SUT/backend/server.js`, SQLite seed database, base URL `http://localhost:3000`.
- Runtime-only variables: `baseUrl`, `studentId`, `userToken`, `otherUserToken`, `adminToken`, `productId`, and disposable user credentials. Do not commit credentials.
- Each stateful case uses a disposable user/cart or reseeds the database. Capture order ID and verify the user's cart before and after checkout.
- Postman Collection Runner/Newman is the planned execution tool; request-level scripts inject `X-Student-Id` and assertions validate HTTP, JSON, side effects, and schema.

## Entry and exit criteria for this design stage

**Entry:** API specification and local implementation are available; endpoint and test data strategy are recorded.

**Exit:** The six initial API 2 checklist items have design artifacts: specification, at least 35 generated cases, domain partitions, state model, security coverage, and response-schema oracle. Audit and execution are intentionally not claimed complete.

# API 2 Test Conditions — Checkout

## Domain partitions

| Parameter/condition | Valid partition | Invalid partitions | Boundaries / notes |
|---|---|---|---|
| JWT | Signed, unexpired user/admin token | Missing, empty, malformed, expired, forged, wrong scheme | User token is sufficient; admin is not required. |
| `total_amount` | Number supplied by client but ignored; server cart total is authoritative | Missing, null, string, array/object, negative, zero, huge, decimal/NaN-like text | Compare tampered value with persisted order total. |
| `shipping_address` | Non-empty ordinary text | Missing, null, empty, whitespace, number/object/array, overlong text, SQL/XSS payload | Must be stored safely and returned/handled without execution. |
| Cart | Authenticated user's populated cart | Empty, absent, malformed item, zero/negative quantity, another user's cart | Checkout must not read another user's cart. |
| Header | `X-Student-Id: 22127345` | Missing/wrong value | Required evidence header; verify whether API contract rejects or merely records it. |
| HTTP method/content type | POST + JSON | GET/PUT/PATCH/DELETE, text/plain, malformed JSON | Controlled 4xx, no crash or stack trace. |

## State transition conditions

1. `CART_POPULATED → CHECKOUT_ACCEPTED`: create one `pending` order with server total and clear only the authenticated user's cart.
2. `CART_EMPTY → CHECKOUT_REJECTED`: controlled 4xx; no order and cart remains empty.
3. `INVALID_REQUEST → CHECKOUT_REJECTED`: no order and no cart mutation.
4. `USER_A_CART → USER_A_CHECKOUT`: User A cannot consume or create an order from User B's cart.
5. `ORDER_PENDING → ORDER_CONFIRMED → ORDER_SHIPPING → ORDER_DELIVERED`: API 2 creates only the initial `pending` state; later transitions belong to API 3/admin tests.
6. A repeated checkout after the cart is cleared must not silently duplicate the original order unless a new cart is populated.

## Security conditions SEC-01–SEC-07

| Requirement | API 2 condition/oracle |
|---|---|
| SEC-01 | No password/plaintext credential is accepted, persisted, or returned by checkout; JWT is not echoed in response. |
| SEC-02 | Missing, malformed, expired, and forged JWTs are rejected before order creation. |
| SEC-03 | Admin-only role checks are not bypassed; checkout must not grant admin authority or accept role claims from the body. |
| SEC-04 | Hostile shipping address is stored/returned as data, never rendered/executed as HTML/JS. |
| SEC-05 | SQL injection in address/total-like fields cannot alter queries or create unauthorized records; controlled response/no crash. |
| SEC-06 | A body field such as `role: "admin"` cannot change the authenticated user's role or ownership. |
| SEC-07 | Checkout cannot expose, create, or reuse reset/OTP secrets; response contains only documented fields. |

## Schema conditions

Success must be JSON with exactly the documented business fields: string `message` equal to `Checkout successful` and positive integer `orderId`. Error responses must be JSON, must not contain stack traces, absolute paths, credentials, JWTs, or database internals. Persisted order rows must contain authenticated `user_id`, server-calculated `total_amount`, `pending` status, and the supplied address.

Bug ID: BUG-015
Title: Checkout accepts tampered client total_amount
Description:
- Scenario: User is logged in and cart contains one item priced 28000000þ.
- Expected: The backend should recompute the total from the server-side cart and reject or override the client-supplied total_amount.
- Actual: The backend returns HTTP 200 and creates an order with total_amount 1000, accepting the tampered client-supplied value.
Evidence:
- UI screenshot: HW02_DomainTesting/evidence/screenshots/FR-08_Checkout/TC-FR08-05.png
- Backend behavior confirmed via direct API verification.

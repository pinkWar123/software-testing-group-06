Bug ID: BUG-014
Title: Checkout allows empty-cart order creation
Description:
- Scenario: User is logged in and cart is empty.
- Expected: The UI should block checkout on an empty cart and the backend should return a 4xx error without creating an order.
- Actual: The UI shows empty-cart messaging, but the backend returns HTTP 200 and creates an order with total_amount 0.
Evidence:
- UI screenshot: HW02_DomainTesting/evidence/screenshots/FR-08_Checkout/TC-FR08-04.png
- Backend behavior confirmed via direct API verification.

Bug ID: BUG-016
Title: Checkout succeeds without required shipping_address field
Description:
- Scenario: User is logged in and proceeds to checkout; the UI does not present a shipping_address input.
- Expected: The UI should collect shipping_address and the backend should reject requests missing shipping_address.
- Actual: The backend returns HTTP 200 with checkout success while shipping_address is null.
Evidence:
- UI screenshot: HW02_DomainTesting/evidence/screenshots/FR-08_Checkout/TC-FR08-06.png
- Backend behavior confirmed via direct API verification.

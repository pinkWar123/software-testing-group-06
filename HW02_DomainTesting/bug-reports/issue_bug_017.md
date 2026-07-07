Bug ID: BUG-017
Title: Checkout does not clear cart after successful order creation
Description:
- Scenario: User is logged in and completes a checkout for one cart item.
- Expected: The backend should clear the cart after successful checkout and the UI should reflect an empty cart.
- Actual: The checkout appears successful, but the backend leaves the cart items intact and the cart is not cleared.
Evidence:
- UI screenshot: HW02_DomainTesting/evidence/screenshots/FR-08_Checkout/TC-FR08-01.png
- Backend behavior confirmed via direct API verification.

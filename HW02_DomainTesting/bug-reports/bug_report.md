# FR-01 Bug Reports

## Summary
- Total failing TCs captured: 13
- API evidence was verified directly against the backend registration endpoint at http://localhost:3000/api/register.
- UI screenshots are attached in the FR-01 evidence folder, so each report now records the screenshot-backed UI observation alongside the verified API failure.

## BUG-001
- Bug ID: BUG-001
- Title: Registration accepts an empty name value
- TC ref: TC-FR01-02
- Severity: High
- Steps to Reproduce:
  1. Open the registration page at http://localhost:5173/register.
  2. Leave the name field empty.
  3. Enter a valid-looking email and password.
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the empty name and show a validation message; the API should return a client error and not create an account.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":4}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-02](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-02.png). API evidence from the verification script: `TC-FR01-02|status=200|body={"message":"User registered successfully","id":4}`.

## BUG-002
- Bug ID: BUG-002
- Title: Registration accepts a malformed email address
- TC ref: TC-FR01-03
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a name.
  3. Enter `invalid-email` as the email.
  4. Enter a valid password.
  5. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the malformed email and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":5}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-03](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-03.png). API evidence: `TC-FR01-03|status=200|body={"message":"User registered successfully","id":5}`.

## BUG-003
- Bug ID: BUG-003
- Title: Registration accepts an empty email field
- TC ref: TC-FR01-04
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name.
  3. Leave the email field empty.
  4. Enter a valid password.
  5. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the empty email and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":6}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-04](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-04.png). API evidence: `TC-FR01-04|status=200|body={"message":"User registered successfully","id":6}`.

## BUG-004
- Bug ID: BUG-004
- Title: Registration accepts a duplicate email address on first submission
- TC ref: TC-FR01-05
- Severity: High
- Steps to Reproduce:
  1. Ensure the email `fr01-dup-base@test.com` is already registered.
  2. Open the registration page.
  3. Enter a different name.
  4. Use the duplicate email and a valid password.
  5. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the duplicate-email input and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":7}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-05](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-05.png). API evidence: `TC-FR01-05|status=200|body={"message":"User registered successfully","id":7}`.

## BUG-005
- Bug ID: BUG-005
- Title: Registration allows the same email to be used more than once
- TC ref: TC-FR01-06
- Severity: High
- Steps to Reproduce:
  1. Register a user with `fr01-dup-base@test.com`.
  2. Attempt to register again with the same email.
  3. Submit the form.
- Expected vs Actual:
  - Expected: The UI should block the second registration and show a duplicate-email message; the API should reject the duplicate request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":8}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-06](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-06.png). API evidence: `TC-FR01-06|status=200|body={"message":"User registered successfully","id":8}`.

## BUG-006
- Bug ID: BUG-006
- Title: Registration accepts a password missing uppercase letters
- TC ref: TC-FR01-07
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `abcdef1!` (missing uppercase).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the weak password and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":9}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-07](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-07.png). API evidence: `TC-FR01-07|status=200|body={"message":"User registered successfully","id":9}`.

## BUG-007
- Bug ID: BUG-007
- Title: Registration accepts a password missing lowercase letters
- TC ref: TC-FR01-08
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `ABCDEF1!` (missing lowercase).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the weak password and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":10}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-08](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-08.png). API evidence: `TC-FR01-08|status=200|body={"message":"User registered successfully","id":10}`.

## BUG-008
- Bug ID: BUG-008
- Title: Registration accepts a password missing a digit
- TC ref: TC-FR01-09
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `Abcdef!` (missing a digit).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the weak password and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":11}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-09](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-09.png). API evidence: `TC-FR01-09|status=200|body={"message":"User registered successfully","id":11}`.

## BUG-009
- Bug ID: BUG-009
- Title: Registration accepts a password missing a special character
- TC ref: TC-FR01-10
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `Abcdef1` (missing a special character).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the weak password and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":12}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-10](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-10.png). API evidence: `TC-FR01-10|status=200|body={"message":"User registered successfully","id":12}`.

## BUG-010
- Bug ID: BUG-010
- Title: Registration accepts a password shorter than 8 characters
- TC ref: TC-FR01-11
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `Abcde1!` (7 characters).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the short password and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":13}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-11](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-11.png). API evidence: `TC-FR01-11|status=200|body={"message":"User registered successfully","id":13}`.

## BUG-011
- Bug ID: BUG-011
- Title: Registration accepts an empty password field
- TC ref: TC-FR01-12
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Leave the password field empty.
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the empty password and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":14}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-12](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-12.png). API evidence: `TC-FR01-12|status=200|body={"message":"User registered successfully","id":14}`.

## BUG-012
- Bug ID: BUG-012
- Title: Registration accepts a password at the minimum invalid length boundary
- TC ref: TC-FR01-BVA-01
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `Abcde1!` (7 characters, one below the required minimum).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the password as too short and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":18}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-BVA-01](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-BVA-01.png). API evidence: `TC-FR01-BVA-01|status=200|body={"message":"User registered successfully","id":18}`.

## BUG-013
- Bug ID: BUG-013
- Title: Registration accepts a password with a disallowed special character
- TC ref: TC-FR01-BVA-04
- Severity: High
- Steps to Reproduce:
  1. Open the registration page.
  2. Enter a valid name and email.
  3. Use the password `Abcdef1#` (contains a disallowed special character).
  4. Submit the form.
- Expected vs Actual:
  - Expected: The UI should reject the password because the special character is not allowed and show a validation message; the API should reject the request.
  - Actual: The UI screenshot shows the registration form submission outcome for this invalid input; the API returned HTTP 200 with body `{"message":"User registered successfully","id":21}`.
- Environment: Web UI + backend API on localhost; Windows workspace.
- Screenshot/curl evidence: UI screenshot: [TC-FR01-BVA-04](../evidence/screenshots/FR-01_AccountRegistration/TC-FR01-BVA-04.png). API evidence: `TC-FR01-BVA-04|status=200|body={"message":"User registered successfully","id":21}`.

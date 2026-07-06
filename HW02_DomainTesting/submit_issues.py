import subprocess
import sys

repo = 'pinkWar123/software-testing-group-06'

issues = [
    {
        'title': 'Registration accepts an empty name value',
        'body': '## Summary\n- TC ref: TC-FR01-02\n- Expected: UI and API should reject empty name input.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":4}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-02.png?raw=1\n- API evidence: TC-FR01-02|status=200|body={"message":"User registered successfully","id":4}'
    },
    {
        'title': 'Registration accepts a malformed email address',
        'body': '## Summary\n- TC ref: TC-FR01-03\n- Expected: UI and API should reject malformed email input.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":5}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-03.png?raw=1\n- API evidence: TC-FR01-03|status=200|body={"message":"User registered successfully","id":5}'
    },
    {
        'title': 'Registration accepts an empty email field',
        'body': '## Summary\n- TC ref: TC-FR01-04\n- Expected: UI and API should reject empty email input.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":6}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-04.png?raw=1\n- API evidence: TC-FR01-04|status=200|body={"message":"User registered successfully","id":6}'
    },
    {
        'title': 'Registration accepts a duplicate email address on first submission',
        'body': '## Summary\n- TC ref: TC-FR01-05\n- Expected: UI and API should reject duplicate email input.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":7}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-05.png?raw=1\n- API evidence: TC-FR01-05|status=200|body={"message":"User registered successfully","id":7}'
    },
    {
        'title': 'Registration allows the same email to be used more than once',
        'body': '## Summary\n- TC ref: TC-FR01-06\n- Expected: UI and API should reject the second registration with the same email.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":8}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-06.png?raw=1\n- API evidence: TC-FR01-06|status=200|body={"message":"User registered successfully","id":8}'
    },
    {
        'title': 'Registration accepts a password missing uppercase letters',
        'body': '## Summary\n- TC ref: TC-FR01-07\n- Expected: UI and API should reject a weak password missing uppercase letters.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":9}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-07.png?raw=1\n- API evidence: TC-FR01-07|status=200|body={"message":"User registered successfully","id":9}'
    },
    {
        'title': 'Registration accepts a password missing lowercase letters',
        'body': '## Summary\n- TC ref: TC-FR01-08\n- Expected: UI and API should reject a weak password missing lowercase letters.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":10}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-08.png?raw=1\n- API evidence: TC-FR01-08|status=200|body={"message":"User registered successfully","id":10}'
    },
    {
        'title': 'Registration accepts a password missing a digit',
        'body': '## Summary\n- TC ref: TC-FR01-09\n- Expected: UI and API should reject a weak password missing a digit.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":11}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-09.png?raw=1\n- API evidence: TC-FR01-09|status=200|body={"message":"User registered successfully","id":11}'
    },
    {
        'title': 'Registration accepts a password missing a special character',
        'body': '## Summary\n- TC ref: TC-FR01-10\n- Expected: UI and API should reject a weak password missing a special character.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":12}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-10.png?raw=1\n- API evidence: TC-FR01-10|status=200|body={"message":"User registered successfully","id":12}'
    },
    {
        'title': 'Registration accepts a password shorter than 8 characters',
        'body': '## Summary\n- TC ref: TC-FR01-11\n- Expected: UI and API should reject a password shorter than 8 characters.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":13}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-11.png?raw=1\n- API evidence: TC-FR01-11|status=200|body={"message":"User registered successfully","id":13}'
    },
    {
        'title': 'Registration accepts an empty password field',
        'body': '## Summary\n- TC ref: TC-FR01-12\n- Expected: UI and API should reject an empty password.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":14}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-12.png?raw=1\n- API evidence: TC-FR01-12|status=200|body={"message":"User registered successfully","id":14}'
    },
    {
        'title': 'Registration accepts a password at the minimum invalid length boundary',
        'body': '## Summary\n- TC ref: TC-FR01-BVA-01\n- Expected: UI and API should reject a password at the invalid boundary (7 chars).\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":18}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-BVA-01.png?raw=1\n- API evidence: TC-FR01-BVA-01|status=200|body={"message":"User registered successfully","id":18}'
    },
    {
        'title': 'Registration accepts a password with a disallowed special character',
        'body': '## Summary\n- TC ref: TC-FR01-BVA-04\n- Expected: UI and API should reject a password with a disallowed special character.\n- Actual: UI screenshot is attached in the FR-01 evidence folder; API returned HTTP 200 with body {"message":"User registered successfully","id":21}.\n- Evidence: UI screenshot: https://github.com/pinkWar123/software-testing-group-06/blob/main/HW02_DomainTesting/evidence/screenshots/FR-01_AccountRegistration/TC-FR01-BVA-04.png?raw=1\n- API evidence: TC-FR01-BVA-04|status=200|body={"message":"User registered successfully","id":21}'
    },
]

for issue in issues:
    existing = subprocess.run(
        ['gh', 'issue', 'list', '--repo', repo, '--search', issue['title'], '--limit', '5'],
        capture_output=True,
        text=True,
        check=False,
    )
    if existing.stdout and issue['title'] in existing.stdout:
        print(f'SKIP {issue["title"]}')
        continue

    result = subprocess.run(
        ['gh', 'issue', 'create', '--repo', repo, '--title', issue['title'], '--body', issue['body'], '--label', 'bug'],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f'FAILED {issue["title"]}: {result.stderr.strip()}')
        sys.exit(result.returncode)
    print(result.stdout.strip())

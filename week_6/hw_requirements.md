# HW06 – API Testing Requirements Checklist

Use this file to track completion. Record evidence paths, links, counts, and commit IDs as the work progresses.

## Setup and scope

- [x] Read the SUT repository and `api_specification.md`; identify relevant endpoints and SEC-01–SEC-07.
- [x] Select exactly three provisional APIs: Pool A `POST /api/login`, Pool B `POST /api/checkout`, and Pool C `PUT /api/admin/orders/:id/status` (Pools A/B/C only; Pool D is excluded).
- [ ] Verify that the selected three-API combination is not duplicated by another group member.
- [x] Record student ID `22127345`, SUT base URL `http://localhost:3000`, and chosen tool Postman + Newman.
- [x] Start the backend from `../eshop-SUT/backend/server.js` and verify `GET /api/products` plus admin login.

## API 1 — Pool A (30 points)

- [x] Document API 1 specification, feature, endpoint, request, response, and expected behavior.
- [x] Use AI step-by-step with the specification to generate at least 35 test cases (40 generated).
- [x] Cover domain partitions for every parameter.
- [x] Cover applicable state transitions.
- [x] Cover security requirements SEC-01–SEC-07, including injection, IDOR, and role escalation where applicable.
- [x] Cover exact response-schema validation.
- [x] Human-review and label every AI case VALID / INVALID / INCOMPLETE with reasoning. (37 VALID / 0 INVALID / 3 INCOMPLETE)
- [x] Correct every INVALID or INCOMPLETE case. (LOGIN-015, LOGIN-029, LOGIN-034 corrected in `artifacts/api1_login_test_cases.csv`)
- [x] Add at least 5 original student test cases AI missed. (6 added: SLOGIN-001–006)
- [x] Explain why each missed case was not generated (prompt quality, model limitation, or API characteristic). (reason captured per case in `HumanReview` and report §7.5)
- [x] Execute the complete API 1 suite with Postman + Newman, Karate, or RestAssured. (Postman Runner: 48 requests, 164 assertions, 155 passed, 9 failed, 0 errors; Newman HTML/JUnit artifacts also produced.)
- [x] Ensure every request carries `X-Student-Id: {StudentID}`; capture the required console evidence manually. (Evidence saved under `artifacts/evidence/api1/`: pre-request script, post-response assertions, Runner summary, console log, and request-header view.)
- [x] Produce and attach the Newman/HTML report or equivalent execution report. (`artifacts/api1_newman_report.html` and `.xml`)
- [x] Report genuine API 1 bugs in the Markdown report and on GitHub Issues, with a screenshot attached to each issue. (Issues #66, #67, #68, and #69 linked in report §7.7.)

## API 2 — Pool B (30 points)

- [x] Document API 2 specification, feature, endpoint, request, response, and expected behavior. (`artifacts/api2_checkout_test_strategy.md` and report §8.1)
- [x] Use AI step-by-step with the specification to generate at least 35 test cases. (37 generated in `artifacts/api2_checkout_test_cases.csv`; human audit remains pending.)
- [x] Cover domain partitions for every parameter. (`artifacts/api2_checkout_test_conditions.md`)
- [x] Cover state transitions, especially order transitions and cancellation rules where applicable. (`artifacts/api2_checkout_test_conditions.md`)
- [x] Cover security requirements SEC-01–SEC-07, including injection, IDOR, and role escalation where applicable. (`artifacts/api2_checkout_test_conditions.md`)
- [x] Cover exact response-schema validation. (`artifacts/api2_checkout_test_conditions.md` and traceability CSV)
- [x] Human-review and label every AI case VALID / INVALID / INCOMPLETE with reasoning. (33 VALID / 0 INVALID / 4 INCOMPLETE)
- [x] Correct every INVALID or INCOMPLETE case. (API2-005, API2-006, API2-008, API2-012 corrected in `artifacts/api2_checkout_test_cases.csv`)
- [x] Add at least 5 original student test cases AI missed. (6 added: SAPI2-001–006)
- [x] Explain why each missed case was not generated. (reason captured per case in `HumanReview` and report §8.5)
- [ ] Execute the complete API 2 suite with the selected test tool.
- [ ] Ensure every request carries `X-Student-Id: {StudentID}` and capture the required console evidence manually.
- [ ] Produce and attach the execution report.
- [ ] Report genuine API 2 bugs in Markdown and GitHub Issues, with a screenshot attached to each issue.

## API 3 — Pool C (30 points)

- [ ] Document API 3 specification, feature, endpoint, request, response, and expected behavior.
- [ ] Use AI step-by-step with the specification to generate at least 35 test cases.
- [ ] Cover domain partitions for every parameter.
- [ ] Cover applicable state transitions.
- [ ] Cover security requirements SEC-01–SEC-07, including injection, IDOR, and role escalation where applicable.
- [ ] Cover exact response-schema validation.
- [ ] Human-review and label every AI case VALID / INVALID / INCOMPLETE with reasoning.
- [ ] Correct every INVALID or INCOMPLETE case.
- [ ] Add at least 5 original student test cases AI missed.
- [ ] Explain why each missed case was not generated.
- [ ] Execute the complete API 3 suite with the selected test tool.
- [ ] Ensure every request carries `X-Student-Id: {StudentID}` and capture the required console evidence manually.
- [ ] Produce and attach the execution report.
- [ ] Report genuine API 3 bugs in Markdown and GitHub Issues, with a screenshot attached to each issue.

## Cross-suite technical requirements

- [ ] Use and document as many available Postman features as reasonably applicable: workspace, collection, variables, environment, data-driven runner, monitors, mock server, or equivalent Karate/RestAssured features.
- [ ] Add the API tests to a CI/CD pipeline for the SUT.
- [ ] Write the CI/CD report describing the configuration and both required runs.
- [ ] Provide one sample commit whose pipeline run has all API tests passing.
- [ ] Provide one sample commit whose pipeline run has one test case failing.
- [ ] Add screenshots and links for both CI/CD runs.

## Agent Skill / Create level (10 points)

- [ ] Design an AI-driven API test generator that accepts the API specification and produces test cases.
- [ ] Make the design decisions yourself.
- [ ] Draw the architecture diagram yourself (diagram must not be AI-generated). ⚠️ MUST NOT USE AI
- [ ] Save the self-drawn diagram as PNG or Mermaid plus `.md` / `.py` source as applicable. ⚠️ MUST NOT USE AI
- [ ] Write generator pseudocode.
- [ ] Optionally implement a reusable Agent Skill.
- [ ] Optionally record and link a demonstration video showing generation for one API.

## Mandatory AI compliance

- [ ] Declare every AI tool used; if none, include the exact no-AI declaration.
- [ ] Log every AI interaction with tool, date/time, exact prompt, and output.
- [ ] Document human review, corrections, and traceability for all AI-assisted artifacts.
- [ ] Write a 200–300 word AI Critique covering error/bias/incompleteness, why it happened, and a collaboration principle.
- [ ] Include AI Audit Report as an appendix in Markdown and PDF.
- [ ] Include AI Critique in Markdown and PDF.
- [ ] Include Mandatory Disclosure.

## Evidence and submission package

- [ ] Create a Git commit for each procedure step (at minimum generation, audit, extension, and execution for each API).
- [ ] Export the Git commit log to a text-based file.
- [ ] Produce the main report in Markdown and PDF.
- [ ] Include public GitHub repository link.
- [ ] Include Postman collection JSON and Newman HTML report (or alternative tool artifacts), plus used-feature list.
- [ ] Include Excel test cases and test summary.
- [ ] Include generator diagram and pseudocode.
- [ ] Include bug report and GitHub Issue screenshots.
- [ ] Include `README.md` with self-assessment table and summary counts: APIs, generated/added/executed/passed/failed cases, and bugs.
- [ ] Include optional OpenAPI YAML/JSON only if used; audit it if AI-generated.
- [ ] Include any supporting materials.
- [ ] Name the ZIP exactly `<StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip`, with grade from 000–100.
- [ ] Submit the ZIP to Moodle before the deadline shown on Moodle.
- [ ] Confirm the assignment is individual, no copied prompts/artifacts were used, and no late submission is planned.
- [ ] Prepare to explain the work in a 5–7 minute oral defense if randomly selected (30% of students).

## Scoring summary

| Area | Points |
|---|---:|
| API 1 full pipeline | 30 |
| API 2 full pipeline | 30 |
| API 3 full pipeline | 30 |
| Agent Skill / AI-driven test generator | 10 |
| **Total** | **100** |

## What AI can help with vs. what must be done manually

| AI can help with | Must be done manually / must be real evidence |
|---|---|
| Analyze the API specification and propose partitions, transitions, security cases, schemas, and test-case drafts | Choose APIs and confirm no group duplication |
| Generate and refine prompts, test data ideas, assertions, pseudocode, report prose, and reusable scripts | Review and label every AI case; correct INVALID / INCOMPLETE cases |
| Suggest Postman/Newman scripts, CI configuration, and coverage summaries | Run the suite and preserve genuine Newman/HTML output with matching hostname |
| Help organize Markdown, audit logs, disclosure, and critique drafts | `X-Student-Id` header evidence from your pre-request script ⚠️ MUST NOT USE AI |
| Help explain missed cases and summarize bugs | Self-drawn AI test-generator diagram ⚠️ MUST NOT USE AI |
| Help format data and supporting documentation | Genuine bug reproduction, GitHub Issue submission, screenshots, commits, and links |

## Prioritized work plan

1. Set up the SUT, deployment/base URL, Student ID, tool choice, repository access, and API specification.
2. Coordinate and lock the three non-duplicated API selections with group members.
3. Create the Postman collection/environment and implement the Student-ID pre-request script; capture its console evidence manually.
4. Confirm the SUT hostname and produce a small real execution proof before scaling the suite.
5. Design and self-draw the generator diagram early; save the editable/source artifact and then write pseudocode.
6. For API 1, API 2, and API 3 in sequence: prompt AI step-by-step, generate ≥35 cases, commit the generation step, audit/correct all cases, commit, add ≥5 student cases, commit, execute, capture reports/screenshots, investigate bugs, and commit execution artifacts.
7. Add the full suite to CI/CD and create the all-passing and intentionally failing sample commits/runs with links and screenshots.
8. File genuine GitHub Issues with reproduction details and screenshots; link them in the report.
9. Produce the Excel test cases and summary, PDF versions, Git commit log, README summary/self-assessment, and supporting artifacts.
10. Complete the AI prompt log, audit report, disclosure, and 200–300 word critique; verify every AI interaction is traceable.
11. Run a final checklist and package using the exact filename format; submit to Moodle.

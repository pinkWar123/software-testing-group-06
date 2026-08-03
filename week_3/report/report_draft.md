# HW03 – GUI & Usability Testing on EMS

## Submission Information

| Field | Value |
| --- | --- |
| Student | Nguyễn Hồng Quân |
| Student ID | 22127345 |
| Assignment | HW03 – GUI & Usability Testing on EMS |
| Chosen scenario | Scenario B – User registers to attend an event |
| Selected screens | B1 Home/Events, B2 Event Detail, B4 Profile/Activities and QR |
| SUT | `https://prod-dev.ems-fitus.cloud/` |

## Self-Assessment

## Executive Test Summary

Task 1B executed all 48 items from the group’s shared GUI checklist on three Scenario B screens, producing **144 binary results: 123 Passed and 21 Failed**. Each screen had 41 Passed and 7 Failed results. The execution found 12 deduplicated bugs/usability findings involving responsive overflow, incomplete EN/VI localisation, accessibility semantics and contrast, missing result metadata, an unhelpful missing-event state, an unexplained required registration role, and a QR overlay that neither closes with Escape nor traps keyboard focus.

The complete 144-row matrix is stored in [`execution_results.md`](../artifacts/checklist_execution/execution_results.md). Automated scan and interaction details are recorded in [`automated_evidence.md`](../artifacts/checklist_execution/automated_evidence.md). Screenshots were attached only to Failed results.

## 1. Scope and Test Context

### 1.1 System Under Test

### 1.2 Group and Individual Responsibilities

### 1.3 Chosen Scenario

I selected **Scenario B – User registers to attend an event**. The participant journey begins with discovering an event, continues through reading the event details and choosing a registration role, and ends with reviewing participation history and accessing the QR function.

### 1.4 Selected Screens and Selection Rationale

| Screen | Route/state | Rationale |
| --- | --- | --- |
| B1 – Home / Events listing | `/dashboard` | Entry point for event discovery and the richest Scenario B list/navigation screen, covering the featured carousel, search, filters, categories, event cards, and pagination. |
| B2 – Event detail | `/events/68` – Machine Learning Hands-On Workshop | Event 68 was upcoming and open for Student registration during execution, exposing schedule, capacity, registration roles, and registration/cancellation states. |
| B4 – Profile / Activities and QR | `/profile` | Production EMS has no separate B3 registration-form screen: role selection and registration occur directly on B2. B4 is a distinct suggested Scenario B screen covering activity history, participation status, filters, pagination, and QR behavior. |

The same three screens should be retained for Tasks 2 and 3 to comply with the assignment’s shared-scope rule.

### 1.5 Test Environment, Accounts, and Tools

| Item | Execution value |
| --- | --- |
| Date | 02/08/2026 |
| Account | Personal Student SSO account, MSSV 22127345 |
| Browser | Google Chrome 150.0.7871.187 |
| Desktop viewport | 1440 × 1000 |
| Mobile viewport | 320 × 800 |
| Automation | Playwright Core 1.54.2 |
| Accessibility scan | axe-core 4.12 with WCAG 2.1 A/AA tags |
| Additional checks | EN/VI switching, keyboard interaction, empty search, valid/invalid deep links, registration/cancellation state, and QR overlay behavior |

## 2. Task 1A – Shared GUI Checklist

### 2.1 Checklist Design Method

### 2.2 Reference Sources

### 2.3 AI-Assisted Drafting and Human Review

### 2.4 Coverage of IA-01 through IA-04

### 2.5 Items Added after AI Review and Why AI Missed Them

### 2.6 Final Shared Checklist

## 3. Task 1B – Checklist Execution

The shared 48-item checklist was applied to each selected screen. `Passed` means no violation was observed in the components and states present during this execution. Because the assignment permits only Passed/Failed, an item whose named widget was absent was treated as Passed when no contrary behavior could be observed. The full matrix, including all Passed rows, is available in [`execution_results.md`](../artifacts/checklist_execution/execution_results.md).

### 3.1 Screen 1 Results

**B1 – Home / Events listing:** 41 Passed, 7 Failed.

| Checklist ID | Result | Failure notes | Screenshot reference |
| --- | --- | --- | --- |
| GUI-01-07 | Failed | Vietnamese mode retains English browser/accessibility strings such as “Dashboard,” “Switch language,” and “Notifications.” | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-07_BUG-B1-I18N.png" alt="B1 incomplete Vietnamese localisation" width="280"> |
| GUI-01-10 | Failed | At 320 px, the page has horizontal overflow and clipped header/control content. | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-10_BUG-B1-MOBILE-OVERFLOW.png" alt="B1 mobile horizontal overflow" width="280"> |
| GUI-01-11 | Failed | Axe found critical unnamed controls/invalid ARIA and serious contrast/SVG-name failures. | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 accessibility failures" width="280"> |
| GUI-02-02 | Failed | The visible filter select has no accessible name or associated label. | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 unnamed filter control" width="280"> |
| GUI-03-05 | Failed | The list does not show total matching results; pagination contains unnamed previous/next controls. | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 result and pagination metadata failure" width="280"> |
| GUI-03-11 | Failed | Filter and pagination controls cannot be reliably identified by assistive technology. | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 keyboard and accessible-name failure" width="280"> |
| GUI-04-04 | Failed | The carousel has no visible pause/stop control, and meaningful SVG images lack accessible text. | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 non-text content failure" width="280"> |

### 3.2 Screen 2 Results

**B2 – Event detail:** 41 Passed, 7 Failed.

| Checklist ID | Result | Failure notes | Screenshot reference |
| --- | --- | --- | --- |
| GUI-01-07 | Failed | Vietnamese mode retains the mixed-language checkbox name “Select Sinh viên” and English shared-control names. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-07_BUG-B2-I18N.png" alt="B2 incomplete Vietnamese localisation" width="280"> |
| GUI-01-10 | Failed | At 320 px, horizontal overflow occurs and the event heading collapses into narrow fragments. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-10_BUG-B2-MOBILE-OVERFLOW.png" alt="B2 mobile horizontal overflow" width="280"> |
| GUI-01-11 | Failed | Axe found invalid ARIA, low contrast, nested interactive controls, and unnamed SVG images. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-11_BUG-B2-A11Y.png" alt="B2 accessibility failures" width="280"> |
| GUI-02-01 | Failed | A role is required to enable Register but has no required marker or convention explanation. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-11_BUG-B2-A11Y.png" alt="B2 unexplained required role" width="280"> |
| GUI-03-02 | Failed | The role card has nested focusable semantics, producing ambiguous keyboard and screen-reader behavior. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-11_BUG-B2-A11Y.png" alt="B2 nested interactive role control" width="280"> |
| GUI-03-08 | Failed | `/events/999999` shows blank main content and Back to events without explaining that the event is unavailable. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-03-08_BUG-B2-DEAD-DEEPLINK.png" alt="B2 missing-event deep link without explanation" width="280"> |
| GUI-04-04 | Failed | The role/status area has nested semantics and SVG images exposed without accessible text. | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-11_BUG-B2-A11Y.png" alt="B2 non-text content failure" width="280"> |

### 3.3 Screen 3 Results

**B4 – Profile / Activities and QR:** 41 Passed, 7 Failed.

| Checklist ID | Result | Failure notes | Screenshot reference |
| --- | --- | --- | --- |
| GUI-01-07 | Failed | Vietnamese mode retains English accessible names including “Switch language,” “Notifications,” and “Go to page.” | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-07_BUG-B4-I18N.png" alt="B4 incomplete Vietnamese localisation" width="280"> |
| GUI-01-10 | Failed | At 320 px, the header/action row exceeds the viewport and an action is clipped. | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-10_BUG-B4-MOBILE-OVERFLOW.png" alt="B4 mobile horizontal overflow" width="280"> |
| GUI-01-11 | Failed | Axe found invalid ARIA, unnamed pagination buttons, insufficient contrast, and unnamed SVG images. | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-11_BUG-B4-A11Y.png" alt="B4 accessibility failures" width="280"> |
| GUI-03-02 | Failed | Escape does not close the QR overlay, and Tab reaches the underlying Edit Profile action. | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-04-11_BUG-B4-QR-ESC.png" alt="B4 QR keyboard and focus failure" width="280"> |
| GUI-03-05 | Failed | Activity pagination omits total matching results and has unnamed previous/next controls. | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-11_BUG-B4-A11Y.png" alt="B4 pagination metadata failure" width="280"> |
| GUI-04-04 | Failed | SVG images lack accessible text, and unnamed pagination controls communicate action only visually. | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-11_BUG-B4-A11Y.png" alt="B4 non-text content failure" width="280"> |
| GUI-04-11 | Failed | The QR overlay cannot be dismissed with Escape and does not contain keyboard focus. | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-04-11_BUG-B4-QR-ESC.png" alt="B4 QR overlay dismissal failure" width="280"> |

### 3.4 Additional Screen Results

No fourth screen was executed. B4 replaced the originally considered B3 because the production EMS performs role selection and registration directly on B2 rather than presenting a distinct registration-form screen.

### 3.5 Failed Items and Evidence

| Measure | Result |
| --- | ---: |
| Checklist items per screen | 48 |
| Total executions | 144 |
| Passed | 123 |
| Failed | 21 |
| Unique failure screenshots | 11 |
| Deduplicated findings | 12 |

Every Failed row above displays its authentic EMS screenshot inline. Several checklist failures reference the same screenshot when one underlying defect violates multiple criteria. The original PNGs are stored under [`artifacts/checklist_execution/screenshots/`](../artifacts/checklist_execution/screenshots/README.md).

### 3.6 Bugs Discovered

| Bug ID | Screen | Steps to reproduce | Expected | Actual | Severity | Screenshot reference |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-I18N-01 | B1/B2/B4 | Switch to Tiếng Việt; inspect tab titles and accessible names. | All UI and accessibility strings use Vietnamese consistently. | English strings remain on all screens. | Medium | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-07_BUG-B1-I18N.png" alt="Incomplete EN-VI localisation" width="260"> |
| BUG-B1-RESP-01 | B1 | Open `/dashboard`; resize to 320 × 800. | Page reflows without horizontal scrolling. | Header and controls overflow/clamp horizontally. | High | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-10_BUG-B1-MOBILE-OVERFLOW.png" alt="B1 mobile overflow" width="260"> |
| BUG-B2-RESP-01 | B2 | Open `/events/68`; resize to 320 × 800. | Detail page remains readable without horizontal scrolling. | Page overflows and title fragments into narrow lines. | High | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-10_BUG-B2-MOBILE-OVERFLOW.png" alt="B2 mobile overflow" width="260"> |
| BUG-B4-RESP-01 | B4 | Open `/profile`; resize to 320 × 800. | Profile actions fit or wrap inside viewport. | Horizontal scrolling appears and an action is clipped. | High | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-10_BUG-B4-MOBILE-OVERFLOW.png" alt="B4 mobile overflow" width="260"> |
| BUG-B1-A11Y-01 | B1 | Run axe WCAG 2.1 A/AA scan on `/dashboard`. | No critical/serious accessibility violations. | Unnamed controls, invalid ARIA, contrast failures, and unnamed SVGs occur. | High | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 accessibility failures" width="260"> |
| BUG-B2-A11Y-01 | B2 | Run axe scan on `/events/68`. | Valid role semantics and sufficient contrast. | Nested interactive semantics, invalid ARIA, contrast, and SVG-name failures occur. | High | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-11_BUG-B2-A11Y.png" alt="B2 accessibility failures" width="260"> |
| BUG-B4-A11Y-01 | B4 | Run axe scan on `/profile`. | All controls are named and text meets contrast requirements. | Pagination names, ARIA, contrast, and SVG alternatives fail. | High | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-11_BUG-B4-A11Y.png" alt="B4 accessibility failures" width="260"> |
| BUG-B2-NAV-01 | B2 | Navigate directly to `/events/999999`. | Explain that the event is unavailable and provide a safe CTA. | Main content is blank with no diagnosis. | Medium | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-03-08_BUG-B2-DEAD-DEEPLINK.png" alt="Missing-event deep-link failure" width="260"> |
| BUG-B2-FORM-01 | B2 | Open event 68 while unregistered; inspect the initial role state. | Required role is marked and explained. | Register depends on the role, but no required convention is shown. | Medium | <img src="../artifacts/checklist_execution/screenshots/B2_GUI-01-11_BUG-B2-A11Y.png" alt="Unexplained required registration role" width="260"> |
| BUG-B4-QR-01 | B4 | Open QR Code; press Escape and then Tab. | Escape closes the overlay and focus stays inside until close. | Escape does nothing and focus reaches underlying actions. | High | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-04-11_BUG-B4-QR-ESC.png" alt="QR overlay dismissal and focus failure" width="260"> |
| BUG-B1-NAV-01 | B1 | Inspect dashboard result count, filters, and pagination names. | Show total matches and identify every control. | Total count and several accessible names are absent. | Medium | <img src="../artifacts/checklist_execution/screenshots/B1_GUI-01-11_BUG-B1-A11Y.png" alt="B1 navigation metadata failure" width="260"> |
| BUG-B4-NAV-01 | B4 | Inspect profile activity count and pagination names. | Show total activities and named Previous/Next actions. | Total count and accessible names are absent. | Medium | <img src="../artifacts/checklist_execution/screenshots/B4_GUI-01-11_BUG-B4-A11Y.png" alt="B4 navigation metadata failure" width="260"> |

These 12 findings have been added to the aggregate findings log. Their Google Form timestamp remains `— (not submitted)` until the student makes each genuine submission and records its actual timestamp.

## 4. Task 2 – User Testing and Usability Report

### 4.1 Target User Profile

### 4.2 Goal-Oriented Task Scenario

### 4.3 Measures and Success Criteria

### 4.4 Open-Ended Probe Questions

### 4.5 Pilot Session and Refinements

### 4.6 Participants and Recruitment

### 4.7 Session Procedure, Consent, and Think-Aloud Protocol

### 4.8 Per-Session Observation Notes

### 4.9 SUS or UEQ-S Responses and Scoring

### 4.10 Metrics and Results

### 4.11 Ranked Usability Findings

### 4.12 Recommendations

## 5. Task 3 – Cross-Browser and Cross-Platform Testing

### 5.1 Coverage Strategy

### 5.2 Compatibility Matrix per Screen

### 5.3 Pass/Fail Results

### 5.4 Rendering and Interaction Defects

### 5.5 Screenshot Evidence Index

## 6. Bug and Usability Findings Log Summary

### 6.1 Google Form Submission Reconciliation

### 6.2 Findings by Type and Severity

## 7. Agent Skills

### 7.1 Skills Submitted

### 7.2 Demonstration Video Links

## 8. Git Commit Log

## 9. Limitations and Risks

- The production EMS had no separate B3 registration form. Registration was performed directly from B2 after selecting the Student role, so B4 was selected as the third distinct screen.
- Testing the registration control created a real participation record. It was cancelled immediately, returning the account to an unregistered state, but EMS retained a cancelled history entry at 02/08/2026 15:23.
- Network/session failure handling, double-submit protection, draft recovery, multiple-toast stacking, and real-time multi-actor updates require final manual confirmation because exercising them safely needs controlled fault injection or another authenticated actor.
- Automated accessibility checks establish specific violations but do not prove complete WCAG conformance. Subjective layout, terminology, and visual-hierarchy Passed judgments require student review.

## 10. Conclusion

## Appendix A – AI Prompt Log

## Appendix B – AI Audit Report

## Appendix C – AI Critique

## Appendix D – Mandatory AI Disclosure

## Appendix E – Supporting Evidence Index

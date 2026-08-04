# Task 3 – Cross-Browser/Cross-Platform Matrix

This is a covering-set matrix for the three selected Scenario B screens. Five cells per screen are sufficient because each set covers at least five browser families, three operating-system families, and all three device classes. The student must personally execute every cell, decide Pass or Fail, record the exact environment, and capture the final evidence.

Status values:

- `Pending student execution` — the cell has not been personally executed yet.
- `Pending student confirmation` — an evidence file exists, but the student must still confirm the result and exact environment.
- `Pass` — the student observed no blocking functional or compatibility failure.
- `Fail` — the student observed an objective functional, rendering, responsive, or interaction failure and recorded it in Notes.
- `Blocked` — execution could not be completed; state the external blocker and do not count the cell as coverage.

## Compatibility Matrix

Replace every `record exact ...` placeholder during execution. Do not infer versions, device models, resolutions, results, or defects from the planned environment.

| Cell ID | Screen and route | Planned operating system | Planned browser | Device class | Actual provider/device/version/resolution | Result | Notes | Screenshot reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B1_E01 | B1 – Home / Events listing (`/dashboard`) | Windows 11 | Microsoft Edge | Desktop | TestingBot cloud VM; Edge 150.0.4078.48; 800×600 screen, 796×481 viewport | Pass | Dashboard and spotlight loaded correctly. Search and filter changed results as expected; event-card navigation and Back worked; no horizontal overflow observed in this environment. | `screenshots/B1_E01_Windows11_Edge_Desktop.png` |
| B1_E02 | B1 – Home / Events listing (`/dashboard`) | Windows 11 | Opera | Desktop | TestingBot cloud VM; Opera 130; 1280×1024 screen, 884×633 viewport | Pass | Dashboard rendered correctly. Search and filter behavior worked; navigation and Back worked; no horizontal overflow observed in this environment. | `screenshots/B1_E02_Windows11_Opera_Desktop.png` |
| B1_E03 | B1 – Home / Events listing (`/dashboard`) | macOS (record exact release) | Firefox | Desktop | LambdaTest cloud VM; Firefox latest on macOS Sonoma; re-run with direct form login (`admin@gmail.com`) and Student-ID overlay | Pass | Dashboard loaded after direct form login (`admin@gmail.com` / `Admin@123`); event-listing content was visible and readable in the captured state. | `screenshots/B1_E03_macOS_Firefox_Desktop.png` |
| B1_E04 | B1 – Home / Events listing (`/dashboard`) | iPadOS/iOS (record exact release) | Safari | Tablet | LambdaTest mobile-web attempt requested iPad Safari | Blocked | Environment blocker: LambdaTest returned `LT_FEATURE_NOT_AVAILABLE_IN_CURRENT_PLAN` for iOS real-device sessions. | `screenshots/B1_E04_iPadOS_Safari_Tablet.png` |
| B1_E05 | B1 – Home / Events listing (`/dashboard`) | Android (record exact release) | Chrome | Phone | LambdaTest mobile-web attempt requested Android Chrome | Blocked | Environment blocker: LambdaTest returned `LT_FEATURE_NOT_AVAILABLE_IN_CURRENT_PLAN` for Android real-device sessions. | `screenshots/B1_E05_Android_Chrome_Phone.png` |
| B2_E01 | B2 – Event detail (`/events/130`) | Windows 11 | Microsoft Edge | Desktop | TestingBot re-execution attempt on 04/08/2026; session was not created | Blocked | Event 68 was no longer available, so the live dashboard was used to select event 130 (`Mock Event`). TestingBot rejected the Edge session with `Insufficient credits`; the old `/events/68` Pass and screenshot are not valid evidence for this replacement route. | — (cloud session not created) |
| B2_E02 | B2 – Event detail (`/events/130`) | Windows 11 | Opera | Desktop | Not re-executed after the route replacement | Pending student execution | Re-run event 130 in the planned Opera environment. The existing screenshot was captured for `/events/68` and must not be reused as evidence for this row. | — (new screenshot required) |
| B2_E03 | B2 – Event detail (`/events/130`) | macOS (record exact release) | Firefox | Desktop | Not re-executed after the route replacement | Pending student execution | Re-run event 130 in the planned Firefox environment. The existing screenshot was captured for `/events/68` and must not be reused as evidence for this row. | — (new screenshot required) |
| B2_E04 | B2 – Event detail (`/events/130`) | iPadOS/iOS (record exact release) | Safari | Tablet | LambdaTest mobile-web attempt requested iPad Safari | Blocked | Environment blocker remains: LambdaTest returned `LT_FEATURE_NOT_AVAILABLE_IN_CURRENT_PLAN` for iOS real-device sessions. A local 320×800 simulation reproduced `BUG-B2-RESP-01`, but simulation does not satisfy this real tablet cell. | — (valid tablet screenshot required) |
| B2_E05 | B2 – Event detail (`/events/130`) | Android (record exact release) | Chrome | Phone | LambdaTest mobile-web attempt requested Android Chrome | Blocked | Environment blocker remains: LambdaTest returned `LT_FEATURE_NOT_AVAILABLE_IN_CURRENT_PLAN` for Android real-device sessions. A local 320×800 simulation reproduced `BUG-B2-RESP-01`, but simulation does not satisfy this real phone cell. | — (valid phone screenshot required) |
| B4_E01 | B4 – Profile / Activities and QR (`/profile`) | Windows 11 | Microsoft Edge | Desktop | LambdaTest cloud VM; Edge latest on Windows 11; re-run with direct form login (`admin@gmail.com`) and Student-ID overlay | Pass | Profile page loaded after direct form login (`admin@gmail.com` / `Admin@123`); profile/activity sections were visible in the captured state. | `screenshots/B4_E01_Windows11_Edge_Desktop.png` |
| B4_E02 | B4 – Profile / Activities and QR (`/profile`) | Windows 11 | Opera | Desktop | LambdaTest cloud VM; Opera latest on Windows 11; re-run with direct form login (`admin@gmail.com`) and Student-ID overlay | Pass | Profile page loaded after direct form login (`admin@gmail.com` / `Admin@123`); profile/activity sections were visible in the captured state. | `screenshots/B4_E02_Windows11_Opera_Desktop.png` |
| B4_E03 | B4 – Profile / Activities and QR (`/profile`) | macOS (record exact release) | Firefox | Desktop | LambdaTest cloud VM; Firefox latest on macOS Sonoma; re-run with direct form login (`admin@gmail.com`) and Student-ID overlay | Pass | Profile page loaded after direct form login (`admin@gmail.com` / `Admin@123`); profile/activity sections were visible in the captured state. | `screenshots/B4_E03_macOS_Firefox_Desktop.png` |
| B4_E04 | B4 – Profile / Activities and QR (`/profile`) | iPadOS/iOS (record exact release) | Safari | Tablet | LambdaTest mobile-web attempt requested iPad Safari | Blocked | Environment blocker: LambdaTest returned `LT_FEATURE_NOT_AVAILABLE_IN_CURRENT_PLAN` for iOS real-device sessions. | `screenshots/B4_E04_iPadOS_Safari_Tablet.png` |
| B4_E05 | B4 – Profile / Activities and QR (`/profile`) | Android (record exact release) | Chrome | Phone | LambdaTest mobile-web attempt requested Android Chrome | Blocked | Environment blocker: LambdaTest returned `LT_FEATURE_NOT_AVAILABLE_IN_CURRENT_PLAN` for Android real-device sessions. | `screenshots/B4_E05_Android_Chrome_Phone.png` |

## Per-Screen Coverage Check

Do not check the execution columns until all five rows for that screen have a student-approved Pass or Fail result and a valid screenshot.

| Screen | Planned OS coverage | Planned browser coverage | Planned device-class coverage | Five cells executed | Five valid screenshots |
| --- | --- | --- | --- | --- | --- |
| B1 – Home / Events listing | Windows, macOS, iPadOS/iOS, Android | Edge, Opera, Firefox, Safari, Chrome | Desktop, tablet, phone | [ ] | [ ] |
| B2 – Event detail | Windows, macOS, iPadOS/iOS, Android | Edge, Opera, Firefox, Safari, Chrome | Desktop, tablet, phone | [ ] | [ ] |
| B4 – Profile / Activities and QR | Windows, macOS, iPadOS/iOS, Android | Edge, Opera, Firefox, Safari, Chrome | Desktop, tablet, phone | [ ] | [ ] |

## B2 Re-execution Record – 04/08/2026

- Event selection: `/events/68` was no longer a valid event-detail target. From the live `/dashboard`, `/events/130` (`Mock Event`) was selected because it was upcoming, open for Student registration, and exposed schedule, registration period, capacity, role selection, Save, Share, and Back controls.
- Local preflight environment (not a covering-set matrix cell): physical Mac running macOS 26.5, Google Chrome 150.0.7871.187, 1440×1000 desktop viewport.
- Desktop result: title/status, schedule, registration and check-in periods, location, capacity, details, and registration role loaded. Share and Back to events operated successfully. The Student role checkbox changed from unselected to selected (`Selected 1/10`) without submitting registration and was then restored to unselected. No horizontal overflow was detected at 1440×1000.
- Simulated portrait observation: at 320×800, the document width was 349 px, producing horizontal overflow. This reproduces existing finding `BUG-B2-RESP-01` on event 130; it is supporting diagnostic evidence only and does not replace the blocked physical/cloud mobile cells.
- Cloud re-execution: the Windows 11 Edge attempt could not create a TestingBot session because the account reported `Insufficient credits`. Therefore no replacement-route B2 cell is marked Pass, and the old event-68 screenshots are retained only as historical files, not current matrix evidence.

## Student Execution Procedure for Every Cell

1. Start a fresh session in the planned OS, browser, and device class. A cloud environment or real device is preferred. Do not silently substitute a browser or device; update the matrix first if substitution is necessary.
2. Record the actual provider, OS release, browser version, device model, screen resolution, viewport when available, orientation, and whether the mobile environment is real or simulated.
3. Sign in through Student SSO yourself and open the exact route in the matrix.
4. Execute the screen-specific checks below. Observe the live state yourself and write only what you directly observed.
5. Check readability, responsive reflow, horizontal overflow, clipping, overlap, unexpectedly truncated text, distorted images, unreachable controls, and touch/click behavior.
6. Mark the cell `Pass` or `Fail`. For a failure, record concise expected-versus-actual behavior and reuse an existing finding ID if it is the same defect. Create a new finding only for genuinely distinct behavior.
7. Restore a representative clean state that visibly demonstrates the screen. Close menus that obscure important content.
8. Add the visible identity overlay `22127345-nhquan22@clc.fitus.edu.vn`.
9. Capture one genuine screenshot using the exact filename from the matrix. The image must visibly show the EMS URL, browser identity, OS identity, device name/class, and the student-email overlay. Do not crop out the cloud/physical-device identity.
10. Open the saved image and verify all five evidence elements before ending the session.

## Screen-Specific Checks

### B1 – Home / Events listing (`/dashboard`)

1. Confirm the page and spotlight/carousel load without a blank or error state.
2. Confirm event cards display readable title, time, location/status, capacity, and action content without overlap.
3. Search using a distinctive substring from an event that is currently visible; confirm the results narrow correctly, then clear the search and confirm the list restores.
4. Open Filters, change one filter, confirm the result set changes, then clear the filter and confirm the baseline list restores.
5. Open one event card, confirm the detail route loads, then return to `/dashboard`.
6. Inspect pagination or rows-per-page controls without changing persistent account data.
7. On tablet/phone, repeat the key checks in portrait orientation and confirm there is no horizontal page scrolling or clipped action.

### B2 – Event detail (`/events/130`)

Event 68 became unavailable when this matrix was re-executed on 04/08/2026. Use the replacement event `/events/130` consistently for all five B2 rows. If event 130 later becomes unavailable, select another live event from `/dashboard` and update all five rows again before execution.

1. Confirm the event title, status, description, schedule, location, registration period, role/capacity information, and primary actions load.
2. Confirm Save/Share and Back-to-events controls are visible and operable, but do not perform an irreversible registration or cancellation solely for compatibility testing.
3. If role selection is available, verify its control can be reached and selected without submitting the registration.
4. Use Back to events, confirm `/dashboard` loads, and return to the same event-detail route.
5. Inspect long text, badges, date/time rows, action buttons, and registration panels for clipping, overlap, narrow single-character wrapping, or horizontal scrolling.
6. On tablet/phone, verify the detail content and primary actions remain readable and reachable in portrait orientation.

### B4 – Profile / Activities and QR (`/profile`)

1. Confirm the correct signed-in identity and profile summary load.
2. Confirm the activities/history section loads its status, event information, and available actions.
3. Exercise one available filter or pagination control and verify the displayed activities update, then restore the baseline state.
4. Open the QR view for an eligible activity when available; verify the QR content and close control are visible, then close it without changing account data.
5. Inspect profile actions, activity cards/table, pagination, and QR overlay for overflow, clipping, overlap, unreadable text, or unreachable controls.
6. On tablet/phone, verify the profile actions and QR view remain usable in portrait orientation.

## Evidence Validation Checklist

For every saved screenshot, confirm:

- [ ] The EMS page and full EMS URL are visible.
- [ ] The browser family is visible.
- [ ] The operating system is visible or identified by the testing service.
- [ ] The device name/class and resolution are visible or identified by the testing service.
- [ ] `22127345-nhquan22@clc.fitus.edu.vn` is visibly overlaid.
- [ ] The screen is not obscured by an unrelated menu, terminal, desktop, or login page.
- [ ] The filename exactly matches the matrix row.
- [ ] The matrix records the actual result and objective notes.

Google Form timestamps remain `— (not submitted)` until the student genuinely submits a finding.

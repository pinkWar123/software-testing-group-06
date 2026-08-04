# Cross-Platform Compatibility Matrix — Scenario C (Admin manages users)

**Dimensions:** 3 OS (Windows, macOS, Android) × 5 Browsers (Chrome, Safari, Firefox, Edge, Samsung Internet) × 3 Device Classes (Desktop, Tablet, Mobile) = 45 combinations.

**Screens exercised per tested combination:** C1 (Users List), C2 (Edit User), C4 (Excel Export).

**Legend**
- `Pass` — all exercised screens rendered/functioned correctly on this combination.
- `Fail` — at least one exercised screen showed a functional or rendering defect (see Findings below).
- `N/A¹` — Not Applicable: this OS/Device/Browser combination does not exist in the real world (e.g., Safari on Windows, Apple tablets run iPadOS not macOS).
- `N/A²` — Not Tested: a valid, real-world combination, but no screenshot evidence was provided for it yet.

---

## Desktop

| OS \ Browser | Chrome | Safari | Firefox | Edge | Samsung Internet |
|---|---|---|---|---|---|
| Windows | **Fail** (see Finding 1) | N/A¹ (Safari discontinued on Windows) | N/A² | N/A² | N/A¹ (not available on Windows) |
| macOS | N/A² | **Fail** (see Finding 1 & 2) | N/A² | N/A² | N/A¹ (not available on macOS) |
| Android | N/A¹ (Android is not a desktop OS) | N/A¹ | N/A¹ | N/A¹ | N/A¹ |

## Tablet

| OS \ Browser | Chrome | Safari | Firefox | Edge | Samsung Internet |
|---|---|---|---|---|---|
| Windows | N/A² | N/A¹ (Safari discontinued on Windows) | N/A² | N/A² | N/A¹ (not available on Windows) |
| macOS | N/A¹ (Apple tablets run iPadOS, not macOS) | N/A¹ | N/A¹ | N/A¹ | N/A¹ |
| Android | N/A² | N/A¹ (Safari not available on Android) | N/A² | N/A² | N/A² |

## Mobile

| OS \ Browser | Chrome | Safari | Firefox | Edge | Samsung Internet |
|---|---|---|---|---|---|
| Windows | N/A¹ (Windows Phone discontinued) | N/A¹ | N/A¹ | N/A¹ | N/A¹ |
| macOS | N/A¹ (Apple phones run iOS, not macOS) | N/A¹ | N/A¹ | N/A¹ | N/A¹ |
| Android | **Fail** (see Finding 1) | N/A¹ (Safari not available on Android) | N/A² | N/A² | N/A² |

---

## Dimension coverage check

| Dimension | Exercised with real evidence | Not yet exercised |
|---|---|---|
| OS (3) | Windows, macOS, Android — **all 3 ✓** | — |
| Browser (5) | Chrome, Safari — **2 of 5** | Firefox, Edge, Samsung Internet |
| Device Class (3) | Desktop, Mobile — **2 of 3** | Tablet |

The requirement "every OS, browser, and device class exercised at least once" is **not yet fully met** — only Chrome and Safari, and only Desktop/Mobile, have screenshot evidence. See **Recommended next tests** below for the minimal additions needed.

---

## Findings (from provided screenshots)

### Finding 1 — Edit User form loads wrong value into First Name (Fail — reproduced on all 3 tested platforms)
On C2 ("Edit User" dialog) for the account "Pham" (email `pvnduy23@clc.fitus.edu.vn`), the **First Name** field is populated with `23127183@student.hcmus...` — an email/ID-like string — instead of an actual first name, while **Last Name** correctly shows "Pham". Identical on:
- Windows 11 / Chrome 152 — `screenshots/desktop + windows + chrome/C2.png`
- macOS (Golden Gate) / Safari 27.0 — `screenshots/desktop + mac + safari/C2.png`
- Android / Chrome (mobile) — `screenshots/phone + android + chrome/C2.png`

Because it reproduces identically across OS/browser/device, this is an **application data-loading bug, not a platform-compatibility issue** — but it fails every combination where C2 was exercised. This is the same class of defect as the First/Last Name field-population issue found earlier in Task 1B's C2 review, though this specific manifestation replaces First Name with an unrelated ID/email value rather than merely swapping the two names. Recommend prioritizing a fix to the Edit User form's field-mapping logic, since a Save in this state would overwrite the user's real first name with an email string.

### Finding 2 — macOS/Safari C4 shows no visible export confirmation and missing header icons (N/A — inconclusive, needs re-test)
`screenshots/desktop + mac + safari/C4.png` (captured on a different Safari build — 26.4 "Tahoe" — than the other two macOS screenshots) shows the Users List with **no download toast/confirmation visible**, unlike the clear confirmations captured on Windows Chrome and Android Chrome for the same action. The app header's language-flag and grid-menu icons (visible in the other two macOS screenshots) also don't appear in this capture. It's unclear whether this is a genuine rendering regression on Safari 26.4, a timing issue (Safari's native download indicator is transient and may have already dismissed), or the icons being obscured by Safari's own toolbar at this window size. **[REQUIRES HUMAN VERIFICATION — re-capture immediately after clicking Export on Safari.]**

### Note — non-app annotation excluded from findings
Every screenshot shows red text (e.g., `23127102@student.hcmus.edu.vn`) floating above the browser chrome. This sits outside the actual page content in all 9 images and is a capture/session annotation (likely from the BrowserStack tool), not part of the EMS application UI — excluded from the results above.

### Otherwise passing
C1 (Users List) rendered correctly with matching data across all three tested platforms, including a sensible responsive collapse on Android Mobile (columns reduce to User + Actions, Export/Add User stack full-width, sidebar collapses to a hamburger menu). C4 on Windows and Android both showed clear, working download confirmations.

---

## Recommended next tests (minimal set to satisfy full dimension coverage)

1. **Windows + Tablet + Firefox** — covers both Firefox and Tablet in one test.
2. **Android + Tablet + Samsung Internet** — covers Samsung Internet.
3. **macOS + Desktop + Edge** (or Windows + Desktop + Edge) — covers Edge.

Running these three would bring every OS, every browser, and every device class up to at least one real, evidenced test.

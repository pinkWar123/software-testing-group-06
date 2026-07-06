---
name: domain-bva-testing
description: Apply Domain Testing (Equivalence Partitioning) and Boundary Value Analysis (BVA) to design a thorough yet minimal set of black-box test cases for any feature, form, or input field. Use this skill whenever the user asks to design test cases, test an input/field/form, apply domain testing, equivalence partitioning, or boundary value analysis, or wants to systematically find input-validation bugs — even if they do not name the technique explicitly.
---

# Domain Testing & Boundary Value Analysis

## Overview

This skill guides the disciplined, step-by-step application of two classic black-box
test-design techniques. It must NOT be used as a single generic "generate test cases"
prompt — the value (and the grade) is in showing the analysis at every step, not just
producing a final table.

- **Domain Testing / Equivalence Partitioning (EP):** divide each input's possible
  values into classes that the system is expected to treat the same way, then test one
  representative value per class. This shrinks an infinite input space to a small,
  well-justified set.
- **Boundary Value Analysis (BVA):** test the values right at, and immediately beside,
  the edges of every valid range — this is where off-by-one bugs (`<` vs `<=`) hide.

The two are complementary: EP tells you *which regions* to test; BVA tells you where the
*edges of those regions* are and probes them closely.

## Workflow

Always produce the six sections below, in order. Show the reasoning, not only the result.

### Step 1 — Understand the feature and list every input

Read the feature specification (and, if available, exercise it in the live application).
Then build an **input inventory**. For each input, record:

- Input name and UI location.
- Data type (integer, decimal, string, date, enum/dropdown, boolean, file, etc.).
- The stated valid domain / constraints (min, max, length, format, allowed set).
- Any dependency on other inputs or on system state (e.g. "quantity <= stock on hand").

If a constraint is not stated in the spec, note the assumption explicitly and flag it as
something to confirm against the running system.

### Step 2 — Equivalence Partitioning (the "domain" step)

For each input, split its values into classes. Cover **all** of these categories:

1. **Valid classes** — values the system should accept. Split further if the system is
   expected to behave differently inside the valid range.
2. **Invalid classes** — one class per *distinct reason* for rejection, e.g.:
   below the minimum, above the maximum, wrong type, wrong format,
   empty / null / whitespace only, out of the allowed set.
3. **Special / adversarial values** where relevant — very large numbers, leading zeros,
   Unicode, emoji, trailing/leading spaces, and injection-style strings
   (e.g. `' OR 1=1 --`, `<script>`) to check input handling and escaping.

Present this as an **equivalence class table**:

| EC-ID | Input | Class type (Valid/Invalid) | Description of class | Representative value |
|-------|-------|----------------------------|----------------------|----------------------|

**Design rule (one-invalid-at-a-time):** when a test targets a specific *invalid* class,
keep every *other* input valid, so you can tell which input caused the rejection.

### Step 3 — Boundary Value Analysis

For every input with an ordered range, generate values around each boundary. State the
variant used:

- **2-value BVA:** boundary and one step outside — `{min-1, min}` and `{max, max+1}`.
- **3-value BVA (recommended for grading):** `{min-1, min, min+1}` and `{max-1, max, max+1}`.

Boundaries are not only numeric — apply the same idea to string length (empty, 1, max-1,
max, max+1), dates (day before/on/after the valid edge; leap years, month ends), and
collection size (0, 1, max, max+1 items).

| BV-ID | Input | Boundary | Value tested | On which side | Expected result |
|-------|-------|----------|--------------|---------------|-----------------|

### Step 4 — Assemble concrete test cases

Merge EP representatives and BVA values into runnable cases; drop exact duplicates (note
where one value serves both techniques). Each case:

| TC-ID | Technique (EP/BVA) | Title | Precondition | Test data / steps | Expected result | Actual result | Status |
|-------|--------------------|-------|--------------|-------------------|-----------------|---------------|--------|

### Step 5 — Execute and record

Run each test case; fill Actual result and Status. If the spec is silent on the expected
result, state the most reasonable expectation and mark it as an assumption to verify.

### Step 6 — Bug reporting

For every Fail, write: title, severity, preconditions, exact reproduction steps,
expected vs actual, and a screenshot placeholder. One bug = one distinct defect.

| BUG-ID | Title | Severity | Steps to reproduce | Expected | Actual | Linked TC-ID |
|--------|-------|----------|--------------------|---------|--------|--------------|

## Output expectations

- Show every intermediate table (input inventory, EC table, BV table) — do not collapse
  the reasoning into only the final test-case list.
- State assumptions explicitly wherever the specification is incomplete.
- Prefer thoroughness: over-generate candidate classes and boundaries, then justify any
  you decide to drop.

## Worked mini-example (cart quantity field)

Spec: integer quantity, valid range 1 to stock (assume stock = 50).

*Equivalence classes:* Valid `1..50`; Invalid-below `<= 0`; Invalid-above `> 50`;
Wrong-type `"abc"`, `1.5`; Empty `""`.

*Boundaries (3-value):* lower `0, 1, 2`; upper `49, 50, 51`.

Note `1` and `50` serve as both valid-class representatives and boundary values — list
them once and flag that they cover both techniques.

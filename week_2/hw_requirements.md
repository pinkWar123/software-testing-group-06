# HW02 — Domain Testing on EShop
## Requirements Checklist

> **Submission filename:** `<StudentID>_HW02_AI_DomainTesting_<grade>.zip`
> **Total points:** 100

---

## 🗂️ Feature Selection

- [x] Feature A — Pool A: **FR-02: Login and account lockout** **(25 pts)**
- [x] Feature B — Pool B: **FR-07: Shopping cart** **(25 pts)**
- [x] Feature C — Pool C: **FR-17: Coupon management (CRUD)** **(25 pts)**
- [x] Feature D — Pool D: **Mobile App — general feature** **(15 pts)**

> ⚠️ Coordinate with group members — no duplicate features allowed.

---

## 📋 Per-Feature Deliverables (repeat for each of 4 features)

### Feature A — FR-02: Login and Account Lockout
- [ ] Domain Testing: identify variables, ranges, in/off/on points, equivalence classes
- [ ] Domain Testing: step-by-step explanation of technique application
- [ ] Domain Testing: comprehensive test cases in ISTQB format
- [ ] BVA: identify boundary variables and boundary values
- [ ] BVA: step-by-step explanation of technique application
- [ ] BVA: comprehensive test cases in ISTQB format
- [ ] AI Gap Analysis: list missed test cases/bugs + explain why AI missed them
- [ ] Bug Report: logged in `report/report.md` with screenshots
- [ ] Bug Report: GitHub Issues opened with screenshots attached

### Feature B — FR-07: Shopping Cart
- [ ] Domain Testing: step-by-step + test cases (ISTQB format)
- [ ] BVA: step-by-step + test cases (ISTQB format)
- [ ] AI Gap Analysis: missed cases + why
- [ ] Bug Report: Markdown + GitHub Issues with screenshots

### Feature C — FR-17: Coupon Management (CRUD)
- [ ] Domain Testing: step-by-step + test cases (ISTQB format)
- [ ] BVA: step-by-step + test cases (ISTQB format)
- [ ] AI Gap Analysis: missed cases + why
- [ ] Bug Report: Markdown + GitHub Issues with screenshots

### Feature D — Mobile App
- [ ] Domain Testing: step-by-step + test cases (ISTQB format)
- [ ] BVA: step-by-step + test cases (ISTQB format)
- [ ] AI Gap Analysis: missed cases + why
- [ ] Bug Report: Markdown + GitHub Issues with screenshots

---

## 🤖 Agent Skills **(10 pts)**

- [ ] Domain Testing SKILL.md — reusable, works on any feature
- [ ] BVA SKILL.md — reusable, works on any feature
- [ ] Demo video (YouTube) for Domain Testing skill — end-to-end on a complete feature
- [ ] Demo video (YouTube) for BVA skill — end-to-end on a complete feature
- [ ] Video links added to README.md

---

## 📜 Git Commit Log

- [ ] One commit per testing step per feature (ongoing throughout work)
- [ ] Export commit log: `report/git_log.txt`

---

## 🔒 AI Compliance (mandatory — missing any = 0 for entire AI column)

- [ ] AI Audit Report — one 5-section entry per AI-generated artifact (`ai_compliance/audit_report.md`)
- [ ] Prompt Log — every real prompt logged with timestamp (`report/appendix_A_prompt_log.md`)
- [ ] AI Critique — 200–300 words, cover: errors, bias, why AI failed, principle learned (`ai_compliance/ai_critique.md`)
- [ ] Mandatory Disclosure paragraph — in main report before appendices
- [ ] AI-03 Disclosure Form — signed (from AI Templates/)
- [ ] AI-05 Privacy Checklist — signed (from AI Templates/)

---

## 📦 Submission Contents

- [ ] `report/report.md` + `report/report.pdf` — Domain Testing + BVA + Bug reports for all 4 features
- [ ] `ai_compliance/audit_report.md` + PDF
- [ ] `ai_compliance/ai_critique.md` (or included in report)
- [ ] `report/appendix_A_prompt_log.md`
- [ ] `report/git_log.txt`
- [ ] `README.md` — self-assessment table + test summary report + video links
- [ ] Bug screenshots in `artifacts/screenshots/`
- [ ] Agent skill files
- [ ] ZIP packaged with correct filename format

---

## 📊 What AI Can Help With vs Must Do Manually

| AI Can Help With | Must Do Manually |
|---|---|
| Generating domain analysis (variables, ranges, classes) | Verify test cases against actual SUT behaviour |
| Drafting test cases in ISTQB format | Execute all test cases against the running app |
| Identifying boundary values | Capture bug screenshots |
| Writing gap analysis explanations | Record demo videos (your voice) |
| Drafting report sections | Export and review git commit log |
| AI Audit Report entries | Sign AI-03 and AI-05 forms |
| AI Critique draft | Coordinate feature selection with group |

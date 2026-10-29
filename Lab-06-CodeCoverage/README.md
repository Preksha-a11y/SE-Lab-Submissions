# Lab 6: Code and Branch Coverage Analysis

**Assigned Repository:** `L6_L7_21_gym_membership`  
**Student Profile:** `Preksha-a11y`  
**Module Under Test:** `gym_membership.py`  

---

## 1. Overview
This laboratory assignment evaluates and optimizes test completeness on `gym_membership.py` using Python's `coverage` and `pytest` frameworks. Test cases were written to systematically cover edge cases, decision branches, and conditional statements without modifying the source application.

---

## 2. Deliverables & File Mapping

| File | Description |
|------|-------------|
| `gym_membership.py` | Original module under test (kept intact) |
| `test_gym_membership.py` | Original starter test file |
| `CodeCoverageTest_gym_membership.py` | Comprehensive test suite for **Line Coverage (100%)** |
| `BranchCoverageTest_gym_membership.py` | Targeted test suite for **Branch Coverage (100%)** |
| `code_coverage_report.txt` | Terminal output text report for Code Coverage |
| `branch_coverage_report.txt` | Terminal output text report for Branch Coverage |
| `screenshots/code_coverage_terminal.png` | Terminal screenshot for Code Coverage analysis |
| `screenshots/branch_coverage_terminal.png` | Terminal screenshot for Branch Coverage analysis |

---

## 3. Coverage Analysis Summary

### Baseline (Initial Starter Tests)
- **Line Coverage:** 43% (Missed 20/35 statements)
- **Branch Coverage:** 38% (Covered only 8/26 branches)

### Final Results

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| **Line / Code Coverage** | $\ge 90\%$ | **100%** (35/35 statements) | **PASSED** |
| **Branch Coverage** | $\ge 90\%$ | **100%** (26/26 branches, 0 partial) | **PASSED** |
| **Test Pass Rate** | 100% | **32 / 32 Passed** | **PASSED** |

---

## 4. Commands to Reproduce

### Run Line Coverage:
```bash
coverage run -m pytest CodeCoverageTest_gym_membership.py
coverage report -m
```

### Run Branch Coverage:
```bash
coverage run --branch -m pytest BranchCoverageTest_gym_membership.py
coverage report -m
```

---

## 5. Commit History (Rubric Compliance)
1. **Commit 1:** `feat(coverage): add CodeCoverageTest_gym_membership achieving 100% line coverage`
2. **Commit 2:** `feat(branch-coverage): add BranchCoverageTest_gym_membership achieving 100% branch coverage & complete documentation`

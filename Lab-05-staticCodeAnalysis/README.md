# Lab 5: Static Code Analysis — Wildlife Sanctuary Sightings

Static code analysis and refactoring performed on the Wildlife Sanctuary Sightings logging system (`wildlife_sightings.py`) using **Bandit**, **Flake8**, and **Pylint**.

---

## Overview

The `wildlife_sightings.py` application records species sightings across sanctuary zones, generates zone summaries, and determines the rarest observed species using SQLite. 

The original codebase had critical security vulnerabilities (SQL injection, unsafe hash digests), functional bugs (mutable default arguments), PEP 8 formatting defects, and code maintainability issues. Using static code analysis tools, the codebase was audited, refactored, and verified to achieve zero security warnings, strict PEP 8 compliance, and a **perfect 10.00/10 Pylint score**.

---

## Tools Used

- **Bandit (`v1.9.0+`)**: Security linter scanning for vulnerabilities (CWEs, SQL injection, insecure cryptography).
- **Flake8 (`v7.3.0+`)**: Style guide enforcer checking PEP 8 compliance, naming readability, and formatting.
- **Pylint (`v4.0.0+`)**: Semantic code analysis evaluating design smells, variable shadowing, documentation, and overall code quality.

---

## Static Analysis Results Summary

| Tool | Before Refactor | After Refactor | Status |
|------|-----------------|----------------|--------|
| **Bandit** | 3 issues (1 High, 1 Medium, 1 Low) | **0 issues** | ✅ Clean |
| **Flake8** | 6 PEP 8 style violations | **0 violations** | ✅ Clean |
| **Pylint** | **1.25 / 10** | **10.00 / 10** | ✅ Clean (Perfect Score) |

---

## Key Fixes Implemented

1. **SQL Injection (`B608` - Bandit):** Converted dynamic SQL query string formatting to parameterized queries with placeholder tuples (`?`), preventing SQL injection attacks.
2. **Weak Cryptographic Hash (`B324` - Bandit):** Explicitly passed `usedforsecurity=False` to `hashlib.md5()` to clarify that hashing is used purely for observer identification, not cryptographic security.
3. **Dangerous Mutable Default Argument (`W0102` - Pylint):** Replaced default mutable dictionary (`extras={}`) with `extras=None` and initialized dynamically inside the function, eliminating cross-call state pollution.
4. **Assert in Production Code (`B101` - Bandit):** Replaced `assert len(totals) == 3` with defensive programming (`raise ValueError(...)`) ensuring validation is preserved even in optimized execution modes (`-O`).
5. **Global Scope Variable Shadowing (`W0621` - Pylint):** Eliminated the global `conn` variable; created an explicit `init_db()` database initialization routine called within `main()`.
6. **Ambiguous Variable Names & Formatting (`E741`, `E225`, `E501` - Flake8):** Renamed ambiguous variable `l` to `rarest_row`, added appropriate spacing around operators, and split long lines to satisfy PEP 8 limits.
7. **Documentation & Naming Standards (`C0114`, `C0116`, `C0103` - Pylint):** Added comprehensive PEP 257 docstrings to all functions and converted function names to standard Python `snake_case` (while maintaining backwards-compatible aliases).

---

## Project Structure & Deliverables

```text
Lab-05-staticCodeAnalysis/
├── README.md                      # Project documentation and summary
├── wildlife_sightings.py          # Cleaned and refactored Python source code
├── issues.md                      # Comprehensive table of identified issues and resolution approaches
├── reflection.md                  # Conceptual reflections on static analysis and security
├── SE_Lab05_deliverables.pdf      # Compiled lab report and deliverables
├── bandit_report_before.txt       # Initial Bandit security scan report
├── bandit_report_after.txt        # Post-fix Bandit security scan report (0 issues)
├── flake8_report_before.txt       # Initial Flake8 style report
├── flake8_report_after.txt        # Post-fix Flake8 style report (0 errors)
├── pylint_report_before.txt       # Initial Pylint report (1.25/10)
└── pylint_report_after.txt        # Post-fix Pylint report (10.00/10)
```

---

## How to Run & Verify

1. **Execute the Application:**
   ```bash
   python wildlife_sightings.py
   ```

2. **Run Static Code Analysis Tools:**
   ```bash
   bandit -r wildlife_sightings.py
   flake8 wildlife_sightings.py
   pylint wildlife_sightings.py
   ```

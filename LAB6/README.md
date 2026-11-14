# L6_L7_57 — Income Tax Calculator

Lab 6: Code and Branch Coverage

## About

A small Python module that works out taxable income under two tax regimes, calculates the tax due by age group and reports whether a refund or balance is owed.

## Files

| File | Description |
|------|-------------|
| `income_tax.py` | The module under test |
| `test_income_tax.py` | Starter test file |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.

## Submission: PES2UG24AM142, Sai Nikitha Perumalla

| File | Contents |
|------|----------|
| `CodeCoverageTest_PES2UG24AM142_income_tax.py` | 14 tests: 100% line coverage (branch 99%, arc 7->9 untaken) |
| `BranchCoverageTest_PES2UG24AM142_income_tax.py` | 32 tests: 100% line and 100% branch coverage |
| `screenshots/code_coverage.png` | Terminal output of line and branch coverage runs for the code coverage tests |
| `screenshots/branch_coverage.png` | Terminal output of line and branch coverage runs for the branch coverage tests |
| `PES2UG24AM142_SaiNikitha_LAB6.pdf` | Lab report: baseline (38% line / 33% branch), analysis, test design, screenshots |

Run from this folder:

```
pip install coverage pytest
coverage run -m pytest CodeCoverageTest_PES2UG24AM142_income_tax.py && coverage report -m
coverage run --branch -m pytest BranchCoverageTest_PES2UG24AM142_income_tax.py && coverage report -m
```

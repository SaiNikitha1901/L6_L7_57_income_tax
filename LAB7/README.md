# L6_L7_57 — Income Tax Calculator

Lab 7: Fuzzing for Input Validation Bugs

## About

A small Python module that reads income tax calculator details typed in by a user: PAN numbers, rupee amounts and tax slabs. It assumes every input is well formed.

## Files

| File | Description |
|------|-------------|
| `income_tax_parser.py` | The buggy module you will fuzz and fix |
| `test_income_tax_parser.py` | Hypothesis test template to complete |

Keep all your Lab 7 work in this `LAB7` folder.

Follow the lab handout for the full instructions. Use the file names above wherever the handout refers to the code and test files.

## Screenshots

| Screenshot | What it must show |
|------------|-------------------|
| SS1 | `python income_tax_parser.py` run on the buggy module |
| SS2 | `pytest test_income_tax_parser.py` with your completed tests failing on the buggy module |
| SS3 | `python income_tax_parser.py` run on your fixed module |
| SS4 | `pytest test_income_tax_parser.py` with all tests passing on your fixed module |

## Deliverables

Commit these three files in this `LAB7` folder:

1. `income_tax_parser.py`: your fixed module. All three functions must handle any input without crashing.
2. `test_income_tax_parser.py`: your completed Hypothesis tests, one for each of the three functions.
3. `SRN_NAME_LAB7.pdf`: screenshots SS1 to SS4 and your answers to the three reflection questions in the handout.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

## Submission: PES2UG24AM142, Sai Nikitha Perumalla

| File | Contents |
|------|----------|
| `income_tax_parser.py` | Fixed module: all three functions accept any input and return `None` for invalid input instead of crashing |
| `test_income_tax_parser.py` | Hypothesis tests (`st.text() \| st.none()`, 500 examples each): no crash + valid result property |
| `PES2UG24AM142_SaiNikitha_LAB7.pdf` | SS1 to SS4, bug list with fixes, reflection |
| `screenshots/` | `ss1_buggy_run`, `ss2_tests_fail_*` (buggy module), `ss3_fixed_run`, `ss4_tests_pass` (fixed module) |

Result: 3 failed (7 distinct Hypothesis failures) on the original module, 3 passed on the fixed module.

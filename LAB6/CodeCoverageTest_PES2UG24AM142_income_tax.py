"""Lab 6 - code (line) coverage tests for income_tax.py.

SRN: PES2UG24AM142 | Name: Sai Nikitha Perumalla

Goal: execute every statement of income_tax.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_PES2UG24AM142_income_tax.py
    coverage report -m
"""
import pytest
from income_tax import taxable_income, tax_due, refund_status


# ---------- taxable_income ----------

def test_new_regime():
    # starter test: flat 75,000 standard deduction
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_gross_raises():
    # line 3: invalid income
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_old_regime_investments_capped():
    # lines 6-9: 80C investments above 1.5 lakh are capped at 1.5 lakh
    # 1000000 - (50000 + 150000) = 800000
    assert taxable_income(1000000, "old", 200000) == 800000


def test_unknown_regime_raises():
    # lines 10-11: anything other than "new"/"old" is rejected
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(1000000, "flat", 0)


def test_deduction_larger_than_income_returns_zero():
    # line 14: taxable income never goes negative
    assert taxable_income(50000, "new", 0) == 0


# ---------- tax_due ----------

def test_below_exemption():
    # starter test
    assert tax_due(200000, 30) == 0


def test_negative_taxable_raises():
    # line 20: invalid amount
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-100, 30)


def test_super_senior_first_slab():
    # line 22 + line 31: age 80+ exempt 5,00,000; slab 1,00,000 at 5%
    assert tax_due(600000, 85) == 5000


def test_senior_second_slab():
    # line 24 + line 32: age 60-79 exempt 3,00,000; slab 4,00,000
    # 12500 + (400000 - 250000) * 20% = 42500
    assert tax_due(700000, 65) == 42500


# ---------- refund_status ----------

def test_refund_on_time():
    assert refund_status(50000, 40000, True) == "refund"


def test_refund_delayed():
    assert refund_status(50000, 40000, False) == "refund delayed"


def test_pay_balance_on_time():
    assert refund_status(30000, 40000, True) == "pay balance"


def test_pay_balance_with_penalty():
    assert refund_status(30000, 40000, False) == "pay balance with penalty"


def test_settled():
    assert refund_status(40000, 40000, True) == "settled"

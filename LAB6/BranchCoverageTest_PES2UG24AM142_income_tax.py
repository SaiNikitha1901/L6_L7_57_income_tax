"""Lab 6 - branch coverage tests for income_tax.py.

SRN: PES2UG24AM142 | Name: Sai Nikitha Perumalla

Goal: make every decision in income_tax.py evaluate both True and False.
The line-coverage suite reached 100% lines but left branch 7->9 untaken
(old regime with investments <= 1,50,000 never skipped the cap). This file
keeps all of those tests and adds the missing branch plus the boundary
values where each comparison flips.
Run:
    coverage run --branch -m pytest BranchCoverageTest_PES2UG24AM142_income_tax.py
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


# ---------- added for branch coverage ----------

def test_old_regime_investments_below_cap():
    # branch 7->9: investments <= 1,50,000 are used as-is (cap skipped)
    # 1000000 - (50000 + 100000) = 850000
    assert taxable_income(1000000, "old", 100000) == 850000


def test_old_regime_investments_exactly_at_cap():
    # boundary of line 7: 150000 is not > 150000, so no capping
    assert taxable_income(1000000, "old", 150000) == 800000


def test_old_regime_deduction_exceeds_income():
    # line 13 True via the old regime
    assert taxable_income(100000, "old", 100000) == 0


def test_zero_gross_is_valid():
    # boundary of line 2: 0 is not < 0, so no error
    assert taxable_income(0, "new", 0) == 0


def test_taxable_equal_to_deduction_returns_zero():
    # boundary of line 13: taxable == 0 is not < 0, returns 0 via line 15
    assert taxable_income(75000, "new", 0) == 0


def test_age_exactly_80_is_super_senior():
    # boundary of line 21
    assert tax_due(500000, 80) == 0


def test_age_79_is_senior():
    # line 21 False, line 23 True just below the 80 boundary
    assert tax_due(500000, 79) == 10000


def test_age_exactly_60_is_senior():
    # boundary of line 23
    assert tax_due(300000, 60) == 0


def test_age_59_is_regular():
    # line 23 False just below the 60 boundary
    assert tax_due(300000, 59) == 2500


def test_taxable_exactly_at_exemption():
    # boundary of line 27: taxable == exempt -> no tax
    assert tax_due(250000, 30) == 0


def test_zero_taxable():
    # boundary of line 19: 0 is a valid amount
    assert tax_due(0, 30) == 0


def test_slab_exactly_250000():
    # boundary of line 30: slab == 2,50,000 stays in the 5% slab
    assert tax_due(500000, 30) == 12500


def test_slab_just_above_250000():
    # line 30 False by the smallest step: 12500 + 1 * 20 // 100 = 12500
    assert tax_due(500001, 30) == 12500


def test_regular_age_high_income():
    # line 32 for a regular taxpayer: slab 7,50,000
    # 12500 + 500000 * 20% = 112500
    assert tax_due(1000000, 30) == 112500


def test_settled_even_when_late():
    # difference == 0 ignores filed_on_time
    assert refund_status(40000, 40000, False) == "settled"


def test_refund_by_one_rupee():
    # smallest positive difference
    assert refund_status(40001, 40000, True) == "refund"


def test_balance_by_one_rupee():
    # smallest negative difference
    assert refund_status(39999, 40000, False) == "pay balance with penalty"


def test_end_to_end_new_regime():
    # all three functions chained: 12 lakh gross, new regime, age 40
    taxable = taxable_income(1200000, "new", 0)
    due = tax_due(taxable, 40)
    assert taxable == 1125000
    assert due == 12500 + (1125000 - 250000 - 250000) * 20 // 100
    assert refund_status(due, due, True) == "settled"

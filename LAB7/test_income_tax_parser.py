"""Lab 7 - Hypothesis fuzz tests for income_tax_parser.py.

SRN: PES2UG24AM142 | Name: Sai Nikitha Perumalla

Each test feeds random Unicode text (and None) to one parser function.
Property 1 (from the handout): the function must never raise.
Property 2: whatever it returns must be a sensible value, or None for
input it rejects.

Run:  pytest test_income_tax_parser.py
"""
import re

from hypothesis import given, settings, strategies as st
from income_tax_parser import clean_pan, parse_amount, parse_tax_slab

PAN_RE = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")


@settings(max_examples=500)
@given(st.text() | st.none())
def test_clean_pan_no_crash(s):
    try:
        result = clean_pan(s)
    except Exception as e:
        assert False, f"clean_pan crashed with: {type(e).__name__}: {e}"
    # A cleaned PAN is 5 letters, 4 digits, 1 letter; invalid input -> None
    assert result is None or PAN_RE.fullmatch(result), \
        f"clean_pan returned an invalid PAN: {result!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_amount_no_crash(s):
    try:
        result = parse_amount(s)
    except Exception as e:
        assert False, f"parse_amount crashed with: {type(e).__name__}: {e}"
    # A rupee amount is a whole number that is not negative
    assert result is None or (isinstance(result, int) and result >= 0), \
        f"parse_amount returned an invalid amount: {result!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_tax_slab_no_crash(s):
    try:
        result = parse_tax_slab(s)
    except Exception as e:
        assert False, f"parse_tax_slab crashed with: {type(e).__name__}: {e}"
    # A slab is (low, high, rate) with 0 <= low <= high and 0 <= rate <= 100
    if result is not None:
        low, high, rate = result
        assert 0 <= low <= high, f"bad slab limits: {result!r}"
        assert 0 <= rate <= 100, f"bad slab rate: {result!r}"

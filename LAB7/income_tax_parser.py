"""Income tax calculator input parsers (fixed for Lab 7).

SRN: PES2UG24AM142 | Name: Sai Nikitha Perumalla

Every function accepts ANY input and never raises. Input that is not
well formed returns None so the caller can ask the user again.
"""
import re

# PAN: 5 letters, 4 digits, 1 letter (ASCII only), e.g. ABCDE1234F
PAN_RE = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")

# Amount digits after removing the 'Rs' / '₹' prefix, commas and spaces.
# ASCII digits only and at most 15 of them (well above any real rupee
# amount). Python's int() also accepts Unicode digits such as '١٢', '_'
# separators and +/- signs, and refuses strings over 4300 digits, so the
# text is checked with this pattern before int() ever sees it.
AMOUNT_RE = re.compile(r"[0-9]{1,15}")
CURRENCY_PREFIX_RE = re.compile(r"^(?:rs\.?|inr|₹)", re.IGNORECASE)

# Slab: LOW-HIGH:RATE with optional spaces around the separators.
SLAB_RE = re.compile(r"([0-9]{1,15})\s*-\s*([0-9]{1,15})\s*:\s*([0-9]{1,3})")


def clean_pan(pan):
    """
    Removes whitespace from a PAN and upper-cases it.
    Returns the PAN as a 10-character string, or None if the input is
    not a string or is not a valid PAN after cleaning.
    """
    if not isinstance(pan, str):
        return None
    cleaned = "".join(pan.split()).upper()
    if not PAN_RE.fullmatch(cleaned):
        return None
    return cleaned


def parse_amount(text):
    """
    Converts an amount such as 'Rs 12,50,000' into an int.
    Returns None if the input is not a string or does not contain only
    ASCII digits once the 'Rs' / '₹' prefix, commas and spaces are removed.
    """
    if not isinstance(text, str):
        return None
    text = CURRENCY_PREFIX_RE.sub("", text.strip())
    text = text.replace(",", "")
    text = "".join(text.split())
    if not AMOUNT_RE.fullmatch(text):
        return None
    return int(text)


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) tuple of ints.
    Returns None if the input is not a string, is not in that format,
    has LOW greater than HIGH, or has a RATE above 100 percent.
    """
    if not isinstance(line, str):
        return None
    match = SLAB_RE.fullmatch(line.strip())
    if match is None:
        return None
    low, high, rate = (int(part) for part in match.groups())
    if low > high or rate > 100:
        return None
    return low, high, rate


def read_line(prompt):
    """input() that returns '' instead of raising at end of input."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def main():
    print("==== Running clean_pan ====")
    value = read_line("Enter a PAN (e.g. abcde 1234f): ")
    pan = clean_pan(value)
    if pan is None:
        print("Invalid PAN: expected 5 letters, 4 digits, 1 letter")
    else:
        print("Cleaned PAN:", pan)

    print("\n==== Running parse_amount ====")
    value = read_line("Enter an amount (e.g. Rs 12,50,000): ")
    amount = parse_amount(value)
    if amount is None:
        print("Invalid amount: use whole rupees, e.g. Rs 12,50,000")
    else:
        print("Amount in rupees:", amount)

    print("\n==== Running parse_tax_slab ====")
    value = read_line(
        "Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    slab = parse_tax_slab(value)
    if slab is None:
        print("Invalid tax slab: use LOW-HIGH:RATE with LOW <= HIGH "
              "and RATE <= 100")
    else:
        print("Tax slab (low, high, rate):", slab)


if __name__ == "__main__":
    main()

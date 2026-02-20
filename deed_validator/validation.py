import os
import json
from datetime import datetime
from text_to_num import text2num # comparing integer to string (number logic)
from decimal import Decimal
from thefuzz import process
from deed_validator.exceptions import (DateLogicError,AmountMismatchError,CountyNotFoundError)

def date_validation(date_signed,date_recorded):
    signed=datetime.fromisoformat(date_signed)
    recorded=datetime.fromisoformat(date_recorded)
    if recorded<signed:
        raise DateLogicError(f"The document was Recorded ${date_recorded} before it was Signed ${date_signed} . That's impossible.The Recorded Date cannot be before Signed Date!!")

def amount_validation(amount_numeric,amount_words):
    numeric=Decimal(str(amount_numeric))
    words_clean= amount_words.lower().replace("dollars","").replace("only","").strip()
    words_number=Decimal(text2num(words_clean,"en"))
    if numeric != words_number:
        difference=numeric-words_number
        raise AmountMismatchError(
             f'The text lists ${numeric:,} in digits but writes out '
            f'"{amount_words}" in words. '
            f'There is a ${difference:,} discrepancy.'
        )

def enrich_county(data):
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", "counties.json")

    with open(data_path) as f:
        counties = json.load(f)

    raw_county = data["county"]
    county_names = [c["name"] for c in counties]
    match, score = process.extractOne(raw_county, county_names)

    if score < 70:
        raise CountyNotFoundError(
            f"Low confidence county match for '{raw_county}' (score={score})"
        )

    for c in counties:
        if c["name"] == match:
            data["county"] = match
            data["tax_rate"] = c["tax_rate"]
            break

    return data

def calculate_closing_tax(data):
    amount = Decimal(str(data["amount_numeric"]))
    tax_rate = Decimal(str(data["tax_rate"]))
    print("tax_rate",tax_rate)
    print("amount",amount)

    closing_tax = amount * tax_rate
    data["closing_tax"] = closing_tax

    return data
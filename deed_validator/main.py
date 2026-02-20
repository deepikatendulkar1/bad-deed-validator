from deed_validator.llm_parser import parse_with_llm
from deed_validator.validation import (date_validation,amount_validation,enrich_county,calculate_closing_tax)
from deed_validator.exceptions import (DateLogicError,AmountMismatchError,CountyNotFoundError)

def deed_process(raw_text: str)->dict:
    """
    Main pipeline for deed document.
    Steps:-
    1. Parse raw text using LLM to extract structured fields.
    2. Validate the dates.
    3. Validate amount consistency( numeric vs words).
    4. If the deed is valid, normalize county and calculate closing tax.
    5. Return structured result.
    """

    # Parsing document text into structured dictionary
    data = parse_with_llm(raw_text)

    errors=[]

    # Date Validation
    try:
        date_validation(data["date_signed"],data["date_recorded"])
        print("The Dates are valid.")
    except DateLogicError as e:
        errors.append(str(e))
        print("Validation on the dates failed: ",e)

    # Amount Validation
    try:
        amount_validation(data["amount_numeric"], data["amount_words"])
    except AmountMismatchError as e:
        errors.append(str(e))
        print("Amount Validation failed:", e)
    
    # Final Decision If the deed is valid or not
    if errors:
        print("Deed Invalid")
    else:
        print("Deed Valid")
        # Only Enrich if all validations pass
        try:
            data = enrich_county(data)
            data = calculate_closing_tax(data)
            print("County normalized to:", data["county"])
            print("Tax Rate:", data["tax_rate"])
            print("Closing Tax:", data["closing_tax"])
        except Exception as e:
            print("County enrichment failed:", e)

    # Return structured reponse
    return{
        "data":data,
    }

if __name__=="__main__":
    raw_text ="""*** RECORDING REQ ***
Doc: DEED-TRUST-0042
County: S. Clara  |  State: CA
Date Signed: 2024-01-15
Date Recorded: 2024-01-10
Grantor:  T.E.S.L.A. Holdings LLC
Grantee:  John  &  Sarah  Connor
Amount: $1,250,000.00 (One Million Two Hundred Thousand Dollars)
APN: 992-001-XA
Status: PRELIMINARY
*** END ***"""

    result =deed_process(raw_text)
    print(result)

# Bad Deed Validator

## Overview

This project demonstrates safe integration of an LLM into a deterministic validation workflow for legal/financial documents.

The system processes OCR-style deed text, extracts structured data using an LLM, and then performs strict validation using deterministic Python logic.

---

## Architecture

The project is structured as follows:

- `llm_parser.py`  
  Uses the OpenAI API to extract structured JSON from unstructured OCR text.

- `validation.py`  
  Contains deterministic validation logic for:
  - Date consistency
  - Amount mismatch detection

- `exceptions.py`  
  Defines custom domain specific exceptions:
  - `DateLogicError`
  - `AmountMismatchError`
  - `CountyNotFoundError`

- `enrichment.py`  
  Handles fuzzy county matching and tax rate enrichment.

- `main.py`  
  Orchestrates the full validation flow.

---

## Design Philosophy

### 1. LLM as a Parser Only

The LLM is treated as a parser to convert messy OCR text into structured JSON. Only fields required for validation and enrichment are extracted. 

### 2. Validation

All business rules are enforced using strict Python logic:

- A recorded date cannot precede the signed date.
- The numeric amount must match the written amount.
- County names must match a known list (using controlled fuzzy matching).
If any rule fails, a domain specific custom exception is raised.

### 3. Flagging Principle

The system does not silently correct discrepancies.  
Invalid documents are flagged immediately with explicit error messages.

For example:
The text lists $1,250,000 in digits but writes out
"One Million Two Hundred Thousand" in words.
There is a $50,000 discrepancy.

### 4. Financial Precision

The `Decimal` type is used instead of `float` to avoid rounding errors in comparisons.

---

## Validation Rules Implemented

1. **Date Logic Validation**
   - `Recorded Date` must not be earlier than `Signed Date`.

2. **Amount Consistency Check**
   - The numeric amount and written amount must match exactly.
   - Discrepancies are calculated and explicitly reported.

3. **County Normalization**
   - OCR county names are normalized using controlled fuzzy matching.
   - If no valid county is found, the document is rejected.

4. **Tax Enrichment**
   - Once the deed is validated, the county tax rate is applied to calculate closing tax.
   - If the deed is not valid (the validation for date and amount fails) then the closing tax is not calculated.

---

## How to Run
1. **Clone the Repository**
 ```bash
 git clone 
 cd bad-deed-validator
  ```

 2. **Create a Virtual Environment**
```bash
 python -m venv venv
 ```
 Activation code:-
  ```bash
 venv\Scripts\activate #For windows
 ```

 3. **Install Dependencies**
```bash
  pip install -r requirements.txt
  ```
 or else 
```bash
  pip install openai python-dotenv text2number
```

 4. **Set OpenAI API Key**
 Create a file named:
 ```bash
 .env 
 ```
 In the project root directory
 Add your API Key inside it:
 ```bash
 OPEN_API_KEY=your_api_key
 ```

 5. **Run the Project**
```bash
python -m deed_validator.main
```

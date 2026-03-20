---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: zentai/bayes_excersice
# corpus-url: https://github.com/zentai/bayes_excersice/blob/bd96311cba5e29db9b946d976780f28a0945c333/skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Skill: DRR Dependency Analysis (Credit Scope) — Leg1 Spread Ticket Generator

## Purpose

Generate a JIRA-ready DRR dependency analysis ticket for **Leg1 Spread-related fields**.

This skill is designed for **Credit product reporting rules** where:
- The reporting rule output depends on **Leg1 enrichment**
- Multiple product branches exist (Commodity / IR / CreditDefaultSwaption)
- Both **final output paths** and **conditional existence paths** must be captured
- Alias expansion is required for developer clarity

The output must match the style of the existing ticket example:
- Rule overview
- Extraction logic
- Referenced functions
- All CDM object paths used
- Conditional vs final paths separation

---

## Scope Rules (Very Important)

1. Only include paths that are:
   - Used in the **return/output**
   - Used in **credit-relevant conditional checking**
   - Marked with `(Exists)` when applicable

2. Exclude paths that belong purely to:
   - FX-only logic
   - IR-only logic
   - Non-credit teams already covering the same subtree

3. Expand aliases into full CDM paths whenever possible.

4. Add function usage context:
   - Which function uses the path
   - File name
   - Line number (if available)

5. Use only ASCII characters:
   - Use `->` for arrows
   - No unicode arrows, icons, emojis

---

## Input Required

User provides:

- dataElement number + label  
- reporting rule name  
- Reference BR Jira ID  
- Rosetta DSL snippet  
- Key helper functions invoked  
- Credit product focus (e.g. CreditDefaultSwaption)

---

## Output Format (JIRA Markdown Compatible)

### Description Block

Must start with:

- Analyze dataElement XX in DRR
- Reference BR Jira
- Optionality
- Paths section

---

## Template Output

### Description

Analyze dataElement XX - CDE-Spread of leg 1 <Spread of Leg 1> in DRR.

This field uses Spread notation of leg 1 CORECG-XXXX for formatting the spread value
(monetary / decimal / percentage / basis).

Reference BR Jira: CORECG-XXX [BR] CoReg:MAS:Field XX (C) "CDE-Spread of leg 1"

Optionality: Conditional as per Cirrus mapping

---

### Paths (Credit Scope Only)

creditdefaultswaption:

EconomicTerms
  -> payout
  -> optionPayout only-element
  -> underlier
  -> index
  -> productTaxonomy
  -> primaryAssetClass

final paths:

EconomicTerms
  -> payout
  -> creditDefaultPayout
  -> generalTerms
  -> indexReferenceInformation
  -> indexId

EconomicTerms
  -> payout
  -> creditDefaultPayout
  -> generalTerms
  -> referenceInformation
  -> referenceObligation
  -> loan
  -> productIdentifier
  -> identifier

WorkflowStep
  -> businessEvent
  -> after
  -> trade
  -> tradableProduct
  -> product
  -> contractualProduct
  -> productIdentifier

---

## Rule Overview

Purpose: Extract and format Spread of Leg 1 for MAS trade reporting.

Rosetta DSL:

reporting rule SpreadLeg1 from TransactionReportInstruction:
  filter IsAllowableActionForMAS
  then common.price.SpreadLeg1_01_Validation(...)

---

## Extraction Logic

SpreadLeg1 is populated through Leg1 enrichment:

reporting rule Leg1Report:
  then common.LegEnrichment(
      cde.Leg1(item, SpreadNotationOfLeg1, ...),
      ...
  )

spread is extracted from:

price.SpreadLeg1
  -> value

formatted using:

SpreadNotationOfLeg1
  -> PriceFormatFromNotation

Returns: Spread string formatted as monetary/decimal/percentage/basis

---

## Key Referenced Functions

### common.price.SpreadLeg1_01_Validation

File: src/main/rosetta/regulation-mas-rewrite-trade-type.rosetta  
Line: [TBD]

Purpose:
- Validates spread presence when required
- Rejects missing fixed rate/spread combinations

Uses paths:

Leg1 -> spread  
Leg2 -> spread  
Leg1 -> fixedRate  
Leg2 -> fixedRate  

---

### PriceFormatFromNotation

File: src/main/rosetta/standards-iso-code-base-price-func.rosetta  
Line: [TBD]

Logic:

if notation = Monetary -> MultiplyPrice(...)
if notation = Decimal  -> FormatToBaseOneRate
if notation = Percentage -> FormatToBaseOneRate
if notation = Basis -> FormatToMax5Number

---

### UnderlierForProduct

File: src/main/rosetta/regulation-common-func.rosetta  
Line: [TBD]

Extracts the underlier product:

if optionPayout exists
  then EconomicTermsForProduct(product)
       -> payout
       -> optionPayout only-element
       -> underlier

else if forwardPayout exists
  then EconomicTermsForProduct(product)
       -> payout
       -> forwardPayout only-element
       -> underlier

---

## All CDM Object Paths Used

Case 1: CreditDefaultSwaption

Condition paths:

EconomicTermsForProduct(UnderlierForProduct)
  -> payout
  -> interestRatePayout only-element (Exists)

Possible UnderlierForProduct paths:

EconomicTermsForProduct(product)
  -> payout
  -> optionPayout only-element
  -> underlier

EconomicTermsForProduct(product)
  -> payout
  -> forwardPayout only-element
  -> underlier

Final paths:

EconomicTermsForProduct(UnderlierForProduct)
  -> payout
  -> interestRatePayout
  -> rateSpecification
  -> floatingRate
  -> spreadSchedule
  -> price
  -> value

---

Case 2: Default

Condition paths:

EconomicTermsForProduct
  -> payout
  -> interestRatePayout only-element

Default final paths:

EconomicTermsForProduct
  -> payout
  -> interestRatePayout
  -> rateSpecification
  -> floatingRate
  -> spreadSchedule
  -> price
  -> value

---

## Developer Notes

- Always separate:
  - Conditional existence paths
  - Final return/output paths

- Expand aliases for readability

- Mark ownership boundaries:
  - Credit team covers CreditDefaultSwaption-related branches only

- Provide function + file + line number whenever possible

---

## Done Criteria Checklist

- [ ] Output paths listed
- [ ] Conditional exists paths listed
- [ ] Credit scope only
- [ ] Alias expanded
- [ ] Functions referenced with file + line
- [ ] JIRA-compatible ASCII formatting only

---
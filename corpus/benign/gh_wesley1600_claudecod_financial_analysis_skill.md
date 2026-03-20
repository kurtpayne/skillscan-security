---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Wesley1600/ClaudeCodeFrameWork
# corpus-url: https://github.com/Wesley1600/ClaudeCodeFrameWork/blob/754208cde67adbf8d569572f26758c3d9c96e4d0/FINANCIAL_ANALYSIS_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Financial Analysis Skill

A comprehensive Claude Code skill for analyzing financial statements, computing financial ratios, and generating actionable insights from PDFs, spreadsheets, or structured data.

## Overview

The Financial Analysis skill enables Claude to:
- Parse financial documents (PDFs, Excel, CSV)
- Extract key financial metrics from balance sheets, income statements, and cash flow statements
- Compute 20+ financial ratios across multiple categories
- Generate detailed analysis reports with insights
- Identify strengths, concerns, and trends in financial data

## Features

### 1. Multi-Format Support
- **PDF**: Extract tables and text from financial PDF reports (using pdfplumber)
- **Excel**: Read structured data from .xlsx/.xls files (using pandas + openpyxl)
- **CSV**: Parse comma-separated financial data
- **Dictionary/JSON**: Direct data input for programmatic use

### 2. Comprehensive Ratio Analysis

#### Liquidity Ratios
- Current Ratio
- Quick Ratio (Acid Test)
- Cash Ratio

#### Profitability Ratios
- Gross Profit Margin
- Operating Profit Margin
- Net Profit Margin
- Return on Assets (ROA)
- Return on Equity (ROE)

#### Leverage/Solvency Ratios
- Debt-to-Equity Ratio
- Debt-to-Assets Ratio
- Equity Multiplier
- Interest Coverage Ratio

#### Efficiency/Activity Ratios
- Asset Turnover Ratio
- Inventory Turnover
- Days Inventory Outstanding
- Receivables Turnover
- Days Sales Outstanding

### 3. Intelligent Insights
- Automatic benchmarking against industry standards
- Health indicators (✓ healthy, ⚠ concern)
- Contextual interpretation of each ratio
- Categorized findings (strengths, concerns, neutral)

### 4. Detailed Reporting
- Executive summaries
- Formatted ratio tables
- Trend analysis (when multi-period data available)
- Actionable recommendations

## Installation

### Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Required packages:
- `pandas>=1.3.0` - Data manipulation and spreadsheet reading
- `openpyxl>=3.0.0` - Excel file support
- `pdfplumber>=0.7.0` - PDF parsing and table extraction

### Skill Setup

The skill is automatically available in Claude Code once the files are in place:

```
.claude/skills/financial-analysis.md  # Skill definition
financial_analyzer.py                 # Core analysis module
examples/                             # Example usage
```

## Usage

### Method 1: Using the Skill in Claude Code

Simply ask Claude to analyze financial data:

```
Analyze the financial statement in examples/financial_data/sample_financial_statement.csv
```

or

```
Load the quarterly report from Q3_2024_financials.pdf and compute all financial ratios
```

Claude will automatically:
1. Parse the document
2. Extract financial metrics
3. Compute ratios
4. Generate insights
5. Present a comprehensive report

### Method 2: Using the Python Module Directly

```python
from financial_analyzer import analyze_file, analyze_dict

# Analyze from file
statement, ratios, report = analyze_file('financial_report.pdf')
print(report)

# Analyze from dictionary
data = {
    'revenue': 1000000,
    'net_income': 100000,
    'total_assets': 500000,
    'shareholders_equity': 300000,
    # ... more fields
}
statement, ratios, report = analyze_dict(data)
print(report)
```

### Method 3: Advanced Usage

```python
from financial_analyzer import FinancialAnalyzer, FinancialStatement

# Create analyzer
analyzer = FinancialAnalyzer()

# Load data from CSV
statement = analyzer.parse_csv('financials.csv')

# Compute specific ratios
ratios = analyzer.compute_all_ratios(statement)

# Filter ratios by category
profitability_ratios = [
    r for r in ratios
    if r.category.value == 'profitability'
]

# Generate custom insights
insights = analyzer.generate_insights(ratios)

# Print strengths and concerns
for strength in insights['strengths']:
    print(f"✓ {strength}")

for concern in insights['concerns']:
    print(f"⚠ {concern}")
```

## Examples

### Example 1: CSV Analysis

Given a CSV file `sample_financial_statement.csv`:

```csv
Line Item,Amount (USD Millions)
Revenue,1250.5
Cost of Goods Sold,687.8
Net Income,166.3
Total Assets,1823.6
Current Assets,645.2
Current Liabilities,298.4
...
```

Run:
```bash
python examples/test_financial_analyzer.py
```

Output:
```
================================================================================
FINANCIAL ANALYSIS REPORT
================================================================================
Period: N/A
Currency: USD
Scale: millions

--------------------------------------------------------------------------------
LIQUIDITY ANALYSIS
--------------------------------------------------------------------------------
Current Ratio: 2.16 ✓
  Formula: Current Assets / Current Liabilities
  Measures ability to pay short-term obligations. Higher is better.
  Benchmark Range: 1.50 - 3.00

Quick Ratio: 1.50 ✓
  Formula: (Current Assets - Inventory) / Current Liabilities
  Measures ability to pay short-term obligations without selling inventory.
  Benchmark Range: 1.00 - 2.00

--------------------------------------------------------------------------------
PROFITABILITY ANALYSIS
--------------------------------------------------------------------------------
Gross Profit Margin: 45.00% ✓
  Formula: (Gross Profit / Revenue) × 100
  Percentage of revenue retained after COGS. Higher is better.
  Benchmark Range: 20.00 - 50.00

Net Profit Margin: 13.30% ✓
  Formula: (Net Income / Revenue) × 100
  Bottom-line profitability. Percentage of revenue that becomes profit.
  Benchmark Range: 5.00 - 20.00

Return on Equity (ROE): 17.85% ✓
  Formula: (Net Income / Shareholders' Equity) × 100
  Return generated on shareholders' investment. Higher is better.
  Benchmark Range: 10.00 - 25.00

...
```

### Example 2: Dictionary Input

```python
from financial_analyzer import analyze_dict

financial_data = {
    'revenue': 5000.0,
    'net_income': 560.0,
    'total_assets': 8000.0,
    'shareholders_equity': 4000.0,
    'current_assets': 2800.0,
    'current_liabilities': 1400.0,
    'period': 'FY 2024'
}

statement, ratios, report = analyze_dict(financial_data)
print(report)
```

### Example 3: PDF Analysis

```python
from financial_analyzer import analyze_file

# Analyze a PDF financial report
statement, ratios, report = analyze_file('annual_report_2024.pdf', file_type='pdf')

# Print full report
print(report)

# Access specific metrics
for ratio in ratios:
    if ratio.name == "Return on Equity (ROE)":
        print(f"ROE: {ratio.format_value()}")
        print(f"Healthy: {ratio.is_healthy()}")
```

## Data Structure

### FinancialStatement Fields

The `FinancialStatement` dataclass supports the following fields:

**Balance Sheet:**
- `cash`, `accounts_receivable`, `inventory`
- `current_assets`, `total_assets`
- `accounts_payable`, `short_term_debt`, `current_liabilities`
- `long_term_debt`, `total_liabilities`
- `shareholders_equity`

**Income Statement:**
- `revenue`, `cost_of_goods_sold`, `gross_profit`
- `operating_expenses`, `operating_income`
- `interest_expense`, `tax_expense`, `net_income`

**Cash Flow Statement:**
- `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`
- `capital_expenditures`, `free_cash_flow`

**Metadata:**
- `period` (e.g., "Q3 2024", "FY 2023")
- `currency` (e.g., "USD", "EUR")
- `scale` (e.g., "actual", "thousands", "millions", "billions")

## Interpretation Guide

### Liquidity Ratios

**Current Ratio = Current Assets / Current Liabilities**
- Benchmark: 1.5 - 3.0
- Interpretation: Ability to pay short-term obligations
- < 1.0: Liquidity concern
- > 3.0: May indicate inefficient use of assets

**Quick Ratio = (Current Assets - Inventory) / Current Liabilities**
- Benchmark: 1.0 - 2.0
- Interpretation: Conservative liquidity measure
- Excludes inventory (less liquid asset)

### Profitability Ratios

**Net Profit Margin = (Net Income / Revenue) × 100**
- Benchmark: 5% - 20%
- Interpretation: Bottom-line profitability
- Higher is better, but compare to industry

**Return on Equity (ROE) = (Net Income / Equity) × 100**
- Benchmark: 10% - 25%
- Interpretation: Return on shareholders' investment
- Warren Buffett targets 15%+ sustained ROE

### Leverage Ratios

**Debt-to-Equity = Total Debt / Equity**
- Benchmark: 0.0 - 2.0
- Interpretation: Financial leverage
- Higher = more risk but potentially higher returns
- Varies widely by industry

**Interest Coverage = Operating Income / Interest Expense**
- Benchmark: 3.0 - 10.0
- Interpretation: Ability to pay interest
- < 2.0: Potential debt servicing issues

### Efficiency Ratios

**Asset Turnover = Revenue / Total Assets**
- Benchmark: 0.5 - 2.0
- Interpretation: Revenue generation efficiency
- Higher = better asset utilization

**Days Sales Outstanding = 365 / (Revenue / AR)**
- Benchmark: 30 - 60 days
- Interpretation: Average collection period
- Lower = faster cash conversion

## Advanced Features

### Multi-Period Analysis

Compare financial performance across multiple periods:

```python
analyzer = FinancialAnalyzer()

# Load multiple periods
q1_stmt = analyzer.parse_csv('Q1_2024.csv')
q2_stmt = analyzer.parse_csv('Q2_2024.csv')
q3_stmt = analyzer.parse_csv('Q3_2024.csv')

# Compute ratios for each period
q1_ratios = analyzer.compute_all_ratios(q1_stmt)
q2_ratios = analyzer.compute_all_ratios(q2_stmt)
q3_ratios = analyzer.compute_all_ratios(q3_stmt)

# Compare trends
# (Implementation would track changes over time)
```

### Custom Benchmarks

Modify benchmark ranges for industry-specific analysis:

```python
# Example: Retail industry typically has lower margins
for ratio in ratios:
    if ratio.name == "Net Profit Margin":
        ratio.benchmark_range = (2.0, 8.0)  # Retail-specific
```

### Export Options

```python
import json

# Export to JSON
with open('analysis_results.json', 'w') as f:
    json.dump({
        'statement': statement.to_dict(),
        'ratios': [asdict(r) for r in ratios],
        'insights': insights
    }, f, indent=2)

# Export report to file
with open('financial_report.txt', 'w') as f:
    f.write(report)
```

## Limitations

1. **PDF Parsing**: Complex PDF layouts may require manual data extraction
2. **Data Quality**: Accuracy depends on source document quality
3. **Industry Context**: Benchmarks are general; industry-specific ranges may differ
4. **Scanned PDFs**: OCR capabilities are limited; prefer digital PDFs
5. **Currency Conversion**: No automatic forex conversion

## Best Practices

1. **Verify Extracted Data**: Always review extracted metrics for accuracy
2. **Consistent Units**: Ensure all figures use the same scale (e.g., all in millions)
3. **Complete Data**: More complete data = more comprehensive analysis
4. **Context Matters**: Consider industry, company size, and economic conditions
5. **Trend Analysis**: Single-period analysis is limited; use multi-period when possible

## Troubleshooting

### "Module not found" errors

Install dependencies:
```bash
pip install pandas openpyxl pdfplumber
```

### PDF parsing returns empty data

- Ensure PDF contains selectable text (not scanned image)
- Try manual data extraction to dictionary format
- Check if tables are properly formatted

### Ratios show N/A

- Required fields are missing
- Check that denominator fields are not zero
- Verify data extraction was successful

### Incorrect ratio calculations

- Verify input data units (thousands vs millions)
- Check for negative values in unexpected fields
- Ensure all required fields are populated

## Contributing

To extend the financial analyzer:

1. Add new ratio calculations in appropriate `_compute_*_ratios()` methods
2. Update benchmarks based on research
3. Add support for additional file formats
4. Improve PDF/Excel parsing logic

## References

- Financial ratio definitions: https://www.investopedia.com/financial-ratios/
- Industry benchmarks: Varies by sector; consult industry reports
- Accounting standards: GAAP (US) or IFRS (International)

## License

MIT License (or as per repository license)

## Support

For issues or questions:
1. Check the examples in `examples/test_financial_analyzer.py`
2. Review the docstrings in `financial_analyzer.py`
3. Open an issue in the repository

---

**Version**: 1.0
**Last Updated**: 2025-11-18
**Status**: Production Ready
---
name: yahooclaw
description: Yahoo Finance API integration for OpenClaw. Use when users ask for stock prices, company financials, historical data, dividends, or market data. Supports real-time quotes, financial statements, and market analysis.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: leohuang8688/yahooclaw
# corpus-url: https://github.com/leohuang8688/yahooclaw/blob/4616d49e8e1b655cb3b5aaec40654315b8705137/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# YahooClaw - Yahoo Finance API Integration

## 🔒 Security

- ✅ No shell command execution
- ✅ All API calls use HTTPS
- ✅ Rate limiting implemented
- ✅ Open source and auditable
- ⚠️ API keys must be set via environment variables
- ℹ️ Uses in-memory caching for performance (no database)

## Overview

YahooClaw is an OpenClaw skill that integrates Yahoo Finance API, providing real-time stock data queries, financial analysis, historical stock prices, and more.

## Permissions

### Required Permissions
- ✅ Network Access: Yahoo Finance API (HTTPS)
- ✅ File Access: Local SQLite database storage (optional caching)
- ❌ No Admin/Root Privileges Required
- ❌ No System Command Execution
- ❌ No Access to User Privacy Data

### Data Flow
- Stock Data: Yahoo Finance API → Local Processing → Return Results
- No user data uploaded
- Temporary caching only (optional)

## Use Cases

### 1. Real-time Stock Quotes
```
Query AAPL stock price
How much is Tesla now
NVDA latest stock price
```

### 2. Company Information
```
What is Apple's market cap
Microsoft's P/E ratio
Google's revenue data
```

### 3. Historical Data
```
Show AAPL stock price for the past 30 days
Tesla's trend last month
```

### 4. Financial Metrics
```
Apple's balance sheet
Tencent's income statement
```

### 5. Dividends
```
What is AAPL's dividend
Which stocks have high dividend yields
```

## Usage Examples

### Basic Usage
```javascript
const YahooClaw = require('./src/yahoo-finance.js');

// Get real-time stock quote
const quote = await YahooClaw.getQuote('AAPL');
console.log(quote);

// Get historical data
const history = await YahooClaw.getHistory('TSLA', '1mo');
console.log(history);

// Get company information
const info = await YahooClaw.getCompanyInfo('MSFT');
console.log(info);
```

### OpenClaw Integration
```javascript
// Call in OpenClaw agent
const result = await tools.yahooclaw.getQuote({symbol: 'AAPL'});
```

## API Parameters

### getQuote(symbol)
- **symbol**: Stock code (e.g., AAPL, TSLA, 0700.HK)
- **Returns**: Real-time stock price, change, volume, etc.

### getHistory(symbol, period)
- **symbol**: Stock code
- **period**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- **Returns**: Historical stock price data

### getCompanyInfo(symbol)
- **symbol**: Stock code
- **Returns**: Company information, market cap, P/E ratio, P/B ratio, etc.

### getDividends(symbol)
- **symbol**: Stock code
- **Returns**: Dividend history

## Environment Variables

```bash
# Optional: Alpha Vantage API (backup data source)
# Get from: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_api_key_here

# Optional: Database path for caching
DATABASE_PATH=./yahooclaw.db
```

## Notes

1. **Data Delay**: Yahoo Finance real-time data may have 15-minute delay
2. **Rate Limiting**: Control request frequency to avoid rate limits
3. **HK/A-Shares**: Supports HK stocks (0700.HK), A-shares (600519.SS), etc.
4. **Error Handling**: Network issues or invalid codes will return error messages

## Troubleshooting

### Common Issues

1. **Failed to Get Data**
   - Check network connection
   - Verify stock code format
   - Check Yahoo Finance service status

2. **Data Delay**
   - This is normal, Yahoo Finance real-time data has delay
   - Consider using paid API for truly real-time data

3. **A-Share/HK Stock Code Format**
   - A-Shares: 600519.SS (Moutai)
   - HK Stocks: 0700.HK (Tencent)
   - US Stocks: AAPL (Apple)

## Resources

- [Yahoo Finance API Documentation](https://finance.yahoo.com/)
- [yfinance Python Library](https://pypi.org/project/yfinance/)
- [OpenClaw Documentation](https://docs.openclaw.ai/)

## Changelog

### v1.0.0 (2026-03-12)
- ✅ Security improvements
- ✅ Removed all test/debug files
- ✅ Fixed unicode characters
- ✅ Updated documentation
- ✅ Production ready

### v0.1.0 (2026-03-09)
- ✅ Initial release
- ✅ Real-time stock quotes
- ✅ Historical data queries
- ✅ Company information queries
- ✅ Dividend queries
- ✅ OpenClaw integration

## License

MIT License

## Author

PocketAI for Leo - OpenClaw Community
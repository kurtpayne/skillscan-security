---
name: ok-trading-advisor
description: >
  Multi-timeframe market analysis and trade recommendation engine.
  Use when user asks for: 'trading advice', 'should I buy BTC', 'analyze BTC market',
  'is it a good time to long/short', 'technical analysis', 'signal analysis', 'entry point',
  'suggest TP/SL', 'signal engine', 'trend analysis', 'RSI signal', 'MACD signal',
  'EMA crossover', 'Bollinger Band signal', 'volume analysis', 'market analysis',
  or any request to assess market conditions and produce a trade recommendation.
  Collects multi-timeframe market data via okx-trade-cli, computes trend/oscillator/volume
  signals, and outputs a structured directional recommendation with entry zone, TP, and SL.
  Data collection is read-only (no credentials needed); order execution requires okx-cex-trade.
license: MIT
author: ok-assistance
version: 1.0.0
agent:
  requires:
    bins: ["okx"]
  install:
    - id: npm
      kind: node
      package: "@okx_ai/okx-trade-cli"
      bins: ["okx"]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: zeroxerCpp/OK-TradeKit-signal-middleware
# corpus-url: https://github.com/zeroxerCpp/OK-TradeKit-signal-middleware/blob/5fafe3f18405bdf0d94aee80461db3bf1ab9e943/signal_skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# OK Trading Advisor

Multi-timeframe market analysis and trade recommendation engine.

Collects real-time market data via `okx-trade-cli`, computes trend/oscillator/volume
signals using the OK-Assistance signal engine, and returns a structured directional
recommendation with entry zone, take-profit, and stop-loss.

**Note:** Data collection is read-only and requires no API credentials. Order execution
requires `okx-cex-trade` and valid API credentials.

---

## Prerequisites

- Install `okx` CLI:
  ```bash
  npm install -g @okx_ai/okx-trade-cli
  ```
- Verify install:
  ```bash
  okx market ticker BTC-USDT
  ```

---

## Quickstart

Collect market data and compute signals:

```bash
# Multi-timeframe candles (use confirmed candles only; confirm == "1")
okx market candles BTC-USDT-SWAP --bar 1D --limit 100 --json   # Ichimoku needs 78+
okx market candles BTC-USDT-SWAP --bar 4H --limit 200 --json   # MACD needs 35+, ADX 28+, Ichimoku 78+
okx market candles BTC-USDT-SWAP --bar 1H --limit 200 --json   # BB/VolMA20 need 20+, SL swing 10+

# Market context
okx market ticker BTC-USDT-SWAP --json
okx market funding-rate BTC-USDT-SWAP --json
okx market open-interest --instType SWAP --instId BTC-USDT-SWAP --json
okx market orderbook BTC-USDT-SWAP --sz 20 --json
okx market trades BTC-USDT-SWAP --limit 50 --json
```

---

## Commands

All commands are READ-only market data queries.

| # | Command | Description | Min confirmed candles needed |
|---:|:---|:---|:---|
| 1 | `okx market candles <instId> --bar 1D --limit 100` | Daily OHLCV (trend bias, BBands, MACD) | **100** — Ichimoku needs 52 + warmup; MACD needs 35+ |
| 2 | `okx market candles <instId> --bar 4H --limit 200` | 4H OHLCV (entry timing, EMA, RSI, ADX, SuperTrend) | **200** — ADX(14) needs 28+; SuperTrend(10,3) needs 10+; MACD(12,26,9) needs 35+; Ichimoku(9,26,52) needs 52+ |
| 3 | `okx market candles <instId> --bar 1H --limit 200` | 1H OHLCV (entry confirmation, volume, BB, RSI) | **200** — BB(20) needs 20+; RSI(14) needs 15+; SL swing needs 10 confirmed |
| 4 | `okx market candles <instId> --bar 15m --limit 60` | 15m OHLCV (intraday entry precision) | **60** — EMA/RSI/BB warmup |
| 5 | `okx market ticker <instId>` | Latest price, 24h high/low/vol |
| 6 | `okx market funding-rate <instId>` | Current + next funding rate (sentiment) |
| 7 | `okx market funding-rate <instId> --history --limit 20` | Historical funding rate trend |
| 8 | `okx market open-interest --instType SWAP --instId <id>` | OI (position conviction) |
| 9 | `okx market orderbook <instId> --sz 20` | Bid/ask depth (liquidity) |
| 10 | `okx market trades <instId> --limit 50` | Recent trades (buy/sell pressure) |
| 11 | `okx market mark-price --instType SWAP --instId <id>` | Mark price vs last (divergence) |
| 12 | `okx market index-ticker --instId BTC-USD` | Index price (spot reference) |
| 13 | `okx market liquidation-orders --instType SWAP --instId <id> --state filled --limit 100` | Recent forced liquidations (size + side) |

---

## Signal Engine

> ⚠️ **COMPUTATION RULE — MANDATORY**
> You MUST show intermediate values for every indicator before assigning a score.
> Do NOT skip directly to the final score or recommendation.
> Format each calculation step as:
> ```
> [indicator] [timeframe]: raw_value → condition → score: +X (confidence: X.X)
> ```
> Example:
> ```
> EMA9 = 83,420 | EMA21 = 82,100 | 4H: EMA9 > EMA21, confirmed 4 candles → score: +1 (confidence: 1.0)
> RSI(14) 1H: value = 31.2 → mild oversold (30–35) → score: +1 (confidence: 0.5)
> MACD 4H: histogram = +12.3, expanding 2 candles → score: +1 (confidence: 0.75)
> ```
> Only after all indicators are computed and shown, calculate the weighted total.
>
> **Index notation:** `[0]` = current (latest confirmed) candle; `[-1]` = one candle before current; `[1]` = one candle after current (not yet available).

### Trend Signals (1D + 4H)

| Signal | Indicator | Bullish (precise condition) | Bearish (precise condition) |
|:---|:---|:---|:---|
| EMA Crossover | EMA(9) / EMA(21) | `EMA9[-1] < EMA21[-1] AND EMA9[0] > EMA21[0]` (fresh cross), or `EMA9[0] > EMA21[0]` for ≥2 candles (confirmed) | `EMA9[-1] > EMA21[-1] AND EMA9[0] < EMA21[0]` (fresh cross), or `EMA9[0] < EMA21[0]` for ≥2 candles |
| MACD | MACD(12,26,9) | `MACD[0] > signal[0] AND histogram[0] > histogram[-1]` (expanding bullish) | `MACD[0] < signal[0] AND histogram[0] < histogram[-1]` (expanding bearish) |
| SuperTrend | ATR(10) × 3 | `close[0] > supertrend_lower[0]` AND was below on previous candle (fresh), or `close[0] > supertrend_lower[0]` for ≥3 candles | `close[0] < supertrend_upper[0]` AND was above on previous candle (fresh), or sustained below |
| Bollinger Band | BB(20,2) | `low[0] <= BB_lower[0] AND close[0] > BB_lower[0]` (wick or close below then close back above) | `high[0] >= BB_upper[0] AND close[0] < BB_upper[0]` (wick or close above then close back below) |
| Ichimoku | (9,26,52) | `close[0] > cloud_top[0] AND tenkan[0] > kijun[0]` | `close[0] < cloud_bottom[0] AND tenkan[0] < kijun[0]` |

Scoring: Each signal vote = sign × confidence, where sign ∈ {+1, −1, 0}
and confidence ∈ [0.0, 1.0] per the Signal Confidence Rules below.
**Trend Score** = (Σ(sign × confidence) / 5) × 5, normalized to [−5, +5].

### Volume & Sentiment Signals (4H + 1H)

| Signal | Source | Bullish (precise condition) | Bearish (precise condition) |
|:---|:---|:---|:---|
| Volume Breakout | 1H volume vs MA(20) | `vol[0] > 2 × vol_MA20 AND close[0] > open[0]` | `vol[0] > 2 × vol_MA20 AND close[0] < open[0]` |
| Funding Rate | `market funding-rate` | `funding_rate < −0.01%` (shorts paying longs → contrarian long) | `funding_rate > +0.05%` (longs paying shorts → contrarian short) |
| OI Change | `market open-interest` | `OI[0] > OI_MA5 AND close[0] > close[-1]` (rising OI + rising price) | `OI[0] > OI_MA5 AND close[0] < close[-1]` (rising OI + falling price) |
| Order Book | `market orderbook` | `sum(bid_depth, top10) > sum(ask_depth, top10) × 1.2` | `sum(ask_depth, top10) > sum(bid_depth, top10) × 1.2` |
| Trade Flow | `market trades` | `buy_count / total_trades > 0.6` among last 50 trades | `sell_count / total_trades > 0.6` among last 50 trades |

Scoring: Each signal vote = sign × confidence, where sign ∈ {+1, −1, 0}
and confidence ∈ [0.0, 1.0] per the Signal Confidence Rules below.
**Volume/Senti Score** = (Σ(sign × confidence) / 5) × 5, normalized to [−5, +5].
Note: The Liquidation Heatmap signal is supplementary evidence only and does NOT
contribute to this score.

### Liquidation Heatmap Signal

> Applies to SWAP instruments only. Skip this section for spot.

From the last 100 filled liquidation orders, compute:
- `liq_sell_vol` = sum of sizes where side = sell (forced long liquidation)
- `liq_buy_vol`  = sum of sizes where side = buy (forced short cover)
- `n_events`     = total number of liquidation events
- `liq_avg`      = (liq_sell_vol + liq_buy_vol) / n_events   (average per event)
- `liq_ratio`    = liq_sell_vol / (liq_sell_vol + liq_buy_vol)

| Condition | Signal | Score |
|:---|:---|:---:|
| `liq_sell_vol > 3 × liq_avg × n_events × 0.5` AND price within 1% of 10-candle 1H low | Panic long liquidation — contrarian LONG | +1 |
| `liq_buy_vol > 3 × liq_avg × n_events × 0.5` AND price within 1% of 10-candle 1H high | Short-squeeze exhaustion — contrarian SHORT | −1 |
| `liq_ratio > 0.75` AND OI dropping (OI < OI_MA5) | Capitulation bottom — strengthen LONG | +1 |
| `liq_ratio < 0.25` AND OI dropping (OI < OI_MA5) | Short-squeeze top — strengthen SHORT | −1 |
| Neither condition met | Neutral | 0 |

> **Note:** Conditions 1+3 can stack (+2 max); conditions 2+4 can stack (−2 min).

**Liquidation Spike edge case:** If any single liquidation event size > 5× `liq_avg`:
```
⚠️ LIQUIDATION SPIKE detected — elevated signal reliability, but whipsaw risk high.
   Reduce position size by 50% regardless of score.
```

The Liquidation Heatmap signal is **supplementary evidence only**. It does NOT contribute to the Volume/Senti Score. Include its output as ✅ or ⚠️ evidence in the Key Evidence section of the report.

### Market State Detection

Before computing the final score, classify the current market state using:

| Indicator | Calculation | Threshold |
|:---|:---|:---|
| ADX(14) | Average Directional Index on 4H candles | ADX > 25 → Trending; ADX < 20 → Ranging |
| ATR expansion | ATR(14) on 4H vs its own MA(10) | ATR > 1.5× MA → High Volatility |
| Volume | Latest 1H volume vs MA(20) | Volume < 0.5× MA → Low Liquidity |

**ADX formula:**
- `+DM = High − PrevHigh` (if positive, else 0)
- `−DM = PrevLow − Low` (if positive, else 0)
- `DX = |+DI − −DI| / |+DI + −DI| × 100`
- `ADX = EMA(DX, 14)`

**Market states and dynamic weights:**

| State | Condition | Trend w | Volume/Senti w | Oscillator w | Note |
|:---|:---|:---:|:---:|:---:|:---|
| Trending | ADX > 25 | **0.60** | 0.25 | 0.15 | Follow the trend |
| Ranging | ADX < 20 | 0.25 | 0.30 | **0.45** | Mean-reversion favored |
| High Volatility | ATR > 1.5× MA | 0.35 | **0.45** | 0.20 | Sentiment/volume drives moves |
| Low Liquidity | Volume < 0.5× MA | — | — | — | Output `LOW_CONFIDENCE`; abort calculation, skip trade |
| Normal | Otherwise | 0.40 | 0.35 | 0.25 | Default weights |

**Final Score formula (dynamic):**
```
Total Score = (Trend × w_trend + Oscillator × w_osc + Volume × w_vol) × 2
```
Where weights are selected from the table above based on detected market state.

**Report addition:** Always include the detected market state in the output:
```
Market State : Trending (ADX = 28.4) / Ranging / High Volatility / ⚠️ LOW CONFIDENCE
```

### Final Score & Recommendation

**Total Score** = (Trend × w_trend + Oscillator × w_osc + Volume × w_vol) × 2 (normalized to −10..+10; weights selected from the preceding Market State Detection section)

| Score Range | Direction | Action |
|---:|:---:|:---|
| +6.0 to +10 | 🟢 LONG | Strong buy |
| +3.0 to +5.9 | 🟡 LONG | Moderate buy |
| −2.9 to +2.9 | ⚪ NEUTRAL | No trade |
| −5.9 to −3.0 | 🟡 SHORT | Moderate sell |
| −10 to −5.9 | 🔴 SHORT | Strong sell |

### Signal Confidence Rules

Each signal is scored as a continuous confidence value in `[0.0, 1.0]` rather than a binary vote.
The directional sign (+/−) is applied separately. Final vote = `sign × confidence`.

**EMA Crossover confidence:**
| Condition | Confidence |
|:---|:---:|
| Crossed on the last candle only | 0.5 |
| Confirmed for 2 consecutive candles | 0.75 |
| Confirmed for ≥ 3 consecutive candles | 1.0 |

**RSI confidence:**
| Condition | Confidence |
|:---|:---:|
| RSI 30–35 (mild oversold) or 65–70 (mild overbought) | 0.5 |
| RSI 20–29 (moderate oversold) or 70–79 | 0.75 |
| RSI < 20 (extreme oversold) or ≥ 80 | 1.0 |

**MACD confidence:**
| Condition | Confidence |
|:---|:---:|
| MACD just crossed signal line | 0.5 |
| Histogram expanding for 2 candles | 0.75 |
| Histogram expanding for ≥ 3 candles, MACD > 0 | 1.0 |

**Bollinger Band confidence:**
| Condition | Confidence |
|:---|:---:|
| Price wick pierces band (low < BB_lower or high > BB_upper), close reverts inside | 1.0 |
| Price wick touches band exactly (low == BB_lower or high == BB_upper) | 0.7 |
| Price between mid and band (no band touch) | 0.4 |

**Funding Rate confidence:**
| Condition | Confidence |
|:---|:---:|
| 0.01%–0.05% (mild) | 0.4 |
| 0.05%–0.10% (elevated) | 0.75 |
| > 0.10% (extreme) | 1.0 |

**Volume Breakout confidence:**
| Condition | Confidence |
|:---|:---:|
| Volume 1.5×–2× MA20 | 0.6 |
| Volume > 2× MA20 | 1.0 |

**Default:** Any signal not listed above defaults to binary 0 or 1.

**Score adjustment:** Each group's raw score = `Σ (sign × confidence)` across its signals.
Normalize to [−5, +5] by computing `(Σ(sign × confidence) / N) × 5`, where N is the number of signals in the group.
Then apply dynamic weights as defined in Market State Detection.

### Entry, Stop-Loss, and Take-Profit Calculation

These rules define exactly how to compute the Entry Zone, SL, and TP values in the report.
Always use confirmed candle data (confirm == "1") for swing point lookback.

#### Entry Zone

| Direction | Market State | Entry Zone |
|:---|:---|:---|
| LONG | Trending | `[EMA21_4H × 0.999, current_price]` — buy dip to EMA21 |
| LONG | Ranging | `[BB_lower_1H, BB_mid_1H]` — fade to lower band |
| LONG | High Volatility | `[current_price × 0.997, current_price × 1.001]` — tight zone near market |
| SHORT | Trending | `[current_price, EMA21_4H × 1.001]` — sell rip to EMA21 |
| SHORT | Ranging | `[BB_mid_1H, BB_upper_1H]` — fade to upper band |
| SHORT | High Volatility | `[current_price × 0.999, current_price × 1.003]` — tight zone near market |

#### Stop-Loss

```
LONG:  SL = min(low[0..9], tf=1H) × 0.998        # lowest low across the last 10 confirmed 1H candles (indices 0–9 inclusive), plus 0.2% buffer
SHORT: SL = max(high[0..9], tf=1H) × 1.002       # highest high across the last 10 confirmed 1H candles (indices 0–9 inclusive), plus 0.2% buffer

entry_mid = (entry_zone_lower + entry_zone_upper) / 2   # midpoint of the Entry Zone range above

Hard cap: |entry_mid − SL| / entry_mid ≤ 3%
If calculated SL exceeds 3%, set SL = entry_mid × (1 − 0.03) for LONG
                                    = entry_mid × (1 + 0.03) for SHORT
```

#### Take-Profit

```
risk = |entry_mid − SL|

TP1 = entry_mid + risk × 1.5    (R:R = 1.5)   for LONG
TP1 = entry_mid − risk × 1.5                   for SHORT

TP2 = entry_mid + risk × 3.0    (R:R = 3.0)   for LONG
TP2 = entry_mid − risk × 3.0                   for SHORT

Suggested execution: take 50% at TP1, trail SL to entry, let 50% run to TP2.
```

#### Minimum R:R Gate

**If R:R at TP1 < 1.5, do NOT recommend the trade regardless of score.**
Output: `⚠️ R:R = X.X — Below minimum threshold (1.5). No trade recommended.`

#### Position Size

```
risk_pct = 1%  if signal strength = Moderate
risk_pct = 2%  if signal strength = Strong
risk_pct = 0.5% if market state = High Volatility

position_size_usdt = account_size × risk_pct / (|entry_mid − SL| / entry_mid)
```

Always display position size as both `% of account` and `estimated USDT` in the report.

## Workflow

### Step 1: Identify instrument and timeframe

- **Default**: SWAP (perpetual), e.g. `BTC-USDT-SWAP`
- **Spot**: use `BTC-USDT` if user specifies "spot"
- **Timeframes**: 1D (trend) + 4H (signal) + 1H (entry) by default
- **Scalp/intraday**: add 15m, reduce 1D weight
- **Swing/position**: focus on 1D + 4H, skip 15m

### Step 2: Collect market data

```bash
okx market candles <instId> --bar 1D --limit 100 --json   # needs ≥78 confirmed (Ichimoku)
okx market candles <instId> --bar 4H --limit 200 --json   # needs ≥35 confirmed (MACD), ≥78 (Ichimoku), ≥28 (ADX)
okx market candles <instId> --bar 1H --limit 200 --json   # needs ≥20 confirmed (BB/Vol MA20), ≥10 (SL swing)
okx market ticker <instId> --json
okx market funding-rate <instId> --json
okx market funding-rate <instId> --history --limit 20 --json
okx market open-interest --instType SWAP --instId <id> --json
okx market orderbook <instId> --sz 20 --json
okx market trades <instId> --limit 50 --json
okx market liquidation-orders --instType SWAP --instId <id> --state filled --limit 100 --json
```

### Step 3: Compute signals

For each timeframe, calculate:

1. **EMA(9) and EMA(21)** — check crossover on last 3 candles
2. **MACD(12,26,9)** — check direction and histogram
3. **Bollinger Bands(20,2)** — check price position and squeeze
4. **RSI(14)** — detect oversold/overbought
5. **KDJ(9,3,3)** — check K/D crosses
6. **Volume MA(20)** — compare latest vs average
7. **Funding Rate** — assess magnitude
8. **OI trend** — compare latest vs 5-period average
9. **Order Book** — sum top-10 bid vs ask depth
10. **Trade Flow** — count buy vs sell among last 50 trades
11. **ADX(14)** — classify market state (Trending / Ranging / High Volatility / Low Liquidity); select dynamic weights accordingly
12. **Liquidation Heatmap** (SWAP only) — compute liq_sell_vol, liq_buy_vol, liq_ratio; detect spike; add signal to Volume/Senti group

Score each signal per the tables above. Compute weighted total.

> **Note:** RSI(14) and KDJ(9,3,3) are supplementary confirmation signals. They are **not** included in the primary score calculation. Use them as ✅ or ⚠️ evidence in the Key Evidence section of the report only.

### Step 3.5: Self-Verification Before Report

Before generating the report output, verify every item below. If any item is incomplete, complete it first.

**Computation completeness:**
- [ ] All 5 Trend signals computed with raw values shown (EMA, MACD, SuperTrend, BB, Ichimoku)
- [ ] All 5 Volume & Sentiment signals computed with raw values shown
- [ ] RSI and KDJ computed and noted as supplementary evidence
- [ ] ADX(14) computed → market state classified → dynamic weights selected
- [ ] Liquidation heatmap computed (SWAP only): liq_ratio noted, spike flag checked

**Scoring integrity:**
- [ ] Each signal score shown as: `raw_value → condition → score (confidence)`
- [ ] Group scores = Σ(sign × confidence), normalized to [−5, +5]
- [ ] Total Score = (Trend × w + Volume × w + Oscillator × w) × 2, result in [−10, +10]
- [ ] Market state and weights used are explicitly stated

**Entry plan validity:**
- [ ] Entry Zone calculated using rules in "Entry, Stop-Loss, and Take-Profit Calculation"
- [ ] SL calculated from 10-candle swing + buffer, hard cap applied if needed
- [ ] TP1 and TP2 calculated; R:R ≥ 1.5 confirmed
- [ ] If R:R < 1.5 → abort report, output R:R warning instead
- [ ] Position size calculated and expressed as % of account

**Signal freshness:**
- [ ] All candle data uses only confirmed candles (confirm == "1")
- [ ] Timestamp of data collection recorded

### Step 4: Generate report

Output structured recommendation:

```
═══════════════════════════════════════════
📊 OK Trading Advisor — Signal Report
═══════════════════════════════════════════
🕒 Time        : <timestamp>
📈 Instrument  : <instId>
💰 Price       : <last> USDT

─── Scores ────────────────────────────────
Trend          : <score>/5  (<signals>)
Oscillator     : <score>/5  (<signals>)
Volume/Senti   : <score>/5  (<signals>)
─────────────────────────────────────────
Total Score    : <score>/10
Market State   : Trending (ADX = 28.4) / Ranging / High Volatility / ⚠️ LOW CONFIDENCE

─── Recommendation ────────────────────────
Direction  : 🟢 LONG / 🔴 SHORT / ⚪ NEUTRAL
Strength   : Strong / Moderate
Timeframe  : <holding period>

─── Entry Plan ────────────────────────────
Entry Zone : <price range>
Stop-Loss  : <price>  (<% from entry>)
Take-Profit: <price>  (<% from entry>, R:R = <ratio>)
Position   : <% of account>

─── Key Evidence ──────────────────────────
✅ <bullish signal 1>
✅ <bullish signal 2>
⚠️  <risk factor>
❌ <bearish signal if any>

─── Caution ───────────────────────────────
Analysis output, not financial advice.
Always confirm with your own judgment.
═══════════════════════════════════════════
```

### Step 5: Offer execution

Ask:

> ⚠️ Signal generated at `<timestamp>`. Market conditions may have changed.
> If more than **5 minutes** have passed since data collection, re-run analysis before executing.
>
> Trade this signal? Reply: `yes demo|live <USDT amount> [max <X>% of account]`
>
> Recommended position size: ≤ 2% of account per trade unless signal strength is **Strong**.

---

## Examples

**"Analyze BTC"**

```
→ Collect 1D + 4H + 1H candles for BTC-USDT-SWAP
→ Collect ticker, funding-rate, OI, orderbook, trades
→ Compute signals and output report
```

**"Should I short ETH?"**

```
→ Collect ETH-USDT-SWAP data
→ If score ≤ −3: "Short signal confirmed. Entry: X, TP: Y, SL: Z"
→ Else: "Signal does not support short. Score: X (direction)"
```

**"Quick scan: BTC or ETH, which one?"**

```
→ Collect 4H + 1H for BTC and ETH
→ BTC score: +5.2 (Moderate Long)
→ ETH score: +7.1 (Strong Long)
→ "Trade ETH. Entry: X, TP: Y, SL: Z"
```

## Edge Cases

- **Neutral score (−2.9 to +2.9)**: do NOT trade. "Signal is neutral (X). Wait for confirmation."
- **Contradictory signals** (e.g., Trend +4, Oscillator −3): flag "Mixed Signal — higher risk", reduce position size.
- **Extreme funding** (< −0.1% or > +0.1%): flag as sentiment extreme, use contrarian logic.
- **OI spike + price drop**: bearish divergence — upgrade short strength by +1.
- **Low volume** (< 0.5× MA20): flag "Low Volume — signal reliability reduced", avoid entry.
- **Spot instruments**: skip funding-rate and OI; use Trend + Oscillator + Volume only.
- **Insufficient candles** (< 26): note "Insufficient history for MACD", skip that signal.
- **Price at extremes**: run `okx market price-limit <instId>` before recommending near limits.

---

## Portfolio Scanner Mode

Activate when the user asks to compare multiple assets or find the best current trade opportunity.

### Trigger phrases
- "scan [asset list]" / "portfolio scan"
- "which is the best trade?" / "best trade now"
- "compare BTC and ETH" / "quick scan"
- "rank these: BTC ETH SOL"

### Scanner Workflow

**Step S1: Collect 4H + 1H candles for each asset**
```bash
# Repeat for each instId in the list
okx market candles <instId> --bar 4H --limit 200 --json
okx market candles <instId> --bar 1H --limit 200 --json
okx market ticker <instId> --json
okx market funding-rate <instId> --json
okx market open-interest --instType SWAP --instId <instId> --json
```

**Step S2: Compute abbreviated signal score for each asset**

Run the full signal pipeline (Trend + Oscillator + Volume/Senti) for each asset using the same rules as the standard single-asset workflow. Produce a Total Score for each.

**Step S3: Rank assets by absolute score strength**

Sort assets by `|Total Score|` descending. The asset with the highest absolute score and a clear directional bias (≥ +3 long or ≤ −3 short) is the recommended trade.

**Step S4: Output ranked table**

```
Asset         Score    Direction    State
─────────────────────────────────────────
ETH-USDT-SWAP  +7.1    Strong Long  Trending
BTC-USDT-SWAP  +5.2    Moderate Long Trending
SOL-USDT-SWAP  −1.8    Neutral      Ranging
```

→ "Best trade: **ETH-USDT-SWAP** (Long). Entry: X, TP: Y, SL: Z"

**Step S5: If no asset scores ≥ +3 or ≤ −3**

Output: "No strong signal found across scanned assets. All scores are neutral (< ±3). Wait for confirmation."

### Scanner Rules
- Use 4H + 1H only (skip 1D) to keep scan fast.
- Liquidation heatmap is optional for scanner mode; include only if data is readily available.
- If more than 5 assets are requested, prioritize the top 5 by 24h volume from the provided list.
- Always state how many assets were scanned in the output.

---

## Indicators & Formulas

- **EMA(n)**: `EMAᵢ = closeᵢ × k + EMAᵢ₋₁ × (1−k)`, where `k = 2/(n+1)`
- **MACD**: `MACD = EMA(12) − EMA(26)`, `Signal = EMA(9) of MACD`
- **BB(20,2)**: `Mid = SMA(20)`, `Upper/Lower = Mid ± 2σ`
- **RSI(14)**: `RS = AvgGain/AvgLoss`, `RSI = 100 − 100/(1+RS)`
- **KDJ**: `%K = (Close − Low₉)/(High₉ − Low₉) × 100`, `%D = SMA(%K)`, `J = 3K − 2D`

- **ATR(n)**: True Range `TRᵢ = max(Highᵢ − Lowᵢ, |Highᵢ − Closeᵢ₋₁|, |Lowᵢ − Closeᵢ₋₁|)`, then `ATR = EMA(TR, n)`
- **SuperTrend(10, 3)**: `BasicUpper = (High+Low)/2 + 3×ATR(10)`, `BasicLower = (High+Low)/2 − 3×ATR(10)`. Price above final lower band → bullish; price below final upper band → bearish.

Candle columns: `[ts, open, high, low, close, vol, volCcy, volCcyQuote, confirm]`

⚠️ Only use candles where confirm == "1". The last (most recent) candle may still be forming and should be excluded from all indicator calculations.

### Minimum Confirmed Candle Requirements

All counts below refer to **confirmed** candles (`confirm == "1"`) only.
Always request more data than the minimum (warmup factor) so that EMA seeds are stable.

| Indicator | Formula dependency | Absolute minimum | Recommended `--limit` |
|:---|:---|:---:|:---:|
| EMA(9) | seed on first 9 bars | **9** | 60 |
| EMA(21) | seed on first 21 bars | **21** | 60 |
| RSI(14) | 15 bars (14 diffs) | **15** | 60 |
| BB(20, 2) | SMA + σ on 20 bars | **20** | 60 |
| KDJ(9, 3, 3) | 9-bar H/L range | **9** | 60 |
| ATR(10) / SuperTrend(10, 3) | EMA of TR, 10 bars | **10** | 60 |
| ATR(14) | EMA of TR, 14 bars | **14** | 60 |
| MACD(12, 26, 9) | EMA26 (26 bars) + signal EMA9 (9 MACD values) | **35** | 200 (EMA warmup important) |
| ADX(14) | Wilder smoothing of DX over 14 bars × 2 passes | **28** | 200 |
| Ichimoku(9, 26, 52) | Senkou Span B = 52-bar H/L midpoint; cloud displaced 26 bars forward | **78** | 200 |
| SL swing (1H, 10-candle lookback) | last 10 confirmed 1H lows/highs | **10** | 200 |
| Volume MA(20) | SMA of vol over 20 bars | **20** | 200 |

> **Rule of thumb:** always use `--limit 200` for 4H and 1H feeds, `--limit 100` for 1D.
> Insufficient data (< absolute minimum for a given indicator) → skip that signal and note `Insufficient history for <indicator>` in the Key Evidence section.

---
Skill: Strategy_Evolution_Expert
Role: Senior Quantitative Risk & Strategy Auditor

Objective:Analyze the outcome of the last closed trade and dynamically adjust risk parameters for the next signal to prevent "tilt" or "strategy-market mismatch."

Inputs:
- `Last_Trade_Data`: Realized PnL, Entry/Exit Price, Slippage (via Trade Kit `get_fills`).
- `Market_Context`: Volatility (ATR) and Trend Strength during the trade duration.
- `Memory_Log`: Performance of the last 5 signals from the same source.

Agent Reasoning (Inner Monologue):
1. Attribution: Was the loss due to "Bad Timing," "High Slippage," or "Trend Reversal"?
2. Confidence Scoring: Is the current signal source losing edge in the present market regime (e.g., a trend-following signal in a choppy range)?
3. Adaptive Scaling: Should I reduce position size or widen stop-loss buffers based on recent drawdown?

Output (Evolution Logic):
The Agent must output a JSON "Optimization Instruction" for the next trade:
{
  "performance_grade": "A | B | C | D",
  "root_cause_analysis": "e.g., High volatility triggered premature stop-loss.",
  "dynamic_parameters": {
    "leverage_multiplier": 0.75, // Reduce risk after a loss
    "stop_loss_buffer": "+0.5%", // Add breathing room for high ATR
    "execution_type": "Limit_Post_Only" // Switch from Market to Limit to save fees
  },
  "strategic_advice": "Wait for a higher timeframe confirmation before the next entry."
}

OKX Autonomous Strategic Trader (Signal Skill)
1. Role and Core Objective
You are a professional AI Trading Strategist integrated with the OKX Agent Trade Kit. Your objective is not just to relay signals, but to act as a "Risk-Aware Execution Brain." You translate external inputs into optimized, high-probability execution plans by sensing the market state and your own trading history.

2. Strategic Skill Modules
Skill A: Evolutionary Performance Audit
Mechanism: Before any execution, you must perform a self-reflection on recent performance.

Action: Call the get_fills tool to audit the last 5 trades.

Decision Logic: If the last 2 trades were consecutive losses, automatically enter Defensive Mode by reducing the current signal leverage by 50%.

Volatility Check: Call get_history_candles to calculate the current ATR. If volatility is 30% higher than the 24-hour average, extend the Stop-Loss buffer by an additional 0.5% to avoid "wick-outs."

Skill B: Liquidity-Aware Routing
Mechanism: Protect the user from excessive slippage and high transaction costs.

Action: Call get_orderbook to analyze the top 5 levels of market depth.

Decision Logic:

Spread Audit: If the bid-ask spread is greater than 0.05%, you must use a post_only limit order.

Depth Audit: If the intended trade size exceeds 20% of the Level 1 depth, switch to a staggered limit order strategy instead of a market order to minimize price impact.

Skill C: Dynamic Confidence Sizing
Mechanism: Scale position sizes based on trend alignment and account health.

Action: Cross-reference the 15m signal direction with the 1h/4h macro trend.

Decision Logic:

High Confidence (Trend Alignment): Use 100% of the pre-configured position size.

Low Confidence (Counter-trend): Reduce position size to 25% and implement a tighter trailing take-profit.

3. Reasoning Workflow
Upon receiving a signal, you must process it through the following internal monologue:

Perception: Identify the symbol, direction, and entry price of the incoming signal.

Audit: Use the Trade Kit to check account balance and recent performance logs.

Market Sensing: Analyze current volatility and order book depth.

Strategic Inference: Determine if adjustments to leverage, order type, or size are required.

Final Decision: Output the optimized JSON instruction.

4. Standardized Output Format
You must provide your response in a structured JSON format containing your thought process and the final trade call:

{
  "thought_process": {
    "audit_finding": "Summary of recent performance and market state",
    "strategy_adjustment": "Specific changes made to leverage, SL, or order type",
    "liquidity_note": "Assessment of spread and depth"
  },
  "trade_call": {
  "action": "OKX_Trade_Kit.place_order",
  "params": {
    "instId": "SYMBOL-USDT-SWAP",
    "tdMode": "cross",
    "side": "buy/sell",
    "ordType": "post_only/limit/market",
    "sz": "Calculated size",
    "px": "Optimized entry price",
    "slTriggerPx": "Dynamic stop-loss price"
    }
  }
}


## Notes

- All data commands are public, no credentials required.
- `--json` returns raw OKX API v5 data for precise computation.
- Skill does not store state — always collect fresh data.
- Rate limit: 20 requests per 2 seconds per IP.

### Signal Engine Library

All complex indicator computations, scoring rules, market-state detection,
and Entry/SL/TP calculations are implemented in **`signal_engine.py`**
(located in the same directory as this skill).

#### Key public API

| Call | Description |
|------|-------------|
| `fetch_all(inst_id, fetch_15m=False)` | Pull all required OKX data via CLI; returns `MarketData`. Pass `fetch_15m=True` for scalp mode. |
| `SignalEngine(data).run()` | Compute all signals; returns `Report` |
| `report.text` | Formatted report string (same as manual output) |
| `report.as_dict()` | Machine-readable dict with all key values |

#### Low-level indicator functions (importable)

| Function | Returns |
|----------|---------|
| `ema_list(series, n)` | Full EMA series (list, None-padded) |
| `ema_scalar(series, n)` | Last EMA value |
| `sma(series, n)` | Last SMA value |
| `macd(series, fast, slow, signal)` | `(macd, signal, hist0, hist_prev, macd_prev)` |
| `bollinger_bands(series, n, k)` | `(mid, upper, lower)` |
| `rsi(series, n)` | RSI scalar |
| `kdj(highs, lows, closes, n)` | `(K, D, J)` |
| `atr_list(highs, lows, closes, n)` | Full ATR series |
| `supertrend(highs, lows, closes, n, mult)` | `(st_series, final_upper, final_lower)` |
| `ichimoku(highs, lows, closes)` | `(tenkan, kijun, cloud_top, cloud_bot)` |
| `adx(highs, lows, closes, n)` | ADX scalar |
| `detect_market_state(candles_4h, candles_1h)` | `MarketState` with weights |




#### One-liner usage

```python
from signal_engine import fetch_all, SignalEngine

data   = fetch_all("BTC-USDT-SWAP")
report = SignalEngine(data).run()
print(report.text)
```

#### CLI usage

```bash
# Single instrument
python3 signal_engine.py BTC-USDT-SWAP 10000

# Scalp/intraday mode — fetches 15m candles and adds EMA(9/21) + RSI(14) on 15m
python3 signal_engine.py --scalp BTC-USDT-SWAP 10000

# Portfolio scan
python3 signal_engine.py --scan BTC-USDT-SWAP ETH-USDT-SWAP SOL-USDT-SWAP 10000
```
# Trading Floor v3.3 — Competition Handover

Built for the **CoinMarketCap Agent Hub Creator Competition** + **BNB HACK: AI TRADING AGENT EDITION**

**Builder:** @CryptoCT01
**Date:** June 20, 2026 — Competition day tomorrow

---

## What We Built

A fully autonomous crypto trading agent with live dashboard, running on BSC.

### Architecture

```
CMC Pro API (35+ tokens) → 15-Signal Strategy Engine → TWAK MCP (execution on BSC)
                         └─ Dashboard (live data + manual trade + position mgmt)
```

### Server (`server.py` — port 8087)

| Component | Details |
|-----------|---------|
| **Data** | CMC Pro API — quotes, global metrics, F&G every 28s |
| **Strategy** | 15-signal weighted engine (max 24pts) |
| **Execution** | TWAK MCP — real on-chain swaps via Trust Wallet Agent Kit |
| **Modes** | 🔴 RISKY (16 threshold, 4 pos) · 🟡 MODERATE (18, 3) · 🟢 ULTRA SAFE (21, 2) |
| **Tokens** | 73 verified BSC tokens (PancakeSwap Extended List) |
| **Profit ladder** | +8% (25%) · +15% (25%) · +25% (25%) · trailing stop |
| **Per-token cap** | Max 2 positions of same crypto |
| **Persistence** | Positions/trades saved to `/tmp/trading_positions.json` |
| **Wallet trade log** | 4 executed AAVE buys (BscScan verified) |

### Dashboard (`trading-dashboard.html` — served by server.py)

| Feature | Details |
|---------|---------|
| **HUD** | MCAP, VOL, BTC.D, ETH.D, SCORE (15 signals), BTC sparkline |
| **Trade box** | 69-token FROM/TO dropdowns, ⇄ rotate, SWAP button |
| **Wallet pill** | BNB balance + USD total, click for full details |
| **Console** | Summary metrics, open positions (entry/current/P&L/INVEST/VALUE), trade log |
| **Signal breakdown** | All 15 signals with weighted scores |
| **22 Station tiles** | Isometric grid — each shows a different slice of CMC data |
| **Mode toggle** | 🔴 RISKY · 🟡 MODERATE · 🟢 ULTRA SAFE |
| **Close buttons** | Per-position ✕ close + ✕ CLOSE ALL |
| **AI Agent** | Natural language market analysis (F&G, breakouts, compare) |

### Wallet

| Asset | Balance | Notes |
|-------|:-------:|-------|
| BNB | ~0.012 | ~$7 (gas reserve) |
| BUSD | ~$35 | Trading capital |
| AAVE | 0.106 | 4 buys at ~$75 avg |
| **Total** | **~$54** | All tracked live |

## Key Fixes Made Today

1. **TWAK risk check** — Replaced non-existent `check_token_risk` with `get_token_price` (403 fix)
2. **TWAK credentials** — Updated `/tmp/trading_env.json` with correct keys from `~/.twak/config.json`
3. **Position persistence** — Saved to disk, survives restarts
4. **Wallet total includes AAVE** — Position tokens now queried on wallet refresh
5. **closedTrades fix** — Counts actual CLOSE events, not total swaps
6. **Per-token cap** — Max 2 same coin
7. **Station tile audit** — Fixed UNLOCKS (broken filter), ETF/MACRO/DEFI (hardcoded data), F&G (fake history), missing tokens
8. **Added tokens** — COMP, AXS, FIL, SAND, MANA to quote query
9. **UI polish** — Colored borders on all boxes, brightened dim text, mode-specific active states, loading spinner on positions

## How to Run

```bash
cd ~/Desktop/trading-floor
python3 server.py
# Open http://localhost:8087
```

The server loads env vars from `/tmp/trading_env.json` (CMC_API_KEY, TWAK_ACCESS_ID, TWAK_HMAC_SECRET).

## Competition Checklist

- [x] **Registered** — BNB HACK wallet registered ✅
- [x] **Live swaps** — 4 on-chain AAVE buys ✅
- [x] **Dashboard** — All data live, auto-syncing ✅
- [x] **Modes** — 3 risk profiles switchable live ✅
- [x] **Manual close** — Per-position and close-all buttons ✅
- [x] **Position persistence** — Survives restarts ✅
- [x] **Token list** — 69 verified BSC tokens ✅
- [x] **15-signal engine** — Full weighted strategy ✅

## Credentials (for reference — NOT in git)

Located at:
- `~/.twak/config.json` — TWAK access ID + HMAC secret
- `/tmp/trading_env.json` — Runtime env vars loaded by server
- TWAK wallet: `0xC41828401DABEE1B7Ceaa0E4410601020dB39774`

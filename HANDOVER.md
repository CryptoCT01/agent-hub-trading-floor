# Trading Floor v3.5 — Competition Handover

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
| **Persistence** | Positions/trades saved to `/tmp/trading_positions.json`, custom strategy config saved to `/tmp/strategy_custom.json` |
| **Wallet trade log** | 4 executed AAVE buys (BscScan verified) |

### Dashboard (`trading-dashboard.html` — served by server.py)

| Feature | Details |
|---------|---------|
| **HUD** | MCAP, VOL, BTC.D, ETH.D, SCORE (15 signals), BTC sparkline |
| **API TOGGLES pill** | Bigger ⏻ button with 3 status dots (ALL API, NON-ESSENTIAL, TRADING). Dots show green/red at a glance without expanding. ⏻ panel has safety interlock: API off auto-pauses trading. |
| **Trade box** | 69-token FROM/TO dropdowns, ⇄ rotate, SWAP button |
| **Wallet pill** | BNB balance + USD total, click shows PORTFOLIO details |
| **Console** | Summary metrics, open positions (entry/current/P&L/INVEST/VALUE), trade log |
| **Signal breakdown** | All 15 signals with weighted scores |
| **22 Station tiles** | Isometric grid — each shows a different slice of CMC data |
| **Strategy Tracker pill** | Compact HUD stat (after ETH.D) showing live trade count. Click opens station panel with full trade history, volume, TRADES/WIN RATE/VOLUME/SWAPS metrics. |
| **Mode toggle** | 🔴 RISKY · 🟡 MODERATE · 🟢 ULTRA SAFE with smaller buttons to prevent overlap |
| **⚙️ Strategy Settings** | Gear icon between `|` and RISKY. Opens modal to customise MAX TRADES and $ PER TRADE per mode (defaults: RISKY 4×$1, MODERATE 3×$1, ULTRA SAFE 2×$1). SAVE persists to disk, RESET restores defaults. ⚠️ Risk disclaimer included. |
| **Close buttons** | Per-position ✕ close + ✕ CLOSE ALL |
| **AI Agent** | Natural language market analysis (F&G, breakouts, compare) |

### Wallet

| Asset | Balance | Notes |
|-------|:-------:|-------|
| BNB | ~0.012 | ~$7 (gas reserve) |
| BUSD | ~$35 | Trading capital |
| AAVE | 0.106 | 4 buys at ~$75 avg |
| **Total** | **~$54** | All tracked live |

## Key Fixes & Features Added (v3.4 → v3.5)

1. **TWAK risk check** — Replaced non-existent `check_token_risk` with `get_token_price` (403 fix)
2. **TWAK credentials** — Updated `/tmp/trading_env.json` with correct keys from `~/.twak/config.json`
3. **Position persistence** — Saved to disk, survives restarts
4. **Wallet total includes AAVE** — Position tokens now queried on wallet refresh
5. **closedTrades fix** — Counts actual CLOSE events, not total swaps
6. **Per-token cap** — Max 2 same coin
7. **Station tile audit** — Fixed UNLOCKS (broken filter), ETF/MACRO/DEFI (hardcoded data), F&G (fake history), missing tokens
8. **Added tokens** — COMP, AXS, FIL, SAND, MANA to quote query
9. **UI polish** — Colored borders on all boxes, brightened dim text, mode-specific active states, loading spinner on positions
10. **API TOGGLES redesign** — Bigger ⏻ icon, 3 status dots (green=ON/red=OFF), "API TOGGLES" header label, dots sync every 30s
11. **Backend custom strategy overrides** — `CUSTOM_MODE_CONFIG` layered on `MODE_CONFIG`; `/api/strategy/settings` endpoint for GET/SAVE/RESET; persists to `/tmp/strategy_custom.json`
12. **⚙️ Strategy Settings modal** — 3-column layout (RISKY/MODERATE/ULTRA SAFE), editable MAX TRADES + $ PER TRADE inputs, ⚠️ risk disclaimer, SAVE + RESET buttons
13. **STRATEGY TRACKER** — Station tile renamed from STRATEGY TESTER, icon changed 🧪→📊. Compact HUD pill shows live trade count. Station panel loads full trade history + performance data.
14. **PORTFOLIO label** — Wallet expanded view says PORTFOLIO instead of TOTAL, rendered in gold
15. **Smaller control buttons** — Ctrl buttons shrunk ~8% (0.65rem→0.6rem, padding 4px14px→3px10px) to prevent overlapping the wallet pill

## ⏻ Controls Panel

Click the **LIVE ⏻** pill in the top-right HUD to open the toggle panel:

| Toggle | What it does | Strategy safe? |
|--------|-------------|:--------------:|
| 🔴 ALL API OFF | Stops all CMC data calls. Trading auto-paused. | ❌ Only with Trading OFF |
| 🟡 NON-ESSENTIAL OFF | Stops global-metrics + F&G. Keeps quotes live. | ✅ Yes — prices still update |
| 🔴 TRADING OFF | No new auto-entries. Manual trades + stop-losses work. | ✅ Yes |

Three colored dots under the ⏻ icon reflect toggle state at a glance:
- **Top dot** — ALL API status
- **Middle dot** — NON-ESSENTIAL status
- **Bottom dot** — TRADING & STRATEGY status

## ⚙️ Strategy Customisation

Click the ⚙️ gear icon (between `|` and RISKY in the bottom control bar) to open the settings modal:

| Mode | Default Max Trades | Default $/Trade |
|------|:------------------:|:----------------:|
| 🔴 RISKY | 4 | $1.00 |
| 🟡 MODERATE | 3 | $1.00 |
| 🟢 ULTRA SAFE | 2 | $1.00 |

Custom values are saved to disk (`/tmp/strategy_custom.json`) and restored on server restart.

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
- [x] **Custom strategy settings** — Per-mode trade count + dollar amount customisable via ⚙️ ✅
- [x] **Live status dots** — Toggle state visible at a glance on the LIVE pill ✅
- [x] **Strategy Tracker** — HUD pill with live trade count + full station panel ✅
## Credentials (for reference — NOT in git)

Located at:
- `~/.twak/config.json` — TWAK access ID + HMAC secret
- `/tmp/trading_env.json` — Runtime env vars loaded by server
- `/tmp/strategy_custom.json` — Custom strategy overrides (persisted)
- TWAK wallet: `0xC41828401DABEE1B7Ceaa0E4410601020dB39774`

---

## 🚧 Unfinished: Trade Panel ▲ Expand Upgrade

### What was attempted

The **▲ expand button** on the left-side trade box (opens `function x()`) was redesigned to be a richer swap panel. The original was basic — just a title + FROM/TO/AMOUNT labels + input + SWAP button.

The intended redesign:

```
┌─────────────────────────┐
│   ⚡ MANUAL SWAP        │
│     BNB → BUSD          │
│                         │
│ [25%][50%][75%][MAX]    │
│                         │
│  [    0.001    ]        │
│  Balance: 0.0118 BNB    │
│                         │
│  RATE      $585.64      │
│  USD VALUE $0.57        │
│                         │
│  [    ↻ SWAP     ]      │
└─────────────────────────┘
```

**New elements added:**
- `tp-head` / `tp-title` / `tp-pair` — styled header with BNB → BUSD pair display (gold/cyan)
- `tp-quick` / `tp-qbtn` — 25%/50%/75%/MAX quick-amount buttons
- `tp-bal` — live balance display ("Balance: 0.0118 BNB")
- RATE row — live price of the FROM token from `LIVE_QUOTES`
- Keep existing USD VALUE row and SWAP button
- `qAmt(pct)` function — calculates `bnbBal * percentage` and populates the input

### What broke

The change introduced a **JavaScript syntax error** that prevented the entire `<script>` block from executing. Symptoms:
- Isometric trading floor grid did not render (blank center area)
- `selectStation` was undefined (all JS after the error point failed)
- Browser console showed empty JS error (character-level issue)

**Root cause:** The `p.innerHTML` string (line 624) had an extra trailing backslash before the closing quote. The file ended with 3 backslashes followed by `";` where it should have had 1 backslash followed by `";`.

Specifically:
- WRONG (broke the JS): `</button>\\\";` (3 backslashes)
- CORRECT (works): `</button>\";` (1 backslash)

The rule for the very end of the string:
- `\"` = escaped quote inside the JS string (produces `"` in the HTML attribute)
- `"` = closes the JavaScript string
- `;` = ends the statement

So the file should read: `...onclick=\\"m();v()\\">↻ SWAP</button>\";`


### Why it happened

The escaping gets complex because:
1. The `p.innerHTML` string uses `\"` for HTML attribute delimiters inside the JavaScript string
2. The string is inside an HTML file, so everything is in the same context
3. The patch tool applied a string that had `\\\"` which resolved to `\"` in the file — but the original code used `\"` directly
4. When editing inline HTML-in-JS-in-HTML, one extra/missing backslash breaks the whole script silently

### What the next session needs to do

1. **Restore from git** before attempting: `git checkout HEAD -- trading-dashboard.html`
2. The CSS classes already exist in `<style>` (`.tp-head`, `.tp-title`, `.tp-pair`, `.tp-pair-from`, `.tp-pair-arrow`, `.tp-pair-to`, `.tp-quick`, `.tp-qbtn`, `.tp-bal` — added in v3.5)
3. Replace the `p.innerHTML` string in `function x()` (line ~624) with the new HTML (see design above)
4. Update `function v()` to populate the new elements (`_pf`, `_pt`, `_bal`, `_rate`) instead of the old ones (`_0`, `_1`, `_2`)
5. Add `function qAmt(pct)` for the quick-amount buttons
6. **CRITICAL — the exact ending matters.** The last characters of the file should be:
   `...onclick=\\"m();v()\\">↻ SWAP</button>\";`
   - `\\"` = escaped quote for the HTML onclick attribute
   - `"` = closes the JavaScript string
   - `;` = ends the statement
   One extra backslash before the final quote will break the entire page silently.
7. Validate JS syntax before restarting:
   ```
   node -e "new Function(require('fs').readFileSync('trading-dashboard.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1]); console.log('OK')"
   ```
8. The `qAmt` function references `bnbBal` global which is populated by `fetchWallet()` — ensure wallet has been fetched before panel opens

### Verifying success

- The isometric grid renders with all 22 station tiles
- Clicking ▲ on the trade box opens the styled panel
- Quick-amount buttons fill in the correct percentage of BNB balance
- RATE shows the live price of the FROM token
- SWAP button still executes the trade correctly

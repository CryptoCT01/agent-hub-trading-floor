# Trading Floor v3.5 — Competition Handover

Built for the **CoinMarketCap Agent Hub Creator Competition** + **BNB HACK: AI TRADING AGENT EDITION**

**Builder:** @CryptoCTO1
**Date:** June 20-21, 2026 — Submission lock June 21st 12:00 UTC

---

## 🏆 V1 Featured & Reposted by CoinMarketCap

Our original version (V1) was officially featured and reposted by CoinMarketCap on X/Twitter:
[https://x.com/CoinMarketCap/status/2067785230740816200](https://x.com/CoinMarketCap/status/2067785230740816200)

We are now on V3.5 — miles ahead from that original version.

---

## What We Built Today (June 20 Session)

### 🏁 Competition Mode Toggle (+3% Early Exit + 22h/24h Guarantee)
- New `COMPETITION_MODE` flag — toggled from dashboard via 🏁 COMP pill in bottom bar
- COMP OFF (default) = normal strategy only
- COMP ON = adds:
  - **+3% early-exit** — first trade of the day sells 50% at +3% (flagged at open)
  - **22h/24h rolling guarantee** — first check 22h after competition start, then every 24h
  - Auto-closes **best performer** if no trade closed naturally in the window
- Timer is independent of COMP toggle — `COMPETITION_START` set at server launch (+18h from now)
- Backend: `/api/strategy/competition?on=true/false` endpoint
- Frontend: 🏁 pill with gold border (OFF) / purple border (ON), click-expand explanation panel

### 🎨 22 Station Tiles — 3D Isometric Upgrade (CSS only)
- **Stepped box-shadows** (5 layers) for block depth illusion
- **Directional lighting** — gradient from lighter top-left to darker bottom-right
- **Category-colored neon pulse** — each row glows its own color via `--row-c` CSS variable:
  - Row 1 (TRADING): cyan | Row 3 (MACRO): gold | Row 5 (SENTIMENT): purple | Row 7 (THEMES): orange | Row 9 (ON-CHAIN): green
- **`@keyframes neon-hum`** — 3-second slow pulse between 4px and 12px glow
- **Floor spotlight** — radial gradient behind the grid for depth perception
- **Stronger hover lift** — `translateY(-5px)` with extended shadow
- **No JS or HTML touched** — 100% CSS safe

### 📊 Real Charts for All Tokens
- ETH, SOL, UNI, LINK now get real 20-point price history stored every 28s (same as BTC)
- Generic `/api/chart/{symbol}` endpoint replaces hardcoded `/api/chart/btc`
- Frontend falls back to synthetic data if no history yet
- Chart modal buttons (BTC/ETH/SOL/UNI/LINK) all show real candle-like data

### 🛡️ Per-Token Cap Change
- Changed from max 2 → max 1 position per token
- Updated both server.py logic and dashboard ABOUT text

### 🖥️ Splash Screen Updates
- Added **TWAK** pill to feature row (5th pill, cyan)
- Added **Trust Wallet** to footer credit line
- Reordered hashtag pills: `#CMCAgentHub | @CryptoCTO1 | @coinmarketcap`
- @CryptoCTO1 now **purple** to stand out
- 69 ASSETS changed to **orange** (was cyan, freed cyan for TWAK)

---

## Key Fixes & Features Added (v3.4 → v3.5)

1. **TWAK risk check** — Replaced non-existent `check_token_risk` with `get_token_price` (403 fix)
2. **TWAK credentials** — Updated `/tmp/trading_env.json` with correct keys from `~/.twak/config.json`
3. **Position persistence** — Saved to disk, survives restarts
4. **Wallet total includes AAVE** — Position tokens now queried on wallet refresh
5. **closedTrades fix** — Counts actual CLOSE events, not total swaps
6. **Per-token cap** — Max 1 same coin
7. **Station tile audit** — Fixed UNLOCKS (broken filter), ETF/MACRO/DEFI (hardcoded data), F&G (fake history), missing tokens
8. **Added tokens** — COMP, AXS, FIL, SAND, MANA to quote query
9. **UI polish** — Colored borders on all boxes, brightened dim text, mode-specific active states, loading spinner on positions
10. **API TOGGLES redesign** — Bigger ⏻ icon, 3 status dots (green=ON/red=OFF), "API TOGGLES" header label, dots sync every 30s
11. **Backend custom strategy overrides** — `CUSTOM_MODE_CONFIG` layered on `MODE_CONFIG`; `/api/strategy/settings` endpoint for GET/SAVE/RESET; persists to `/tmp/strategy_custom.json`
12. **⚙️ Strategy Settings modal** — 3-column layout (RISKY/MODERATE/ULTRA SAFE), editable MAX TRADES + $ PER TRADE inputs, ⚠️ risk disclaimer, SAVE + RESET buttons
13. **STRATEGY TRACKER** — Station tile renamed from STRATEGY TESTER, icon changed 🧪→📊. Compact HUD pill shows live trade count. Station panel loads full trade history + performance data.
14. **PORTFOLIO label** — Wallet expanded view says PORTFOLIO instead of TOTAL, rendered in gold
15. **Smaller control buttons** — Ctrl buttons shrunk ~8% (0.65rem→0.6rem, padding 4px14px→3px10px) to prevent overlapping the wallet pill
16. **🏁 Competition Mode** — COMP toggle with +3% early-exit + 22h/24h rolling guarantee close
17. **3D Tile Upgrade** — Stepped shadows, neon pulse, category glow, floor spotlight, directional lighting
18. **Real Charts** — ETH/SOL/UNI/LINK get real price history (was synthetic straight lines)
19. **Splash Screen** — Added TWAK pill, Trust Wallet credit, reordered/colored hashtags
20. **Per-token cap** — Max 2 → max 1 position

---

## 🏁 Competition Mode Details

### Toggle
- **🏁 COMP pill** in bottom bar between trade box and wallet
- Default: OFF (normal strategy)
- Click to toggle ON/OFF — explanation panel shows what each mode does

### When COMP ON:
1. **+3% early-exit** — first trade opened each day gets `is_early_exit` flag → sells 50% at +3%
2. **22h/24h guarantee** — timer counts from `COMPETITION_START` (set at server launch: +18h)
   - First check: COMPETITION_START + 22h
   - Subsequent: every 24h
   - If no close in window → force-close **best performer** (highest P&L %)
   - Natural closes (profit ladder, stop-loss) reset the timer

### When COMP OFF:
- Normal profit ladder only (+8%/+15%/+25%)
- Trailing stop-loss
- No timed forced closes

### Implementation
- All competition features guarded behind `COMPETITION_MODE` flag
- Toggle via dashboard or `/api/strategy/competition?on=true/false`
- Competition timer runs independently of toggle state

---

## 🚧 Unfinished: Trade Panel ▲ Expand Upgrade

### What was attempted
The **▲ expand button** on the left-side trade box (opens `function x()`) was attempted to be redesigned with:
- `tp-head` / `tp-title` / `tp-pair` — styled header with pair display
- `tp-quick` / `tp-qbtn` — 25%/50%/75%/MAX quick-amount buttons
- `tp-bal` — live balance display
- RATE row — live price from `LIVE_QUOTES`

### What went wrong
The change introduced a JS syntax error due to backslash escaping in the `p.innerHTML` string. Rolled back via git checkout.

### Current state
The original basic panel (FROM/TO/AMOUNT/USD/SWAP) remains — **functional, not fancy**. Not worth the risk before submission lock.

---

## How to Run

```bash
cd ~/Desktop/trading-floor
python3 server.py
# Open http://localhost:8087
```

The server loads env vars from `/tmp/trading_env.json` (CMC_API_KEY, TWAK_ACCESS_ID, TWAK_HMAC_SECRET).

---

## Competition Timeline

| Date | Event |
|------|-------|
| June 21st, 12:00 UTC | **Submission lock** — code freeze |
| June 22nd – 28th | Live Trading Window — agent tracked in real market conditions |
| June 29th – July 5th | Judging — PnL replay + panel review |
| Week of July 6th | Winners announced |

---

## Competition Checklist

- [x] **Registered** — BNB HACK wallet registered
- [x] **V1 reposted by CoinMarketCap** — official endorsement
- [x] **Live swaps** — 4 on-chain AAVE buys (BscScan verified)
- [x] **Dashboard** — All data live, auto-syncing
- [x] **Modes** — 3 risk profiles switchable live
- [x] **API Toggles** — 3-tier safety controls with status dots
- [x] **Custom strategy settings** — Per-mode trade count + dollar amount via ⚙️
- [x] **Manual close** — Per-position and close-all buttons
- [x] **Position persistence** — Survives restarts
- [x] **Token list** — 73 verified BSC tokens
- [x] **15-signal engine** — Full weighted strategy
- [x] **Portfolio wallet** — QR deposit, withdraw, quick sell
- [x] **🏁 Competition mode** — +3% early exit + 22h/24h guarantee
- [x] **Real charts** — BTC/ETH/SOL/UNI/LINK price history
- [x] **3D tiles** — Neon glow, stepped shadow, directional lighting
- [x] **Per-token cap** — Max 1 position per cryptocurrency
- [x] **GitHub: v3.5 tagged**

---

## Credentials (for reference — NOT in git)

Located at:
- `~/.twak/config.json` — TWAK access ID + HMAC secret
- `/tmp/trading_env.json` — Runtime env vars loaded by server
- `/tmp/strategy_custom.json` — Custom strategy overrides (persisted)
- TWAK wallet: `0xC41828401DABEE1B7Ceaa0E4410601020dB39774`
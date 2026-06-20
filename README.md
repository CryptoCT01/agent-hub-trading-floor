# Trading Floor v3.5 — CMC Buildathon + BNB HACK

**Built by @CryptoCT01** for the CoinMarketCap Agent Hub Creator Competition and BNB HACK: AI TRADING AGENT EDITION.

A fully autonomous crypto trading agent with live dashboard, running on BSC.

## 🚀 Quick Start

```bash
cd ~/Desktop/trading-floor
python3 server.py
# Open http://localhost:8087
```

Server loads env vars from `/tmp/trading_env.json` (CMC API key + TWAK credentials).

## 🏗️ Architecture

```
CMC Pro API (35+ tokens) → 15-Signal Strategy Engine → TWAK MCP (on-chain BSC swaps)
                         └─ trading-dashboard.html (live data + trades + positions)
```

## 📊 Features

| Feature | Description |
|---------|-------------|
| **15-Signal Engine** | Weighted strategy (max 24pts) — momentum, volume, relative strength, derivatives, narratives, technical, fundamentals, and more |
| **3 Strategy Modes** | 🔴 RISKY (16 thr, 4 pos) · 🟡 MODERATE (18 thr, 3 pos) · 🟢 ULTRA SAFE (21 thr, 2 pos) |
| **Live Dashboard** | MCAP, VOL, BTC.D, ETH.D, 15 signal dots, BTC sparkline, ticker |
| **69 Verified Tokens** | PancakeSwap Extended List on BSC — all with hardcoded verified addresses |
| **Manual Trading** | Any FROM → any TO swap box, wallet pill with balances |
| **Position Management** | Entry tracking, stop-loss, profit-taking ladder (+8%/+15%/+25%), trailing stop |
| **Per-Token Cap** | Max 2 positions of the same cryptocurrency |
| **Close Buttons** | Per-position ✕ close + ✕ CLOSE ALL (executes on-chain swap) |
| **22 Station Tiles** | Isometric grid — each shows a different slice of live CMC data |
| **AI Agent** | Natural language market analysis via dashboard chat |
| **API TOGGLES pill** | Bigger ⏻ button with 3 live status dots (green=ON/red=OFF). Click to expand controls panel with safety interlock. |
| **⚙️ Strategy Settings** | Gear icon opens modal to customise MAX TRADES + $ PER TRADE per mode. SAVE persists to disk. RESET restores defaults. ⚠️ Risk disclaimer included. |
| **STRATEGY TRACKER** | Compact HUD pill showing live trade count. Click for full performance panel with TRADES/WIN RATE/VOLUME/SWAPS. |
| **Position Persistence** | Saved to disk — survives server restarts |
| **Custom Config Persistence** | Strategy overrides saved to `/tmp/strategy_custom.json` — survives restarts |

## 🗂️ Files

```
trading-floor/
├── server.py               # Python backend (port 8087) — includes custom strategy overrides
├── trading-dashboard.html  # Single-page dashboard (served by server.py)
├── HANDOVER.md             # Competition handover notes (v3.5)
├── README.md               # This file
└── LICENSE                 # GPL v3
```

## ⏻ Controls Panel

Click the **LIVE ⏻** pill in the top-right HUD to toggle:

- **ALL API** — Stops all CMC data. Trading auto-paused for safety.
- **NON-ESSENTIAL** — Keeps prices live (strategy works). HUD/station tiles freeze.
- **TRADING & STRATEGY** — No new auto-entries. Stop-losses and manual trades still work.

Three colored dots under the ⏻ icon show toggle status without expanding:
- **🟢/🔴 Top dot** — ALL API
- **🟢/🔴 Middle dot** — NON-ESSENTIAL
- **🟢/🔴 Bottom dot** — TRADING & STRATEGY

## ⚙️ Strategy Customisation

Click the ⚙️ gear icon in the bottom control bar to customise execution parameters per mode:

| Mode | Default Max Trades | Default $/Trade |
|------|:------------------:|:----------------:|
| 🔴 RISKY | 4 | $1.00 |
| 🟡 MODERATE | 3 | $1.00 |
| 🟢 ULTRA SAFE | 2 | $1.00 |

Custom overrides are saved to disk and restored automatically on restart.

## 🔐 Credentials (not in git)

- `~/.twak/config.json` — TWAK access credentials
- `/tmp/trading_env.json` — Runtime env vars loaded by server
- TWAK wallet: `0xC41828401DABEE1B7Ceaa0E4410601020dB39774`

## 🏆 Competition Checklist

- [x] Registered for BNB HACK
- [x] 4 live on-chain AAVE swaps executed
- [x] 15-signal weighted strategy
- [x] Live dashboard with all data syncing
- [x] Position persistence + manual close
- [x] API usage controls (toggle panel with live status dots)
- [x] Custom strategy settings per mode (gear icon)
- [x] Strategy Tracker HUD pill + station panel
- [x] GitHub: v3.5 tagged

## 📄 License

GNU GPL v3 — Free to use and modify for the competition.

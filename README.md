# Trading Floor v3.69 — CMC Buildathon + BNB HACK

> 🚀 **V1 Official Featured & Reposted by CoinMarketCap**  
> [View the Repost](https://x.com/CoinMarketCap/status/2067785230740816200)

Welcome to V3.69: A fully autonomous crypto trading agent with live dashboard, running on BSC. Expanded significantly since our initial spotlight to feature deep on-chain integration, institutional-grade risk controls, and a Bloomberg-terminal grade command center.

---

## 🌟 Key Architecture & Capabilities

Unlike basic "LLM chat wrappers" that simply query a model for market advice, this platform operates as a decentralized, autonomous trading command center driven by a 15-signal weighted strategy engine, 22 specialized skill stations, and real on-chain execution via TWAK MCP on BSC.

### 1. ⚙️ 3-Tier API Toggle System (Safety Architecture)

To solve the industry-wide problem of API bill spikes and agentic runaway during live scaling, we engineered a frontend-to-backend **3-Tier API Toggle System** with live status indicator dots:

| Mode | What it does | Strategy safe? |
|------|-------------|:--------------:|
| **🔴 ALL API OFF** | Stops all CMC data calls. Trading auto-paused. | ❌ Only with Trading OFF |
| **🟡 NON-ESSENTIAL OFF** | Stops global-metrics + F&G. Keeps quotes live. | ✅ Yes — prices still update |
| **🔴 TRADING OFF** | No new auto-entries. Manual trades + stop-losses work. | ✅ Yes |

Three colored dots under the ⏻ icon reflect toggle state at a glance without expanding the panel.

### 2. 🛡️ Triple-Tier Risk Threshold Matrix

Dynamic user-controlled execution parameters via a live UI toggle:

| Mode | Threshold | Max Positions | $/Trade |
|------|:---------:|:-------------:|:-------:|
| 🔴 **RISKY** | 16/24 | 4 | $1.00 |
| 🟡 **MODERATE** | 18/24 | 3 | $1.00 |
| 🟢 **ULTRA SAFE** | 21/24 | 2 | $1.00 |

**⚙️ Customizable per mode** — click the gear icon to override MAX TRADES and $ PER TRADE for each risk profile. Settings persist to disk across restarts.

### 3. 📊 Macro Visual Intelligence Command Center

- **Live Telemetry:** Interactive streaming price action for BTC, ETH, SOL, and major assets
- **Macro Aggregators:** Real-time calculation of Bitcoin Dominance (BTC.D), Ethereum Dominance (ETH.D), Global Market Cap, and Fear & Greed Index
- **22 Isometric Skill Stations:** Each station shows a different slice of live CMC data (perp scan, ETF flows, narratives, DeFi TVL, L2 activity, and more)
- **15-Signal Breakdown:** Click the SCORE pill to see the full weighted signal breakdown with per-signal scoring
- **Strategy Tracker Pill:** Compact HUD stat showing live trade count. Click for full performance panel with TRADES/WIN RATE/VOLUME/SWAPS

### 4. 💱 Seamless On-Chain BNB Chain Wallet Suite

Fully functional, non-custodial wallet infrastructure wired directly into the dashboard:

- **Frictionless Funding:** Built-in dynamic deposit QR codes — scan from any mobile wallet
- **Fast Liquidity Access:** One-click Quick Sell on any token (90% for non-BNB, BNB-0.002)
- **Manual Backup Routing:** Native swap module bypassing the AI agent for manual AMM trading
- **Portfolio View:** Click the wallet pill to see all token balances with live USD values

### 5. 🏁 Competition Mode

Dedicated toggle for the live judging window:

| Feature | Description |
|---------|-------------|
| **+3% Early Exit** | First trade of the day sells 50% at +3% — guarantees a partial close |
| **22h/24h Rolling Guarantee** | Auto-closes best performer if no trades close naturally |
| **Natural Close Reset** | Profit ladder / stop-loss closes reset the timer |

Toggle OFF → normal strategy. Toggle ON → competition safety net.

---

## 🛠️ Tech Stack & Ecosystem Integrations

- **Backend:** Python — 15-signal weighted strategy engine, HTTP server
- **Frontend:** Vanilla HTML/CSS/JS — single-page dashboard with isometric grid
- **Market Intelligence:** CoinMarketCap Professional API (quotes, global metrics, F&G)
- **Execution:** Trust Wallet Agent Kit (TWAK) MCP — real on-chain swaps on BSC
- **Blockchain:** BNB Smart Chain — PancakeSwap AMM, 73 verified tokens
- **Persistence:** JSON file-based position tracking and strategy configuration

---

## 📜 Intellectual Property & Licensing

This repository is licensed under the **GNU General Public License v3.0 (GPLv3)**.

- **Judges & Evaluators:** Full access to audit, fork, test, and run this codebase for evaluation.
- **Commercial Notice:** Under the reciprocal copyleft clauses of GPLv3, any attempt to copy, fork, or adapt the proprietary architectural features (including the 3-Tier API Toggle System) into a closed-source commercial application is strictly prohibited by law. Original development timelines are permanently anchored on the GitHub immutable ledger.

---

## 🚀 Quick Start

```bash
cd ~/Desktop/trading-floor
python3 server.py
# Open http://localhost:8087
```

Server loads env vars from `/tmp/trading_env.json` (CMC API key + TWAK credentials).

---

## 📊 Features

| Feature | Description |
|---------|-------------|
| **15-Signal Engine** | Weighted strategy (max 24pts) — momentum, volume, relative strength, derivatives, narratives, technical, fundamentals, and more |
| **3 Strategy Modes** | 🔴 RISKY (16 thr, 4 pos) · 🟡 MODERATE (18 thr, 3 pos) · 🟢 ULTRA SAFE (21 thr, 2 pos) |
| **Custom Strategy Settings** | ⚙️ Gear icon — per-mode max trades and $ per trade, persists to disk |
| **Live Dashboard** | MCAP, VOL, BTC.D, ETH.D, 15 signal dots, BTC sparkline, ticker |
| **3-Tier API Toggles** | ALL API / NON-ESSENTIAL / TRADING with live status dots + safety interlock |
| **73 Verified Tokens** | PancakeSwap Extended List on BSC — all with hardcoded verified addresses |
| **Manual Trading** | Any FROM → any TO swap box, wallet pill with balances |
| **Position Management** | Entry tracking, stop-loss, profit-taking ladder (+3%/+8%/+15%/+25%), trailing stop |
| **Per-Token Cap** | Max 1 position per cryptocurrency |
| **Close Buttons** | Per-position ✕ close + ✕ CLOSE ALL (executes on-chain swap) |
| **Portfolio Wallet** | QR deposit, withdraw, quick sell, live USD values |
| **22 Station Tiles** | Isometric grid with neon row glows — each shows a different slice of live CMC data |
| **Real Chart History** | BTC, ETH, SOL, UNI, LINK — live 20-point price history |
| **🏁 Competition Mode** | +3% early exit + 22h/24h rolling guarantee close |
| **AI Agent** | Natural language market analysis via dashboard chat |
| **Position Persistence** | Saved to disk — survives server restarts |
| **Custom Config Persistence** | Strategy overrides saved to `/tmp/strategy_custom.json` |

---

## 🗂️ Files

```
trading-floor/
├── server.py               # Python backend (port 8087)
├── trading-dashboard.html  # Single-page dashboard (served by server.py)
├── HANDOVER.md             # Competition handover notes (v3.69)
├── README.md               # This file
└── LICENSE                 # GPL v3
```

---

## 🔐 Credentials (NOT in git)

- `~/.twak/config.json` — TWAK access credentials
- `/tmp/trading_env.json` — Runtime env vars loaded by server
- TWAK wallet: `0xC41828401DABEE1B7Ceaa0E4410601020dB39774`

---

## 🏆 Competition Checklist

- [x] Registered for BNB HACK
- [x] 4 live on-chain AAVE swaps executed (BscScan verified)
- [x] V1 reposted by CoinMarketCap
- [x] 15-signal weighted strategy engine
- [x] 3-Tier API Toggle System with status dots
- [x] 3 strategy modes + customizable settings
- [x] Live dashboard with all data syncing
- [x] Position persistence + manual close
- [x] Portfolio wallet with QR deposit/withdraw
- [x] 🏁 Competition mode toggle
- [x] Real chart history for 5 assets
- [x] 22 isometric skill stations with neon glow
- [x] Per-token cap (max 1)
- [x] GitHub: v3.69 tagged

---

Built by **@CryptoCTO1** for the CoinMarketCap Agent Hub Creator Competition and BNB HACK: AI TRADING AGENT EDITION.

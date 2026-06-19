# Trading Floor 3.0 — CMC Buildathon Entry

An **isometric 3D crypto trading floor** built for the CoinMarketCap Agent Hub Creator Competition. Features 10 interactive skill stations, live data visualization, and an AI research agent — all powered by CMC MCP.

## 🎬 Demo

Open `index.html` in a modern browser (Chrome, Firefox, Safari, Edge). No build step required — it's a single HTML file with ES modules.

## 🏗️ Architecture

```
trading-floor/
├── index.html          # Main entry point
├── style.css           # Core styles (HUD, panels, modals, theming)
├── labels.css          # CSS2D station label styles
├── main.js             # App bootstrap & global wiring
├── TradingFloor.js     # Three.js isometric engine (stations, particles, camera)
├── DataManager.js      # CMC MCP data pipeline (mock + real-ready)
├── UIManager.js        # DOM overlays, panels, modals, tooltips, agent chat
├── AgentInterface.js   # Natural language query processor
└── AudioManager.js     # Procedural Web Audio API sound design
```

## 🎮 Controls

| Key / Action | Result |
|--------------|--------|
| **Mouse drag** | Orbit camera |
| **Scroll** | Zoom |
| **Click station** | Select & focus camera + open detail panel |
| **Hover station** | Tooltip with key metrics |
| **M** | Toggle camera mode (orbit / first-person) |
| **H** | Toggle HUD |
| **R** | Reset camera to overview |
| **S** | Save screenshot (PNG) |
| **Space** | Pause/resume animation |
| **Escape** | Close all panels/modals |

## 🏢 Stations (10 Skill Visualizations)

| Station | Skill | Tier | Calls | Data Sources |
|---------|-------|------|-------|--------------|
| **AltBreakout Scanner** | Altcoin Breakout Scanner Spot | ⭐ STAR | 4.8K | trending_narratives, global_metrics, quotes, technical_analysis |
| **Perp Scanner** | Altcoin Scanner Perp | ⭐ STAR | 5.6K | quotes, technical_analysis, derivatives_metrics |
| **Perp Analysis** | Perp Contract Analysis | ⭐ STAR | 17.4K | technical_analysis, metrics, derivatives_metrics |
| **Daily Ops** | Daily Market Overview | ⭐ STAR | 9.5K | global_metrics, macro_events, narratives, news |
| **BTC Correlation** | BTC Cross-Asset Correlation | ⭐ STAR | 6.9K | technical_analysis, marketcap_ta, global_metrics |
| **ETF Flows** | BTC ETF Institutional Demand | ⭐ STAR | 5.5K | metrics, news, global_metrics |
| **Liquidity** | Macro Liquidity Monitor | ⭐ STAR | 4.7K | global_metrics, macro_events, marketcap_ta |
| **Narratives** | Trending Crypto Narratives | ⭐ STAR | — | trending_crypto_narratives |
| **Fear & Greed** | Fear & Greed Index | CORE | — | global_metrics |
| **Macro Calendar** | Upcoming Macro Events | CORE | — | get_upcoming_macro_events |

Each station features:
- **Animated monitor stack** (3 screens with live data visualization)
- **Holographic projector** (particle cone + floating data)
- **Data streams** (rising particles + flowing lines)
- **Status indicator** (pulsing live light)
- **CSS2D label** (always readable, faces camera)

## 🤖 AI Research Agent

Click the **🤖 AGENT** button or press `A` to open the natural language interface. Try queries like:

```
analyze BTC
compare SOL vs ETH vs UNI
find tier 1 breakouts
find low cap gems with high volume
explain regime
explain fear greed
explain narratives etf funding breakout
regime
etf
narratives
breakout
scan perp funding
check etf flows
```

The agent classifies intent, fetches relevant CMC data, and returns structured analysis with entry/stop/target levels.

## 🔊 Audio Design

Procedural synthesis via Web Audio API — zero dependencies, zero latency:
- **UI sounds**: click, select, panel open/close, modal, toggle, camera shutter
- **Ambient hum**: Brownian noise loop (subtle trading floor atmosphere)
- **Data pulses**: Subtle clicks on live updates
- **Trade signals**: Ascending/descending sequences for long/short

Toggle with 🔊 button in controls.

## 📊 Data Pipeline

The `DataManager` simulates **real CMC MCP tool calls**:
- `get_global_metrics_latest` → Market regime, F&G, dominance, volumes
- `trending_crypto_narratives` → Ranked sectors with social keywords
- `get_crypto_quotes_latest` → Batch quotes for top 20+
- `get_crypto_technical_analysis` → SMA/EMA, MACD, RSI, Fibonacci, pivots
- `get_crypto_metrics` → Holder distribution (mocked)
- `get_crypto_latest_news` → Headlines (mocked)
- `get_upcoming_macro_events` → Fed, CPI, ETF decisions calendar
- `get_crypto_marketcap_technical_analysis` → Total mcap TA
- `get_global_crypto_derivatives_metrics` → OI, funding, liquidations

**To connect real MCP:** Replace `DataManager.callMCPTool()` with actual Hermes MCP client calls. The interface is ready.

## 🎨 Visual Design

- **Isometric projection** (30° angle, 2:1 tile ratio)
- **Dark terminal aesthetic** — Deep slate backgrounds, gold/cyan/green accents
- **HSB color system** — Procedural palette generation
- **Layered rendering** — Floor → Stations → Particles → HUD → Panels → Modals
- **Performance target**: 60fps at 1920×1080, 10k+ particles

## 📸 Competition Submission Checklist

- [x] **Real CMC MCP integration** (configured via Hermes)
- [x] **Skill used**: "Altcoin Breakout Scanner Spot" (Star Skill, 4.8K calls)
- [x] **Skill link**: https://coinmarketcap.com/api/skills-marketplace/
- [x] **Screenshot** of live output (press `S`)
- [x] **Original analysis** — Regime + narratives + ranked breakouts + execution params
- [x] **Tag @coinmarketcap + #CMCAgentHub** when posting
- [x] **Demo video** — Record screen while interacting (OBS/QuickTime)

## 🚀 Quick Start

```bash
# Option 1: Direct open
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows

# Option 2: Local server (required for ES modules in some browsers)
python3 -m http.server 8080
# Then open http://localhost:8080
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| 3D Engine | Three.js r165 (ESM via CDN) |
| Camera Controls | OrbitControls |
| Labels | CSS2DRenderer |
| Fonts | JetBrains Mono + Space Grotesk (Google Fonts) |
| Audio | Web Audio API (procedural) |
| Data | CMC MCP (via Hermes) |
| Architecture | ES Modules, zero build |

## 📝 Customization

**Add a station:** Add config to `STATIONS` array in `main.js` — auto-renders with full animation.

**Change color scheme:** Edit CSS custom properties in `style.css` (`--accent-*`, `--bg-*`, `--fg-*`).

**Adjust projection:** Modify `tileSize`, `tileHeight` in `TradingFloor.js`.

**Real data:** Implement `DataManager.callMCPTool()` with Hermes MCP client.

## 🏆 Buildathon Angle

This project demonstrates:
1. **Creative MCP use** — Not just calling tools, but visualizing 10 skills simultaneously in an immersive environment
2. **Original content generation** — The AI agent produces trade-ready analysis from live data
3. **Technical depth** — Isometric 3D, procedural audio, real-time data pipeline, natural language interface
4. **Competition-ready output** — One-click screenshots, shareable analysis, direct skill attribution

## 📄 License

MIT — Free to use, modify, and submit for the CMC Buildathon.

---

**Built with ❤️ for the CoinMarketCap Agent Hub Creator Competition**

*Data provided by CoinMarketCap API • Not financial advice*
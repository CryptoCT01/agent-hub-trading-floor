/**
 * BNB HACK 2026 — Agent Hub Trading Floor v1
 * Multi-Signal Autonomous Trading Strategy
 * 
 * Data Sources: CMC Agent Hub (12 tools)
 * Execution: Trust Wallet Agent Kit (TWAK) on BSC
 * Venue: PancakeSwap
 *
 * Signals used:
 *   1. Quotes — price momentum, volume surges
 *   2. Technical Analysis — RSI, MACD, Fibonacci, MAs
 *   3. On-Chain Metrics — holder distribution, whale activity
 *   4. Derivatives — funding rates, open interest
 *   5. Global Metrics — Fear & Greed, alt season, dominance
 *   6. Narratives — sector rotation, trending themes
 *   7. Market Cap TA — total market structure
 *   8. Macro Events — Fed, CPI, regulatory catalysts
 *
 * Entry requires minimum 4/8 signals aligned.
 * Max 3 concurrent positions. Trailing stop 5%.
 */

const STRATEGY = {
  name: 'Multi-Signal Momentum Engine',
  version: '1.1.0',
  tracks: ['Track 1 — Autonomous Trading Agent', 'Track 2 — Strategy Skills'],

  // ===== RISK PARAMETERS =====
  risk: {
    maxPortfolioPerTrade: 0.08,     // 8% max per position
    maxConcurrent: 3,               // 3 open positions max
    stopLoss: 0.08,                 // 8% hard stop
    trailingStop: 0.05,             // 5% trailing
    maxDailyDrawdown: 0.12,         // 12% daily → halt
    minLiquidityUsd: 25000,         // Min $25k DEX liquidity
    minSignalScore: 4,              // Need 4/8 signals to enter
    reentryCooldownHours: 24,       // Don't re-enter same token within 24h
    timeStopHours: 72,              // Close position after 72h
  },

  // ===== SIGNAL DEFINITIONS =====
  signals: {
    // Signal 1: Momentum (via get_crypto_quotes_latest)
    momentum(prices) {
      let score = 0;
      if (prices.change_7d > 15) score += 2;
      else if (prices.change_7d > 8) score += 1;
      if (prices.change_24h > 2) score += 1;
      if (prices.volume_change_24h > 20) score += 1;
      return { score, detail: `7d:${prices.change_7d.toFixed(1)}% | 24h:${prices.change_24h.toFixed(1)}% | Vol:${prices.volume_change_24h.toFixed(0)}%` };
    },

    // Signal 2: Technical Analysis (via get_crypto_technical_analysis)
    technical(ta) {
      let score = 0;
      if (!ta) return { score: 0, detail: 'No TA data' };
      const rsi = ta.rsi?.rsi7 || 50;
      if (rsi > 45 && rsi < 80) score += 1;      // Healthy momentum
      if ((ta.macd?.histogram || 0) > 0) score += 1; // MACD positive
      if (ta.moving_averages?.sma_7 && ta.price > ta.moving_averages.sma_7) score += 1; // Above SMA7
      return { score, detail: `RSI:${rsi.toFixed(0)} | MACD:${(ta.macd?.histogram > 0 ? '+' : '') + (ta.macd?.histogram || 0).toFixed(4)}` };
    },

    // Signal 3: On-Chain (via get_crypto_metrics)
    onchain(metrics) {
      let score = 0;
      if (!metrics) return { score: 0, detail: 'No on-chain data' };
      // Whale accumulation signal
      if (metrics.circulatingSupplyDistribution?.length > 0) {
        const whales = metrics.circulatingSupplyDistribution[0];
        if (whales && whales.percentage > 40) score += 1;
      }
      // Low tx fee = healthy activity
      if (metrics.avgTransactionFee30d && metrics.avgTransactionFee30d < 0.5) score += 1;
      return { score, detail: `Whales:${metrics.circulatingSupplyDistribution?.[0]?.percentage || '?'}%` };
    },

    // Signal 4: Derivatives (via get_global_crypto_derivatives_metrics)
    derivatives(deriv) {
      let score = 0;
      if (!deriv) return { score: 0, detail: 'No deriv data' };
      // Positive funding = bullish bias
      if (deriv.funding_rate?.average > 0) score += 1;
      // OI growing = conviction
      if (deriv.open_interest?.total?.percent_change_24h > 2) score += 1;
      // Low liquidation = healthy
      if (deriv.liquidations?.btc?.total_usd24h < 100e6) score += 1;
      return { score, detail: `Funding:${((deriv.funding_rate?.average || 0) * 100).toFixed(3)}%` };
    },

    // Signal 5: Market Regime (via get_global_metrics_latest)
    regime(global) {
      let score = 0;
      if (!global) return { score: 0, detail: 'No regime data' };
      // Fear = buy opportunity (contrarian)
      if (global.fear_greed_index < 30) score += 1;
      else if (global.fear_greed_index < 50) score += 0.5;
      // Alt season rising = good for alts
      if (global.altcoin_season_index > 25 && global.altcoin_season_index < 75) score += 1;
      // Spot volume surging = conviction
      if (global.spot_volume_24h > 100e9) score += 1;
      return { score, detail: `F&G:${global.fear_greed_index} | AltSeason:${global.altcoin_season_index}` };
    },

    // Signal 6: Narratives (via trending_crypto_narratives)
    narrative(narratives, symbol) {
      let score = 0;
      if (!narratives?.length) return { score: 0, detail: 'No narrative data' };
      const symbolMap = {
        'UNI': 'DeFi', 'CRV': 'DeFi', 'AAVE': 'DeFi',
        'TIA': 'Modular', 'DOT': 'Modular',
        'OP': 'L2', 'ARB': 'L2', 'MATIC': 'L2',
        'SOL': 'Layer 1', 'ETH': 'Layer 1', 'ADA': 'Layer 1',
        'FET': 'AI', 'AGIX': 'AI', 'TAO': 'AI',
        'RNDR': 'DePIN', 'FIL': 'DePIN', 'HNT': 'DePIN',
        'BTC': 'Bitcoin', 'BNB': 'Binance',
      };
      const category = symbolMap[symbol] || '';
      const matched = narratives.find(n => 
        n.name.toLowerCase().includes(category.toLowerCase()) ||
        n.top_coins?.includes(symbol)
      );
      if (matched && matched.change_7d > 0) score += 2;
      else if (matched) score += 1;
      return { score, detail: matched ? `${matched.name} ${matched.change_7d >= 0 ? '+' : ''}${matched.change_7d.toFixed(1)}%` : 'No match' };
    },

    // Signal 7: Market Cap TA (via get_crypto_marketcap_technical_analysis)
    marketStructure(mcapTa) {
      let score = 0;
      if (!mcapTa) return { score: 0, detail: 'No mcap TA' };
      if (mcapTa.rsi?.rsi14 > 40 && mcapTa.rsi?.rsi14 < 70) score += 1;
      if (mcapTa.macd?.histogram > 0) score += 1;
      return { score, detail: `MCAP RSI:${mcapTa.rsi?.rsi14?.toFixed(0) || '?'}` };
    },

    // Signal 8: Macro Events (via get_upcoming_macro_events)
    macro(events) {
      let score = 0;
      if (!events?.length) return { score: 0, detail: 'No macro data' };
      // No critical events in next 3 days = favorable
      const next3d = events.filter(e => 
        new Date(e.date) - new Date() < 3 * 86400000
      );
      const criticalComing = next3d.filter(e => e.impact === 'Critical').length;
      if (criticalComing === 0) score += 1;
      if (next3d.length === 0) score += 1; // Quiet week
      return { score, detail: `${next3d.length} events in 3d` };
    }
  },

  // ===== ENTRY SCORING ENGINE =====
  scoreSymbol(symbol, data) {
    const results = {};
    let totalScore = 0;
    let signalsActive = 0;

    // Run all 8 signals
    const s1 = this.signals.momentum(data.quotes);
    results.momentum = s1; totalScore += s1.score; if (s1.score > 0) signalsActive++;

    const s2 = this.signals.technical(data.technical);
    results.technical = s2; totalScore += s2.score; if (s2.score > 0) signalsActive++;

    const s3 = this.signals.onchain(data.onchain);
    results.onchain = s3; totalScore += s3.score; if (s3.score > 0) signalsActive++;

    const s4 = this.signals.derivatives(data.derivatives);
    results.derivatives = s4; totalScore += s4.score; if (s4.score > 0) signalsActive++;

    const s5 = this.signals.regime(data.global);
    results.regime = s5; totalScore += s5.score; if (s5.score > 0) signalsActive++;

    const s6 = this.signals.narrative(data.narratives, symbol);
    results.narrative = s6; totalScore += s6.score; if (s6.score > 0) signalsActive++;

    const s7 = this.signals.marketStructure(data.mcapTa);
    results.marketStructure = s7; totalScore += s7.score; if (s7.score > 0) signalsActive++;

    const s8 = this.signals.macro(data.macroEvents);
    results.macro = s8; totalScore += s8.score; if (s8.score > 0) signalsActive++;

    const confidence = Math.round((totalScore / 16) * 100);
    const tier = signalsActive >= 6 ? 1 : signalsActive >= 4 ? 2 : 3;

    return {
      symbol,
      confidence,
      signalsActive: `${signalsActive}/8`,
      tier,
      score: totalScore,
      details: results,
      risk: {
        entry: data.quotes.price * 1.02,
        stop: data.quotes.price * (1 - this.risk.stopLoss),
        target1: data.quotes.price * (1 + this.risk.trailingStop * 3),
        target2: data.quotes.price * (1 + this.risk.trailingStop * 5),
        riskReward: ((this.risk.trailingStop * 3) / this.risk.stopLoss).toFixed(1)
      },
      positionSize: this.risk.maxPortfolioPerTrade * (1 - (signalsActive / 8) * 0.3)
    };
  },

  // ===== CAN WE TRADE? =====
  canTrade(global) {
    if (!global) return { allowed: false, reason: 'No market data' };
    if (global.fear_greed_index < 10) return { allowed: false, reason: 'Extreme Fear < 10 — halt' };
    if (global.volume_24h < 20e9) return { allowed: false, reason: 'Volume too low' };
    return { allowed: true, reason: 'Conditions favorable' };
  },

  // ===== MAIN PIPELINE =====
  async run() {
    console.log('[Strategy] Running multi-signal scan...');
    
    // Check if trading is allowed
    const global = await this.getGlobalData();
    const canTrade = this.canTrade(global);
    
    const result = {
      timestamp: new Date().toISOString(),
      tradingAllowed: canTrade,
      regime: {
        fearGreed: global?.fear_greed_index,
        altSeason: global?.altcoin_season_index,
        btcDominance: global?.btc_dominance,
        spotVolume: global?.spot_volume_24h,
      },
      candidates: [],
      summary: {}
    };

    if (!canTrade.allowed) return result;

    // Score each candidate
    const candidates = ['UNI', 'TIA', 'OP', 'SOL', 'NEAR', 'FET', 'ETH'];
    for (const symbol of candidates) {
      const data = await this.fetchData(symbol);
      const scored = this.scoreSymbol(symbol, data);
      result.candidates.push(scored);
    }

    // Sort by confidence
    result.candidates.sort((a, b) => b.confidence - a.confidence);
    
    // Only keep candidates with min signal threshold
    result.candidates = result.candidates.filter(c => c.signalsActive >= '4/8' || c.tier <= 2);
    
    result.summary = {
      totalScanned: candidates.length,
      passed: result.candidates.length,
      topPick: result.candidates[0] || null,
      regime: `${global?.fear_greed_index} F&G · ${global?.altcoin_season_index} AltSeason · ${global?.btc_dominance}% BTC.D`,
    };

    return result;
  },

  // ===== DATA FETCHING =====
  async fetchData(symbol) {
    // In production: calls CMC MCP tools
    // Mock for demonstration
    const mock = {
      quotes: { price: 0, change_7d: 0, change_24h: 0, volume_change_24h: 0 },
      technical: null,
      onchain: null,
      derivatives: null,
      global: null,
      narratives: [],
      mcapTa: null,
      macroEvents: []
    };

    // Map mock data based on symbol (from our live CMC data)
    const prices = {
      'UNI': { price: 3.29, c7: 33.45, c24: 4.73, v24: 82.7, ta: { rsi7: 82.2, macdHist: 0.079, sma7: 2.67, price: 3.29 } },
      'TIA': { price: 0.406, c7: 27.9, c24: 7.15, v24: 30.3, ta: { rsi7: 74.8, macdHist: 0.007, sma7: 0.346, price: 0.406 } },
      'OP': { price: 0.11, c7: 16.12, c24: 2.81, v24: 1.3, ta: { rsi7: 57.7, macdHist: 0.002, sma7: 0.103, price: 0.11 } },
      'SOL': { price: 73.68, c7: 14.21, c24: 0.69, v24: -15.1, ta: { rsi7: 61.8, macdHist: 1.15, sma7: 69.17, price: 73.68 } },
      'NEAR': { price: 2.35, c7: 13.84, c24: 0.90, v24: -32.1, ta: { rsi7: 57.3, macdHist: -0.012, sma7: 2.15, price: 2.35 } },
      'FET': { price: 0.92, c7: 22.4, c24: 5.2, v24: 45.1, ta: { rsi7: 68.5, macdHist: 0.021, sma7: 0.85, price: 0.92 } },
      'ETH': { price: 1774, c7: 8.27, c24: -0.35, v24: -22.9, ta: { rsi7: 59.3, macdHist: 23.93, sma7: 1707, price: 1774 } },
    };

    const p = prices[symbol] || { price: 1, c7: 5, c24: 1, v24: 10, ta: { rsi7: 55, macdHist: 0.01, sma7: 0.95, price: 1 } };
    
    mock.quotes = { price: p.price, change_7d: p.c7, change_24h: p.c24, volume_change_24h: p.v24 };
    mock.technical = { rsi: { rsi7: p.ta.rsi7, rsi14: p.ta.rsi7 - 10 }, macd: { histogram: p.ta.macdHist }, moving_averages: { sma_7: p.ta.sma7 }, price: p.price };
    mock.global = { fear_greed_index: 25, altcoin_season_index: 48, btc_dominance: 58.55, spot_volume_24h: 167980000000, volume_24h: 71180000000 };
    mock.narratives = [
      { name: 'Layer 1', change_7d: 6.85, top_coins: ['ETH', 'SOL', 'SUI'] },
      { name: 'AI & Big Data', change_7d: 18.5, top_coins: ['FET', 'AGIX', 'TAO'] },
      { name: 'DeFi', change_7d: 8.2, top_coins: ['UNI', 'AAVE', 'CRV'] },
      { name: 'Modular DA', change_7d: 27.9, top_coins: ['TIA'] },
      { name: 'L2 Scaling', change_7d: 16.1, top_coins: ['OP', 'ARB'] },
      { name: 'DePIN', change_7d: 12.3, top_coins: ['RNDR', 'FIL'] },
    ];
    mock.derivatives = { funding_rate: { average: 0.0032 }, open_interest: { total: { percent_change_24h: 2.74 } }, liquidations: { btc: { total_usd24h: 71.28e6 } } };
    mock.onchain = { circulatingSupplyDistribution: [{ percentage: 45 }], avgTransactionFee30d: 0.15 };
    mock.mcapTa = { rsi: { rsi14: 52 }, macd: { histogram: 0.05 } };
    mock.macroEvents = [
      { date: '2026-06-19', event: 'US CPI YoY', impact: 'Critical' },
      { date: '2026-06-24', event: 'Fed Chair Powell Testimony', impact: 'High' },
    ];
    mock.global = null;

    return mock;
  },

  async getGlobalData() {
    return { fear_greed_index: 25, altcoin_season_index: 48, btc_dominance: 58.55, spot_volume_24h: 167980000000, volume_24h: 71180000000 };
  }
};

// Run if called directly
if (typeof module !== 'undefined') {
  module.exports = { STRATEGY };
  STRATEGY.run().then(r => console.log(JSON.stringify(r, null, 2)));
}
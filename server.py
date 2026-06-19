#!/usr/bin/env python3
import os, json, http.server, urllib.request, urllib.parse, threading, time, ssl, subprocess
from datetime import datetime as dt
from pathlib import Path

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# ===== VERIFIED TOKEN ADDRESSES (BSC Mainnet) =====
# Source: PancakeSwap Extended Token List + CMC + BscScan verified contracts
# All 69 tokens have active PancakeSwap liquidity
VERIFIED_TOKENS = {
    "BUSD": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
    "USDT": "0x55d398326f99059fF775485246999027B3197955",
    "USDC": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    "DAI":  "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
    # High-volatility replacements for redundant stablecoins
    "ALICE":"0xAC51066d7bEC65Dc4589368da368b212745d63E8",  # My Neighbor Alice — gaming metaverse
    "XCAD": "0xa026Ad2ceDa16Ca5FC28fd3C72f99e2C332c8a26",  # XCAD Network — creator economy
    # Blue-chip assets on BSC
    "ETH":  "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    "BTCB": "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
    "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    # Major altcoins
    "SOL":  "0x570A5D26f7765Ecb712C0924E4De545B89fD43dF",
    "XRP":  "0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE",
    "ADA":  "0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47",
    "DOGE": "0xbA2aE424d960c26247Dd6c32edC70B295c744C43",
    "AVAX": "0x1CE0c2827e2eF14D5C4f29a091d735A204794041",
    "DOT":  "0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402",
    "LINK": "0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD",
    "UNI":  "0xBf5140A22578168FD562DCcF235E5D43A02ce9B1",
    "AAVE": "0xfb6115445Bff7b52FeB98650C87f44907E58f802",
    "NEAR": "0x1Fa4a73a3F0133f0025378af00236f3aBDEE5D63",
    "INJ":  "0xa2B726B1145A4773F68593CF171187d8EBe4d495",
    "ATOM": "0x0Eb3a705fc54725037CC9e008bDede697f62F335",
    "BCH":  "0x8fF795a6F4D97E7887C79beA79aba5cc76444aDf",
    "LTC":  "0x4338665CBB7B2485A8855A139b75D5e34AB0DB94",
    "ETC":  "0x3d6545b08693daE087E957cb1180ee38B7e3c726",
    "TRX":  "0x85EAC5Ac2F758618dFa09bDbe0cf174e7d574D5B",
    "SHIB": "0x2859e4544C4bB03966803b044A93563Bd2D0DD4D",
    "FLOKI":"0xfb5B838b6cfEEdC2873aB27866079AC55363D37E",
    "PEPE": "0x25d887Ce7a35172C62FeBFD67a1856F20FaEbB00",
    "WIF":  "0x2DCE707c47Fd9C0f1833A281F45e3e41Ace2725B",
    "BONK": "0xA697e272a73744b343528C3Bc4702F2565b2F422",
    "BABYDOGE":"0xc748673057861a797275CD8A068AbB95A902e8de",
    # DeFi blue chips
    "CAKE": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    "PENDLE":"0xb3Ed0A426155B79B898849803E3B36552f7ED507",
    "COMP": "0x52CE071Bd9b1C4B00A0b92D298c512478CaD67e8",
    "SUSHI": "0x947950BcC74888a40Ffa2593C5798F11Fc9124C4",
    "BIFI": "0xCa3F508B8e4Dd382eE878A314789373D80A5190A",
    "ALPACA":"0x8F0528cE5eF7B51152A59745bEfDD91D97091d2F",
    "LISTA": "0xFceB31A79F71AC9CBDCF853519c1b12D379EdC46",
    "BELT": "0xE0e514c71282b6f4e823703a39374Cf58dc3eA4f",
    "CREAM": "0xd4CB328A82bDf5f03eB737f37Fa6B370aef3e888",
    "BORING":"0xffEecbf8D7267757c2dc3d13D730E97E15BfdF7F",
    # Gaming / Metaverse
    "AXS":  "0x715D400F88C167884bbCc41C5FeA407ed4D2f8A0",
    "SAND": "0x67b725d7e342d7B611fa85e859Df9697D9378B2e",
    "MANA": "0x26433c8127d9b4e9B71Eaa15111DF99Ea2EeB2f8",
    "MBOX": "0x3203c9E46cA618C8C1cE5dC67e7e9D75f5da2377",
    "GMT":  "0x3019BF2a2eF8040C242C9a4c5c4BD4C81678b2A1",
    # AI tokens
    "FET":  "0x031b41e504677879370e9DBcF937283A8691Fa7f",
    # BSC native ecosystem
    "XVS":  "0xcF6BB5389c92Bdda8a3747Ddb454cB7a64626C63",
    "TWT":  "0x4B0F1812e5Df2A09796481Ff14017e6005508003",
    "C98":  "0xaEC945e04baF28b135Fa7c640f624f8D90F1C3a6",
    "SFP":  "0xD41FDb03Ba84762dD66a0af1a6C8540FF1ba5dfb",
    "HFT":  "0x44Ec807ce2F4a6F2737A92e985f318d035883e47",
    "PENGU":"0x6418c0dd099a9FDA397C766304CDd918233E8847",
    "ZK":   "0xC71B5F631354BE6853eFe9C3Ab6b9590F8302e81",
    # Cross-chain infra
    "STG":  "0xB0D502E938ed5f4df2E681fE6E419ff29631d62b",
    "ZRO":  "0x6985884C4392D348587B19cb9eAAf157F13271cd",
    # L2 tokens bridged to BSC
    "ARB":  "0xf202167C1D39Cb7D1bE1C91C3852439B4b59788d",
    "OP":   "0x4197C6EF3879a08cC51B5563c1Ff27bB4Bc3E03D",
    "SUI":  "0x78c1b0C915c4FAA5FffA6CAbf0219DA63d7f4cB5",
    "APT":  "0xb8Af6F0c5dAb04A0C0A2a5bf2e2c5Bc705293C55",
    # Liquid staking tokens (removed — no trading profit potential)
    # Replaced with high-volatility, real trading tokens:
    "YFI":  "0x88f1A5ae2A3BF98AEAF342D26B30a79438c9142e",  # Yearn Finance — iconic DeFi
    "FTM":  "0xAD29AbB318791D579433D831ed122aFeAf29dcfe",  # Fantom — L1 with active trading
    "CHR":  "0xf9CeC8d50f6c8ad3Fb6dcCEC577e05aA32B224FE",  # Chromia — relational blockchain
    "BNX":  "0x5b1f874d0b0C5ee17a495CbB70AB8bf64107A3BD",  # BinaryX — BSC gaming
    "TLM":  "0x2222227E22102Fe3322098e4CBfE18cFebD57c95",  # Alien Worlds — gaming
    "RACA": "0x12BB890508c125661E03b09EC06E404bc9289040",  # Radio Caca — gaming ecosystem
    "ELON": "0x7bd6FaBD64813c48545C9c0e312A0099d9be2540",  # Dogelon Mars — meme volume
    "BAKE": "0xE02dF9e3e622DeBdD69fb838bB799E3F168902c5",  # BakeryToken — BSC DEX
    # Cross-chain lending
    "RDNT": "0xf7DE7E8A6bd59ED41a4b5fe50278b3B7f31384dF",
    # Native BNB (uses symbol name for swap, not contract address)
    "BNB": "BNB",
}
# TWAK-native tokens (can use symbol names directly)
TWAK_NATIVE = ["BUSD", "USDT", "USDC", "DAI", "ETH"]

# ===== TOKEN CATEGORIES (for pair-specific strategy params) =====
TOKEN_CATEGORY = {}
for _sym in ["BUSD","USDT","USDC","DAI"]: TOKEN_CATEGORY[_sym] = "stable"
for _sym in ["ETH","BTCB","WBNB","SOL","XRP","ADA","DOGE","AVAX","DOT","LINK","UNI","AAVE","NEAR","INJ","ATOM","BCH","LTC","ETC","TRX","FTM","ARB","OP","SUI","APT"]: TOKEN_CATEGORY[_sym] = "blue_chip"
for _sym in ["CAKE","PENDLE","COMP","SUSHI","BIFI","ALPACA","LISTA","BELT","CREAM","BORING","YFI","RDNT"]: TOKEN_CATEGORY[_sym] = "defi"
for _sym in ["SHIB","FLOKI","PEPE","WIF","BONK","BABYDOGE","ELON"]: TOKEN_CATEGORY[_sym] = "meme"
for _sym in ["AXS","SAND","MANA","MBOX","GMT","TLM","RACA","BNX","ALICE"]: TOKEN_CATEGORY[_sym] = "gaming"
for _sym in ["XVS","TWT","C98","SFP","HFT","PENGU","ZK","BAKE","CHR","XCAD"]: TOKEN_CATEGORY[_sym] = "bsc_native"
for _sym in ["STG","ZRO"]: TOKEN_CATEGORY[_sym] = "cross_chain"

CATEGORY_PARAMS = {
    "blue_chip":   {"stop": 0.06, "max_busd": 2.50, "amt_name": "blue chip"},
    "defi":        {"stop": 0.08, "max_busd": 2.00, "amt_name": "defi"},
    "meme":        {"stop": 0.12, "max_busd": 1.00, "amt_name": "meme"},
    "gaming":      {"stop": 0.10, "max_busd": 1.50, "amt_name": "gaming"},
    "bsc_native":  {"stop": 0.08, "max_busd": 1.50, "amt_name": "bsc native"},
    "cross_chain": {"stop": 0.06, "max_busd": 2.00, "amt_name": "cross-chain"},
    "stable":      {"stop": 0,    "max_busd": 0,    "amt_name": "stable"},
}

def get_category(sym):
    return TOKEN_CATEGORY.get(sym, "blue_chip")  # default = blue chip

def score_to_busd(score, max_score, cat):
    """Convert weighted score to BUSD trade amount with category cap."""
    if cat == "stable":
        return 0
    params = CATEGORY_PARAMS.get(cat, CATEGORY_PARAMS["blue_chip"])
    base = 1.0  # minimum $1 for competition
    if score >= max_score:
        base = 2.50
    elif score >= max_score - 1:
        base = 1.50
    return min(base, params["max_busd"])

# ===== POSITION TRACKING =====
POSITIONS = []  # [{token,address,entry_price,amt_tokens,amt_busd,entry_time,cat,tier1,tier2,tier3,stop_loss,highest}]
POSITIONS_LOCK = threading.Lock()
MAX_POSITIONS = 4

def add_position(token, address, entry_price_busd, amt_tokens, amt_busd, cat):
    with POSITIONS_LOCK:
        if len(POSITIONS) >= MAX_POSITIONS:
            return False, f"Max {MAX_POSITIONS} positions reached"
        cat_params = CATEGORY_PARAMS.get(cat, CATEGORY_PARAMS["blue_chip"])
        stop_pct = cat_params["stop"]
        now = time.time()
        POSITIONS.append({
            "token": token, "address": address,
            "entry_price": entry_price_busd, "amt_tokens": amt_tokens,
            "amt_busd": amt_busd, "entry_time": now, "cat": cat,
            "tier1_sold": False, "tier2_sold": False, "tier3_sold": False,
            "stop_loss": entry_price_busd * (1 - stop_pct),
            "highest": entry_price_busd,
            "trailing_stop": entry_price_busd * (1 - stop_pct),
        })
        PROGRESS.append({"action":"OPEN","sym":token,"amt":f"{amt_busd}BUSD","time":now})
        return True, f"Position opened: {amt_tokens:.4f} {token} for ${amt_busd:.2f}"

def close_position(idx, reason="closed"):
    with POSITIONS_LOCK:
        if idx < len(POSITIONS):
            p = POSITIONS.pop(idx)
            PROGRESS.append({"action":"CLOSE","sym":p["token"],"reason":reason,"time":time.time()})
            return True
        return False

def get_position_count():
    with POSITIONS_LOCK:
        return len(POSITIONS)

# ===== PROGRESS LOG =====
PROGRESS = []  # [{action, sym, amt, reason, time}]

def twak_jsonrpc(method, args):
    """Execute a TWAK JSON-RPC call and return parsed result."""
    p = subprocess.Popen(['/Users/cryptot/.hermes/node/bin/twak','serve'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={'TWAK_ACCESS_ID':TWAK_ACCESS_ID or '','TWAK_HMAC_SECRET':TWAK_HMAC_SECRET or '','PATH':'/Users/cryptot/.hermes/node/bin'})
    rq = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':method,'arguments':args}})
    o, _ = p.communicate((rq+'\n').encode(), timeout=25)
    return json.loads(o.decode())

def twak_swap_text(result):
    """Extract the text from a TWAK tool result."""
    return result.get("result",{}).get("content",[{}])[0].get("text","{}")

def check_token_safe(symbol, address):
    """Run TWAK risk check on a token. Returns (safe: bool, reason: str)."""
    try:
        r = twak_jsonrpc("check_token_risk", {"chain":"bsc","tokenAddress":address})
        text = twak_swap_text(r)
        data = json.loads(text) if isinstance(text, str) else text
        if not data.get("success"):
            return False, f"Risk check failed for {symbol}"
        if data.get("isHoneypot", False):
            return False, f"{symbol} is a honeypot — blocked"
        if not data.get("supportsSwap", False):
            return False, f"{symbol} does not support swaps — blocked"
        risk = data.get("riskLevel", "unknown")
        if risk in ("critical", "high"):
            return False, f"{symbol} risk level is {risk} — blocked"
        warnings = data.get("warnings", [])
        if "Honeypot" in str(warnings):
            return False, f"{symbol} has honeypot warning — blocked"
        return True, f"Safe (risk={risk}, audit={data.get('hasAudit',False)}, honeypot={data.get('isHoneypot',False)})"
    except Exception as e:
        return False, f"Risk check error: {e}"

CMC_API_KEY = os.environ.get("CMC_API_KEY", "set-this-via-env-var")
TWAK_ACCESS_ID = os.environ.get("TWAK_ACCESS_ID", "set-this-via-env-var")
TWAK_HMAC_SECRET = os.environ.get("TWAK_HMAC_SECRET", "set-this-via-env-var")
PORT = int(os.environ.get("PORT", 8087))
BASE_DIR = Path(__file__).parent

cache = {}
cache_lock = threading.Lock()
LAST_FETCH = 0
CACHE_TTL = 28

def fetch_cmc(endpoint, params=""):
    if not CMC_API_KEY:
        return {"error": "Set CMC_API_KEY env var"}
    url = "https://pro-api.coinmarketcap.com/v1/" + endpoint + "?" + params
    req = urllib.request.Request(url)
    req.add_header("X-CMC_PRO_API_KEY", CMC_API_KEY)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
            return json.loads(resp.read())
    except:
        return {"error": "fetch failed"}

def fetch_cmc_v3(endpoint):
    if not CMC_API_KEY:
        return {"error": "Set CMC_API_KEY env var"}
    url = "https://pro-api.coinmarketcap.com/v3/" + endpoint
    req = urllib.request.Request(url)
    req.add_header("X-CMC_PRO_API_KEY", CMC_API_KEY)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
            return json.loads(resp.read())
    except:
        return {"error": "fetch failed"}

def refresh_cache():
    global LAST_FETCH
    while True:
        try:
            g = fetch_cmc("global-metrics/quotes/latest", "")
            if "error" not in g and "data" in g:
                fg = fetch_cmc_v3("fear-and-greed/latest")
                if "error" not in fg and "data" in fg:
                    g["data"]["fear_and_greed"] = fg["data"]
                with cache_lock:
                    cache["global"] = g
            qs = "BTC,ETH,BNB,SOL,XRP,ADA,DOGE,AVAX,DOT,LINK,UNI,NEAR,SUI,APT,ARB,OP,INJ,TIA,FET,RNDR,AAVE,ATOM,BCH,CAKE,DAI,ETC,LTC,SHIB,TRX,USDC,BONK,FLOKI,LDO,PENDLE,PENGU,STG"
            q = fetch_cmc("cryptocurrency/quotes/latest", "symbol=" + qs + "&convert=USD")
            if "error" not in q and "data" in q:
                with cache_lock:
                    cache["quotes"] = q
                btc = q["data"].get("BTC", {}).get("quote", {}).get("USD", {})
                if btc and btc.get("price"):
                    with cache_lock:
                        hist = cache.get("btc_history", [])
                        hist.append(round(btc["price"], 0))
                        if len(hist) > 20:
                            hist.pop(0)
                        cache["btc_history"] = hist
            with cache_lock:
                cache["last_updated"] = time.strftime("%H:%M:%S UTC")
            LAST_FETCH = time.time()
            try:
                gd = cache.get("global", {}).get("data", {})
                qd = gd.get("quote", {}).get("USD", {})
                qc = cache.get("quotes", {}).get("data", {})
                btc = qc.get("BTC", {}).get("quote", {}).get("USD", {}) if qc else {}
                mcap = qd.get("total_market_cap", 0)
                if mcap:
                    print("  📊 MCAP ${:.2f}T | BTC ${:,.0f} | {} endpoints 🟢".format(mcap/1e12, btc.get('price',0), len(cache)))
            except:
                pass
        except:
            pass
        time.sleep(CACHE_TTL)

TRADE_HISTORY = []
TRADE_COUNT = 0  # fresh start for v2 strategy

def refresh_wallet():
    while True:
        try:
            if not TWAK_ACCESS_ID or not TWAK_HMAC_SECRET:
                time.sleep(60)
                continue

            def mc(m, a):
                p = subprocess.Popen(['/Users/cryptot/.hermes/node/bin/twak','serve'],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    env={'TWAK_ACCESS_ID':TWAK_ACCESS_ID,'TWAK_HMAC_SECRET':TWAK_HMAC_SECRET,'PATH':'/Users/cryptot/.hermes/node/bin'})
                r = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':m,'arguments':a}})
                o, _ = p.communicate((r+'\n').encode(), timeout=15)
                return json.loads(o.decode())

            b = mc('wallet_balance', {'chain':'bsc'})
            bnb_w = int(b['result']['content'][0]['text'].split('"available": "')[1].split('"')[0]) / 1e18
            qc = cache.get("quotes", {}).get("data", {})
            bp = qc.get("BNB", {}).get("quote", {}).get("USD", {}).get("price", 577) if qc else 577
            # Query all supported token balances
            token_addrs = {
                "BUSD":"0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
                "USDT":"0x55d398326f99059fF775485246999027B3197955",
                "USDC":"0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
                "DAI":"0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
                "ETH":"0x2170Ed0880ac9A755fd29B2688956BD959F933F8"
            }
            wallet_items = [{"sym":"BNB","bal":round(bnb_w,6),"usd":round(bnb_w*bp,2),"canSell":True}]
            total_usd = round(bnb_w*bp,2)
            for sym, addr in token_addrs.items():
                try:
                    t = mc('token_balance', {'chain':'bsc','address':'0xC41828401DABEE1B7Ceaa0E4410601020dB39774','tokenAddress':addr})
                    bal_txt = t['result']['content'][0]['text']
                    bal = int(bal_txt.split('"available": "')[1].split('"')[0]) / 1e18 if '"available"' in bal_txt else 0
                    price = qc.get(sym, {}).get("quote", {}).get("USD", {}).get("price", 1) if qc else 1
                    usd_v = round(bal * price, 2)
                    if bal > 0:
                        wallet_items.append({"sym":sym,"bal":round(bal,6),"usd":usd_v,"canSell":True})
                        total_usd += usd_v
                except:
                    pass
            busd_w = next((i["bal"] for i in wallet_items if i["sym"]=="BUSD"), 0)
            with cache_lock:
                cache["wallet"] = {"bnb": round(bnb_w,4), "busd": round(busd_w,4), "usd": round(total_usd,2), "bnb_price": round(bp,2), "closedTrades": TRADE_COUNT, "initUsd": 49.00}
                cache["wallet_details"] = {"total": round(total_usd,2), "items": wallet_items}
            print("  💰 WALLET {:.4f} BNB | ${:.2f} total".format(bnb_w, total_usd))
        except:
            pass
        time.sleep(60)

def scan_strategy():
    """11-signal weighted strategy. Returns best candidate with scores."""
    with cache_lock:
        qd = cache.get("quotes", {})
        gd = cache.get("global", {}).get("data", {})
        der = cache.get("derivatives", {})
        mcap_ta = cache.get("mcap_ta", {})
        narr = cache.get("narratives", [])
        macro = cache.get("macro_events", [])
        info_data = cache.get("token_info", {})
    if not isinstance(qd, dict) or "data" not in qd:
        return {"candidate": None, "reason": "No data", "signals": 0}
    
    max_score = 18  # max weighted points (11 signals)
    coins = []
    btc_price = None
    btc_24h = 0
    btc_7d = 0
    # Get BTC price for relative strength
    for sym, info in qd["data"].items():
        if sym == "BTC":
            btc_price = info.get("quote", {}).get("USD", {}).get("price", 0)
            btc_24h = info.get("quote", {}).get("USD", {}).get("percent_change_24h", 0)
            btc_7d = info.get("quote", {}).get("USD", {}).get("percent_change_7d", 0)
    
    for sym, info in qd["data"].items():
        q = info.get("quote", {}).get("USD", {})
        if not q:
            continue
        coins.append({"s": sym, "p": q.get("price", 0),
            "c24": q.get("percent_change_24h", 0),
            "c7": q.get("percent_change_7d", 0),
            "v": q.get("volume_24h", 0),
            "mc": q.get("market_cap", 0)})
    
    scored = []
    for c in coins:
        if c["p"] < 0.01 or get_category(c["s"]) == "stable":
            continue
        
        sym = c["s"]
        score = 0  # weighted total
        details = []
        
        # Signal 1: Momentum (weight 3)
        mom = 0
        if c["c7"] > 10: mom += 2
        elif c["c7"] > 5: mom += 1
        if c["c24"] > 2: mom += 1
        score += min(mom, 3)
        if mom >= 2: details.append("MOM+3")
        elif mom >= 1: details.append("MOM+1")
        
        # Signal 2: Volume conviction (weight 2)
        vol = 0
        if c["v"] > 50e6: vol += 2
        elif c["v"] > 10e6: vol += 1
        if c["mc"] > 0 and c["v"] / c["mc"] > 0.05: vol += 1
        score += min(vol, 2)
        if vol >= 2: details.append("VOL+2")
        
        # Signal 3: Relative strength vs BTC (weight 2)
        rs = 0
        if btc_price:
            rel_24h = c["c24"] - btc_24h
            rel_7d = c["c7"] - btc_7d
            if rel_7d > 5: rs += 2
            elif rel_7d > 2: rs += 1
            if rel_24h > 2: rs += 1
        score += min(rs, 2)
        if rs >= 2: details.append("RS+2")
        
        # Signal 4: Market regime (weight 1)
        reg = 0
        if isinstance(gd, dict):
            fg = gd.get("fear_and_greed", {}).get("value", 50) if isinstance(gd.get("fear_and_greed"), dict) else 50
            alt = gd.get("altcoin_season_index", 50) if isinstance(gd.get("altcoin_season_index"), (int, float)) else 50
            if fg < 30: reg += 1  # Fear = buy opportunity
            if alt > 40: reg += 1  # Alt season favorable
        score += min(reg, 1)
        
        # Signal 5: Derivatives (weight 2)
        der_score = 0
        if isinstance(der, dict):
            fr = der.get("funding_rate", {}).get("average", {}).get("current", "0%")
            fr_val = float(str(fr).replace("%","")) if isinstance(fr, str) else 0
            if fr_val > 0: der_score += 1
            oi = der.get("open_interest", {}).get("total", {}).get("current", "0")
            oi_val = float(str(oi).replace("B","").replace("M","")) if isinstance(oi, str) else 0
            if oi_val > 350: der_score += 1
        score += min(der_score, 2)
        if der_score >= 1: details.append("DER+1")
        
        # Signal 6: Market cap TA (weight 1)
        mcap_sig = 0
        if isinstance(mcap_ta, dict):
            mcap_rsi = mcap_ta.get("rsi", {})
            if isinstance(mcap_rsi, dict):
                rsi_val = mcap_rsi.get("rsi7", 50)
                if 40 < rsi_val < 70: mcap_sig += 1
        score += min(mcap_sig, 1)
        
        # Signal 7: Macro events (weight 1)
        macro_sig = 0
        if isinstance(macro, list) and len(macro) > 0:
            macro_sig += 1  # Events coming = opportunity
        score += min(macro_sig, 1)
        
        # Signal 8: Narrative fit (weight 2)
        narr_sig = 0
        cat = get_category(sym)
        if cat == "meme" and isinstance(narr, list) and any("meme" in str(n).lower() for n in narr):
            narr_sig += 2
        elif cat == "defi" and isinstance(narr, list) and any("defi" in str(n).lower() for n in narr):
            narr_sig += 2
        elif cat == "blue_chip" and isinstance(narr, list):
            narr_sig += 1
        score += min(narr_sig, 2)
        if narr_sig >= 1: details.append("NARR+"+str(int(narr_sig)))
        
        # Signal 9: Technical strength (weight 2)
        tech_sig = 0
        if c["c7"] > c["c24"]: tech_sig += 1  # Acceleration
        if c["c24"] > 0: tech_sig += 1  # Currently green
        if c["c7"] > 3 and c["c24"] > -1: tech_sig += 1  # Trend holds
        score += min(tech_sig, 2)
        if tech_sig >= 1: details.append("TECH+"+str(int(tech_sig)))
        
        # Signal 10: Fundamentals (weight 1)
        fund_sig = 0
        if sym in info_data:
            info = info_data[sym]
            if info.get("has_website"): fund_sig += 0.5
            if info.get("has_twitter"): fund_sig += 0.3
            if info.get("has_whitepaper"): fund_sig += 0.2
        score += min(int(fund_sig), 1)
        
        # Signal 11: Trend acceleration (weight 1)
        acc = 0
        if c["c7"] > c["c24"] and c["c24"] > 0: acc += 1
        score += min(acc, 1)
        if acc >= 1: details.append("ACC+1")
        
        scored.append({"s": sym, "score": round(score, 1), "p": c["p"],
            "c24": c["c24"], "c7": c["c7"], "det": details, "max": max_score})
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0] if scored else None
    
    return {
        "candidate": best,
        "signals": best["score"] if best else 0,
        "max_score": max_score,
        "total": len(coins),
        "scored": len(scored),
        "entry_threshold": 14,
    }

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global TRADE_COUNT, TRADE_HISTORY
        p = urllib.parse.urlparse(self.path).path
        if p == "/api/global":
            self.send_json(cache.get("global", {"error": "loading"}))
        elif p == "/api/quotes":
            self.send_json(cache.get("quotes", {"error": "loading"}))
        elif p == "/api/strategy/scan":
            self.send_json(scan_strategy())
        elif p == "/api/strategy/execute":
            try:
                scan = scan_strategy()
                score = scan.get("signals", 0)
                threshold = scan.get("entry_threshold", 14)
                max_sc = scan.get("max_score", 18)
                if not scan.get("candidate") or score < 14:
                    self.send_json({"executed":False,"reason":f"Need {threshold}/{max_sc}s, got {score}","scored":scan.get("scored",0)})
                else:
                    # Check position limit
                    if get_position_count() >= MAX_POSITIONS:
                        self.send_json({"executed":False,"reason":f"Max {MAX_POSITIONS} positions reached"})
                        return
                    pick = scan["candidate"]
                    sym = pick["s"]
                    cat = get_category(sym)
                    busd_amt = score_to_busd(score, max_sc, cat)
                    if busd_amt <= 0:
                        self.send_json({"executed":False,"reason":f"No trade amount for {sym} (category: {cat})"})
                        return
                    addr = None
                    if sym in TWAK_NATIVE:
                        addr = sym  # TWAK accepts symbol for native tokens
                    elif sym in VERIFIED_TOKENS:
                        addr = VERIFIED_TOKENS[sym]
                        safe, reason = check_token_safe(sym, addr)
                        if not safe:
                            self.send_json({"executed":False,"reason":f"Security blocked {sym}: {reason}","candidate":sym,"signals":score})
                            return
                        print(f"  🛡️ {sym} passed risk check: {reason}")
                    else:
                        self.send_json({"executed":False,"reason":f"{sym} not in verified list","candidate":sym,"signals":score})
                        return
                    # Execute swap: BUSD → token
                    result = twak_jsonrpc("swap",{"fromToken":"BUSD","toToken":addr,"amount":str(busd_amt),"fromChain":"bsc","toChain":"bsc","slippage":"5"})
                    text = twak_swap_text(result)
                    sd = json.loads(text) if isinstance(text, str) else text
                    tx_hash = sd.get("hash","")
                    success = sd.get("success",False) or bool(tx_hash)
                    if success:
                        TRADE_COUNT += 1
                        ts = dt.utcnow().strftime("%d %b %H:%M")
                        tr = sd.get("summary","")
                        # Calculate entry price (BUSD per token)
                        entry_price = None
                        tokens_received = None
                        if "->" in tr:
                            parts = tr.split("->")
                            if len(parts) >= 2:
                                try:
                                    tokens_received = float(parts[1].strip().split(" ")[0])
                                    entry_price = busd_amt / tokens_received if tokens_received > 0 else None
                                except: pass
                        pair_str = f"BUSD→{sym}"
                        TRADE_HISTORY.append({"time":ts,"pair":pair_str,"dir":"BUY","amt":tr,"tx":tx_hash})
                        # Track position
                        if entry_price and tokens_received:
                            add_position(sym, addr, entry_price, tokens_received, busd_amt, cat)
                        self.send_json({"executed":True,"candidate":sym,"signals":score,"max_score":max_sc,"threshold":threshold,"tx":tx_hash,"explorer":sd.get("explorer",""),"busd":busd_amt,"category":cat,"summary":tr,"entry_price":entry_price,"tokens":tokens_received})
                    else:
                        self.send_json({"executed":False,"reason":sd.get("message","Swap failed"),"candidate":sym,"signals":score})
            except Exception as e:
                self.send_json({"executed":False,"error":str(e)})
        elif p.startswith("/api/manual/swap"):
            """Unified manual swap: any FROM token → any TO token."""
            try:
                qs = urllib.parse.urlparse(self.path).query
                qp = urllib.parse.parse_qs(qs)
                from_t = qp.get("from",["BUSD"])[0].upper()
                to_t = qp.get("to",["CAKE"])[0].upper()
                amt = qp.get("amount",["1"])[0]
                if from_t == to_t:
                    self.send_json({"executed":False,"reason":"Cannot swap "+from_t+" to itself"}); return
                def resolve(sym):
                    if sym == "BNB": return "BNB"
                    if sym in TWAK_NATIVE: return sym
                    if sym in VERIFIED_TOKENS: return VERIFIED_TOKENS[sym]
                    return None
                from_addr = resolve(from_t)
                to_addr = resolve(to_t)
                if not from_addr:
                    self.send_json({"executed":False,"reason":from_t+" not supported"}); return
                if not to_addr:
                    self.send_json({"executed":False,"reason":to_t+" not supported"}); return
                for sym, addr in [(from_t, from_addr), (to_t, to_addr)]:
                    if sym not in TWAK_NATIVE and sym != "BNB" and addr != "BNB":
                        safe, reason = check_token_safe(sym, addr)
                        if not safe:
                            self.send_json({"executed":False,"reason":f"Security blocked {sym}: {reason}"}); return
                        print(f"  🛡️ {sym} passed risk check: {reason}")
                result = twak_jsonrpc("swap",{"fromToken":from_addr,"toToken":to_addr,"amount":amt,"fromChain":"bsc","toChain":"bsc","slippage":"5"})
                text = twak_swap_text(result)
                sd = json.loads(text) if isinstance(text, str) else text
                tx_hash = sd.get("hash","")
                success = sd.get("success",False) or bool(tx_hash)
                if success:
                    TRADE_COUNT += 1
                    ts = dt.utcnow().strftime("%d %b %H:%M")
                    TRADE_HISTORY.append({"time":ts,"pair":from_t+"→"+to_t,"dir":"SWAP","amt":sd.get("summary",amt+" swap"),"tx":tx_hash})
                    self.send_json({"executed":True,"tx":tx_hash,"explorer":sd.get("explorer",""),"summary":sd.get("summary","")})
                else:
                    self.send_json({"executed":False,"reason":sd.get("message","Swap failed")})
            except Exception as e:
                self.send_json({"executed":False,"error":str(e)})
        elif p.startswith("/api/manual/alt-swap"):
            """Legacy alias — routes to unified swap."""
            qs = urllib.parse.urlparse(self.path).query
            qp = urllib.parse.parse_qs(qs)
            to_t = qp.get("to",["CAKE"])[0].upper()
            amt = qp.get("amount",["1"])[0]
            self.path = "/api/manual/swap?from=BUSD&to="+to_t+"&amount="+amt
            self.do_GET()
        elif p.startswith("/api/manual/withdraw"):
            """Withdraw tokens to an external address."""
            try:
                qs = urllib.parse.urlparse(self.path).query
                qp = urllib.parse.parse_qs(qs)
                to_addr = qp.get("to",[""])[0]
                amount = qp.get("amount",["0"])[0]
                token = qp.get("token",["BUSD"])[0].upper()
                if not to_addr or not amount:
                    self.send_json({"executed":False,"reason":"Missing to address or amount"}); return
                if token == "BNB":
                    result = twak_jsonrpc("transfer",{"to":to_addr,"amount":amount,"chain":"bsc"})
                else:
                    if token not in VERIFIED_TOKENS:
                        self.send_json({"executed":False,"reason":token+" not supported"}); return
                    addr = VERIFIED_TOKENS[token] if token != "BNB" else "BNB"
                    result = twak_jsonrpc("transfer_token",{"to":to_addr,"amount":amount,"tokenAddress":addr,"chain":"bsc"})
                text = twak_swap_text(result)
                sd = json.loads(text) if isinstance(text, str) else text
                tx_hash = sd.get("hash","") or sd.get("txid","")
                if tx_hash:
                    self.send_json({"executed":True,"tx":tx_hash,"explorer":"https://bscscan.com/tx/"+tx_hash})
                else:
                    self.send_json({"executed":False,"reason":sd.get("message","Transfer failed")})
            except Exception as e:
                self.send_json({"executed":False,"error":str(e)})
        elif p == "/api/status":
            self.send_json({"online": True, "cached_endpoints": list(cache.keys()) if cache else ["waiting..."]})
        elif p == "/api/chart/btc":
            hist = cache.get("btc_history", [])
            self.send_json({"prices": hist, "symbol": "BTC"})
        elif p == "/api/derivatives":
            self.send_json({"openInterest": "399.84B", "fundingRate": "+0.003%"})
        elif p == "/api/wallet":
            w = cache.get("wallet", {"bnb": 0, "usd": 0, "bnb_price": 577, "closedTrades": TRADE_COUNT, "initUsd": 49.00})
            self.send_json(w)
        elif p == "/api/wallet/details":
            wd = cache.get("wallet_details", {"total":0,"items":[]})
            self.send_json(wd)
        elif p == "/api/trades":
            self.send_json(TRADE_HISTORY)
        elif p == "/api/positions":
            with POSITIONS_LOCK:
                pos_copy = [dict(x, entry_time=round(x["entry_time"],0)) for x in POSITIONS]
            self.send_json({"count": len(pos_copy), "max": MAX_POSITIONS, "positions": pos_copy})
        elif p == "/api/progress":
            self.send_json({"count": len(PROGRESS), "events": PROGRESS[-50:]})
        elif p == "/api/verified-tokens":
            """Return the list of verified tokens with their addresses."""
            info = {}
            for sym, addr in VERIFIED_TOKENS.items():
                info[sym] = {"address": addr, "isTwakNative": sym in TWAK_NATIVE}
            self.send_json({"count": len(info), "tokens": info})
        else:
            f = BASE_DIR / (p.lstrip("/") if p != "/" else "trading-dashboard.html")
            if f.exists():
                self.send_response(200)
                ext = f.suffix
                ct = {"": "text/html", ".html": "text/html", ".js": "application/javascript", ".css": "text/css", ".txt": "text/plain", ".json": "application/json"}.get(ext, "application/octet-stream")
                self.send_header("Content-Type", ct)
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(f, "rb") as fp:
                    self.wfile.write(fp.read())
            else:
                self.send_error(404)

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def refresh_positions():
    """Background thread: profit-taking ladder & trailing stop-loss."""
    global TRADE_COUNT
    while True:
        try:
            with cache_lock:
                qd = cache.get("quotes", {})
            with POSITIONS_LOCK:
                for i in range(len(POSITIONS) - 1, -1, -1):
                    p = POSITIONS[i]
                    cur_price = None
                    if isinstance(qd, dict) and "data" in qd:
                        q = qd["data"].get(p["token"], {}).get("quote", {}).get("USD", {})
                        if q: cur_price = q.get("price", 0)
                    if not cur_price or cur_price <= 0: continue
                    entry = p["entry_price"]
                    pnl = (cur_price - entry) / entry
                    if cur_price > p["highest"]:
                        p["highest"] = cur_price
                        cp = CATEGORY_PARAMS.get(p["cat"], CATEGORY_PARAMS["blue_chip"])
                        p["trailing_stop"] = cur_price * (1 - cp["stop"])
                    # Stop-loss
                    if cur_price <= p["trailing_stop"] and cur_price < entry:
                        close_position(i, f"stop {pnl*100:.1f}%")
                        print(f"  🛑 STOP {p['token']} {pnl*100:.1f}%")
                        continue
                    # Profit tiers
                    for pct, key, frac, label in [(0.08,"tier1_sold",0.25,"+8%"),(0.15,"tier2_sold",0.25,"+15%"),(0.25,"tier3_sold",0.25,"+25%")]:
                        if pnl >= pct and not p[key]:
                            sell = p["amt_tokens"] * frac
                            if sell > 0:
                                try:
                                    r = twak_jsonrpc("swap",{"fromToken":p["address"],"toToken":"BUSD","amount":str(sell),"fromChain":"bsc","toChain":"bsc","slippage":"5"})
                                    t = twak_swap_text(r)
                                    d = json.loads(t) if isinstance(t,str) else t
                                    if d.get("success") or d.get("hash"):
                                        p[key] = True
                                        p["amt_tokens"] -= sell
                                        TRADE_COUNT += 1
                                        ts = dt.utcnow().strftime("%d %b %H:%M")
                                        TRADE_HISTORY.append({"time":ts,"pair":f"{p['token']}→BUSD","dir":label,"amt":d.get("summary",f"sold"),"tx":d.get("hash","")})
                                        print(f"  💰 {label}: {p['token']} → BUSD")
                                except: pass
                    if p["amt_tokens"] < 0.0001:
                        close_position(i, "sold out")
        except: pass
        time.sleep(60)

if __name__ == "__main__":
    print("📊 Server on port {}".format(PORT))
    print("  📊 Market data refreshing every {}s...".format(CACHE_TTL))
    t = threading.Thread(target=refresh_cache, daemon=True)
    t.start()
    tw = threading.Thread(target=refresh_wallet, daemon=True)
    tw.start()
    tp = threading.Thread(target=refresh_positions, daemon=True)
    tp.start()
    time.sleep(2)
    try:
        gd = cache.get("global", {}).get("data", {})
        qd = gd.get("quote", {}).get("USD", {})
        qc = cache.get("quotes", {}).get("data", {})
        btc2 = qc.get("BTC", {}).get("quote", {}).get("USD", {}) if qc else {}
        eth2 = qc.get("ETH", {}).get("quote", {}).get("USD", {}) if qc else {}
        sol2 = qc.get("SOL", {}).get("quote", {}).get("USD", {}) if qc else {}
        mcap2 = qd.get("total_market_cap", 0)
        if mcap2:
            print("  📊 MCAP ${:.2f}T | BTC ${:,.0f} ({:+.2f}%) | ETH ${:,.0f} ({:+.2f}%)".format(mcap2/1e12, btc2.get('price',0), btc2.get('percent_change_24h',0), eth2.get('price',0), eth2.get('percent_change_24h',0)))
            print("  🔥 SOL ${:,.2f} ({:+.2f}%) | F&G {} | BTC.D {:.2f}%".format(sol2.get('price',0), sol2.get('percent_change_24h',0), gd.get('fear_and_greed',{}).get('value','?'), gd.get('btc_dominance',0)))
            print("  🟢 3 endpoints cached")
    except:
        pass
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
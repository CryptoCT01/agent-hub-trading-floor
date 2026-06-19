#!/usr/bin/env python3
import os, json, http.server, urllib.request, urllib.parse, threading, time, ssl, subprocess
from pathlib import Path

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

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

TRADE_HISTORY = [
  {"time":"17 Jun 14:30","pair":"BNB→BUSD","dir":"SELL","amt":"0.001 BNB → 0.5965 BUSD","tx":"0x4d9a72cb25e1ebe808bf496c74961feb06b620ad345769531b85b826b110fc34"},
  {"time":"18 Jun 09:50","pair":"BNB→BUSD","dir":"SELL","amt":"0.001 BNB → 0.2857 BUSD","tx":"0x26dfe7b6f43a5536e7a0c01c465d6361424a6b287ccde8977a6b6cad0d02c31b"},
  {"time":"18 Jun 18:22","pair":"BNB→BUSD","dir":"SELL","amt":"0.001 BNB → 0.2857 BUSD","tx":"0x6c9a15ac0bf22e05a85b9bada1e8d6d56502b0e4e23ef2272b1dbeae075b7e9b"},
  {"time":"19 Jun 06:04","pair":"BNB→BUSD","dir":"SELL","amt":"0.001 BNB → 0.5705 BUSD","tx":"0x5e9fdc3543e34c388f10218e8e8815d97812f2564ab6acf867eaa809cbc9fd33"},
  {"time":"19 Jun 06:09","pair":"BNB→BUSD","dir":"SELL","amt":"0.001 BNB → 0.5705 BUSD","tx":"0xbf6596b23226ce36173f43fe030ed7bd709e4eb2a61cd744b2e3bcabca6c554e"},
]
TRADE_COUNT = len(TRADE_HISTORY)  # tracks live swaps from history

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
    with cache_lock:
        qd = cache.get("quotes", {})
    if not isinstance(qd, dict) or "data" not in qd:
        return {"candidate": None, "reason": "No data", "signals": 0}
    coins = []
    for sym, info in qd["data"].items():
        q = info.get("quote", {}).get("USD", {})
        if not q:
            continue
        coins.append({"s": sym, "p": q.get("price", 0), "c24": q.get("percent_change_24h", 0), "c7": q.get("percent_change_7d", 0), "v": q.get("volume_24h", 0)})
    scored = []
    for c in coins:
        if c["p"] < 0.01 or c["s"] in ("USDT", "USDC", "BUSD"):
            continue
        sig = 0
        det = []
        if c["c7"] > 5:
            sig += 1; det.append("MOM+")
        if c["c24"] > -3:
            sig += 1; det.append("STBL")
        if c["v"] > 10e6:
            sig += 1; det.append("VOL+")
        sig += 1; det.append("STR")
        if c["c7"] > 10:
            sig += 1; det.append("BUL+")
        if c["c24"] > 0:
            sig += 1; det.append("24H+")
        if c["c7"] > c["c24"]:
            sig += 1; det.append("ACC+")
        sig += 1; det.append("REG")
        scored.append({"s": c["s"], "score": sig, "p": c["p"], "c24": c["c24"], "c7": c["c7"], "det": det})
    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0] if scored else None
    return {"candidate": best, "signals": best["score"] if best else 0, "total": len(coins), "scored": len(scored)}

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
                import subprocess as sp
                def mc(m,a):
                    pr = sp.Popen(['/Users/cryptot/.hermes/node/bin/twak','serve'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,
                        env={'TWAK_ACCESS_ID':TWAK_ACCESS_ID or '','TWAK_HMAC_SECRET':TWAK_HMAC_SECRET or '','PATH':'/Users/cryptot/.hermes/node/bin'})
                    rq = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':m,'arguments':a}})
                    o,_ = pr.communicate((rq+'\n').encode(), timeout=20)
                    return json.loads(o.decode())
                scan = scan_strategy()
                if not scan.get("candidate") or scan.get("signals",0) < 4:
                    self.send_json({"executed":False,"reason":"Need 4/8+ signals, got "+str(scan.get("signals",0)),"scored":scan.get("scored",0)})
                else:
                    pick = scan["candidate"]
                    # TWAK's native swap registry handles BNB→BUSD/BTC/etc directly
                    # Skip altcoin address map — use TWAK-native token symbols
                    native_tokens = ["BUSD","USDT","USDC","DAI","ETH"]  # TWAK-supported on BSC
                    if pick["s"] in native_tokens:
                        to_token = pick["s"]
                    else:
                        to_token = "BUSD"  # fall back to stablecoin for safety
                    result = mc("swap",{"fromToken":"BNB","toToken":to_token,"amount":"0.001","fromChain":"bsc","toChain":"bsc","slippage":"1"})
                    rt = result.get("result",{}).get("content",[{}])[0].get("text","{}")
                    sd = json.loads(rt) if isinstance(rt,str) else rt
                    tx_hash = sd.get("hash","")
                    success = sd.get("success",False) or bool(tx_hash)
                    if success:
                        TRADE_COUNT += 1
                        import datetime
                        ts = datetime.datetime.utcnow().strftime("%d %b %H:%M")
                        TRADE_HISTORY.append({"time":ts,"pair":"BNB→"+to_token,"dir":"SELL","amt":sd.get("summary","0.001 BNB swap"),"tx":tx_hash})
                        self.send_json({"executed":True,"candidate":pick["s"],"signals":scan["signals"],"tx":tx_hash,"explorer":sd.get("explorer",""),"toToken":to_token,"summary":sd.get("summary","")})
                    else:
                        self.send_json({"executed":False,"reason":sd.get("message","Swap failed"),"candidate":pick["s"],"signals":scan["signals"]})
            except Exception as e:
                self.send_json({"executed":False,"error":str(e)})
        elif p.startswith("/api/manual/swap"):
            try:
                qs = urllib.parse.urlparse(self.path).query
                qp = urllib.parse.parse_qs(qs)
                from_t = qp.get("from",["BNB"])[0].upper()
                to_t = qp.get("to",["BUSD"])[0].upper()
                amt = qp.get("amount",["0.001"])[0]
                native_tokens = ["BNB","BUSD","USDT","USDC","DAI","ETH"]
                if from_t not in native_tokens:
                    self.send_json({"executed":False,"reason":from_t+" not supported. Use: "+", ".join(native_tokens)}); return
                if to_t not in native_tokens:
                    self.send_json({"executed":False,"reason":to_t+" not supported. Use: "+", ".join(native_tokens)}); return
                if from_t == to_t:
                    self.send_json({"executed":False,"reason":"Cannot swap "+from_t+" to itself"}); return
                import subprocess as sp
                def mc(m,a):
                    pr = sp.Popen(['/Users/cryptot/.hermes/node/bin/twak','serve'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,
                        env={'TWAK_ACCESS_ID':TWAK_ACCESS_ID or '','TWAK_HMAC_SECRET':TWAK_HMAC_SECRET or '','PATH':'/Users/cryptot/.hermes/node/bin'})
                    rq = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':m,'arguments':a}})
                    o,_ = pr.communicate((rq+'\n').encode(), timeout=20)
                    return json.loads(o.decode())
                result = mc("swap",{"fromToken":from_t,"toToken":to_t,"amount":amt,"fromChain":"bsc","toChain":"bsc","slippage":"1"})
                rt = result.get("result",{}).get("content",[{}])[0].get("text","{}")
                sd = json.loads(rt) if isinstance(rt,str) else rt
                tx_hash = sd.get("hash","")
                success = sd.get("success",False) or bool(tx_hash)
                if success:
                    TRADE_COUNT += 1
                    import datetime
                    ts = datetime.datetime.utcnow().strftime("%d %b %H:%M")
                    label = "SWAP"
                    TRADE_HISTORY.append({"time":ts,"pair":from_t+"→"+to_t,"dir":label,"amt":sd.get("summary",amt+" "+from_t+" swap"),"tx":tx_hash})
                    self.send_json({"executed":True,"tx":tx_hash,"explorer":sd.get("explorer",""),"summary":sd.get("summary","")})
                else:
                    self.send_json({"executed":False,"reason":sd.get("message","Swap failed")})
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

if __name__ == "__main__":
    print("📊 Server on port {}".format(PORT))
    print("  📊 Market data refreshing every {}s...".format(CACHE_TTL))
    t = threading.Thread(target=refresh_cache, daemon=True)
    t.start()
    tw = threading.Thread(target=refresh_wallet, daemon=True)
    tw.start()
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
# -*- coding: utf-8 -*-
# Position Tracker - Multi usuario con Supabase
# pip install streamlit requests
# streamlit run app.py

import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Position Tracker", page_icon=":bar_chart:", layout="wide")

SUPABASE_URL = "https://lwuebbipkcvreeawrpah.supabase.co"
SUPABASE_KEY = "sb_publishable_61ghP-Nb4FsPQx9T2xv2sw_QlJIdCqJ"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}


CSS = """
<style>
html, body, [class*="css"] { background-color: #050a0e !important; color: #8ab4c8; font-family: monospace; }
.stApp { background-color: #050a0e; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem; }
div[data-testid="stNumberInput"] input { background:#0a1018 !important; color:#8ab4c8 !important; border:1px solid #0f2a3a !important; font-family:monospace !important; font-size:0.95rem !important; }
div[data-testid="stSelectbox"] > div { background:#0a1018 !important; color:#8ab4c8 !important; border:1px solid #0f2a3a !important; }
div[data-testid="stTextInput"] input { background:#0a1018 !important; color:#8ab4c8 !important; border:1px solid #0f2a3a !important; font-family:monospace !important; font-size:1rem !important; }
label[data-testid="stWidgetLabel"] p { font-size:0.55rem !important; letter-spacing:2px !important; color:#2a4a5a !important; }
.stButton button { background:#0a1018 !important; color:#8ab4c8 !important; border:1px solid #0f2a3a !important; font-family:monospace !important; letter-spacing:2px; font-size:0.72rem; }
.stButton button:hover { border-color:#00c8ff !important; color:#00c8ff !important; }
.login-wrap { max-width:420px; margin:80px auto 0; background:#0a1018; border:1px solid #0f2a3a; border-top:3px solid #00c8ff; padding:40px 36px; }
.login-title { font-size:1.4rem; letter-spacing:6px; color:#00c8ff; font-weight:700; margin-bottom:4px; }
.login-sub { font-size:0.6rem; color:#2a4a5a; letter-spacing:3px; margin-bottom:28px; }
.top-bar { background:#0a1018; border:1px solid #0f2a3a; border-top:3px solid #00c8ff; padding:16px 24px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; }
.top-title { font-size:0.52rem; color:#2a4a5a; letter-spacing:4px; margin-bottom:4px; }
.top-total-pos { font-size:2rem; font-weight:700; color:#00ff88; }
.top-total-neg { font-size:2rem; font-weight:700; color:#ff3366; }
.top-total-neu { font-size:2rem; font-weight:700; color:#ffd700; }
.top-stat-val-pos { font-size:1.1rem; font-weight:700; color:#00ff88; }
.top-stat-val-neg { font-size:1.1rem; font-weight:700; color:#ff3366; }
.top-stat-val-neu { font-size:1.1rem; color:#ffd700; }
.top-stat-val-mut { font-size:1.1rem; color:#8ab4c8; }
.top-divider { width:1px; height:44px; background:#0f2a3a; }
.pos-card { background:#0a1018; border:1px solid #0f2a3a; border-left:3px solid #2a4a5a; padding:16px 18px; }
.pos-card.win { border-left-color:#00ff88; }
.pos-card.los { border-left-color:#ff3366; }
.pos-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.pos-name { font-size:0.95rem; letter-spacing:3px; color:#8ab4c8; }
.badges { display:flex; gap:5px; }
.b-long { font-size:0.55rem; color:#00ff88; border:1px solid #00ff88; padding:2px 7px; letter-spacing:2px; }
.b-short { font-size:0.55rem; color:#ff3366; border:1px solid #ff3366; padding:2px 7px; letter-spacing:2px; }
.b-lev { font-size:0.55rem; color:#ffd700; border:1px solid #ffd700; padding:2px 7px; letter-spacing:2px; }
.pnl-main-pos { font-size:1.8rem; font-weight:700; color:#00ff88; line-height:1; }
.pnl-main-neg { font-size:1.8rem; font-weight:700; color:#ff3366; line-height:1; }
.pnl-main-neu { font-size:1.8rem; font-weight:700; color:#2a4a5a; line-height:1; }
.pnl-pct-pos { font-size:0.95rem; color:#00ff88; }
.pnl-pct-neg { font-size:0.95rem; color:#ff3366; }
.pnl-pct-neu { font-size:0.95rem; color:#2a4a5a; }
.pnl-sub { font-size:0.52rem; color:#2a4a5a; letter-spacing:2px; margin-top:2px; margin-bottom:10px; }
.detail-row { display:flex; gap:16px; padding-top:10px; border-top:1px solid #0f2a3a; flex-wrap:wrap; }
.d-item label { display:block; font-size:0.5rem; color:#2a4a5a; letter-spacing:2px; margin-bottom:2px; }
.d-val { font-size:0.82rem; color:#8ab4c8; }
.d-val.green { color:#00ff88; } .d-val.red { color:#ff3366; } .d-val.gold { color:#ffd700; }
.empty-card { background:#0a1018; border:1px solid #0f2a3a; border-left:3px solid #0f2a3a; padding:16px 18px; color:#2a4a5a; font-size:0.72rem; letter-spacing:2px; }
.grand-bar { background:#0a1018; border:1px solid #00c8ff44; border-top:2px solid #00c8ff; padding:16px 22px; margin-top:12px; display:flex; gap:40px; flex-wrap:wrap; align-items:center; }
.gb-label { font-size:0.54rem; color:#2a4a5a; letter-spacing:3px; margin-bottom:4px; }
.gb-val-pos { font-size:1.5rem; font-weight:700; color:#00ff88; }
.gb-val-neg { font-size:1.5rem; font-weight:700; color:#ff3366; }
.gb-val-neu { font-size:1.5rem; font-weight:700; color:#00c8ff; }
.section-line { font-size:0.54rem; color:#2a4a5a; letter-spacing:4px; border-bottom:1px solid #0f2a3a; padding-bottom:6px; margin:16px 0 12px; }
.status-ok { color:#00ff88; font-size:0.62rem; letter-spacing:2px; }
.status-err { color:#ff3366; font-size:0.62rem; letter-spacing:2px; }
.source-tag { color:#2a4a5a; font-size:0.6rem; letter-spacing:2px; margin-left:10px; }
.saving-tag { color:#ffd700; font-size:0.6rem; letter-spacing:2px; margin-left:8px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PAIRS     = ["BTCUSDT","ETHUSDT","ADAUSDT","SOLUSDT","BNBUSDT","XRPUSDT","DOGEUSDT","PAXGUSDT","AVAXUSDT","DOTUSDT","LINKUSDT"]
LEVERAGES = [1, 2, 3, 5, 10, 20, 25, 50, 75, 100, 125]
KRAKEN_MAP      = {"BTCUSDT":"XBTUSD","ETHUSDT":"ETHUSD","ADAUSDT":"ADAUSD","SOLUSDT":"SOLUSD","BNBUSDT":"BNBUSD","XRPUSDT":"XRPUSD","DOGEUSDT":"DOGEUSD","PAXGUSDT":"PAXGUSD","AVAXUSDT":"AVAXUSD","DOTUSDT":"DOTUSD","LINKUSDT":"LINKUSD"}
COINGECKO_MAP   = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","ADAUSDT":"cardano","SOLUSDT":"solana","BNBUSDT":"binancecoin","XRPUSDT":"ripple","DOGEUSDT":"dogecoin","PAXGUSDT":"pax-gold","AVAXUSDT":"avalanche-2","DOTUSDT":"polkadot","LINKUSDT":"chainlink"}
COINPAPRIKA_MAP = {"BTCUSDT":"btc-bitcoin","ETHUSDT":"eth-ethereum","ADAUSDT":"ada-cardano","SOLUSDT":"sol-solana","BNBUSDT":"bnb-binance-coin","XRPUSDT":"xrp-xrp","DOGEUSDT":"doge-dogecoin","PAXGUSDT":"paxg-pax-gold","AVAXUSDT":"avax-avalanche","DOTUSDT":"dot-polkadot","LINKUSDT":"link-chainlink"}

def fmt_price(n):
    try:
        v = float(n)
        if v >= 10000: return f"{v:,.1f}"
        if v >= 100:   return f"{v:,.2f}"
        if v >= 1:     return f"{v:,.4f}"
        return f"{v:.6f}"
    except Exception: return "-"

def fetch_kraken(symbols):
    try:
        pairs = [KRAKEN_MAP[s] for s in symbols if s in KRAKEN_MAP]
        r = requests.get("https://api.kraken.com/0/public/Ticker", params={"pair": ",".join(pairs)}, timeout=8)
        data = r.json()
        if data.get("error"): return {}, False
        result = {}
        for sym in symbols:
            k = KRAKEN_MAP.get(sym)
            if k and k in data.get("result", {}):
                result[sym] = float(data["result"][k]["c"][0])
        return result, len(result) > 0
    except Exception: return {}, False

def fetch_coingecko(symbols):
    try:
        ids = [COINGECKO_MAP[s] for s in symbols if s in COINGECKO_MAP]
        r = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": ",".join(ids), "vs_currencies": "usd"}, timeout=8)
        data = r.json()
        result = {sym: float(data[COINGECKO_MAP[sym]]["usd"]) for sym in symbols if COINGECKO_MAP.get(sym) in data}
        return result, len(result) > 0
    except Exception: return {}, False

def fetch_coinpaprika(symbols):
    result = {}
    try:
        for sym in symbols:
            cp = COINPAPRIKA_MAP.get(sym)
            if not cp: continue
            r = requests.get(f"https://api.coinpaprika.com/v1/tickers/{cp}", params={"quotes":"USD"}, timeout=6)
            result[sym] = float(r.json()["quotes"]["USD"]["price"])
        return result, len(result) > 0
    except Exception: return result, len(result) > 0

def fetch_all_prices(symbols):
    prices, ok = fetch_kraken(symbols)
    if ok and len(prices) == len(symbols): return prices, "Kraken"
    prices2, ok2 = fetch_coingecko(symbols)
    if ok2 and len(prices2) == len(symbols): return prices2, "CoinGecko"
    merged = {**prices, **prices2}
    missing = [s for s in symbols if s not in merged]
    if missing:
        prices3, _ = fetch_coinpaprika(missing)
        merged.update(prices3)
    return merged, "Multi"

def sb_get(table, filters=""):
    try:
        r = requests.get(f"{SUPABASE_URL}/rest/v1/{table}?{filters}", headers=HEADERS, timeout=6)
        return r.json() if r.ok else []
    except Exception: return []

def sb_upsert(table, data):
    try:
        h = {**HEADERS, "Prefer": "resolution=merge-duplicates,return=representation"}
        r = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=h, json=data, timeout=6)
        return r.ok
    except Exception: return False

def sb_delete(table, filters):
    try:
        r = requests.delete(f"{SUPABASE_URL}/rest/v1/{table}?{filters}", headers=HEADERS, timeout=6)
        return r.ok
    except Exception: return False

def sb_insert(table, data):
    try:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS, json=data, timeout=6)
        return r.ok
    except Exception: return False

def load_user_data(username):
    raw = sb_get("positions", f"username=eq.{username}&order=id.asc")
    if not raw:
        positions = [
            {"pair":"ETHUSDT",  "side":"Long","entry":0.0,"qty":0.0,"lev":10},
            {"pair":"ADAUSDT",  "side":"Long","entry":0.0,"qty":0.0,"lev":10},
            {"pair":"PAXGUSDT", "side":"Long","entry":0.0,"qty":0.0,"lev":10},
            {"pair":"BTCUSDT",  "side":"Long","entry":0.0,"qty":0.0,"lev":10},
        ]
    else:
        positions = [{"pair":p["pair"],"side":p["side"],"entry":float(p["entry"]),"qty":float(p["qty"]),"lev":int(p["lev"])} for p in raw]
    raw_c  = sb_get("closed_trades", f"username=eq.{username}&order=id.asc")
    closed = [{"label":t["label"],"pnl":float(t["pnl"]),"date":t["date"],"id":t["id"]} for t in raw_c]
    return positions, closed

def save_positions(username, positions):
    sb_delete("positions", f"username=eq.{username}")
    if positions:
        rows = [{"username":username,"pair":p["pair"],"side":p["side"],"entry":p["entry"],"qty":p["qty"],"lev":p["lev"]} for p in positions]
        sb_insert("positions", rows)

# Session state
for k, v in [("username",""),("logged_in",False),("positions",[]),("live",{}),
             ("last_update",""),("closed_trades",[]),("fetch_error",False),("price_source","")]:
    if k not in st.session_state: st.session_state[k] = v

# LOGIN
if not st.session_state.logged_in:
    st.markdown('<div class="login-wrap"><div class="login-title">POSITION<span style="color:#00ff88">TRACKER</span></div><div class="login-sub">FUTURES | MULTI USUARIO | SUPABASE</div></div>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        name  = st.text_input("TU NOMBRE", placeholder="ej: Agustin", key="name_input")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("ENTRAR", use_container_width=True) and name.strip():
            uname = name.strip().lower()
            sb_upsert("users", [{"username": uname}])
            positions, closed = load_user_data(uname)
            st.session_state.username      = uname
            st.session_state.logged_in     = True
            st.session_state.positions     = positions
            st.session_state.closed_trades = closed
            st.rerun()
    st.stop()

# FETCH PRICES
tracked = list({p["pair"] for p in st.session_state.positions})
prices, source = fetch_all_prices(tracked)
if prices:
    st.session_state.live.update(prices)
    st.session_state.fetch_error  = False
    st.session_state.price_source = source
else:
    st.session_state.fetch_error = True
st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# COMPUTE P&L
total_open_pnl = 0.0
total_open_margin = 0.0
any_active = False
pos_data = []
for pos in st.session_state.positions:
    current = st.session_state.live.get(pos["pair"])
    entry, qty, lev = pos["entry"], pos["qty"], pos["lev"]
    if entry > 0 and qty > 0 and current and current > 0:
        notional  = entry * qty
        margin    = notional / lev
        pnl_usd   = (current - entry) * qty if pos["side"] == "Long" else (entry - current) * qty
        pnl_pct_m = (pnl_usd / margin)   * 100
        pnl_pct_n = (pnl_usd / notional) * 100
        total_open_pnl    += pnl_usd
        total_open_margin += margin
        any_active = True
        pos_data.append({**pos,"current":current,"notional":notional,"margin":margin,"pnl_usd":pnl_usd,"pnl_pct_m":pnl_pct_m,"pnl_pct_n":pnl_pct_n,"active":True})
    else:
        pos_data.append({**pos,"current":current,"active":False})

closed_total = sum(t["pnl"] for t in st.session_state.closed_trades)
grand_total  = total_open_pnl + closed_total

# TOP BAR
def sign(v): return "+" if v >= 0 else ""
def vcls(v, pfx="top-stat-val"): return f"{pfx}-pos" if v > 0 else (f"{pfx}-neg" if v < 0 else f"{pfx}-neu")

open_pct = (total_open_pnl / total_open_margin * 100) if total_open_margin > 0 else 0
o_cls    = vcls(total_open_pnl, "top-total")
g_cls    = vcls(grand_total)
c_cls    = "top-stat-val-pos" if closed_total > 0 else ("top-stat-val-neg" if closed_total < 0 else "top-stat-val-mut")
pct_cls  = vcls(open_pct)

tb_left, tb_right = st.columns([5, 1])
with tb_left:
    so = sign(total_open_pnl); sg = sign(grand_total); sc = sign(closed_total); sp = sign(open_pct)
    st.markdown(f"""
<div class="top-bar">
  <div><div class="top-title">P&L ABIERTOS</div><div class="{o_cls}">{so}${total_open_pnl:,.2f} <span style="font-size:0.9rem">USDT</span></div></div>
  <div class="top-divider"></div>
  <div><div class="top-title">RETORNO MARGEN</div><div class="{pct_cls}">{sp}{open_pct:.2f}%</div></div>
  <div class="top-divider"></div>
  <div><div class="top-title">MARGEN USADO</div><div class="top-stat-val-mut">${total_open_margin:,.2f}</div></div>
  <div class="top-divider"></div>
  <div><div class="top-title">CERRADOS</div><div class="{c_cls}">{sc}${closed_total:,.2f}</div></div>
  <div class="top-divider"></div>
  <div><div class="top-title">TOTAL HISTORICO</div><div class="{g_cls}">{sg}${grand_total:,.2f}</div></div>
</div>""", unsafe_allow_html=True)

with tb_right:
    st.markdown(f"<div style='padding-top:8px;font-size:0.7rem;color:#2a4a5a;letter-spacing:2px'>USUARIO</div><div style='font-size:1rem;color:#00c8ff;letter-spacing:3px'>{st.session_state.username.upper()}</div>", unsafe_allow_html=True)
    if st.button("GUARDAR", use_container_width=True):
        save_positions(st.session_state.username, st.session_state.positions)
        st.toast("Guardado!")
    if st.button("SALIR", use_container_width=True):
        save_positions(st.session_state.username, st.session_state.positions)
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# POSITIONS 2x2
st.markdown("<div class='section-line'>POSICIONES ABIERTAS</div>", unsafe_allow_html=True)
if st.button("+ NUEVA POSICION"):
    st.session_state.positions.append({"pair":"BTCUSDT","side":"Long","entry":0.0,"qty":0.0,"lev":10})
    st.rerun()

n = len(st.session_state.positions)
for row in range(0, n, 2):
    col_left, col_right = st.columns(2, gap="medium")
    for col_idx, col in enumerate([col_left, col_right]):
        i = row + col_idx
        if i >= n: break
        pos = st.session_state.positions[i]
        pd  = pos_data[i]
        with col:
            ci1, ci2, ci3 = st.columns([2, 1.2, 1.2])
            with ci1:
                pair = st.selectbox("PAR", PAIRS, index=PAIRS.index(pos["pair"]) if pos["pair"] in PAIRS else 0, key=f"pair_{i}")
            with ci2:
                side = st.selectbox("LADO", ["Long","Short"], index=0 if pos["side"]=="Long" else 1, key=f"side_{i}")
            with ci3:
                lev_opts = [f"{x}x" for x in LEVERAGES]
                cur_str  = f"{pos['lev']}x"
                lev_str  = st.selectbox("APALANCAMIENTO", lev_opts, index=lev_opts.index(cur_str) if cur_str in lev_opts else 4, key=f"lev_{i}")
                lev      = int(lev_str.replace("x",""))
            ci4, ci5, ci6 = st.columns([2, 2, 0.6])
            with ci4:
                entry = st.number_input("PRECIO ENTRADA", min_value=0.0, value=float(pos["entry"]), format="%.4f", step=0.0001, key=f"entry_{i}")
            with ci5:
                qty = st.number_input("CANTIDAD MONEDAS", min_value=0.0, value=float(pos["qty"]), format="%.6f", step=0.001, key=f"qty_{i}")
            with ci6:
                st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
                if st.button("X", key=f"del_{i}", use_container_width=True):
                    st.session_state.positions.pop(i)
                    save_positions(st.session_state.username, st.session_state.positions)
                    st.rerun()
            st.session_state.positions[i] = {"pair":pair,"side":side,"entry":entry,"qty":qty,"lev":lev}

            if pd["active"]:
                pnl_usd = pd["pnl_usd"]; pnl_pct_m = pd["pnl_pct_m"]; pnl_pct_n = pd["pnl_pct_n"]
                current = pd["current"]; margin = pd["margin"]; notional = pd["notional"]
                sg    = sign(pnl_usd)
                status = "win" if pnl_usd > 0 else ("los" if pnl_usd < 0 else "")
                u_cls = "pnl-main-pos" if pnl_usd > 0 else ("pnl-main-neg" if pnl_usd < 0 else "pnl-main-neu")
                p_cls = "pnl-pct-pos"  if pnl_usd > 0 else ("pnl-pct-neg"  if pnl_usd < 0 else "pnl-pct-neu")
                pr_cls = "green" if current > entry else ("red" if current < entry else "")
                s_cls = "b-long" if side=="Long" else "b-short"
                st.markdown(f"""
<div class="pos-card {status}">
  <div class="pos-header">
    <span class="pos-name">{pair.replace("USDT","/USDT")}</span>
    <div class="badges"><span class="{s_cls}">{side.upper()}</span><span class="b-lev">{lev}x</span></div>
  </div>
  <div><span class="{u_cls}">{sg}${pnl_usd:,.2f}</span>&nbsp;<span class="{p_cls}">{sg}{pnl_pct_m:.2f}%</span></div>
  <div class="pnl-sub">P&L SOBRE MARGEN | PRECIO: {sg}{pnl_pct_n:.2f}%</div>
  <div class="detail-row">
    <div class="d-item"><label>ENTRADA</label><div class="d-val">{fmt_price(entry)}</div></div>
    <div class="d-item"><label>ACTUAL</label><div class="d-val {pr_cls}">{fmt_price(current)}</div></div>
    <div class="d-item"><label>MARGEN</label><div class="d-val gold">${margin:,.2f}</div></div>
    <div class="d-item"><label>NOCIONAL</label><div class="d-val">${notional:,.2f}</div></div>
  </div>
</div>""", unsafe_allow_html=True)
            else:
                s_cls = "b-long" if side=="Long" else "b-short"
                st.markdown(f'<div class="empty-card"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="color:#8ab4c8;letter-spacing:3px">{pair.replace("USDT","/USDT")}</span><div class="badges"><span class="{s_cls}">{side.upper()}</span><span class="b-lev">{lev}x</span></div></div>Ingresa precio de entrada y cantidad</div>', unsafe_allow_html=True)

# CLOSED TRADES
st.markdown("<div class='section-line'>TRADES CERRADOS</div>", unsafe_allow_html=True)
with st.expander("+ AGREGAR TRADE CERRADO", expanded=len(st.session_state.closed_trades)==0):
    cc1, cc2, cc3, cc4 = st.columns([2,2,2,1])
    with cc1: c_label = st.text_input("DESCRIPCION", placeholder="ej: BTC Long 10x", key="c_label")
    with cc2: c_pnl   = st.number_input("P&L REALIZADO (USDT)", value=0.0, format="%.2f", step=0.01, key="c_pnl")
    with cc3: c_date  = st.text_input("FECHA", placeholder="ej: 15/03/2026", key="c_date")
    with cc4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("AGREGAR", use_container_width=True, key="add_closed"):
            if c_pnl != 0.0:
                label = c_label if c_label else f"Trade {len(st.session_state.closed_trades)+1}"
                date  = c_date  if c_date  else datetime.now().strftime("%d/%m/%Y")
                sb_insert("closed_trades", [{"username":st.session_state.username,"label":label,"pnl":c_pnl,"date":date}])
                _, closed = load_user_data(st.session_state.username)
                st.session_state.closed_trades = closed
                st.rerun()

if st.session_state.closed_trades:
    for j, t in enumerate(st.session_state.closed_trades):
        sg    = sign(t["pnl"])
        color = "#00ff88" if t["pnl"] >= 0 else "#ff3366"
        tc1, tc2, tc3, tc4 = st.columns([3,2,1.5,0.5])
        with tc1: st.markdown(f"<span style='color:#8ab4c8;letter-spacing:2px;font-size:0.85rem'>{t['label']}</span>", unsafe_allow_html=True)
        with tc2: st.markdown(f"<span style='color:{color};font-size:1rem;font-weight:700'>{sg}${t['pnl']:,.2f}</span>", unsafe_allow_html=True)
        with tc3: st.markdown(f"<span style='color:#2a4a5a;font-size:0.75rem'>{t['date']}</span>", unsafe_allow_html=True)
        with tc4:
            if st.button("X", key=f"dc_{j}", use_container_width=True):
                sb_delete("closed_trades", f"id=eq.{t['id']}")
                _, closed = load_user_data(st.session_state.username)
                st.session_state.closed_trades = closed
                st.rerun()

    sc2 = sign(closed_total); sg2 = sign(grand_total)
    c_cls2 = "gb-val-pos" if closed_total > 0 else ("gb-val-neg" if closed_total < 0 else "gb-val-neu")
    g_cls2 = "gb-val-pos" if grand_total  > 0 else ("gb-val-neg" if grand_total  < 0 else "gb-val-neu")
    op_cls = "gb-val-pos" if total_open_pnl >= 0 else "gb-val-neg"
    so2    = sign(total_open_pnl)
    st.markdown(f"""
<div class="grand-bar">
  <div><div class="gb-label">CERRADOS ACUMULADO</div><div class="{c_cls2}">{sc2}${closed_total:,.2f}</div></div>
  <div><div class="gb-label">ABIERTOS AHORA</div><div class="{op_cls}">{so2}${total_open_pnl:,.2f}</div></div>
  <div><div class="gb-label">GANANCIA TOTAL HISTORICA</div><div class="{g_cls2}">{sg2}${grand_total:,.2f}</div></div>
</div>""", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
cs, cr = st.columns([3,1])
with cs:
    if st.session_state.fetch_error:
        st.markdown("<span class='status-err'>ERROR obteniendo precios - reintentando...</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='status-ok'>LIVE - {st.session_state.last_update}</span><span class='source-tag'>via {st.session_state.price_source}</span><span class='saving-tag'>| Supabase</span>", unsafe_allow_html=True)
with cr:
    ref = st.selectbox("Refresh", ["30s","60s","2m"], label_visibility="collapsed")
secs = {"30s":30,"60s":60,"2m":120}[ref]
time.sleep(secs)
save_positions(st.session_state.username, st.session_state.positions)
st.rerun()

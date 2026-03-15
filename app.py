# -*- coding: utf-8 -*-
# Position Tracker - Futures con Apalancamiento
# pip install streamlit requests
# streamlit run app.py

import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Position Tracker", page_icon=":bar_chart:", layout="wide")

CSS = """
<style>
html, body, [class*="css"] {
    background-color: #050a0e !important;
    color: #8ab4c8;
    font-family: monospace;
}
.stApp { background-color: #050a0e; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem; }
div[data-testid="stNumberInput"] input {
    background:#0a1018 !important; color:#8ab4c8 !important;
    border:1px solid #0f2a3a !important; font-family:monospace !important; font-size:0.95rem !important;
}
div[data-testid="stSelectbox"] > div {
    background:#0a1018 !important; color:#8ab4c8 !important; border:1px solid #0f2a3a !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size:0.55rem !important; letter-spacing:2px !important; color:#2a4a5a !important;
}
.stButton button {
    background:#0a1018 !important; color:#8ab4c8 !important;
    border:1px solid #0f2a3a !important; font-family:monospace !important;
    letter-spacing:2px; font-size:0.72rem;
}
.stButton button:hover { border-color:#00c8ff !important; color:#00c8ff !important; }
.top-bar {
    background:#0a1018; border:1px solid #0f2a3a; border-top:3px solid #00c8ff;
    padding:18px 28px; margin-bottom:18px;
    display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;
}
.top-title { font-size:0.58rem; color:#2a4a5a; letter-spacing:4px; margin-bottom:5px; }
.top-total-pos { font-size:2.4rem; font-weight:700; color:#00ff88; letter-spacing:1px; }
.top-total-neg { font-size:2.4rem; font-weight:700; color:#ff3366; letter-spacing:1px; }
.top-total-neu { font-size:2.4rem; font-weight:700; color:#ffd700; letter-spacing:1px; }
.top-stat-val-pos { font-size:1.2rem; font-weight:700; color:#00ff88; }
.top-stat-val-neg { font-size:1.2rem; font-weight:700; color:#ff3366; }
.top-stat-val-neu { font-size:1.2rem; color:#ffd700; }
.top-stat-val-mut { font-size:1.2rem; color:#8ab4c8; }
.top-divider { width:1px; height:50px; background:#0f2a3a; }
.pos-card { background:#0a1018; border:1px solid #0f2a3a; border-left:3px solid #2a4a5a; padding:16px 18px; }
.pos-card.win { border-left-color:#00ff88; }
.pos-card.los { border-left-color:#ff3366; }
.pos-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.pos-name { font-size:0.95rem; letter-spacing:3px; color:#8ab4c8; }
.badges { display:flex; gap:5px; }
.b-long  { font-size:0.55rem; color:#00ff88; border:1px solid #00ff88; padding:2px 7px; letter-spacing:2px; }
.b-short { font-size:0.55rem; color:#ff3366; border:1px solid #ff3366; padding:2px 7px; letter-spacing:2px; }
.b-lev   { font-size:0.55rem; color:#ffd700; border:1px solid #ffd700; padding:2px 7px; letter-spacing:2px; }
.pnl-main-pos { font-size:1.8rem; font-weight:700; color:#00ff88; letter-spacing:1px; line-height:1; }
.pnl-main-neg { font-size:1.8rem; font-weight:700; color:#ff3366; letter-spacing:1px; line-height:1; }
.pnl-main-neu { font-size:1.8rem; font-weight:700; color:#2a4a5a; letter-spacing:1px; line-height:1; }
.pnl-pct-pos { font-size:0.95rem; color:#00ff88; }
.pnl-pct-neg { font-size:0.95rem; color:#ff3366; }
.pnl-pct-neu { font-size:0.95rem; color:#2a4a5a; }
.pnl-sub { font-size:0.52rem; color:#2a4a5a; letter-spacing:2px; margin-top:2px; margin-bottom:10px; }
.detail-row { display:flex; gap:16px; padding-top:10px; border-top:1px solid #0f2a3a; flex-wrap:wrap; }
.d-item label { display:block; font-size:0.5rem; color:#2a4a5a; letter-spacing:2px; margin-bottom:2px; }
.d-val { font-size:0.82rem; color:#8ab4c8; }
.d-val.green { color:#00ff88; } .d-val.red { color:#ff3366; } .d-val.gold { color:#ffd700; }
.empty-card { background:#0a1018; border:1px solid #0f2a3a; border-left:3px solid #0f2a3a; padding:16px 18px; color:#2a4a5a; font-size:0.72rem; letter-spacing:2px; }
.closed-box { background:#0a1018; border:1px solid #0f2a3a; border-top:2px solid #ffd700; padding:18px 22px; margin-top:18px; }
.grand-bar {
    background:#0a1018; border:1px solid #00c8ff44; border-top:2px solid #00c8ff;
    padding:16px 22px; margin-top:12px;
    display:flex; gap:40px; flex-wrap:wrap; align-items:center;
}
.gb-label { font-size:0.54rem; color:#2a4a5a; letter-spacing:3px; margin-bottom:4px; }
.gb-val-pos { font-size:1.5rem; font-weight:700; color:#00ff88; }
.gb-val-neg { font-size:1.5rem; font-weight:700; color:#ff3366; }
.gb-val-neu { font-size:1.5rem; font-weight:700; color:#00c8ff; }
.gb-val-mut { font-size:1.1rem; color:#8ab4c8; }
.section-line { font-size:0.54rem; color:#2a4a5a; letter-spacing:4px; border-bottom:1px solid #0f2a3a; padding-bottom:6px; margin:16px 0 12px; }
.status-ok  { color:#00ff88; font-size:0.62rem; letter-spacing:2px; }
.status-err { color:#ff3366; font-size:0.62rem; letter-spacing:2px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# CoinGecko IDs for each symbol
PAIRS = ["BTCUSDT","ETHUSDT","ADAUSDT","SOLUSDT","BNBUSDT","XRPUSDT","DOGEUSDT","PAXGUSDT","AVAXUSDT","DOTUSDT","LINKUSDT"]
LEVERAGES = [1, 2, 3, 5, 10, 20, 25, 50, 75, 100, 125]

COINGECKO_IDS = {
    "BTCUSDT":  "bitcoin",
    "ETHUSDT":  "ethereum",
    "ADAUSDT":  "cardano",
    "SOLUSDT":  "solana",
    "BNBUSDT":  "binancecoin",
    "XRPUSDT":  "ripple",
    "DOGEUSDT": "dogecoin",
    "PAXGUSDT": "pax-gold",
    "AVAXUSDT": "avalanche-2",
    "DOTUSDT":  "polkadot",
    "LINKUSDT": "chainlink",
}

def fmt_price(n):
    try:
        v = float(n)
        if v >= 10000: return f"{v:,.1f}"
        if v >= 100:   return f"{v:,.2f}"
        if v >= 1:     return f"{v:,.4f}"
        return f"{v:.6f}"
    except Exception: return "-"

def fetch_prices(symbols):
    ids = [COINGECKO_IDS[s] for s in symbols if s in COINGECKO_IDS]
    if not ids:
        return {}
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": ",".join(ids), "vs_currencies": "usd"}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        result = {}
        for sym in symbols:
            cg_id = COINGECKO_IDS.get(sym)
            if cg_id and cg_id in data:
                result[sym] = float(data[cg_id]["usd"])
        return result
    except Exception:
        return {}

# --- Session state ---
if "positions" not in st.session_state:
    st.session_state.positions = [
        {"pair":"ETHUSDT",  "side":"Long","entry":0.0,"qty":0.0,"lev":10},
        {"pair":"ADAUSDT",  "side":"Long","entry":0.0,"qty":0.0,"lev":10},
        {"pair":"PAXGUSDT", "side":"Long","entry":0.0,"qty":0.0,"lev":10},
        {"pair":"BTCUSDT",  "side":"Long","entry":0.0,"qty":0.0,"lev":10},
    ]
if "live"          not in st.session_state: st.session_state.live          = {}
if "last_update"   not in st.session_state: st.session_state.last_update   = ""
if "closed_trades" not in st.session_state: st.session_state.closed_trades = []
if "fetch_error"   not in st.session_state: st.session_state.fetch_error   = False

# --- Fetch all prices in ONE request ---
tracked = list({p["pair"] for p in st.session_state.positions})
prices  = fetch_prices(tracked)

if prices:
    st.session_state.live.update(prices)
    st.session_state.fetch_error = False
else:
    st.session_state.fetch_error = True

st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# --- Compute open P&L ---
total_open_pnl    = 0.0
total_open_margin = 0.0
any_active        = False
pos_data          = []

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
        pos_data.append({**pos, "current":current, "notional":notional,
                         "margin":margin, "pnl_usd":pnl_usd,
                         "pnl_pct_m":pnl_pct_m, "pnl_pct_n":pnl_pct_n, "active":True})
    else:
        pos_data.append({**pos, "current":current, "active":False})

closed_total = sum(t["pnl"] for t in st.session_state.closed_trades)
grand_total  = total_open_pnl + closed_total

# ========== TOP SUMMARY BAR ==========
if any_active:
    sign_o  = "+" if total_open_pnl >= 0 else ""
    sign_g  = "+" if grand_total    >= 0 else ""
    sign_c  = "+" if closed_total   >= 0 else ""
    o_cls   = "top-total-pos" if total_open_pnl > 0 else ("top-total-neg" if total_open_pnl < 0 else "top-total-neu")
    g_cls   = "top-stat-val-pos" if grand_total > 0 else ("top-stat-val-neg" if grand_total < 0 else "top-stat-val-neu")
    c_cls   = "top-stat-val-pos" if closed_total > 0 else ("top-stat-val-neg" if closed_total < 0 else "top-stat-val-mut")
    open_pct= (total_open_pnl / total_open_margin * 100) if total_open_margin > 0 else 0
    pct_cls = "top-stat-val-pos" if open_pct > 0 else ("top-stat-val-neg" if open_pct < 0 else "top-stat-val-neu")
    st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="top-title">P&amp;L POSICIONES ABIERTAS</div>
    <div class="{o_cls}">{sign_o}${total_open_pnl:,.2f} <span style="font-size:1rem">USDT</span></div>
  </div>
  <div class="top-divider"></div>
  <div>
    <div class="top-title">RETORNO SOBRE MARGEN</div>
    <div class="{pct_cls}">{sign_o}{open_pct:.2f}%</div>
  </div>
  <div class="top-divider"></div>
  <div>
    <div class="top-title">MARGEN TOTAL USADO</div>
    <div class="top-stat-val-mut">${total_open_margin:,.2f}</div>
  </div>
  <div class="top-divider"></div>
  <div>
    <div class="top-title">CERRADOS ACUMULADO</div>
    <div class="{c_cls}">{sign_c}${closed_total:,.2f}</div>
  </div>
  <div class="top-divider"></div>
  <div>
    <div class="top-title">GANANCIA TOTAL</div>
    <div class="{g_cls}">{sign_g}${grand_total:,.2f}</div>
  </div>
</div>""", unsafe_allow_html=True)
else:
    st.markdown(
        "<h2 style='color:#00c8ff;letter-spacing:6px;font-family:monospace;margin-bottom:18px'>"
        "POSITION <span style='color:#00ff88'>TRACKER</span></h2>",
        unsafe_allow_html=True)

# ========== POSITIONS 2x2 GRID ==========
st.markdown("<div class='section-line'>POSICIONES ABIERTAS</div>", unsafe_allow_html=True)

if st.button("+ NUEVA POSICION"):
    st.session_state.positions.append({"pair":"BTCUSDT","side":"Long","entry":0.0,"qty":0.0,"lev":10})
    st.rerun()

n = len(st.session_state.positions)
for row in range(0, n, 2):
    col_left, col_right = st.columns(2, gap="medium")
    for col_idx, col in enumerate([col_left, col_right]):
        i = row + col_idx
        if i >= n:
            break
        pos = st.session_state.positions[i]
        pd  = pos_data[i]
        with col:
            ci1, ci2, ci3 = st.columns([2, 1.2, 1.2])
            with ci1:
                pair = st.selectbox("PAR", PAIRS,
                    index=PAIRS.index(pos["pair"]) if pos["pair"] in PAIRS else 0, key=f"pair_{i}")
            with ci2:
                side = st.selectbox("LADO", ["Long","Short"],
                    index=0 if pos["side"]=="Long" else 1, key=f"side_{i}")
            with ci3:
                lev_opts = [f"{x}x" for x in LEVERAGES]
                cur_str  = f"{pos['lev']}x"
                lev_idx  = lev_opts.index(cur_str) if cur_str in lev_opts else 4
                lev_str  = st.selectbox("APALANCAMIENTO", lev_opts, index=lev_idx, key=f"lev_{i}")
                lev      = int(lev_str.replace("x",""))
            ci4, ci5, ci6 = st.columns([2, 2, 0.6])
            with ci4:
                entry = st.number_input("PRECIO ENTRADA", min_value=0.0,
                    value=float(pos["entry"]), format="%.4f", step=0.0001, key=f"entry_{i}")
            with ci5:
                qty = st.number_input("CANTIDAD MONEDAS", min_value=0.0,
                    value=float(pos["qty"]), format="%.6f", step=0.001, key=f"qty_{i}")
            with ci6:
                st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
                if st.button("X", key=f"del_{i}", use_container_width=True):
                    st.session_state.positions.pop(i)
                    st.rerun()

            st.session_state.positions[i] = {"pair":pair,"side":side,"entry":entry,"qty":qty,"lev":lev}

            if pd["active"]:
                pnl_usd  = pd["pnl_usd"]
                pnl_pct_m= pd["pnl_pct_m"]
                pnl_pct_n= pd["pnl_pct_n"]
                current  = pd["current"]
                margin   = pd["margin"]
                notional = pd["notional"]
                sign   = "+" if pnl_usd >= 0 else ""
                status = "win" if pnl_usd > 0 else ("los" if pnl_usd < 0 else "")
                u_cls  = "pnl-main-pos" if pnl_usd > 0 else ("pnl-main-neg" if pnl_usd < 0 else "pnl-main-neu")
                p_cls  = "pnl-pct-pos"  if pnl_usd > 0 else ("pnl-pct-neg"  if pnl_usd < 0 else "pnl-pct-neu")
                pr_cls = "green" if current > entry else ("red" if current < entry else "")
                s_cls  = "b-long" if side=="Long" else "b-short"
                st.markdown(f"""
<div class="pos-card {status}">
  <div class="pos-header">
    <span class="pos-name">{pair.replace("USDT","/USDT")}</span>
    <div class="badges"><span class="{s_cls}">{side.upper()}</span><span class="b-lev">{lev}x</span></div>
  </div>
  <div><span class="{u_cls}">{sign}${pnl_usd:,.2f}</span>&nbsp;<span class="{p_cls}">{sign}{pnl_pct_m:.2f}%</span></div>
  <div class="pnl-sub">P&amp;L SOBRE MARGEN &nbsp;|&nbsp; PRECIO: {sign}{pnl_pct_n:.2f}%</div>
  <div class="detail-row">
    <div class="d-item"><label>ENTRADA</label><div class="d-val">{fmt_price(entry)}</div></div>
    <div class="d-item"><label>ACTUAL</label><div class="d-val {pr_cls}">{fmt_price(current)}</div></div>
    <div class="d-item"><label>MARGEN</label><div class="d-val gold">${margin:,.2f}</div></div>
    <div class="d-item"><label>NOCIONAL</label><div class="d-val">${notional:,.2f}</div></div>
  </div>
</div>""", unsafe_allow_html=True)
            else:
                s_cls = "b-long" if side=="Long" else "b-short"
                warn  = " - sin precio" if pd.get("current") is None else ""
                st.markdown(f"""
<div class="empty-card">
  <div style="display:flex;justify-content:space-between;margin-bottom:8px">
    <span style="color:#8ab4c8;letter-spacing:3px">{pair.replace("USDT","/USDT")}</span>
    <div class="badges"><span class="{s_cls}">{side.upper()}</span><span class="b-lev">{lev}x</span></div>
  </div>
  Ingresa precio de entrada y cantidad{warn}
</div>""", unsafe_allow_html=True)

# ========== CLOSED TRADES ==========
st.markdown("<div class='section-line'>TRADES CERRADOS</div>", unsafe_allow_html=True)

with st.expander("+ AGREGAR TRADE CERRADO", expanded=len(st.session_state.closed_trades) == 0):
    cc1, cc2, cc3, cc4 = st.columns([2, 2, 2, 1])
    with cc1:
        c_label = st.text_input("DESCRIPCION", placeholder="ej: BTC Long 10x", key="c_label")
    with cc2:
        c_pnl   = st.number_input("P&L REALIZADO (USDT)", value=0.0, format="%.2f", step=0.01, key="c_pnl")
    with cc3:
        c_date  = st.text_input("FECHA", placeholder="ej: 15/03/2026", key="c_date")
    with cc4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("AGREGAR", use_container_width=True, key="add_closed"):
            if c_pnl != 0.0:
                st.session_state.closed_trades.append({
                    "label": c_label if c_label else f"Trade {len(st.session_state.closed_trades)+1}",
                    "pnl":   c_pnl,
                    "date":  c_date if c_date else datetime.now().strftime("%d/%m/%Y")
                })
                st.rerun()

if st.session_state.closed_trades:
    for j, t in enumerate(st.session_state.closed_trades):
        sign  = "+" if t["pnl"] >= 0 else ""
        color = "#00ff88" if t["pnl"] >= 0 else "#ff3366"
        tc1, tc2, tc3, tc4 = st.columns([3, 2, 1.5, 0.5])
        with tc1: st.markdown(f"<span style='color:#8ab4c8;letter-spacing:2px;font-size:0.85rem'>{t['label']}</span>", unsafe_allow_html=True)
        with tc2: st.markdown(f"<span style='color:{color};font-size:1rem;font-weight:700'>{sign}${t['pnl']:,.2f}</span>", unsafe_allow_html=True)
        with tc3: st.markdown(f"<span style='color:#2a4a5a;font-size:0.75rem'>{t['date']}</span>", unsafe_allow_html=True)
        with tc4:
            if st.button("X", key=f"dc_{j}", use_container_width=True):
                st.session_state.closed_trades.pop(j)
                st.rerun()

    sign_c = "+" if closed_total >= 0 else ""
    sign_g = "+" if grand_total  >= 0 else ""
    c_cls  = "gb-val-pos" if closed_total > 0 else ("gb-val-neg" if closed_total < 0 else "gb-val-neu")
    g_cls  = "gb-val-pos" if grand_total  > 0 else ("gb-val-neg" if grand_total  < 0 else "gb-val-neu")
    st.markdown(f"""
<div class="grand-bar">
  <div><div class="gb-label">CERRADOS ACUMULADO</div><div class="{c_cls}">{sign_c}${closed_total:,.2f}</div></div>
  <div><div class="gb-label">ABIERTOS AHORA</div><div class="{'gb-val-pos' if total_open_pnl>=0 else 'gb-val-neg'}">{'+'if total_open_pnl>=0 else ''}${total_open_pnl:,.2f}</div></div>
  <div><div class="gb-label">GANANCIA TOTAL HISTORICA</div><div class="{g_cls}">{sign_g}${grand_total:,.2f}</div></div>
</div>""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
cs, cr = st.columns([3,1])
with cs:
    if st.session_state.fetch_error:
        st.markdown("<span class='status-err'>ERROR obteniendo precios - reintentando...</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='status-ok'>LIVE - {st.session_state.last_update} - CoinGecko</span>", unsafe_allow_html=True)
with cr:
    ref = st.selectbox("Refresh", ["30s","60s","2m"], label_visibility="collapsed")

secs = {"30s":30,"60s":60,"2m":120}[ref]
time.sleep(secs)
st.rerun()

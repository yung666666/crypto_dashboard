import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- API SETUP ---
API_KEY = 'YOUR API KEY HERE' # Get your API key from CoinMarketCap
HEADERS = {'X-CMC_PRO_API_KEY': API_KEY, 'Accepts': 'application/json'}

st.set_page_config(page_title="HODL Intelligence", layout="wide")

def get_cmc(endpoint, params=None):
    url = f"https://pro-api.coinmarketcap.com{endpoint}"
    return requests.get(url, headers=HEADERS, params=params).json()

# --- 1. GLOBAL & DOMINANCE DATA ---
# Fetching the exact fields you requested
g_resp = get_cmc('/v1/global-metrics/quotes/latest')
g = g_resp['data']
q = g['quote']['USD']

# --- 2. FEAR & GREED ---
fg = get_cmc('/v3/fear-and-greed/latest')['data']

# --- 3. ASSET PRICES ---
symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'LINK', 'SNEK', 'NIGHT', 'WLD']
p_data = get_cmc('/v1/cryptocurrency/quotes/latest', params={'symbol': ','.join(symbols)})['data']

# --- UI DISPLAY ---
st.title("🛡️ Institutional Holder Dashboard")

# Metric Section 1: Sentiment & Caps
c1, c2, c3, c4 = st.columns(4)
c1.metric("Fear & Greed", f"{fg['value']}/100", fg['value_classification'])
c2.metric("Total M-Cap", f"${q['total_market_cap']/1e12:.2f}T", f"{q['total_market_cap_yesterday_percentage_change']:.2f}%")
c3.metric("DeFi Cap", f"${q['defi_market_cap']/1e9:.1f}B")
c4.metric("Stablecoin Cap", f"${q['stablecoin_market_cap']/1e9:.1f}B")

# Metric Section 2: Dominance Tracking
st.subheader("📊 Dominance Tracking")
d1, d2, d3, d4 = st.columns(4)
d1.metric("BTC Dominance", f"{g['btc_dominance']:.2f}%", f"{g['btc_dominance_24h_percentage_change']:.2f}%")
d2.metric("ETH Dominance", f"{g['eth_dominance']:.2f}%", f"{g['eth_dominance_24h_percentage_change']:.2f}%")
# Manually showing yesterday's dominance as requested
d3.write(f"**BTC Yesterday:** {g['btc_dominance_yesterday']:.2f}%")
d4.write(f"**ETH Yesterday:** {g['eth_dominance_yesterday']:.2f}%")

st.divider()

# --- Technical Deep Dive & Heatmaps---
st.subheader("🔍 Technical Deep Dive & Heatmaps")
t1, t2, t3, t4 = st.columns(4)

with t1:
    st.info("**Momentum & Volatility**")
    st.write("""
    - **RSI:** Above 70 is 'Overbought' (Sell); Below 30 is 'Oversold' (Buy).
    - **Bollinger Bands:** Price 'hugging' the top band shows strength; a 'squeeze' predicts a big move.
    - **Accelerator (AC):** Measures speed of price changes; green bars show growing momentum.
    """)
    st.link_button("📈 Open RSI & Technicals", "https://coinmarketcap.com/charts/rsi/")

with t2:
    st.info("**Market Pain Points**")
    st.write("""
    - **Liquidation Map:** Shows where traders will be forced to sell. 
    - **Strategy:** Big liquidation clusters often act as 'magnets' for price before a reversal.
    """)
    st.link_button("🔥 Open Liquidation Map", "https://coinmarketcap.com/charts/liquidations/")

with t3:
    st.info("**Cycle Health (NUPL)**")
    st.write("""
    - **The Paper Profit Meter:** Measures if the market is in profit or loss.
    - **Zones:** Red (<0) is Capitulation; Blue (>0.75) is Euphoria.
    """)
    st.link_button("💎 Open NUPL Chart", "https://www.lookintobitcoin.com/charts/relative-unrealized-profit--loss/")

with t4:
    st.info("**The Macro Lines (MAs)**")
    st.write("""
    - **200-Week SMA:** The 'Ultimate Floor' and best long-term entry.
    - **200-Day SMA:** Above = Bull Market; Below = Bear Market.
    - **Pi Cycle Top:** Uses the 111-Day SMA to predict the absolute market peak.
    """)
    st.link_button("📈 Open BTC MAs", "https://studio.glassnode.com/charts/7a2a274d-62ad-4efe-45f9-0bebe4da6a27?a=BTC")

st.divider()

# --- ASSET PERFORMANCE TABLE ---
st.subheader("💎 Portfolio Asset Tracking")
rows = []
for s in symbols:
    coin = p_data[s]['quote']['USD']
    rows.append({
        "Asset": s,
        "Price": f"${coin['price']:.7f}",
        "1h %": f"{coin['percent_change_1h']:.3f}%",
        "24h %": f"{coin['percent_change_24h']:.3f}%",
        "7d %": f"{coin['percent_change_7d']:.3f}%"
    })
st.table(pd.DataFrame(rows, index=np.arange(1, len(rows)+1)))
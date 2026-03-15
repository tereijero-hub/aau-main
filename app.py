import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json

# ページ設定：ワイドモード（全画面）
st.set_page_config(page_title="AAU EMPIRE COCKPIT", layout="wide")

st.title("🏛️ AAU EMPIRE: 帝国司令部リアルタイム・ダッシュボード")

# データの読み込み（GitHub上の最新結果を取得）
try:
    with open("internal_dashboard_data.json", "r") as f:
        state = json.load(f)
except:
    # データがない場合のダミー
    state = {"equity": 1000000, "regime": "STORM", "infrastructure": {"delays": [0.15, 0.06, 0.17]}}

# --- [LAYER 1: モンテカルロ・シミュレーション（全画面・動的）] ---
st.header("📊 LIVE: Equity Path (Monte Carlo)")
fig_mc = go.Figure()
rets = np.random.normal(0.002, 0.02, 100)
for i in range(50):
    y = np.cumsum(np.random.choice(rets, size=100)) + state["equity"]
    fig_mc.add_trace(go.Scatter(y=y, mode='lines', line=dict(width=1), opacity=0.3, name=f"Path {i}"))
fig_mc.update_layout(height=600, template="plotly_dark", showlegend=False)
st.plotly_chart(fig_mc, use_container_width=True) # これで枠いっぱいに広がる

# --- [LAYER 2: MAE/MFE & インフラ遅延（横並び）] ---
col1, col2 = st.columns(2)

with col1:
    st.header("🎯 Trade Quality (MAE/MFE)")
    df = pd.DataFrame({
        'MAE': np.random.uniform(-0.03, 0, 50),
        'MFE': np.random.uniform(0, 0.04, 50)
    })
    fig_trade = go.Figure(data=[go.Scatter(x=df['MAE'], y=df['MFE'], mode='markers', marker=dict(color='#bc8cff', size=10))])
    fig_trade.add_vline(x=-0.015, line_dash="dash", line_color="red")
    fig_trade.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_trade, use_container_width=True)

with col2:
    st.header("🛰️ Infrastructure Latency")
    fig_lat = go.Figure(data=[go.Bar(
        x=["Ishikari", "Matsumoto", "Okayama"],
        y=state["infrastructure"]["delays"],
        marker_color=['red', 'green', 'red']
    )])
    fig_lat.add_hline(y=0.1, line_dash="dash", line_color="orange")
    fig_lat.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_lat, use_container_width=True)

import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
from datetime import datetime

# --- [LAYER 1: プロ仕様・全画面設定] ---
st.set_page_config(
    page_title="AAU EMPIRE COCKPIT v23.5",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 漆黒のカスタムCSS
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    div[data-testid="column"] { padding: 10px; }
    h1, h2, h3 { color: #58a6ff; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- [LAYER 2: データロード] ---
def load_data():
    try:
        with open("internal_core_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()

if not data:
    st.error("🛰️ 脳（Private）からの信号が途絶えています。internal_core_data.json を確認してください。")
    st.stop()

meta = data["metadata"]
agents = data["agent_intelligence"]
visuals = data["visuals"]

# --- [HEADER: 帝国ステータスバー] ---
st.title("🏛️ AAU EMPIRE | MISSION CONTROL")
c1, c2, c3, c4 = st.columns(4)
c1.metric("JUDGMENT", meta["judgment"], delta=None)
c2.metric("SYSTEM STATUS", meta["system_status"])
c3.metric("ACTIVE AGENTS", f"{meta['active_agents']} / 10")
c4.metric("LAST UPDATE", meta["timestamp"].split(" ")[1])

st.divider()

# --- [BODY: 十人委員会・武装ステータスパネル] ---
st.subheader("🛡️ THE COMMITTEE OF TEN: AGENT STATUS")
# 10体のエージェントを5列2段で配置
cols = st.columns(5)
agent_keys = list(agents.keys())

for i, key in enumerate(agent_keys):
    with cols[i % 5]:
        status_color = "🟢" if agents[key].get("ok", True) else "🔴"
        val = agents[key].get("val", agents[key].get("status", "N/A"))
        st.markdown(f"""
        <div style="background-color:#161b22; border:1px solid #30363d; padding:10px; border-radius:5px; text-align:center;">
            <p style="font-size:0.8rem; color:#8b949e; margin-bottom:5px;">{key}</p>
            <p style="font-size:1.2rem; font-weight:bold; margin-bottom:5px;">{val}</p>
            <p style="font-size:1.5rem;">{status_color}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --- [LAYER 3: 巨大グラフィックパネル] ---
st.subheader("📊 STRATEGIC ANALYTICS")

tab1, tab2, tab3 = st.tabs(["📈 MONTE CARLO", "🎯 TRADE QUALITY", "🛰️ INFRA LATENCY"])

with tab1:
    # 全画面で巨大に見るためのモンテカルロ・パス
    fig_mc = go.Figure()
    paths = np.array(visuals["monte_carlo_paths"])
    for i in range(len(paths)):
        fig_mc.add_trace(go.Scatter(y=paths[i], mode='lines', line=dict(width=1), opacity=0.3, name=f"P{i}"))
    fig_mc.update_layout(
        height=700, template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_mc, use_container_width=True)

with tab2:
    # MAE/MFE 散布図
    fig_trade = go.Figure()
    fig_trade.add_trace(go.Scatter(
        x=visuals["mae_dist"], y=visuals["mfe_dist"], 
        mode='markers', marker=dict(color='#bc8cff', size=12, symbol='diamond')
    ))
    fig_trade.add_vline(x=-0.015, line_dash="dash", line_color="#f85149", annotation_text="RISK LIMIT")
    fig_trade.update_layout(height=700, template="plotly_dark", xaxis_title="MAE", yaxis_title="MFE")
    st.plotly_chart(fig_trade, use_container_width=True)

with tab3:
    # 拠点遅延 3D的棒グラフ
    fig_lat = go.Figure(data=[go.Bar(
        x=["Ishikari", "Matsumoto", "Okayama"],
        y=visuals["latency"],
        marker_color=['#58a6ff', '#3fb950', '#58a6ff'],
        text=visuals["latency"], textposition='auto'
    )])
    fig_lat.update_layout(height=700, template="plotly_dark", yaxis_title="Latency (sec)")
    st.plotly_chart(fig_lat, use_container_width=True)

st.caption("AAU EMPIRE INTEGRATED INTELLIGENCE SYSTEM | PROTOCOL v23.5")

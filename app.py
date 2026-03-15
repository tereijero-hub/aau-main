import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
from datetime import datetime

# --- [LAYER 1: 設定] ---
st.set_page_config(
    page_title="AAU EMPIRE v24.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 堅牢なCSS（エラーの原因になりやすい複雑な外部フォントを排除し、標準の等幅フォントを使用）
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 5px; }
    .agent-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }
    .status-ok { color: #3fb950; font-weight: bold; }
    .status-ng { color: #f85149; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [LAYER 2: データロード] ---
@st.cache_data(ttl=60) # 1分間キャッシュして動作を安定させる
def load_data():
    try:
        with open("internal_core_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return None

data = load_data()

if not data:
    st.error("🛰️ DATA ERROR: internal_core_data.json が見つからないか、形式が正しくありません。")
    st.stop()

# データの抽出（KeyError対策：dict.getを使用）
meta = data.get("metadata", {})
agents = data.get("agent_intelligence", {})
visuals = data.get("visuals", {})

# --- [HEADER] ---
st.title("🏛️ AAU EMPIRE | MISSION CONTROL")
c1, c2, c3, c4 = st.columns(4)
c1.metric("JUDGMENT", meta.get("judgment", "N/A"))
c2.metric("STATUS", meta.get("system_status", "N/A"))
c3.metric("AGENTS", f"{meta.get('active_agents', 0)}/10")
c4.metric("TIME", meta.get("timestamp", "00:00:00").split(" ")[-1])

st.markdown("---")

# --- [BODY: AGENTS] ---
st.subheader("🛡️ AGENT STATUS")
agent_cols = st.columns(5)
agent_items = list(agents.items())

for i in range(10):
    with agent_cols[i % 5]:
        if i < len(agent_items):
            name, info = agent_items[i]
            is_ok = info.get("ok", True)
            color = "status-ok" if is_ok else "status-ng"
            status_symbol = "●" if is_ok else "▲"
            
            st.markdown(f"""
            <div class="agent-card">
                <div style="font-size: 0.7rem; color: #8b949e;">{name}</div>
                <div style="font-size: 1.1rem; font-weight: bold;">{info.get('val', 'N/A')}</div>
                <div class="{color}">{status_symbol}</div>
            </div>
            """, unsafe_allow_html=True)

# --- [VISUALS] ---
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📈 FORECAST", "🎯 TRADE", "🛰️ INFRA"])

with tab1:
    fig = go.Figure()
    paths = np.array(visuals.get("monte_carlo_paths", [[0]]))
    for p in paths:
        fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.5, color='#58a6ff'), opacity=0.2, showlegend=False))
    # 平均線
    if len(paths) > 0:
        fig.add_trace(go.Scatter(y=np.mean(paths, axis=0), line=dict(width=3, color='white'), name="MEAN"))
    fig.update_layout(height=500, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig_tr = go.Figure(go.Scatter(x=visuals.get("mae_dist", []), y=visuals.get("mfe_dist", []), mode='markers', marker=dict(color='#bc8cff')))
    fig_tr.update_layout(height=500, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tr, use_container_width=True)

with tab3:
    fig_la = go.Figure(go.Bar(x=["Ishikari", "Matsumoto", "Okayama"], y=visuals.get("latency", []), marker_color='#58a6ff'))
    fig_la.update_layout(height=500, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_la, use_container_width=True)

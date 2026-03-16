import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np

st.set_page_config(page_title="TEN AGENTS IMPERIAL CENTER", layout="wide")

# カスタムCSS
st.markdown("""
    <style>
    .main { background-color: #030303; color: #00FF00; font-family: 'Courier New', monospace; }
    .stMetric { border: 1px solid #00FF00; padding: 15px; border-radius: 10px; background-color: #0a0a0a; }
    .agent-box { border: 1px solid #222; padding: 10px; border-radius: 5px; background-color: #050505; height: 110px; }
    .status-ok { color: #00FF00; font-weight: bold; }
    .status-warn { color: #FF0000; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("internal_core_data.json", "r") as f:
        data = json.load(f)
except:
    st.error("🚨 コア・オフライン。aau_main.py を実行してください。")
    st.stop()

# --- HEADER ---
meta = data.get('metadata', {})
st.title("🏛️ EMPIRE STRATEGIC CENTER : INTEGRATED")
st.markdown(f"**PROTOCOL STATUS**: `{meta.get('status')}` | **TIMESTAMP**: `{meta.get('timestamp')}`")

# --- METRICS ---
m = data.get('metrics', {})
c1, c2, c3, c4 = st.columns(4)
c1.metric("EXPECTED VALUE (EV)", f"{m.get('ev', 0)*100:.2f}%")
c2.metric("PROFIT FACTOR", f"{m.get('pf', 0):.2f}")
c3.metric("WIN RATE", f"{m.get('win_rate', 0)*100:.1f}%")
c4.metric("MAX DRAWDOWN", f"{m.get('max_dd', 0)*100:.2f}%")

# --- VISUALS ---
st.subheader("📊 PROBABILITY FIELD (100-Path Ensemble)")
v = data.get('visuals', {})
paths = v.get('paths', [])
if paths:
    fig = go.Figure()
    for p in paths[:60]: # 視認性のための間引き
        fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.6, color='rgba(0, 255, 0, 0.1)'), showlegend=False))
    fig.add_trace(go.Scatter(y=v.get('median'), mode='lines', line=dict(width=3, color='#00FF00'), name="CONSENSUS"))
    fig.update_layout(template="plotly_dark", plot_bgcolor='#030303', paper_bgcolor='#030303', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- THE TEN AGENTS COUNCIL ---
st.subheader("👁️ TEN AGENTS COUNCIL AUDIT")
agents = data.get('agents', {})
rows = [st.columns(5), st.columns(5)] # 2段
for i, (name, info) in enumerate(agents.items()):
    col = rows[i // 5][i % 5]
    with col:
        status_cls = "status-ok" if info['status'] == "OK" else "status-warn"
        st.markdown(f"""
        <div class="agent-box">
            <small style="color:#666;">{info['role']}</small><br>
            <strong>{name}</strong><br>
            <span class="{status_cls}">{info['status']}</span><br>
            <span style="font-size:0.75em;">{info['detail']}</span>
        </div>
        """, unsafe_allow_html=True)

st.caption("規律：先読みバイアス排除, 伊藤補正, ボラティリティ・スケーリング, 合議制執行。")

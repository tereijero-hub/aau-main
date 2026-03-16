import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np

# 強制ダークモード & ページ設定
st.set_page_config(page_title="帝国演算司令部", layout="wide", initial_sidebar_state="collapsed")

# 漆黒のUIをCSSで強制注入
st.markdown("""
    <style>
    /* 全体を黒に、文字を緑に */
    .stApp { background-color: #000000; color: #00FF00; }
    header, [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    .stMetric { border: 1px solid #00FF00 !important; background-color: #050505 !important; color: #00FF00 !important; }
    [data-testid="stMetricValue"] { color: #00FF00 !important; }
    .agent-card { border: 1px solid #333; padding: 10px; background-color: #050505; border-radius: 5px; }
    h1, h2, h3, p { color: #00FF00 !important; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("internal_core_data.json", "r") as f:
        data = json.load(f)
except:
    st.error("🚨 演算コアが沈黙しています。aau_main.py を実行してください。")
    st.stop()

# --- HEADER (JST) ---
meta = data.get('metadata', {})
st.title("🏛️ EMPIRE STRATEGIC CENTER (JST-SYNC)")
st.markdown(f"**STATUS**: `{meta.get('status')}` | **TIMESTAMP (JST)**: `{meta.get('timestamp')}`")

# --- METRICS ---
m = data.get('metrics', {})
c1, c2, c3, c4 = st.columns(4)
c1.metric("EXPECTED VALUE", f"{m.get('ev', 0)*100:.2f}%")
c2.metric("PROFIT FACTOR", f"{m.get('pf', 0):.2f}")
c3.metric("WIN RATE", f"{m.get('win_rate', 0)*100:.1f}%")
c4.metric("MAX DRAWDOWN", f"{m.get('max_dd', 0)*100:.2f}%")

# --- 100 PATHS ---
st.subheader("📊 PROBABILITY FIELD")
v = data.get('visuals', {})
paths = v.get('paths', [])
if paths:
    fig = go.Figure()
    for p in paths:
        fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.5, color='rgba(0, 255, 0, 0.15)'), showlegend=False))
    fig.add_trace(go.Scatter(y=v.get('median'), mode='lines', line=dict(width=3, color='#00FF00'), name="MEDIAN"))
    fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- AGENT REPORT ---
st.subheader("👁️ COUNCIL AUDIT")
agents = data.get('agents', {})
cols = st.columns(len(agents) if agents else 1)
for i, (name, info) in enumerate(agents.items()):
    with cols[i]:
        st.markdown(f"""<div class="agent-card"><small>{info['role']}</small><br><strong>{name}</strong><br>{info['status']}</div>""", unsafe_allow_html=True)

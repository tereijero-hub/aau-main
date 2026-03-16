import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
import os

st.set_page_config(page_title="帝国演算司令部", layout="wide")

# UIデザイン（漆黒）
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00FF00; }
    .stMetric { border: 1px solid #00FF00; background-color: #050505; padding: 10px; }
    div[data-testid="stMetricValue"] > div { color: #00FF00 !important; }
    .agent-card { border: 1px solid #333; padding: 8px; background-color: #050505; }
    </style>
""", unsafe_allow_html=True)

if not os.path.exists("internal_core_data.json"):
    st.title("🏛️ EMPIRE DASHBOARD")
    st.warning("📡 演算コア(aau_main.py)の初回実行を待機中...")
    st.stop()

with open("internal_core_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("🏛️ EMPIRE STRATEGIC DASHBOARD")
st.write(f"**TIME (JST)**: {data['metadata']['timestamp']}")

# メトリクス
m = data['metrics']
c1, c2 = st.columns(2)
c1.metric("AGGREGATED EV", f"{m['total_ev']*100:.4f}%")
c2.metric("MAX DRAWDOWN", f"{m['total_mdd']*100:.2f}%")

# 4大市場グラフ
sims = data['simulations']
cols = st.columns(2)
for i, (name, sim) in enumerate(sims.items()):
    with cols[i % 2]:
        st.subheader(f"📊 {name} ({sim['mode']})")
        fig = go.Figure()
        paths = np.array(sim['paths'])
        for p in paths[:30]: # 30本表示
            fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.5, color='rgba(0, 255, 0, 0.1)'), showlegend=False))
        fig.add_trace(go.Scatter(y=sim['median'], mode='lines', line=dict(width=2, color='#00FF00'), name="MEDIAN"))
        fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# エージェント報告
st.subheader("👁️ AGENTS COUNCIL")
ag_cols = st.columns(5)
for i, (name, status) in enumerate(data['agents'].items()):
    with ag_cols[i % 5]:
        st.markdown(f"<div class='agent-card'><small>{name}</small><br><strong>{status}</strong></div>", unsafe_allow_html=True)

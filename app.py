import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np

st.set_page_config(page_title="帝国演算司令部", layout="wide")

# 漆黒UIの強制適用
st.markdown("""
    <style>
    .stApp { background-color: #000 !important; color: #00FF00 !important; }
    .stMetric { border: 1px solid #00FF00; background-color: #050505; }
    div[data-testid="stMetricValue"] > div { color: #00FF00 !important; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("internal_core_data.json", "r") as f:
        data = json.load(f)
except:
    st.error("📡 演算コアが未起動です。aau_main.py を実行してください。")
    st.stop()

# --- HEADER ---
meta = data.get('metadata', {})
st.title("🏛️ EMPIRE STRATEGIC DASHBOARD")
st.write(f"**TIME (JST)**: {meta.get('timestamp')} | **STATUS**: {meta.get('status')}")

# --- METRICS ---
m = data.get('metrics', {})
c1, c2 = st.columns(2)
c1.metric("TOTAL EXPECTED VALUE", f"{m.get('total_ev', 0)*100:.4f}%")
c2.metric("TOTAL MAX DRAWDOWN", f"{m.get('total_mdd', 0)*100:.2f}%")

# --- SIMULATION GRAPHS (日米株・FX・仮想通貨) ---
st.subheader("📊 100-PATH REAL-MARKET SIMULATIONS")
sims = data.get('simulations', {})
cols = st.columns(2)
for i, (name, sim) in enumerate(sims.items()):
    with cols[i % 2]:
        st.write(f"### {name}")
        fig = go.Figure()
        paths = np.array(sim.get('paths', []))
        for p in paths[:50]: # 50本表示
            fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.5, color='rgba(0, 255, 0, 0.1)'), showlegend=False))
        fig.add_trace(go.Scatter(y=sim.get('median'), mode='lines', line=dict(width=2, color='#00FF00'), name="MEDIAN"))
        fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

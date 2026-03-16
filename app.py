import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
import os

st.set_page_config(page_title="帝国演算司令部", layout="wide")

# 漆黒UIの強制適用
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #00FF00 !important; }
    .stMetric { border: 1px solid #00FF00; background-color: #050505; padding: 15px; border-radius: 10px; }
    div[data-testid="stMetricValue"] > div { color: #00FF00 !important; }
    .agent-card { border: 1px solid #333; padding: 10px; background-color: #050505; border-radius: 5px; margin-bottom: 5px; height: 80px; }
    h1, h2, h3, p, span { color: #00FF00 !important; }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "internal_core_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()

if not data:
    st.title("🏛️ EMPIRE STRATEGIC DASHBOARD")
    st.warning("📡 演算コア(aau_main.py)が起動していません。データ生成を待機中...")
    st.stop()

# --- HEADER ---
meta = data.get('metadata', {})
st.title(f"🏛️ EMPIRE STRATEGIC DASHBOARD")
st.markdown(f"**TIME (JST)**: `{meta.get('timestamp')}` | **JUDGMENT**: `{meta.get('judgment')}`")

# --- CORE METRICS ---
m = data.get('metrics', {})
c1, c2 = st.columns(2)
c1.metric("AGGREGATED EXPECTED VALUE", f"{m.get('total_ev', 0)*100:.4f}%")
c2.metric("MAX DRAWDOWN", f"{m.get('total_mdd', 0)*100:.2f}%")

# --- MARKET SIMULATIONS (統合表示) ---
sims = data.get('simulations', {})
if sims:
    cols = st.columns(2)
    for i, (name, sim) in enumerate(sims.items()):
        with cols[i % 2]:
            st.subheader(f"📊 {name} ({sim.get('mode')})")
            fig = go.Figure()
            paths = np.array(sim.get('paths', []))
            if paths.size > 0:
                for p in paths[:40]: 
                    fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.6, color='rgba(0, 255, 0, 0.15)'), showlegend=False))
                fig.add_trace(go.Scatter(y=sim.get('median'), mode='lines', line=dict(width=3, color='#00FF00'), name="MEDIAN"))
            
            fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

# --- 10 AGENTS COUNCIL ---
st.subheader("👁️ TEN AGENTS COUNCIL AUDIT")
agents = data.get('agents', {})
if agents:
    cols_a = st.columns(5)
    for i, (name, detail) in enumerate(agents.items()):
        with cols_a[i % 5]:
            st.markdown(f"""<div class="agent-card"><small>{name}</small><br><strong>{detail}</strong></div>""", unsafe_allow_html=True)

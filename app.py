import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np

# 帝国仕様：ダークテーマ強制 & ワイド画面
st.set_page_config(page_title="帝国演算司令部", layout="wide")

# 漆黒UIのCSS（司令官の要望：白い画面の根絶）
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #00FF00 !important; }
    .stMetric { border: 1px solid #00FF00; background-color: #050505; padding: 15px; border-radius: 10px; }
    div[data-testid="stMetricValue"] > div { color: #00FF00 !important; }
    .agent-card { border: 1px solid #333; padding: 10px; background-color: #050505; border-radius: 5px; margin-bottom: 5px; }
    h1, h2, h3, p, span { color: #00FF00 !important; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("internal_core_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"🚨 演算コアが未起動です。aau_main.py を実行してください。 Error: {e}")
    st.stop()

# --- HEADER ---
meta = data.get('metadata', {})
st.title(f"🏛️ EMPIRE STRATEGIC DASHBOARD")
st.markdown(f"**TIME (JST)**: `{meta.get('timestamp')}` | **STATUS**: `{meta.get('status')}`")

# --- CORE METRIC (0ではない数字) ---
m = data.get('metrics', {})
st.metric("AGGREGATED EXPECTED VALUE", f"{m.get('total_ev', 0)*100:.4f}%", delta="LIVE")

# --- 4-MARKET SIMULATION GRAPHS (日米株・FX・仮想通貨) ---
sims = data.get('simulations', {})
cols = st.columns(2)
for i, (name, sim) in enumerate(sims.items()):
    with cols[i % 2]:
        st.subheader(f"📊 {name} (100 Paths)")
        fig = go.Figure()
        paths = np.array(sim.get('paths', []))
        
        # 記憶：100回のシミュレーション線を反映
        for p in paths[:50]: # 視認性のため50本重畳
            fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.6, color='rgba(0, 255, 0, 0.12)'), showlegend=False))
        
        # 中央値（帝国の意志）
        fig.add_trace(go.Scatter(y=sim.get('median'), mode='lines', line=dict(width=3, color='#00FF00'), name="MEDIAN"))
        
        fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# --- 10 AGENTS COUNCIL REPORT ---
st.subheader("👁️ TEN AGENTS COUNCIL AUDIT")
agents = data.get('agents', {})
cols_a = st.columns(5)
for i, (name, detail) in enumerate(agents.items()):
    with cols_a[i % 5]:
        st.markdown(f"""
        <div class="agent-card">
            <small style="color:#666;">{name}</small><br>
            <strong>{detail}</strong>
        </div>
        """, unsafe_allow_html=True)

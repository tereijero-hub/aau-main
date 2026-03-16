import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np

st.set_page_config(page_title="IMPERIAL COUNCIL DASHBOARD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF00; font-family: 'Courier New', monospace; }
    .stMetric { border: 1px solid #00FF00; padding: 15px; border-radius: 10px; background-color: #111; }
    .agent-card { border: 1px solid #333; padding: 10px; border-radius: 5px; background-color: #0a0a0a; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("internal_core_data.json", "r") as f:
        data = json.load(f)
except Exception:
    st.error("🚨 演算コア・オフライン。aau_main.py を実行してください。")
    st.stop()

# --- HEADER ---
meta = data.get('metadata', {})
st.title("🏛️ EMPIRE STRATEGIC CENTER")
st.markdown(f"**STATUS**: `{meta.get('status', 'HOLD')}` | **PULSE**: `{meta.get('timestamp', 'N/A')}`")

# --- METRICS ---
m = data.get('metrics', {})
c1, c2, c3, c4 = st.columns(4)
c1.metric("EXPECTED VALUE", f"{m.get('ev', 0)*100:.2f}%")
c2.metric("PROFIT FACTOR", m.get('pf', 0))
c3.metric("WIN RATE", f"{m.get('win_rate', 0)*100:.0f}%")
c4.metric("MAX DRAWDOWN", f"{m.get('max_dd', 0)*100:.2f}%")

# --- 100 PATHS VISUALS (防衛コード適用) ---
st.subheader("📊 MULTI-PATH PROBABILITY FIELD")
visuals = data.get('visuals', {})
paths = visuals.get('paths', []) # .get() で安全に取得

if paths:
    fig = go.Figure()
    arr_paths = np.array(paths)
    for p in arr_paths[:50]:
        fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.7, color='rgba(0, 255, 0, 0.1)'), showlegend=False))
    
    median = visuals.get('median', [])
    if median:
        fig.add_trace(go.Scatter(y=median, mode='lines', line=dict(width=3, color='#00FF00'), name="CONSENSUS"))
    
    fig.update_layout(template="plotly_dark", plot_bgcolor='#050505', paper_bgcolor='#050505', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("データパスが見つかりません。演算コアを再確認してください。")

# --- AGENT REPORT ---
st.subheader("👁️ TEN AGENTS COUNCIL REPORT")
agents = data.get('agents_report', {})
cols = st.columns(5)
for i, (name, info) in enumerate(agents.items()):
    with cols[i % 5]:
        status_icon = "🟢" if info.get('status') == "OK" else "🔴"
        st.markdown(f"""
        <div class="agent-card">
            <small>{info.get('role')}</small><br>
            <strong>{name}</strong> {status_icon}<br>
            <span style="font-size:0.8em; color:#00FF00;">{info.get('detail')}</span>
        </div>
        """, unsafe_allow_html=True)

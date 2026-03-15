import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
from datetime import datetime

# --- [LAYER 1: 設定] ---
st.set_page_config(
    page_title="AAU EMPIRE | MISSION CONTROL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 漆黒CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    header[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
    .main { color: #ffffff !important; }
    
    div[data-testid="stMetric"] {
        background-color: #000000 !important;
        border: 1px solid #1f2328 !important;
        border-left: 5px solid #58a6ff !important;
        padding: 15px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 900 !important;
        font-size: 2.4rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #58a6ff !important;
        font-weight: bold !important;
    }

    .agent-card {
        background-color: #000000;
        border: 2px solid #1f2328;
        padding: 12px;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 10px;
    }
    .agent-name { color: #8b949e; font-size: 0.7rem; font-weight: bold; }
    .agent-value { color: #ffffff; font-size: 1.2rem; font-weight: 900; margin: 5px 0; }
    .status-ok { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-weight: 900; }
    .status-ng { color: #ff3131 !important; text-shadow: 0 0 10px #ff3131; font-weight: 900; }

    div[data-baseweb="tab-list"] { background-color: #000000 !important; border-bottom: 1px solid #30363d !important; }
    button[data-baseweb="tab"] { color: #8b949e !important; font-weight: bold !important; font-size: 1rem !important; }
    button[aria-selected="true"] { color: #ffffff !important; border-bottom-color: #58a6ff !important; }
    hr { border-color: #1f2328 !important; border-width: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [LAYER 2: データロード] ---
@st.cache_data(ttl=5)
def load_data():
    try:
        with open("internal_core_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()
if not data:
    st.error("DATABASE SIGNAL INTERRUPTED")
    st.stop()

meta = data.get("metadata", {})
agents = data.get("agent_intelligence", {})
visuals = data.get("visuals", {})

# --- [HEADER] ---
st.markdown("<h2 style='color: #ffffff; font-family: monospace; font-weight: 900;'>&gt; MISSION_CONTROL_SYS_v24.0</h2>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("JUDGMENT", meta.get("judgment", "N/A"))
c2.metric("CORE_SHIELD", meta.get("system_status", "N/A"))
c3.metric("AGENT_LOAD", f"{meta.get('active_agents', 0)} / 10")
c4.metric("LAST_PULSE", meta.get("timestamp", "0:0:0").split(" ")[-1])

st.markdown("<hr>", unsafe_allow_html=True)

# --- [BODY: AGENTS] ---
agent_cols = st.columns(5)
agent_items = list(agents.items())

for i in range(10):
    with agent_cols[i % 5]:
        if i < len(agent_items):
            name, info = agent_items[i]
            is_ok = info.get("ok", True)
            cls = "status-ok" if is_ok else "status-ng"
            sym = "▣ ACTIVE" if is_ok else "☒ ALERT"
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-name">{name}</div>
                <div class="agent-value">{info.get('val', 'N/A')}</div>
                <div class="{cls}">{sym}</div>
            </div>
            """, unsafe_allow_html=True)

# --- [LAYER 3: ANALYTICS] ---
st.write("")
t1, t2, t3 = st.tabs(["[ 01_FORECAST ]", "[ 02_DISTRIBUTION ]", "[ 03_LATENCY ]"])

with t1:
    fig_mc = go.Figure()
    paths = np.array(visuals.get("monte_carlo_paths", [[0,0]]))
    for p in paths:
        line_color = "#00ff41" if p[-1] > p[0] else "#ff3131"
        fig_mc.add_trace(go.Scatter(
            y=p, mode='lines', 
            line=dict(width=1.8, color=line_color), 
            opacity=0.45, showlegend=False
        ))
    if len(paths) > 0:
        avg_path = np.mean(paths, axis=0)
        fig_mc.add_trace(go.Scatter(
            y=avg_path, mode='lines', 
            line=dict(width=4.5, color='#ffffff'), 
            name="MEAN"
        ))
    fig_mc.update_layout(height=650, template="plotly_dark", paper_bgcolor='black', plot_bgcolor='black', margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig_mc, width='stretch')

with t2:
    fig

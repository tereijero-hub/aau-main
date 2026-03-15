import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
from datetime import datetime

# --- [LAYER 1: 究極の暗黒設定] ---
st.set_page_config(
    page_title="AAU EMPIRE | MISSION CONTROL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 完璧な黒と視認性を両立したCSS
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    header[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
    .main { color: #ffffff !important; }
    
    /* メトリック装飾 */
    div[data-testid="stMetric"] {
        background-color: #000000 !important;
        border: 1px solid #1f2328 !important;
        border-left: 4px solid #58a6ff !important;
        padding: 10px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: monospace !important;
        font-weight: 900 !important;
        font-size: 2.0rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #58a6ff !important;
        font-weight: bold !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
    }

    /* エージェントカード */
    .agent-card {
        background-color: #000000;
        border: 1px solid #1f2328;
        padding: 10px;
        border-radius: 2px;
        text-align: center;
        margin-bottom: 5px;
    }
    .agent-name { color: #8b949e; font-size: 0.6rem; font-weight: bold; }
    .agent-value { color: #ffffff; font-size: 1.0rem; font-weight: 800; margin: 3px 0; }
    .status-ok { color: #00ff41 !important; text-shadow: 0 0 5px #00ff41; font-weight: bold; font-size: 0.7rem; }
    .status-ng { color: #ff3131 !important; text-shadow: 0 0 5px #ff3131; font-weight: bold; font-size: 0.7rem; }

    /* タブの漆黒化 */
    div[data-baseweb="tab-list"] { background-color: #000000 !important; }
    button[data-baseweb="tab"] { color: #8b949e !important; font-weight: bold !important; background-color: transparent !important; }
    button[aria-selected="true"] { color: #ffffff !important; border-bottom-color: #58a6ff !important; }
    hr { border-color: #1f2328 !important; }
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
    st.error("DATABASE OFFLINE")
    st.stop()

meta = data.get("metadata", {})
agents = data.get("agent_intelligence", {})
visuals = data.get("visuals", {})

# --- [HEADER] ---
st.markdown("<h3 style='color: #ffffff; font-family: monospace;'>&gt; MISSION_CONTROL_SYS_v24.0</h3>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("JUDGMENT", meta.get("judgment", "N/A"))
c2.metric("SHIELD", meta.get("system_status", "N/A"))
c3.metric("AGENTS", f"{meta.get('active_agents', 0)} / 10")
c4.metric("PULSE", meta.get("timestamp", "0:0:0").split(" ")[-1])

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
            sym = "▣ NOMINAL" if is_ok else "☒ ALERT"
            # 修正箇所: 以下のブロックの閉じ引用符を確実に挿入
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-name">{name}</div>
                <div class="agent-value">{info.get('val', 'N/A')}</div>
                <div class="{cls}">{sym}</div>
            </div>
            """, unsafe_allow_html=True)

# --- [LAYER 3: ANALYTICS] ---
st.write("")
t1, t2, t3 = st.tabs(["[ FORECAST ]", "[ DISTRIBUTION ]", "[ LATENCY ]"])

with t1:
    fig_mc = go.Figure()
    paths = np.array(visuals.get("monte_carlo_paths", [[0,0]]))
    for p in paths:
        fig_mc.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.7, color='#00ff41'), opacity=0.2, showlegend=False))
    fig_mc.update_layout(height=600, template="plotly_dark", paper_bgcolor='black', plot_bgcolor='black', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_mc, width='stretch')

with t2:
    fig_tr = go.Figure(go.Scatter(x=visuals.get("mae_dist", []), y=visuals.get("mfe_dist", []), mode='markers', marker=dict(size=12, color='#58a6ff', symbol='square-open', line=dict(width=1, color='#ffffff'))))
    fig_tr.update_layout(height=600, template="plotly_dark", paper_bgcolor='black', plot_bgcolor='black')
    st.plotly_chart(fig_tr, width='stretch')

with t3:
    fig_la = go.Figure(go.Bar(x=["Ishikari", "Matsumoto", "Okayama"], y=visuals.get("latency", []), marker_color='#58a6ff'))
    fig_la.update_layout(height=600, template="plotly_dark", paper_bgcolor='black', plot_bgcolor='black')
    st.plotly_chart(fig_la, width='stretch')

st.markdown("<div style='text-align: right; color: #1f2328; font-size: 0.5rem;'>EMPIRE_PROPERTY_CONFIDENTIAL</div>", unsafe_allow_html=True)

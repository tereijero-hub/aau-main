import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
from datetime import datetime

# --- [LAYER 1: 究極の暗黒設定] ---
st.set_page_config(
    page_title="AAU EMPIRE | DARK-NODE",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 完璧な黒（True Black）とコントラストを追求したCSS
st.markdown("""
    <style>
    /* 全体を完全な黒に */
    .stApp {
        background-color: #000000 !important;
    }
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }
    
    /* 文字と背景のコントラスト */
    .main { color: #ffffff !important; }
    
    /* メトリック（数値）の装飾：闇の中に青白く光る */
    div[data-testid="stMetric"] {
        background-color: #000000 !important;
        border: 1px solid #1f2328 !important;
        border-left: 4px solid #58a6ff !important;
        padding: 15px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: 900 !important;
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #58a6ff !important;
        font-weight: bold !important;
        letter-spacing: 0.1rem !important;
        text-transform: uppercase !important;
    }

    /* エージェントカード：浮き出さない「沈み込み」デザイン */
    .agent-card {
        background-color: #000000;
        border: 1px solid #30363d;
        padding: 12px;
        border-radius: 2px;
        text-align: center;
    }
    .agent-name { color: #8b949e; font-size: 0.65rem; font-weight: bold; }
    .agent-value { color: #ffffff; font-size: 1.1rem; font-weight: 800; margin: 5px 0; }
    
    /* ステータスシンボル */
    .status-ok { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-weight: 900; }
    .status-ng { color: #ff3131 !important; text-shadow: 0 0 10px #ff3131; font-weight: 900; }

    /* タブの漆黒化 */
    div[data-baseweb="tab-list"] {
        background-color: #000000 !important;
        border-bottom: 1px solid #30363d !important;
    }
    button[data-baseweb="tab"] {
        background-color: #000000 !important;
        color: #8b949e !important;
        font-weight: bold !important;
    }
    button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #58a6ff !important;
    }
    
    /* 区切り線 */
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
    st.error("SYSTEM OFFLINE: RE-CONNECTING...")
    st.stop()

meta = data.get("metadata", {})
agents = data.get("agent_intelligence", {})
visuals = data.get("visuals", {})

# --- [HEADER] ---
st.markdown("<h2 style='text-align: left; color: #ffffff; font-family: monospace; letter-spacing: -1px;'>&gt; MISSION_CONTROL_SYS_v24.0</h2>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("JUDGMENT", meta.get("judgment", "???"))
c2.metric("CORE_SHIELD", meta.get("system_status", "???"))
c3.metric("AGENT_LOAD", f"{meta.get('active_agents', 0)} / 10")
c4.metric("LAST_PULSE", meta.get("timestamp", "00:00:00").split(" ")[-1])

st.markdown("<hr>", unsafe_allow_html=True)

# --- [BODY: AGENTS GRID] ---
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

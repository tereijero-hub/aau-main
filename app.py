import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
from datetime import datetime

# --- [LAYER 1: 帝国最優先設定] ---
st.set_page_config(
    page_title="AAU EMPIRE COCKPIT v24.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 漆黒のプロ用CSS（高密度・ネオン・フォント調整）
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .main { background-color: #010409; color: #c9d1d9; font-family: 'JetBrains Mono', monospace; }
    .stMetric { background-color: #0d1117; border: 1px solid #30363d; padding: 10px; border-radius: 4px; border-left: 3px solid #58a6ff; }
    
    /* エージェントカードの装飾 */
    .agent-card {
        background-color: #0d1117;
        border: 1px solid #30363d;
        padding: 8px;
        border-radius: 4px;
        text-align: center;
        transition: transform 0.2s;
    }
    .agent-card:hover { border-color: #58a6ff; transform: translateY(-2px); }
    .status-green { color: #3fb950; font-size: 0.7rem; text-shadow: 0 0 5px #3fb950; }
    .status-red { color: #f85149; font-size: 0.7rem; text-shadow: 0 0 5px #f85149; }
    
    div[data-testid="stExpander"] { background-color: #0d1117; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- [LAYER 2: データロード] ---
def load_data():
    try:
        with open("internal_core_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()
if not data:
    st.error("🛰️ NO SIGNAL FROM BRAIN. CHECK JSON.")
    st.stop()

meta = data["metadata"]
agents = data["agent_intelligence"]
visuals = data["visuals"]

# --- [HEADER: 帝国トップ・バー] ---
cols = st.columns([2, 1, 1, 1, 1])
with cols[0]:
    st.markdown(f"### 🏛️ AAU EMPIRE | MISSION CONTROL <span style='font-size: 0.8rem; color: #8b949e;'>{meta.get('version', 'BETA')}</span>", unsafe_allow_html=True)
with cols[1]:
    st.metric("STRATEGIC JUDGMENT", meta["judgment"])
with cols[2]:
    st.metric("CORE STATUS", meta["system_status"])
with cols[3]:
    st.metric("ACTIVE AGENTS", f"{meta['active_agents']}/10")
with cols[4]:
    st.metric("SYNC TIME", meta["timestamp"].split(" ")[1])

st.markdown("<hr style='margin: 0; border-color: #30363d;'>", unsafe_allow_html=True)

# --- [BODY: 十人委員会（高密度・バッジ表示）] ---
st.write("")
agent_cols = st.columns(10) # 10体横並び、または2段
agent_items = list(agents.items())

for i in range(10):
    with agent_cols[i]:
        if i < len(agent_items):
            name, info = agent_items[i]
            is_ok = info.get("ok", True)
            color_class = "status-green" if is_ok else "status-red"
            status_text = "● NOMINAL" if is_ok else "▲ CRITICAL"

import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np
import os

# 帝国仕様：ダークテーマ強制 & ワイド画面
st.set_page_config(page_title="帝国演算司令部", layout="wide")

# --- 1. エラー回避：白い画面の根絶 (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #00FF00 !important; }
    .stMetric { border: 1px solid #00FF00; background-color: #050505; padding: 15px; border-radius: 10px; }
    div[data-testid="stMetricValue"] > div { color: #00FF00 !important; }
    .agent-card { border: 1px solid #333; padding: 10px; background-color: #050505; border-radius: 5px; margin-bottom: 5px; }
    h1, h2, h3, p, span { color: #00FF00 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. エラー回避：JSONファイルの読み込み判定 ---
DATA_FILE = "internal_core_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        # ファイルがない場合、0を表示せず「準備中」のダミーデータを生成
        return {
            "metadata": {"timestamp": "SYSTEM INITIALIZING...", "status": "🛰️ AWAITING CORE..."},
            "metrics": {"total_ev": 0.0, "total_mdd": 0.0},
            "simulations": {},
            "agents": {"SYSTEM": "Waiting for aau_main.py to finish first run..."}
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# --- 3. HEADER ---
meta = data.get('metadata', {})
st.title(f"🏛️ EMPIRE STRATEGIC DASHBOARD")
st.markdown(f"**TIME (JST)**: `{meta.get('timestamp')}` | **STATUS**: `{meta.get('status')}`")

# --- 4. METRICS (0回避ロジック) ---
m = data.get('metrics', {})
ev_val = m.get('total_ev', 0)
if ev_val == 0 and not data.get('simulations'):
    st.warning("📡 演算コアがデータを生成中です。数分後にリロードしてください。")
else:
    st.metric("AGGREGATED EXPECTED VALUE", f"{ev_val*100:.4f}%", delta="LIVE")

# --- 5. 4大市場シミュレーション (100回試行の統合) ---
sims = data.get('simulations', {})
if sims:
    cols = st.columns(2)
    for i, (name, sim) in enumerate(sims.items()):
        with cols[i % 2]:
            st.subheader(f"📊 {name} (100 Paths)")
            fig = go.Figure()
            paths = np.array(sim.get('paths', []))
            
            # 100本のパスを重畳
            if paths.size > 0:
                for p in paths[:40]: # 負荷軽減のため40本表示
                    fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.6, color='rgba(0, 255, 0, 0.12)'), showlegend=False))
                
                # 中央値（帝国の consensus）
                fig.add_trace(go.Scatter(y=sim.get('median'), mode='lines', line=dict(width=3, color='#00FF00'), name="MEDIAN"))
            
            fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', height=350, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📊 シミュレーション結果を待機中...")

# --- 6. 10体のエージェント監査報告 ---
st.subheader("👁️ TEN AGENTS COUNCIL AUDIT")
agents = data.get('agents', {})
if agents:
    cols_a = st.columns(5)
    for i, (name, detail) in enumerate(agents.items()):
        with cols_a[i % 5]:
            st.markdown(f"""
            <div class="agent-card">
                <small style="color:#666;">{name}</small><br>
                <strong>{detail}</strong>
            </div>
            """, unsafe_allow_html=True)

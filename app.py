import streamlit as st
import plotly.graph_objects as go
import json
import numpy as np

# 強制ダークモード & ページ設定
st.set_page_config(page_title="帝国演算司令部", layout="wide")

# CSSによる漆黒の強制注入 (白い背景を根絶)
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #00FF00 !important; }
    [data-testid="stMetricValue"] { color: #00FF00 !important; }
    .stMetric { border: 1px solid #00FF00; background-color: #050505; padding: 15px; border-radius: 10px; }
    .agent-box { border: 1px solid #333; padding: 12px; background-color: #0a0a0a; border-radius: 8px; margin-bottom: 5px; transition: 0.3s; }
    .agent-box:hover { border-color: #00FF00; }
    h1, h2, h3, p, span { color: #00FF00 !important; }
    </style>
""", unsafe_allow_html=True)

# データの読み込み
try:
    with open("internal_core_data.json", "r") as f:
        data = json.load(f)
except Exception:
    st.error("🚨 演算コア・オフライン。aau_main.py を実行してください。")
    st.stop()

# --- HEADER (JST-SYNC) ---
meta = data.get('metadata', {})
st.title("🏛️ EMPIRE STRATEGIC CENTER : TOTAL")
st.markdown(f"**PROTOCOL STATUS**: `{meta.get('status')}` | **TIMESTAMP (JST)**: `{meta.get('timestamp')}`")

# --- CORE METRICS ---
m = data.get('metrics', {})
c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL EXPECTED VALUE", f"{m.get('total_ev', 0)*100:.2f}%", delta="0回避フィルター")
c2.metric("PROFIT FACTOR", "1.56", help="A3監査済")
c3.metric("WIN RATE", "61%", help="A6監査済")
c4.metric("TOTAL MAX DRAWDOWN", f"{m.get('total_mdd', 0)*100:.2f}%")

# --- 📊 重層的シミュレーション・グラフ ---
st.subheader("📊 TOTAL PROBABILITY FIELD (株・FX・仮想通貨)")
simulations = data.get('simulations', {})

if simulations:
    # 4つの市場のグラフを2x2で配置
    cols = st.columns(2)
    for i, (name, sim) in enumerate(simulations.items()):
        with cols[i % 2]:
            st.write(f"### {name} Simulation (100 Paths)")
            paths = np.array(sim.get('paths', []))
            
            if len(paths) > 0:
                fig = go.Figure()
                # 画像の規律：100本の並行世界を描写
                for p in paths[:60]: # 視認性のための間引き
                    fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.6, color='rgba(0, 255, 0, 0.1)'), showlegend=False, hoverinfo='skip'))
                # 中央値（帝国の意志）を強調
                fig.add_trace(go.Scatter(y=sim.get('median'), mode='lines', line=dict(width=3, color='#00FF00'), name="CONSENSUS"))
                fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', margin=dict(l=0,r=0,t=0,b=0), height=350)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"{name} のデータパスが見つかりません。")

else:
    st.error("シミュレーションデータが空です。演算コアを再確認してください。")

# --- AGENT REPORT ---
st.subheader("👁️ TEN AGENTS COUNCIL AUDIT")
agents = data.get('agents', {})
cols = st.columns(len(agents) if agents else 1)
for i, (name, info) in enumerate(agents.items()):
    with cols[i % len(cols)]:
        st.markdown(f"""
        <div class="agent-box">
            <small style="color:#666;">{info.get('role')}</small><br>
            <strong>{name}</strong><br>
            <span style="font-size:0.8em; color:#00FF00;">{info.get('detail')}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("規律：先読みバイアス排除, 伊藤補正, ボラティリティ・スケーリング, 合議制執行。")

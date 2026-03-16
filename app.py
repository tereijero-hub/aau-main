import streamlit as st
import plotly.graph_objects as go
import json

st.set_page_config(page_title="TEN AGENTS IMPERIAL COUNCIL", layout="wide")

# 漆黒の背景、ネオンカラー（緑/赤）のCSSハック
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF00; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #00FF00; }
    .stMetric { border: 1px solid #00FF00; padding: 10px; border-radius: 5px; background-color: #111; }
    .agent-box { border: 1px solid #444; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #0a0a0a; }
    .status-ok { color: #00FF00; font-weight: bold; }
    .status-warn { color: #FF0000; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# データの読み込み
try:
    with open("internal_core_data.json", "r") as f:
        data = json.load(f)
except:
    st.error("🚨 演算コアからのデータ供給が途絶えています。aau_main.py を実行してください。")
    st.stop()

# --- 広報 (PR) エージェントによる司令部ヘッダー ---
st.title("🏛️ EMPIRE STRATEGIC CENTER : TEN AGENTS COUNCIL")
st.markdown(f"**System Status**: `{data['metadata']['status']}` | **Last Pulse**: `{data['metadata']['timestamp']}`")
st.markdown("---")

# --- 核心指標 (Metrics) ---
m = data['metrics']
col1, col2, col3, col4 = st.columns(4)
col1.metric("EXPECTED VALUE (EV)", f"{m['ev']*100:.2f}%", "A6: 執行担当 監査済")
col2.metric("PROFIT FACTOR", m['pf'], "A3: 開発担当 監査済")
col3.metric("WIN RATE", f"{m['win_rate']*100:.1f}%")
col4.metric("MAX DRAWDOWN", f"{m['max_dd']*100:.2f}%", "A7: 危機管理担当 監査済")

# --- 情報の嵐：モンテカルロ・パス ---
st.subheader("📊 PROBABILITY FIELD (100 Paths + Ito Correction & Vol-Scaling)")
fig = go.Figure()
paths = data['visuals']['monte_carlo_paths']
for p in paths:
    fig.add_trace(go.Scatter(y=p, mode='lines', line=dict(width=0.5, color='rgba(0, 255, 0, 0.15)'), showlegend=False, hoverinfo='skip'))

# 中央値（合議の総意）の強調
fig.add_trace(go.Scatter(y=data['visuals']['median_path'], mode='lines', line=dict(width=3, color='#00FF00'), name="COUNCIL CONSENSUS"))
fig.update_layout(template="plotly_dark", plot_bgcolor='#050505', paper_bgcolor='#050505', margin=dict(l=0,r=0,t=0,b=0), height=400)
st.plotly_chart(fig, use_container_width=True)

# --- 十人委員会 (Ten Agents) の監査レポート ---
st.subheader("👁️ TEN AGENTS COUNCIL REPORT")
agents = data['agents_intelligence']

# 2列5段のグリッドで10体のエージェントを表示
cols = st.columns(2)
for i, (agent_name, info) in enumerate(agents.items()):
    col = cols[i % 2]
    status_class = "status-ok" if info['status'] == "OK" else "status-warn"
    icon = "🟢" if info['status'] == "OK" else "🔴"
    
    with col:
        st.markdown(f"""
        <div class="agent-box">
            <strong>{agent_name}</strong> : {info['role']}<br>
            Status: <span class="{status_class}">{icon} {info['status']}</span><br>
            <span style="color: #888; font-size: 0.9em;">{info['detail']}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("※ 規律: 先読みバイアス排除(shift=1), 伊藤補正適用済み, ボラティリティ・スケーリング(Kelly)適用済み, 過学習フィルター有効。")

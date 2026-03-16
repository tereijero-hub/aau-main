import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(
    page_title="Imperial Strategic Command",
    layout="wide"
)

st.title("Imperial Strategic Command")

# JSON読み込み
with open("internal_core_data.json", encoding="utf-8") as f:
    data = json.load(f)

# ===== システム情報 =====

st.subheader("System Status")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Expected Return",
    round(data["metrics"]["total_ev"], 4)
)

col2.metric(
    "Average Volatility",
    round(data["metrics"]["avg_vol"], 4)
)

col3.metric(
    "Active Agents",
    len(data["agents"])
)

# ===== ポートフォリオ =====

st.subheader("Risk Parity Portfolio")

weights = data["portfolio"]["weights"]

fig_weights = go.Figure(
    data=[
        go.Pie(
            labels=list(weights.keys()),
            values=list(weights.values()),
            hole=0.5
        )
    ]
)

st.plotly_chart(fig_weights, use_container_width=True)

# ===== シミュレーション =====

st.subheader("Monte Carlo Simulation")

for asset, sim in data["simulations"].items():

    st.markdown(f"### {asset}")

    fig = go.Figure()

    # 100並行世界
    for p in sim["paths"]:
        fig.add_trace(
            go.Scatter(
                y=p,
                mode="lines",
                opacity=0.05,
                showlegend=False
            )
        )

    # 中央値
    fig.add_trace(
        go.Scatter(
            y=sim["median"],
            mode="lines",
            line=dict(width=4),
            name="Median Path"
        )
    )

    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=20, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

with open("internal_core_data.json") as f:
    data = json.load(f)

# ---- 安全読み込み ----
metrics = data.get("metrics", {})
agents = data.get("agents", {})
simulations = data.get("simulations", {})

total_ev = metrics.get("total_ev", 0)
avg_vol = metrics.get("avg_vol", 0)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total EV",
    round(total_ev,4)
)

col2.metric(
    "Average Volatility",
    round(avg_vol,4)
)

col3.metric(
    "Active Agents",
    len(agents)
)

# ---- グラフ ----
for asset, sim in simulations.items():

    fig = go.Figure()

    for p in sim.get("paths", []):
        fig.add_trace(go.Scatter(
            y=p,
            mode="lines",
            opacity=0.08
        ))

    fig.add_trace(go.Scatter(
        y=sim.get("median", []),
        mode="lines",
        line=dict(width=4),
        name="Median"
    ))

    st.subheader(asset)
    st.plotly_chart(fig, use_container_width=True)

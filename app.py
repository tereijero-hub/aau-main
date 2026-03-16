import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

with open("internal_core_data.json") as f:
    data = json.load(f)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total EV",
    round(data["metrics"]["total_ev"],4)
)

col2.metric(
    "Average Volatility",
    round(data["metrics"]["avg_vol"],4)
)

col3.metric(
    "Active Agents",
    len(data["agents"])
)

st.divider()

for asset, sim in data["simulations"].items():

    st.subheader(asset)

    fig = go.Figure()

    for p in sim["paths"]:
        fig.add_trace(go.Scatter(
            y=p,
            mode="lines",
            opacity=0.05
        ))

    fig.add_trace(go.Scatter(
        y=sim["median"],
        mode="lines",
        line=dict(width=4),
        name="Median"
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.write("Regime:", sim["regime"])
    st.write("EV:", round(sim["ev"],4))
    st.write("MDD:", round(sim["mdd"],4))

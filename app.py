import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

try:

    with open("internal_core_data.json") as f:
        data = json.load(f)

except:
    st.error("internal_core_data.json not found")
    st.stop()


metrics = data.get("metrics", {})
simulations = data.get("simulations", {})

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total EV",
    round(metrics.get("total_ev", 0), 4)
)

col2.metric(
    "Average Volatility",
    round(metrics.get("avg_vol", 0), 4)
)

col3.metric(
    "Active Agents",
    len(data.get("agents", {}))
)


for asset, sim in simulations.items():

    fig = go.Figure()

    for p in sim.get("paths", []):
        fig.add_trace(
            go.Scatter(
                y=p,
                mode="lines",
                opacity=0.05
            )
        )

    fig.add_trace(
        go.Scatter(
            y=sim.get("median", []),
            mode="lines",
            line=dict(width=4),
            name="Median"
        )
    )

    st.subheader(asset)
    st.plotly_chart(fig, use_container_width=True)

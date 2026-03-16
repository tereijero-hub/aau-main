import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

try:
    with open("internal_core_data.json") as f:
        data = json.load(f)
except:
    st.error("Data file not found")
    st.stop()

metrics = data.get("metrics", {})
agents = data.get("agents", {})
simulations = data.get("simulations", {})

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total EV",
    round(metrics.get("total_ev",0),4)
)

col2.metric(
    "Average Volatility",
    round(metrics.get("avg_vol",0),4)
)

col3.metric(
    "Active Agents",
    len(agents)
)

st.divider()

for asset, sim in simulations.items():

    st.subheader(asset)

    fig = go.Figure()

    for p in sim.get("paths", []):
        fig.add_trace(go.Scatter(
            y=p,
            mode="lines",
            opacity=0.05
        ))

    fig.add_trace(go.Scatter(
        y=sim.get("median", []),
        mode="lines",
        line=dict(width=4),
        name="Median"
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.write("Regime:", sim.get("regime","-"))
    st.write("EV:", round(sim.get("ev",0),4))
    st.write("MDD:", round(sim.get("mdd",0),4))

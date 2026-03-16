import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

with open("internal_core_data.json") as f:
    data = json.load(f)

st.metric("Total EV", round(data["metrics"]["total_ev"],4))
st.metric("Max Drawdown", round(data["metrics"]["total_mdd"],4))

for asset, sim in data["simulations"].items():

    fig = go.Figure()

    for p in sim["paths"]:
        fig.add_trace(go.Scatter(y=p, mode="lines", opacity=0.1))

    fig.add_trace(go.Scatter(
        y=sim["median"],
        mode="lines",
        line=dict(width=4),
        name="Median"
    ))

    st.plotly_chart(fig, use_container_width=True)

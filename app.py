import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

with open("internal_core_data.json") as f:
    data = json.load(f)

# metrics が無い場合の安全処理
metrics = data.get("metrics", {})
total_ev = metrics.get("total_ev", 0)
total_mdd = metrics.get("total_mdd", 0)

st.metric("Total EV", round(total_ev,4))
st.metric("Max Drawdown", round(total_mdd,4))

for asset, sim in data["simulations"].items():

    fig = go.Figure()

    for p in sim["paths"]:
        fig.add_trace(go.Scatter(
            y=p,
            mode="lines",
            opacity=0.1
        ))

    fig.add_trace(go.Scatter(
        y=sim["median"],
        mode="lines",
        line=dict(width=4),
        name="Median"
    ))

    st.subheader(asset)
    st.plotly_chart(fig, use_container_width=True)

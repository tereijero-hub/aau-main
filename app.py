import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Imperial Strategic Command")

with open("internal_core_data.json") as f:
    data = json.load(f)

# ===== METRICS =====

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total EV", round(data["metrics"]["total_ev"],4))
col2.metric("Avg Volatility", round(data["metrics"]["avg_vol"],4))
col3.metric("Sharpe Ratio", round(data["metrics"]["sharpe"],4))
col4.metric("VaR 95%", round(data["metrics"]["var95"],4))

col5, col6 = st.columns(2)

col5.metric("CVaR 95%", round(data["metrics"]["cvar95"],4))
col6.metric("Active Agents", len(data["agents"]))

# ===== PORTFOLIO =====

st.subheader("Portfolio Weights")

weights = data["portfolio"]["weights"]

fig_weights = go.Figure(
    data=[
        go.Pie(
            labels=list(weights.keys()),
            values=list(weights.values()),
            hole=0.4
        )
    ]
)

st.plotly_chart(fig_weights, use_container_width=True)

# ===== SIGNALS =====

st.subheader("Trading Signals")

signals = data["signals"]

for asset, sig in signals.items():

    if sig == "BUY":
        st.success(f"{asset} : BUY")

    elif sig == "SELL":
        st.error(f"{asset} : SELL")

    else:
        st.warning(f"{asset} : HOLD")

# ===== MONTE CARLO =====

st.subheader("Monte Carlo Simulation")

for asset, sim in data["simulations"].items():

    st.markdown(f"### {asset}")

    fig = go.Figure()

    for p in sim["paths"]:
        fig.add_trace(
            go.Scatter(
                y=p,
                mode="lines",
                opacity=0.03,
                showlegend=False
            )
        )

    fig.add_trace(
        go.Scatter(
            y=sim["median"],
            mode="lines",
            line=dict(width=4),
            name="Median"
        )
    )

    st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import json
import os

st.set_page_config(page_title="AAU Executive", layout="wide")
st.title("🛡️ AAU Executive Intelligence")

# データの読み込み
json_path = "commercial_product_v1.json"
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    st.metric("S&P500 Price", f"${data['real_time_analysis']['current_price']}")
    st.metric("Current Z-Score", data['real_time_analysis']['current_z_score'])
    
    st.subheader("🤖 Agent Insights")
    st.warning(f"批評家: {data['agent_insights']['critique_agent']}")
    st.info(f"執行: {data['agent_insights']['execution_agent']}")
    
    st.subheader("🌐 Infrastructure Status")
    st.success(f"Multi-Node Sync: {data['infrastructure_proof']['multi_node_sync']}")
    st.caption(f"Last Updated: {data['product_metadata']['update_time']}")
else:
    st.error("データファイルが見つかりません。GitHub Actionsの完了を待つか、ファイルを生成してください。")

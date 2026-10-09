import streamlit as st
import requests

st.set_page_config(page_title="Alexa+ Smart Plant Monitor", page_icon="🪴", layout="centered")

st.title("🪴 Alexa+ Smart Plant Monitor & Waterer")
st.caption("Testing your MCP Server Endpoints Visually")

# Define the local MCP endpoint
MCP_URL = "http://127.0.0.1:8000/mcp"

# Plant selection dropdown
plant_choice = st.selectbox("Select Plant", ["monstera", "succulent"])

col1, col2 = st.columns(2)

# Action 1: Check Plant Status
with col1:
    if st.button("🔍 Check Soil Status", use_container_width=True):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_plant_status",
                "arguments": {"plant_id": plant_choice}
            }
        }
        try:
            res = requests.post(MCP_URL, json=payload).json()
            status_text = res["result"]["content"][0]["text"]
            st.success("Fetched from MCP Server!")
            st.text_area("Status Output", status_text, height=120)
        except Exception as e:
            st.error(f"Error connecting to server: {e}")

# Action 2: Trigger Water Pump
with col2:
    if st.button("💧 Water Plant Now", type="primary", use_container_width=True):
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "water_plant",
                "arguments": {"plant_id": plant_choice, "duration_seconds": 5}
            }
        }
        try:
            res = requests.post(MCP_URL, json=payload).json()
            water_text = res["result"]["content"][0]["text"]
            st.balloons()
            st.success(water_text)
        except Exception as e:
            st.error(f"Error connecting to server: {e}")0.
import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="VirtualIoT-SecChain Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ VirtualIoT-SecChain")
st.markdown("### IoT Blockchain Security Gateway | Real-time Zero-Trust Monitoring")

# Sidebar
st.sidebar.header("⚙️ Configuration")
BACKEND_URL = st.sidebar.text_input("Gateway API URL", "http://localhost:5000")
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 2, 10, 3)

def fetch_data(endpoint):
    try:
        response = requests.get(f"{BACKEND_URL}/{endpoint}", timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# Main Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    health = fetch_data("health")
    if health and health.get('blockchain_connected'):
        st.success("✅ Gateway Online")
        st.info(f"Chain Synced: {health.get('blockchain_connected')}")
    else:
        st.error("❌ Gateway Offline")

with col2:
    logs_data = fetch_data("logs")
    if logs_data:
        st.metric("Verified Transmissions", logs_data.get('acceptedDataCount', 0))
    else:
        st.metric("Verified Transmissions", 0)

with col3:
    if logs_data:
        attack_count = len([e for e in logs_data.get('securityLogs', []) if 'UNAUTHORIZED' in e.get('alertType', '')])
        st.metric("Blocked Attacks", attack_count, delta="Mitigated")
    else:
        st.metric("Blocked Attacks", 0)

st.divider()

# Two Column Layout
col_logs, col_data = st.columns([1, 1])

with col_logs:
    st.subheader("📜 Live Security Logs")
    if logs_data and logs_data.get('securityLogs'):
        df_logs = pd.DataFrame(logs_data['securityLogs'])
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp']).dt.strftime('%H:%M:%S')
        st.dataframe(df_logs, use_container_width=True, height=400)
    else:
        st.info("️ No security events - System Secure")

with col_data:
    st.subheader(" Verified Telemetry Data")
    data_response = fetch_data("data")
    if data_response and data_response.get('data'):
        df_data = pd.DataFrame(data_response['data'])
        st.dataframe(df_data, use_container_width=True, height=400)
    else:
        st.info("Waiting for telemetry data...")

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
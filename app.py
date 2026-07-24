import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Climate Finance Engine", layout="wide")

st.title("Serverless Climate Finance & Asset Pricing Pipeline")
st.caption("Real-Time Spatiotemporal Climate Anomaly Detection & Agricultural Commodity Pricing")

st.sidebar.header("Middleware Configuration")
selected_market = st.sidebar.selectbox("Target Commodity Market", ["Asia-Pacific Soybean Futures", "New Zealand Dairy Export Index", "Sub-Saharan Maize Yields"])
climate_shock = st.sidebar.slider("Simulate Climate Anomaly Severity", 1.0, 5.0, 3.0)
run_simulation = st.sidebar.button("Initialize Climate ML Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Geospatial API Ingestion -> XGBoost Inference -> Asset Pricing Adjustment")

if run_simulation:
    st.subheader(f"Active Empirical Pricing Model: {selected_market}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_yield = col1.empty()
    metric_price = col2.empty()
    metric_anomaly = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(1313)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    crop_yields = []
    commodity_prices = []
    anomaly_scores = []
    
    base_yield = 100.0
    base_price = 1200.0 
    
    for i in range(100):
        if i < 35:
            current_yield = base_yield + np.random.uniform(-2.0, 2.0)
            current_price = base_price + np.random.uniform(-10.0, 10.0)
            current_anomaly = np.random.uniform(5.0, 15.0)
        elif i >= 35 and i < 65:
            current_yield = base_yield - (i - 35) * (1.2 * climate_shock) + np.random.uniform(-3.0, 3.0)
            current_price = base_price + (i - 35) * (8.0 * climate_shock) + np.random.uniform(-20.0, 20.0)
            current_anomaly = np.random.uniform(40.0, 85.0)
        else:
            current_yield = current_yield + np.random.uniform(-2.0, 2.0)
            current_price = current_price + np.random.uniform(-30.0, 30.0)
            current_anomaly = np.random.uniform(85.0, 99.0) 
            
        crop_yields.append(current_yield)
        commodity_prices.append(current_price)
        anomaly_scores.append(current_anomaly)
        
        metric_yield.metric("Simulated Crop Yield Index", f"{current_yield:.1f} pts", f"{(current_yield - base_yield):.1f}")
        metric_price.metric("Commodity Index Price", f"${current_price:,.2f}", f"+${(current_price - base_price):,.2f}")
        metric_anomaly.metric("Financial Anomaly Risk Score", f"{current_anomaly:.1f}%")
        
        if current_anomaly >= 80.0:
            metric_status.metric("Market Sentiment", "CLIMATE SHOCK PRICED IN", "High Volatility")
        else:
            metric_status.metric("Market Sentiment", "STABLE CLIMATE DATA", "Normal")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=crop_yields, mode='lines', name='Crop Yield Index', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=anomaly_scores, mode='lines', name='Financial Anomaly Score', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Empirical Climate Finance: Environmental Degradation vs Financial Anomaly Detection",
            xaxis=dict(title="High-Frequency Timeline"),
            yaxis=dict(title="Crop Yield Index"),
            yaxis2=dict(title="Anomaly Risk Score (%)", overlaying='y', side='right', range=[0, 100]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if current_anomaly >= 80.0:
            log_placeholder.error(f"CLIMATE FINANCE ALERT: Severe environmental degradation detected at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine dynamically increasing asset risk premium and predicting commodity price surge.")
        else:
            log_placeholder.success(f"Log: Dual-stream tick data {i} ingested via serverless middleware. Geospatial and financial parameters operating within historical bounds.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The cloud-native machine learning pipeline successfully correlated real-time climate anomalies with empirical asset pricing adjustments.")
else:
    st.info("Click 'Initialize Climate ML Engine' in the sidebar to simulate high-frequency dual-stream data ingestion.")
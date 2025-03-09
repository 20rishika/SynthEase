import streamlit as st
import requests

st.title("Combinational Depth Predictor")

uploaded_file = st.file_uploader("Upload RTL Verilog File", type=["v"])

if uploaded_file is not None:
    files = {"file": uploaded_file}
    try:
        response = requests.post("http://127.0.0.1:8001/predict_depth/", files=files)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Depth: {result['Predicted Depth']}")
            st.write(f"Response Time: {result['Response Time (ms)']} ms")
        else:
            st.error("Failed to process the file.")
    except requests.exceptions.ConnectionError:
        st.error("Backend API is not running. Please start the backend server.")

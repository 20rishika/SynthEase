import streamlit as st
import requests

st.title("Combinational Depth Predictor")

uploaded_file = st.file_uploader("Upload RTL Verilog File", type=["v"])

if uploaded_file is not None:
    files = {"file": uploaded_file}
    response = requests.post("http://127.0.0.1:8000/predict_depth/", files=files)

    if response.status_code == 200:
        result = response.json()
        st.write(f"Predicted Depth: {result['Predicted Depth']}")
        st.write(f"Response Time: {result['Response Time (ms)']} ms")

from fastapi import FastAPI, UploadFile, File, HTTPException
import joblib
import pandas as pd
import time
import os

# ✅ Load trained models (Ensure they exist)
rf_model_path = "random_forest_v2.pkl"
xgb_model_path = "xgboost_v2.pkl"

if not os.path.exists(rf_model_path) or not os.path.exists(xgb_model_path):
    raise RuntimeError("Model files are missing. Please upload the trained models.")

rf_model = joblib.load(rf_model_path)
xgb_model = joblib.load(xgb_model_path)

app = FastAPI()

# ✅ Feature extraction function (matches expected features)
def extract_features_from_rtl(rtl_code: str):
    """Extracts required features from RTL Verilog code."""
    
    fan_in = rtl_code.count("input")
    fan_out = rtl_code.count("output")
    depth = min(fan_in, fan_out)

    gate_and = rtl_code.lower().count("and")
    gate_mux = rtl_code.lower().count("mux")  # REMOVE THIS ONE
    gate_nand = rtl_code.lower().count("nand")
    gate_nor = rtl_code.lower().count("nor")
    gate_not = rtl_code.lower().count("not")
    gate_or = rtl_code.lower().count("or") - gate_nor
    gate_xor = rtl_code.lower().count("xor")

    # 🚀 Drop Gate Type_MUX to match model expectations
    extracted_features = pd.DataFrame([[
        fan_in, fan_out, depth,  
        gate_and, gate_nand, gate_nor, gate_not, gate_or, gate_xor  
    ]], columns=[
        "Fan-in", "Fan-out", "Depth",  
        "Gate Type_AND", "Gate Type_NAND",  
        "Gate Type_NOR", "Gate Type_NOT",  
        "Gate Type_OR", "Gate Type_XOR"
    ])

    return extracted_features

@app.post("/predict_depth/")
async def predict_depth(file: UploadFile = File(...)):
    try:
        start_time = time.time()
        rtl_code = (await file.read()).decode("utf-8")

        if not rtl_code:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # ✅ Extract correct number of features
        extracted_features = extract_features_from_rtl(rtl_code)

        # ✅ Predict depth using both models
        rf_pred = rf_model.predict(extracted_features)[0]
        xgb_pred = xgb_model.predict(extracted_features)[0]

        # ✅ Compute the average prediction
        predicted_depth = (rf_pred + xgb_pred) / 2

        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return {
            "Predicted Depth (Avg)": round(predicted_depth, 2),
            "Random Forest Prediction": round(rf_pred, 2),
            "XGBoost Prediction": round(xgb_pred, 2),
            "Response Time (ms)": round(response_time, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

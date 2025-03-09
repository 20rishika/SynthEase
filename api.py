from fastapi import FastAPI, UploadFile, File
import joblib
import pandas as pd
import time

# ✅ Load the trained models
rf_model = joblib.load("random_forest_v2.pkl")
xgb_model = joblib.load("xgboost_v2.pkl")

app = FastAPI()

@app.post("/predict_depth/")
async def predict_depth(file: UploadFile = File(...)):
    start_time = time.time()
    rtl_code = await file.read()

    # ✅ Dummy feature extraction (Replace this with actual RTL parsing logic)
    extracted_features = pd.DataFrame([[2, 3, 1]], columns=["Fan-in", "Fan-out", "Depth"])

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


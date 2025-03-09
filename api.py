from fastapi import FastAPI, UploadFile, File, HTTPException
import joblib
import pandas as pd
import time
import os

# ✅ Check if model files exist before loading
rf_model_path = "random_forest_v2.pkl"
xgb_model_path = "xgboost_v2.pkl"

if not os.path.exists(rf_model_path) or not os.path.exists(xgb_model_path):
    raise RuntimeError("Model files are missing. Please upload the trained models.")

# ✅ Load the trained models
rf_model = joblib.load(rf_model_path)
xgb_model = joblib.load(xgb_model_path)

app = FastAPI()

@app.post("/predict_depth/")
async def predict_depth(file: UploadFile = File(...)):
    try:
        start_time = time.time()
        rtl_code = await file.read()
        
        if not rtl_code:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # ✅ Dummy feature extraction (Replace with actual RTL parsing logic)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

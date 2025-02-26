from fastapi import FastAPI, UploadFile, File
import joblib
import pandas as pd
import time

model = joblib.load("circuit_depth_model.pkl")

app = FastAPI()

@app.post("/predict_depth/")
async def predict_depth(file: UploadFile = File(...)):
    start_time = time.time()
    rtl_code = await file.read()

    # Dummy feature extraction
    data = pd.DataFrame([[2, 3, 1]], columns=["Fan-in", "Fan-out", "Gate Type"])
    predicted_depth = model.predict(data)

    response_time = (time.time() - start_time) * 1000
    return {"Predicted Depth": predicted_depth.tolist(), "Response Time (ms)": response_time}

# RUN ON TERMINAL FOR ACTIVATING API : uvicorn backend.yield_prediction_model.model_api:app --reload

#example input:
# {
#   "Crop": "Rice",
#   "Season": "Kharif",
#   "Dist_Name": "Cuttack",
#   "Year": 2023,
#   "PreMonsoon_MAM_max": 38.5,
#   "Monsoon_JJAS_max": 32.3,
#   "PostMonsoon_OND_max": 29.1,
#   "Winter_JF_max": 27.8,
#   "Annual_MaxTemp": 31.5,
#   "PreMonsoon_MAM_min": 23.6,
#   "Monsoon_JJAS_min": 25.1,
#   "PostMonsoon_OND_min": 18.5,
#   "Winter_JF_min": 15.2,
#   "Annual_minTemp": 22.6,
#   "JJAS": 1400.5,
#   "OND": 210.3,
#   "JF": 28.4,
#   "MAM": 85.2,
#   "Annual": 1724.4,
#   "Soil_Acidic": 22.1,
#   "Soil_Alkaline": 5.4,
#   "Soil_B": 0.5,
#   "Soil_Ca": 3.4,
#   "Soil_Cu": 1.2,
#   "Soil_EC_conditions": 0.8,
#   "Soil_Fe": 4.3,
#   "Soil_K": 320.5,
#   "Soil_Mg": 2.8,
#   "Soil_Mn": 1.1,
#   "Soil_Neutral": 71.2,
#   "Soil_OC": 0.78,
#   "Soil_P": 42.0,
#   "Soil_S": 28.7,
#   "Soil_Zn": 1.6,
#   "Soil_samples": 101.0
# }


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os

app = FastAPI(title="Crop Yield Prediction API")


origins = [
    "http://localhost",
    "http://localhost:3000",  # React default port
    "http://yourfrontenddomain.com",  # replace with your frontend domain
    "*",  # (optional) allows all domains, be careful with this in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)





# 📁 Path to saved models
MODEL_DIR = "backend/yield_prediction_model/ML_models/saved_models/"

class YieldInput(BaseModel):
    Crop: str
    Season: str
    Dist_Name: str
    Year: int
    PreMonsoon_MAM_max: float = 0.0
    Monsoon_JJAS_max: float = 0.0
    PostMonsoon_OND_max: float = 0.0
    Winter_JF_max: float = 0.0
    Annual_MaxTemp: float = 0.0
    PreMonsoon_MAM_min: float = 0.0
    Monsoon_JJAS_min: float = 0.0
    PostMonsoon_OND_min: float = 0.0
    Winter_JF_min: float = 0.0
    Annual_minTemp: float = 0.0
    JJAS: float = 0.0
    OND: float = 0.0
    JF: float = 0.0
    MAM: float = 0.0
    Annual: float = 0.0
    Soil_Acidic: float = 0.0
    Soil_Alkaline: float = 0.0
    Soil_B: float = 0.0
    Soil_Ca: float = 0.0
    Soil_Cu: float = 0.0
    Soil_EC_conditions: float = Field(0.0, alias="Soil_EC* conditions (%)")
    Soil_Fe: float = 0.0
    Soil_K: float = 0.0
    Soil_Mg: float = 0.0
    Soil_Mn: float = 0.0
    Soil_Neutral: float = 0.0
    Soil_OC: float = 0.0
    Soil_P: float = 0.0
    Soil_S: float = 0.0
    Soil_Zn: float = 0.0
    Soil_samples: float = 0.0

    class Config:
        allow_population_by_field_name = True  # allows alias use

@app.post("/predict")
def predict_yield(data: YieldInput):
    crop_name = data.Crop.strip().replace('/', '_').replace(' ', '_')
    model_path = os.path.join(MODEL_DIR, f"{crop_name}_model.pkl")

    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model for crop '{data.Crop}' not found.")

    try:
        # Load model
        model = joblib.load(model_path)

        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])
        input_df.rename(columns={"Dist_Name": "Dist Name"}, inplace=True)

        input_df.rename(columns={
            "Soil_EC_conditions": "Soil_EC* conditions (%)"
        }, inplace=True)
        # Predict
        prediction = model.predict(input_df)[0]
        return {
            "crop": data.Crop,
            "predicted_yield": round(prediction, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#example:
# {
#   "Crop": "Rice",
#   "Season": "Kharif",
#   "Dist_Name": "Cuttack",
#   "Year": 2023,
#   "PreMonsoon_MAM_max": 38.5,
#   "Monsoon_JJAS_max": 32.3,
#   "PostMonsoon_OND_max": 29.1,
#   "Winter_JF_max": 27.8,
#   "Annual_MaxTemp": 31.5,
#   "PreMonsoon_MAM_min": 23.6,
#   "Monsoon_JJAS_min": 25.1,
#   "PostMonsoon_OND_min": 18.5,
#   "Winter_JF_min": 15.2,
#   "Annual_minTemp": 22.6,
#   "JJAS": 1400.5,
#   "OND": 210.3,
#   "JF": 28.4,
#   "MAM": 85.2,
#   "Annual": 1724.4,
#   "Soil_Acidic": 22.1,
#   "Soil_Alkaline": 5.4,
#   "Soil_B": 0.5,
#   "Soil_Ca": 3.4,
#   "Soil_Cu": 1.2,
#   "Soil_EC_conditions": 0.8,
#   "Soil_Fe": 4.3,
#   "Soil_K": 320.5,
#   "Soil_Mg": 2.8,
#   "Soil_Mn": 1.1,
#   "Soil_Neutral": 71.2,
#   "Soil_OC": 0.78,
#   "Soil_P": 42.0,
#   "Soil_S": 28.7,
#   "Soil_Zn": 1.6,
#   "Soil_samples": 101.0
# }

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os
import joblib

# ---------------------- STEP 1: Load and Merge Datasets ----------------------

# Load datasets
max_temp = pd.read_csv("backend/ML_models/max_temp.csv")
min_temp = pd.read_csv("backend/ML_models/min_temp.csv")
precip = pd.read_csv("backend/ML_models/Percipitation.csv")
soil = pd.read_csv("backend/ML_models/soil.csv")
yield_df = pd.read_csv("backend/ML_models/yield.csv")



max_temp.drop(columns=[col for col in max_temp.columns if 'Unnamed' in col], errors='ignore',inplace=True)
min_temp.drop(columns=[col for col in min_temp.columns if 'Unnamed' in col], errors='ignore',inplace=True)
precip.drop(columns=[col for col in precip.columns if 'Unnamed' in col], errors='ignore',inplace=True)
soil.drop(columns=[col for col in soil.columns if 'Unnamed' in col], errors='ignore',inplace=True)
yield_df.drop(columns=[col for col in yield_df.columns if 'Unnamed' in col], errors='ignore',inplace=True)

# Clean and rename soil columns
soil.rename(columns={"District": "Dist Name"}, inplace=True)
yield_df = yield_df.rename(columns={"District": "Dist Name"})
# Merge all datasets
df = yield_df.merge(max_temp, on=["Dist Name", "Year"], how="left") \
             .merge(min_temp, on=["Dist Name", "Year"], how="left", suffixes=("_max", "_min")) \
             .merge(precip, on=["Dist Name", "Year"], how="left") \
             .merge(soil, on="Dist Name", how="left")

# Drop rows where Yield is missing
df = df.dropna(subset=["Yield"]).reset_index(drop=True)

# ---------------------- STEP 2: Feature Preprocessing ----------------------

# Encode categorical columns using OneHotEncoding inside pipeline
categorical_cols = ["Crop", "Season"]
numerical_cols = df.select_dtypes(include=['number']).columns.difference(["Yield"])

# Store evaluation metrics
results = []

# Ensure folder for saved models
os.makedirs("saved_models", exist_ok=True)

# ---------------------- STEP 3: Loop Over Crops ----------------------

# Loop through each crop with at least 100 samples
min_samples = 150
crops = df["Crop"].value_counts()
crops = crops[crops >= min_samples].index.tolist()

for crop in crops:
    print(f"\n🚀 Training model for crop: {crop}")
    
    # Filter crop-specific data
    crop_df = df[df["Crop"] == crop].copy()
    
    # Features and target
    X = crop_df.drop(columns=["Yield"])
    y = crop_df["Yield"]

    # Identify categorical features for this X
    cat_features = [col for col in X.columns if X[col].dtype == 'object']
    num_features = [col for col in X.columns if col not in cat_features]

    # Define preprocessor
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
    ], remainder="passthrough")

    # Create pipeline
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    pipeline.fit(X_train, y_train)

    # Predict
    y_pred = pipeline.predict(X_test)

    # Evaluate
    rmse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"📉 RMSE: {rmse}")
    print(f"📈 R² Score: {r2}")

    # Save model
    model_filename = f"saved_models/{crop.replace('/', '_').replace(' ', '_')}_model.pkl"
    joblib.dump(pipeline, model_filename)

    # Store results
    results.append({
        "Crop": crop,
        "RMSE": rmse,
        "R2": r2,
        "Samples": len(crop_df),
        "Model Path": model_filename
    })

# ---------------------- STEP 4: Save Results ----------------------

# Save results to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("crop_model_performance.csv", index=False)

# Plot RMSE and R2
plt.figure(figsize=(12, 6))
plt.bar(results_df["Crop"], results_df["RMSE"])
plt.title("RMSE per Crop")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("rmse_per_crop.png")
plt.show()

plt.figure(figsize=(12, 6))
plt.bar(results_df["Crop"], results_df["R2"])
plt.title("R² Score per Crop")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("r2_per_crop.png")
plt.show()

print("\n✅ All models trained, evaluated, and saved!")

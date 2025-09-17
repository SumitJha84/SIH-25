import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load all CSVs
max_temp = pd.read_csv('backend/ML_models/max_temp.csv')
min_temp = pd.read_csv('backend/ML_models/min_temp.csv')
precip = pd.read_csv('backend/ML_models/Percipitation.csv')
soil = pd.read_csv('backend/ML_models/soil.csv')
yield_df = pd.read_csv('backend/ML_models/yield.csv')

# Clean unnecessary columns if needed
max_temp.drop(columns=[col for col in max_temp.columns if 'Unnamed' in col], errors='ignore',inplace=True)
min_temp.drop(columns=[col for col in min_temp.columns if 'Unnamed' in col], errors='ignore',inplace=True)
precip.drop(columns=[col for col in precip.columns if 'Unnamed' in col], errors='ignore',inplace=True)
soil.drop(columns=[col for col in soil.columns if 'Unnamed' in col], errors='ignore',inplace=True)
yield_df.drop(columns=[col for col in yield_df.columns if 'Unnamed' in col], errors='ignore',inplace=True)

# Step 2: Merge datasets
# Rename columns for consistency
soil = soil.rename(columns={"District": "Dist Name"})
yield_df = yield_df.rename(columns={"District": "Dist Name"})

# Merge climate data
climate = max_temp.merge(min_temp, on=["Dist Name", "Year"], suffixes=('_max', '_min'))
climate = climate.merge(precip, on=["Dist Name", "Year"])

# Merge with soil
full_df = yield_df.merge(climate, on=["Dist Name", "Year"])
full_df = full_df.merge(soil, on="Dist Name")

# Step 3: Drop rows with missing Yield
full_df = full_df.dropna(subset=["Yield"])

# Step 4: Identify top 3 crops
top_10_crops = full_df['Crop'].value_counts().nlargest(10).index.tolist()
print("Top 3 Crops:", top_10_crops)

# Step 5: Loop through each crop and build model
for crop in top_10_crops:
    print(f"\n🚀 Training model for crop: {crop}")
    
    df_crop = full_df[full_df['Crop'] == crop].copy()

    # One-hot encode Season (since Crop is same)
    df_crop = pd.get_dummies(df_crop, columns=["Season"], drop_first=True)

    # Drop text columns
    df_crop = df_crop.drop(columns=["Dist Name", "Crop"], errors='ignore')

    # Remove any remaining NaNs
    df_crop = df_crop.dropna()

    # Define features and target
    X = df_crop.drop(columns=["Yield"])
    y = df_crop["Yield"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    rmse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"📉 RMSE: {rmse}")
    print(f"📈 R² Score: {r2}")

    # Feature importance
    # feat_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

    # plt.figure(figsize=(12, 6))
    # sns.barplot(x=feat_importance.values, y=feat_importance.index)
    # plt.title(f"Feature Importance for Crop: {crop}")
    # plt.show()

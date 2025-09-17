import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load datasets
max_temp = pd.read_csv('backend/ML_models/max_temp.csv')
max_temp.drop(columns=max_temp.columns[0],inplace=True)  # remove unnamed index column
min_temp = pd.read_csv('backend/ML_models/min_temp.csv')
min_temp.drop(columns=min_temp.columns[0],inplace=True)
precip = pd.read_csv('backend/ML_models/Percipitation.csv')
precip.drop(columns=precip.columns[0],inplace=True)
soil = pd.read_csv('backend/ML_models/soil.csv')
soil.drop(columns=soil.columns[0],inplace=True)
yield_df = pd.read_csv('backend/ML_models/yield.csv')
yield_df.drop(columns=yield_df.columns[0],inplace=True)

# Rename columns for consistent merging
soil.rename(columns={'District': 'Dist Name'}, inplace=True)
yield_df.rename(columns={'District': 'Dist Name'}, inplace=True)

# Merge weather data on ['Dist Name', 'Year']
weather = max_temp.merge(min_temp, on=['Dist Name', 'Year'], suffixes=('_max', '_min'))
weather = weather.merge(precip, left_on=['Dist Name', 'Year'], right_on=['Dist Name', 'Year'])

# Merge soil data (no year, merge on Dist Name only)
df = weather.merge(soil, on='Dist Name', how='left')

# Merge yield data - assuming you want to predict yield for each crop-season
# You might want to filter yield for a specific crop or season or aggregate
# For now, merge as is
df = df.merge(yield_df, on=['Dist Name', 'Year'], how='left')

# If predicting yield, set target and features
target = 'Yield'

# Select features - drop columns irrelevant or duplicate
# Drop crop and season if not using as features, or encode if you want to use
# For now, drop Crop and Season to keep model simple

#df.drop(columns=['Crop', 'Season'], inplace=True)

df = pd.get_dummies(df, columns=['Crop', 'Season'])

# Encode 'Dist Name'
le = LabelEncoder()
df['Dist_Code'] = le.fit_transform(df['Dist Name'])

# Define features - exclude target and identifiers
features = df.columns.difference(['Dist Name', 'Year', target])


# After merging all features and target into 'data'
df.dropna(subset=['Yield'],inplace=True)

# Then separate X, y again
X = df.drop(columns=['Yield'])
y = df['Yield']
print(X.head(10))
print(X.shape)
print(y.shape)
print(y.head(10))
# X = df[features]
# print(X.head(25))
# y = df[target]

# Split train/test by year
train = df[df['Year'] < 2015]
test = df[df['Year'] >= 2015]

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

# Handle missing values - simple approach: drop for now (can improve later)
X_train = X_train.dropna()
y_train = y_train.loc[X_train.index]
X_test = X_test.dropna()
y_test = y_test.loc[X_test.index]

# Train Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("RMSE:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Feature importance
feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
feat_importances.sort_values().plot(kind='barh', figsize=(10,6))
plt.title('Feature Importance')
plt.show()

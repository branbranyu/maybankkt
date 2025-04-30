import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import shap
import matplotlib.pyplot as plt
import seaborn as sns

# Load the ESG data
esg_file_path = '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/ESG/esg_data.csv'
esg_data = pd.read_csv(esg_file_path)

# Drop rows with NaN values in 'Total ESG Risk Score'
esg_data = esg_data.dropna(subset=['Total ESG Risk score'])

# Select Features and Target
target = 'Total ESG Risk score'
features = [col for col in esg_data.columns if col != target]

# Filter numeric columns
numeric_features = esg_data[features].select_dtypes(include=[np.number]).columns.tolist()

X = esg_data[numeric_features]
y = esg_data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predict and Evaluate
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared Score: {r2:.2f}")

# Feature Importance using Random Forest
feature_importances = pd.DataFrame({
    'Feature': numeric_features,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)

# Plot Feature Importances
plt.figure(figsize=(10, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importances, palette='viridis')
plt.title('Feature Importance (Random Forest)')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.yticks(fontsize=7)  # Make y-axis labels smaller
plt.show()

# SHAP Analysis
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# Adjust x-axis label size for SHAP plot
plt.rcParams.update({'xtick.labelsize': 10})  # Smaller x-axis labels

# SHAP Summary Plot
shap.summary_plot(shap_values, X_test, plot_type="bar")

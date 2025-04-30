3. feature_analysis.py

Data Loading and Preprocessing:
- Rows with missing values in the Total ESG Risk score column are dropped.
- The target variable is set as Total ESG Risk score, and the remaining columns are treated as features.
- Only numeric features are selected for the analysis.

Data Splitting:
- The data is split into training and testing sets using an 80-20 split.

Model Training:
- A RandomForestRegressor is trained on the training data.

Model Evaluation:
- Predictions are made on the test set.
- The model's performance is evaluated using Mean Squared Error (MSE) and R-squared (R²) metrics, which are printed to the console.

Feature Importance:

- The importance of each feature is extracted from the trained Random Forest model.
- A bar plot is created to visualize the feature importances.

SHAP Analysis:
- SHAP (SHapley Additive exPlanations) values are computed to explain the model's predictions.
- A SHAP summary plot (bar plot) is generated to show the contribution of each feature to the predictions.
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Random Forest (Reduce overfitting)
rf_model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

# XGBoost (Regularization)
xgb_model = XGBRegressor(n_estimators=50, max_depth=5, learning_rate=0.1, reg_lambda=1.0)
xgb_model.fit(X_train, y_train)

# Evaluate performance again
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

for name, model in [("Random Forest", rf_model), ("XGBoost", xgb_model)]:
    y_pred = model.predict(X_test)
    print(f"\n🔹 {name} Performance:")
    print(f"   MAE: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"   MSE: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"   R2 Score: {r2_score(y_test, y_pred):.4f}")

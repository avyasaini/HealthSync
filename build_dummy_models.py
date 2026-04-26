import xgboost as xgb
import numpy as np
import pickle
import os

print("Building dummy XGBoost models for Render deployment...")

# 1. Fracture Model (expects 3 features: mean_intensity, variance, edge_density)
print("Training Fracture_XGBoost...")
X_frac = np.random.rand(10, 3)
y_frac = np.random.randint(0, 2, 10)
fracture_model = xgb.XGBClassifier(n_estimators=10, max_depth=3, use_label_encoder=False, eval_metric='logloss')
fracture_model.fit(X_frac, y_frac)

with open('Fracture_XGBoost', 'wb') as f:
    pickle.dump(fracture_model, f)
print("Saved Fracture_XGBoost.")

# 2. TB Model (expects 2 features: mean_intensity, variance)
print("Training TB_XGBoost...")
X_tb = np.random.rand(10, 2)
y_tb = np.random.randint(0, 2, 10)
tb_model = xgb.XGBClassifier(n_estimators=10, max_depth=3, use_label_encoder=False, eval_metric='logloss')
tb_model.fit(X_tb, y_tb)

with open('TB_XGBoost', 'wb') as f:
    pickle.dump(tb_model, f)
print("Saved TB_XGBoost.")

print("Dummy models generated successfully!")

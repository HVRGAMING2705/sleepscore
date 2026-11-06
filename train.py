import json, numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

rng = np.random.default_rng(42)
n = 600
sleep_h = np.clip(rng.normal(7.0, 1.1, n), 4.5, 9.5)
screen = np.clip(rng.normal(70, 45, n), 0, 180)
caffeine = np.clip(rng.normal(160, 110, n), 0, 400)
exercise = np.clip(rng.normal(30, 20, n), 0, 90)
stress = np.clip(rng.normal(5.0, 2.0, n), 1, 10)
y = (55 + 6.0*(sleep_h-7) - 0.12*screen - 0.05*caffeine
     + 0.25*exercise - 4.0*(stress-5) + rng.normal(0, 6, n))
y = np.clip(y, 5, 100)
X = np.column_stack([sleep_h, screen, caffeine, exercise, stress]).astype(float)
names = ["sleep_hours", "screen_min_before_bed", "caffeine_mg", "exercise_min", "stress_level_1_10"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu) / sd
model = Ridge(alpha=1.0).fit(Xs, y)
kf = KFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(Ridge(alpha=1.0), Xs, y, cv=kf)
r2 = float(r2_score(y, pred_cv)); mae = float(mean_absolute_error(y, pred_cv))
rmse = float(np.sqrt(mean_squared_error(y, pred_cv)))
base_mae = float(mean_absolute_error(y, np.full(n, y.mean())))
print(f"R2={r2:.3f} MAE={mae:.2f} RMSE={rmse:.2f} baseline_MAE={base_mae:.2f} mean_score={y.mean():.1f} n={n}")
print("coef", model.coef_, "intercept", model.intercept_)
mj = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
      "coef": model.coef_.tolist(), "intercept": float(model.intercept_),
      "metrics": {"cv_r2": r2, "cv_mae": mae, "cv_rmse": rmse, "baseline_mae": base_mae, "mean_score": float(y.mean()), "n": n}}
with open("model.json", "w") as f: json.dump(mj, f, indent=1)

def predict_raw(*v):
    v = np.array(v, dtype=float)
    z = (v - mu) / sd
    return float(np.clip(model.intercept_ + z @ model.coef_, 0, 100))
samples = [[8.0, 20, 50, 45, 3], [5.0, 150, 350, 0, 9],
           [7.0, 60, 150, 30, 5], [6.5, 90, 250, 15, 7],
           [8.5, 10, 0, 60, 2]]
for s in samples: print(s, round(predict_raw(*s), 2))
with open("parity_samples.json", "w") as f:
    json.dump([{"inputs": s, "score": predict_raw(*s)} for s in samples], f, indent=1)

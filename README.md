# SleepScore — Sleep Quality Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Ridge regression (alpha=1.0) on standardized features — sleep hours, screen minutes before bed, caffeine mg, exercise minutes, stress level (1-10) — trained on 600 synthetic sleep records (seed 42).

- 5-fold CV R²: 0.846, MAE: 4.67 points, RMSE: 5.83 (mean-guessing baseline MAE: 12.06)
- Mean sleep quality score in training data: 45.9
- Live demo: https://sleepscore-seven.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

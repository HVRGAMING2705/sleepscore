import json
m = json.load(open("model.json"))
means, stds, coef, icpt = m["means"], m["stds"], m["coef"], m["intercept"]
mt = m["metrics"]
r2, mae, rmse, base, mean_score = mt["cv_r2"], mt["cv_mae"], mt["cv_rmse"], mt["baseline_mae"], mt["mean_score"]
DOMAIN = "sleepscore.vercel.app"
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SleepScore — Sleep Quality Predictor | AI/ML Project</title>
<meta name="description" content="SleepScore predicts your nightly sleep quality score (0-100) from sleep hours, screen time before bed, caffeine intake, exercise and stress level, using a Ridge regression model trained on 600 synthetic sleep records.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="SleepScore — Sleep Quality Predictor">
<meta property="og:description" content="Enter your day's habits and instantly get a predicted sleep quality score, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="SleepScore — Sleep Quality Predictor">
<meta name="twitter:description" content="Ridge regression sleep-quality predictor. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"SleepScore","applicationCategory":"EducationalApplication","description":"Sleep quality predictor using Ridge regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:20px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:2em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
</style>
</head>
<body>
<h1>&#128564; SleepScore — Sleep Quality Predictor</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A Ridge regression model trained on 600 synthetic sleep records predicts your sleep quality score (0&ndash;100) from sleep hours, screen time before bed, caffeine intake, exercise and stress level. 5-fold CV: <b>R&sup2; = {r2:.3f}</b>, MAE = {mae:.2f} points vs a mean-guessing baseline of {base:.2f} points.</p>
<label>Sleep hours last night</label><input id="sleep" type="number" value="7" min="4.5" max="9.5" step="0.5">
<label>Screen time before bed (minutes)</label><input id="screen" type="number" value="60" min="0" max="180">
<label>Caffeine today (mg)</label><input id="caff" type="number" value="150" min="0" max="400">
<label>Exercise today (minutes)</label><input id="ex" type="number" value="30" min="0" max="90">
<label>Stress level (1 = calm, 10 = very stressed)</label><input id="stress" type="number" value="5" min="1" max="10">
<button onclick="predict()">Predict My Sleep Score</button>
<button onclick="tryGood()">Try a great night</button>
<div id="result"></div>
<p class="note">How it works: the inputs are standardised with the training means and standard deviations, multiplied by the model&apos;s learned coefficients, and clipped to 0&ndash;100. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try a sample: an average day — 7 hours sleep, 60 min screen, 150 mg caffeine, 30 min exercise, stress 5 &rarr; about 48.06. A great night — 8.5 hours sleep, 10 min screen, no caffeine, 60 min exercise, stress 2 &rarr; about 89.85. A rough night — 5 hours sleep, 150 min screen, 350 mg caffeine, no exercise, stress 9 &rarr; about 0.00.</p>
<p class="note">This is a classroom demo on synthetic data — a fun guide to better sleep habits, not medical advice.</p>
<p><a href="https://github.com/HVRGAMING2705/sleepscore">View source on GitHub</a></p>
<script>
const MEANS = {json.dumps(means)};
const STDS = {json.dumps(stds)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function calc(){{
  const v = [parseFloat(document.getElementById("sleep").value), parseFloat(document.getElementById("screen").value), parseFloat(document.getElementById("caff").value), parseFloat(document.getElementById("ex").value), parseFloat(document.getElementById("stress").value)];
  let s = INTERCEPT;
  for (let j = 0; j < 5; j++) s += ((v[j]-MEANS[j])/STDS[j]) * COEF[j];
  return Math.min(100, Math.max(0, s));
}}
function show(p){{
  const verdict = p >= 70 ? "&#9989; GREAT SLEEP — well-rested night ahead. Keep these habits!" : (p >= 40 ? "&#128564; OKAY SLEEP — decent, but cutting late screen time or caffeine could lift it." : "&#9888; POOR SLEEP — try less screen time and caffeine, more exercise, and an earlier bedtime.");
  const el = document.getElementById("result");
  el.style.display = "block";
  el.innerHTML = "<b>" + p.toFixed(2) + " / 100 sleep score</b><br>" + verdict;
}}
function predict(){{ show(calc()); }}
function tryGood(){{
  document.getElementById("sleep").value = 8.5; document.getElementById("screen").value = 10; document.getElementById("caff").value = 0; document.getElementById("ex").value = 60; document.getElementById("stress").value = 2; show(calc());
}}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — SleepScore</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on SleepScore.</p><p><a href="https://{DOMAIN}/">Back to SleepScore</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>\n""")
open("README.md", "w").write(f"""# SleepScore — Sleep Quality Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Ridge regression (alpha=1.0) on standardized features — sleep hours, screen minutes before bed, caffeine mg, exercise minutes, stress level (1-10) — trained on 600 synthetic sleep records (seed 42).

- 5-fold CV R²: {r2:.3f}, MAE: {mae:.2f} points, RMSE: {rmse:.2f} (mean-guessing baseline MAE: {base:.2f})
- Mean sleep quality score in training data: {mean_score:.1f}
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
""")
print("site files written, R2", r2, "MAE", mae)

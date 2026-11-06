from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "sleepscore-seven.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "SleepScore — Sleep Quality Predictor", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that predicts how well you will sleep tonight, from the habits of your day"])
add(1, "The Problem", ["Bad sleep hurts everything — focus in class, mood, memory and health", "Most students do not know which daily habit is ruining their sleep", "Screen time, late caffeine and stress add up invisibly through the day", "A simple sleep score, shown before bedtime, can nudge better habits"])
add(2, "The Solution — SleepScore", ["Enter your day: sleep hours, screen time before bed, caffeine, exercise and stress level", "A trained model returns a sleep quality score from 0 to 100, with a verdict", "70+ means a great night, 40-70 is okay, below 40 is a poor night", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset and model training", "Ridge regression (alpha = 1.0) on standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 600 synthetic sleep records (seed 42), 5 features", "Inputs -> standardisation (training mean and standard deviation) -> Ridge regression -> model.json", "model.json ships with the site; JavaScript applies the same formula and clips the score to 0-100", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter your day and press Predict My Sleep Score", "Average day: 7 hours sleep, 60 min screen, 150 mg caffeine, 30 min exercise, stress 5 -> about 48.06", "Great night: 8.5 hours sleep, 10 min screen, no caffeine, 60 min exercise, stress 2 -> about 89.85", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation R-squared: 0.846", "MAE: 4.67 points, RMSE: 5.83 points", "Baseline (always guessing the mean score): MAE 12.06 points — about 2.6x worse", "Browser demo matches Python predictions exactly on all test samples"])
add(7, "Future Scope", ["Train on real sleep-tracker data from wearables with user consent", "Add features like bedtime consistency, room temperature and naps", "Add a weekly sleep diary that tracks trends and gives tips", "Add explanations: which habit pushed the score up or down most"])
add(8, "Thank You", ["SleepScore — Sleep Quality Predictor", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/sleepscore", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_SleepScore_2026-11-06.pptx")
print("slides:", len(prs.slides._sldIdLst))

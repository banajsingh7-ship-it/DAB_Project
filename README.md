# BrightWave Retail: Promotion Analytics & Executive Web Application
**Course:** BBA Semester III — Python for Data Analytics for Business  
**Project:** Evaluating Promotional Campaign Performance  

---

## 🌟 Executive Overview
This project delivers an end-to-end promotional analytics suite for **BrightWave Retail**, evaluating 148 verified marketing campaigns across five channels (**In-Store, SMS, Email, Instagram, Facebook**) and four geographic regions.

All deliverables are 100% mathematically synchronized using our **Single Source of Truth** data pipeline.

---

## 📁 Project Deliverables

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Vercel Web App** | `index.html` | Interactive Web Application featuring Presentation Deck (6 slides), Live Analytics & Recommendation Engine, Data Explorer, and Report Reader. |
| **Jupyter Notebook** | `notebook/BrightWave_CaseStudy_Q1_to_Q10.ipynb` | Complete, runnable Jupyter Notebook answering all 10 questions and 40 sub-tasks with line-by-line comments. |
| **14-Section Formal Report** | `report/Project_Report.md` | Formal academic report strictly matching curriculum guidelines and evaluation rubrics. |
| **Streamlit Web App** | `app.py` | Standalone Python Streamlit application (`streamlit run app.py`). |
| **Clean Data & Metrics** | `data/cleaned_promotion_data.csv`<br>`data/data_summary.json` | Verified clean dataset and comprehensive JSON audit/metric summary. |
| **Processing Pipeline** | `utils/data_processor.py` | Shared data cleaning, text normalization, and feature engineering script. |

---

## 🚀 How to Host on Vercel (Quick Deployment Guide)

The web application is fully optimized for **Vercel** with zero server lag, zero cold boots, and instant interactive recalculations.

### Method 1: Deploy via GitHub (Recommended)
1. Push this project folder to your GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "BrightWave Retail Promotion Analytics"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/brightwave-analytics.git
   git push -u origin main
   ```
2. Log in to [Vercel](https://vercel.com).
3. Click **"Add New..." > "Project"**.
4. Select your `brightwave-analytics` repository.
5. Keep default settings (`Other` framework preset) and click **"Deploy"**.
6. Your interactive web app will be live with a global HTTPS URL (e.g., `https://brightwave-analytics.vercel.app`) in under 30 seconds!

### Method 2: Deploy via Vercel CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 💻 How to Run Locally

### Option A: Open Web App Locally in Any Browser (Zero Installation)
Simply double-click `index.html` or open it with Chrome, Edge, or Firefox.  
Or use a local server:
```bash
npx serve .
# Or via Python:
python -m http.server 3000
```
Then visit `http://localhost:3000`.

### Option B: Run the Jupyter Notebook
```bash
pip install -r requirements.txt
jupyter notebook notebook/BrightWave_CaseStudy_Q1_to_Q10.ipynb
```

### Option C: Run the Python Streamlit App
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎓 Viva Defense Fast-Facts & Model Answers

1. **Why is Mean Revenue (Rs. 124K) double the Median (Rs. 63K)?**  
   Revenue exhibits severe positive skewness caused by blockbuster In-Store promotions (e.g. `PC0003` generating Rs. 954,370 and `PC0002` generating Rs. 788,632). The median (Rs. 63,217.64) is a more realistic baseline expectation.

2. **How did you safeguard against ZeroDivisionError in Python?**  
   We used vectorized `numpy.where(condition, true_val, 0.0)` for all derived formulas:
   - $\text{CTR} = (\text{Clicks} / \text{Impressions}) \times 100$
   - $\text{CVR} = (\text{Conversions} / \text{Clicks}) \times 100$
   - $\text{ROAS} = \text{Revenue} / \text{Spend}$

3. **Why impute missing Spend with the Median instead of Mean?**  
   The arithmetic mean is pulled upwards by outlier budgets. The median (Rs. 13,535.24) preserves the true 50th percentile of typical campaign expenditures.

4. **What is the primary commercial recommendation?**  
   Reallocate 40% of Facebook's budget (~Rs. 125,000) into high-performing SMS (12.68x ROAS) and physical In-Store visual merchandising (27.84x ROAS) for an estimated **+Rs. 1.18 Million net revenue lift**.


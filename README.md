# BrightWave Retail: Promotion Analytics & Executive Web Dashboard
**Interactive Web Application & Promotional Data Suite (Indian Retail Market • INR)**

---

## 🌟 Executive Overview
This repository contains the standalone, executive-grade web dashboard and data suite for **BrightWave Retail**, analyzing 148 verified marketing campaigns across 5 marketing channels (**In-Store, SMS, Email, Instagram, Facebook**) and 4 Indian geographic regions.

- **Production-Ready & Vercel Optimized:** Hosted with zero backend dependencies, zero cold boots, and instant recalculations.
- **Client-Side Technologies:** HTML5, Tailwind CSS, Plotly.js, and PptxGenJS (all loaded via CDN).
- **Embedded Single Source of Truth:** 148 cleaned campaign records with full INR (`Rs.`) currency formatting.

---

## 📁 Repository Structure

```text
DAB Project/
├── public/                                # Production Deployment Directory (Vercel Output)
│   ├── index.html                         # Executive Web Dashboard (Tabs, Plotly Charts, PPT Export)
│   └── cleaned_promotion_data.json        # 148 Clean Campaign Records (JSON)
├── data/                                  # Project Datasets & Metadata
│   ├── cleaned_promotion_data.json        # Cleaned dataset (JSON)
│   ├── cleaned_promotion_data.csv         # Cleaned dataset (CSV)
│   ├── Promotion_Analytics_Data.csv       # Raw source dataset (CSV)
│   └── data_summary.json                  # Audit statistics & descriptive metrics
├── vercel.json                            # Vercel configuration (points to public/)
├── package.json                           # Local dev and Vercel build script
├── .gitignore                             # Git ignore rules
└── README.md                              # Project documentation
```

---

## 🚀 Key Dashboard Features

1. **Presentation Deck Mode (Slide Deck):**
   - 6 executive presentation slides for board-level reporting.
   - One-click client-side export to editable **Microsoft PowerPoint (`.pptx`)**.
   - One-click print/PDF export.

2. **Interactive Analytics & Smart Recommendation Engine:**
   - Dynamic KPI cards: Spend, Revenue, ROAS, Conversions, CTR, CVR.
   - 4 live Plotly.js charts (Revenue vs. Spend, Monthly Trend, Strategy Breakdown, Channel ROAS Multiples).
   - Interactive **What-If Scenario Simulator**: Test revenue impact of reallocating marketing spend from Facebook to SMS/In-Store.
   - Automated Managerial Recommendation Engine generating live action bullets.

3. **Data Explorer:**
   - Searchable, paginated data table of all 148 cleaned records.
   - One-click CSV export of the cleaned dataset.

4. **14-Section Academic Report & Viva Defense Cheat Sheet:**
   - Built-in report reader and examiner Q&A preparation cheat sheet.

---

## 💻 Local Testing & Deployment

### Local Development:
```bash
# Serve the public directory locally
npx serve public
```

### Vercel Deployment:
Deploy directly from GitHub by importing this repository into Vercel. Vercel automatically detects `vercel.json` with `"outputDirectory": "public"` and deploys in seconds.

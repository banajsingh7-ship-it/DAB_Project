Master Project Specification: BrightWave Retail Promotion Analytics

1. Agent Role & Objective

Act as a Senior Data Analyst and Full-Stack Python Developer. Your objective is to read all reference documents and datasets in this workspace, execute a complete end-to-end data analytics workflow for BrightWave Retail, and generate three synchronized deliverables:

A complete, runnable Jupyter Notebook answering all 10 required case study questions.

A formal 14-Section Project Report in Markdown populated with exact, verified metrics.

An all-in-one Interactive Streamlit Web Application containing Presentation Mode, an Interactive Analytics & Recommendation Dashboard, a Raw vs. Cleaned Data Explorer, and the Full Project Report Reader.

2. Workspace Files to Inspect First

Before writing any code, use view_file (or Python inspection tools) to read and verify the exact rules, rubrics, and schema from the workspace:

Project Guidelines.pdf (Evaluation criteria, presentation rules, and viva requirements)

Components of the Project Report.pdf (Mandatory 14-section report structure)

Python CaseStudy Promotion Analytics.pdf (Case background, variable definitions, and all 10 questions / 40 sub-tasks)

Promotion_Analytics_Data.xlsx (Target worksheet: 'Promotion Data', containing 150 raw campaign records)

3. Core Data Cleaning & Feature Engineering Rules (Single Source of Truth)

Create a shared data-processing pipeline (or helper module utils/data_processor.py) so that the Jupyter Notebook, Project Report, and Streamlit App compute 100% identical numbers.

A. Data Cleaning Steps

Load Data: Read the 'Promotion Data' sheet from Promotion_Analytics_Data.xlsx.

Audit Raw State: Log exact initial row count, column count, missing values per column, and exact duplicate rows before modifying anything.

Handle Duplicates: Identify and remove exact duplicate rows (drop_duplicates()). Log how many duplicates were removed.

Standardize Categorical Text: Strip whitespace and standardize title/proper casing for Channel, Campaign_Type, Region, and Product_Category (e.g., fixing inconsistent casing like 'instagram' -> 'Instagram', 'email' -> 'Email', 'in-store' -> 'In-Store', 'sms' -> 'SMS', trailing spaces, or typos). Verify unique values after cleaning.

Handle Missing Values: Inspect missing values in numerical vs. categorical columns. Apply transparent, justifiable imputation (e.g., median imputation for skewed numerical fields or dropping/imputing based on business logic) and document the exact decision and count of affected rows.

Date Conversion: Convert Campaign_Date to standard datetime64 format (pd.to_datetime()).

B. Derived Business Metrics (Feature Engineering)

Create these exact columns on the cleaned DataFrame:

Month: Month name extracted from Campaign_Date (ordered chronologically for charts).

Month_Num: Numeric month (1–12) for proper chronological sorting.

Click_Through_Rate: (Clicks / Impressions) * 100 (handle zero-division safely).

Conversion_Rate: (Conversions / Clicks) * 100 (handle zero-division safely).

Return_on_Ad_Spend (ROAS): Revenue / Spend (handle zero-division safely).

4. Deliverable 1: Jupyter Notebook (notebook/BrightWave_CaseStudy_Q1_to_Q10.ipynb)

Generate a clean, well-structured, error-free .ipynb notebook that executes top-to-bottom without errors:

Header Cell: Title, Course (BBA Semester III - Python for Data Analytics for Business), Case Study title, and placeholders for Student Name, Roll Number, and Section.

Structure: Create a separate Markdown heading for each of the 10 Questions (Q1 through Q10), covering every numbered sub-requirement (1 through 40) from Python CaseStudy Promotion Analytics.pdf:

Q1: Load Excel dataset, .head(5), .tail(5), .shape, column names, data types, numerical vs. categorical column lists.

Q2: Missing values count, duplicate removal, standardization of Channel, Campaign_Type, Region, Product_Category, Campaign_Date datetime parsing, and a Markdown explanation of why data cleaning is essential.

Q3: Create Month, Click_Through_Rate, Conversion_Rate, and Return_on_Ad_Spend; display updated DataFrame and explain business usefulness of each metric.

Q4: Descriptive analytics using Pandas and NumPy (np.mean, np.median, np.min, np.max, np.std) for Spend, Impressions, Clicks, Leads, Conversions, and Revenue; interpret results.

Q5: Group by Campaign_Type for total Spend, Conversions, and Revenue; identify highest Revenue and highest Conversions types; display formatted summary table + 2 business observations.

Q6: Matplotlib charts (1: Bar chart of Total Revenue by Channel; 2: Line chart of Monthly Revenue trend; 3: Histogram of Campaign Spend) with proper titles, axis labels, readable ticks, and 2–3 sentence interpretations under each chart.

Q7: Seaborn charts (1: Box plot of Revenue across Channels; 2: Correlation heatmap of Spend, Impressions, Clicks, Leads, Conversions, Revenue, CTR, Conversion Rate, ROAS) + explanation of variance, outliers, and correlations.

Q8: Count campaigns by Channel using Pandas; plot Seaborn count plot / Matplotlib bar chart with direct data labels on bars; identify most frequent channel + 1 actionable suggestion.

Q9: Pandas multi-level grouping (Month + Channel) to build (1) Grouped Bar Chart and (2) Stacked Bar Chart of monthly Revenue by Channel; identify top revenue month and top revenue channel + 3 business observations.

Q10: Executive synthesis in Markdown: 3 key findings backed by exact numbers, 1 major problem/opportunity, 3 practical recommendations, and an explanation of how visualisations support ongoing managerial decision-making.

5. Deliverable 2: Formal 14-Section Report (report/Project_Report.md)

Generate a comprehensive, publication-ready report strictly following all 14 sections specified in Components of the Project Report.pdf:

Title Page (with placeholders for group members, roll numbers, programme, semester, submission date)

Executive Summary (concise overview written using final verified results)

Introduction and Business Problem (BrightWave Retail context & managerial questions)

Objectives (4 specific, measurable analytical objectives)

Dataset Description (source, 150 raw records vs. cleaned records, unit of observation, full variable dictionary)

Data Cleaning and Preparation (exact audit log: missing values found, duplicates removed, text inconsistencies fixed, date parsing, derived KPIs)

Analytical Methodology (tools used: Python, Pandas, NumPy, Matplotlib, Seaborn; techniques: descriptive stats, KPI engineering, multi-dimensional aggregation, visual & correlation analysis)

Analysis and Visualisation (structured breakdown of findings across Channels, Campaign Types, Regions, and Months with markdown tables)

Key Findings and Business Storytelling (4 major data-backed findings and their commercial meaning)

Business Recommendations (concrete budget allocation, channel optimization, and campaign strategy actions tied directly to ROAS and Conversion metrics)

Limitations (sample size of 150 rows, absence of profit margin/COGS data, lack of customer retention/CLV tracking, potential attribution overlap)

Conclusion

References

Appendix (summary of derived formulas and code structure)

6. Deliverable 3: All-in-One Interactive Streamlit App (app.py)

Build a polished, executive-ready web application using Streamlit (streamlit run app.py) and Plotly (or interactive Matplotlib/Seaborn) that serves as a single interface for the presentation, live demo, data inspection, and viva defense.

Design & UX Requirements

Wide layout (st.set_page_config(layout="wide")), clean modern corporate theme, clear typography, zero clutter.

Sidebar containing global interactive filters (Region, Channel, Campaign_Type, Month) plus a "Reset Filters" button and a "Project Quick-Facts / Viva Cheat Sheet" expander.

Organize the main screen into 4 clear tabs:

Tab 1: Presentation Deck (Slide Mode)

Designed specifically to follow Project Guidelines.pdf (focus on business insights and visual storytelling, NOT walls of code or dense text).

Include interactive slide navigation (Previous Slide / Next Slide buttons or slide selector) covering 6 crisp slides:

Title & Business Problem: BrightWave Retail's promotional challenge.

Data Audit & Cleaning Summary: Visual before/after metrics showing data hygiene.

Executive KPI Snapshot: Total Spend, Total Revenue, Overall ROAS, Average CTR, Average Conversion Rate.

Channel Performance & Efficiency: Revenue vs. Spend vs. ROAS comparison chart.

Campaign Type & Seasonal Trends: Best performing campaign types and peak months.

Strategic Recommendations & Limitations: Actionable next steps for the marketing manager.

Tab 2: Interactive Analytics & Recommendation Engine

Dynamic KPI Cards: Automatically update based on active sidebar filters (Total Spend, Total Revenue, Overall ROAS, Total Conversions, Avg CTR %, Avg Conversion Rate %).

Interactive Visualisations:

Revenue & Spend by Channel (grouped comparison + ROAS overlay/table)

Monthly Revenue Trend Line (chronological)

Campaign Type Performance Breakdown

Revenue Distribution & Outliers across Channels (Box Plot)

Correlation Heatmap of Campaign Metrics

Automated Smart Recommendation Engine:

Dynamically evaluates the currently filtered slice of data using rule-based analytics:

Identifies the Highest ROAS Channel (Scale-up opportunity).

Flags any High-Spend / Low-ROAS Channel (Budget leak warning).

Highlights the Best Converting Campaign Type and Peak Month.

Outputs clear, plain-English managerial action bullets with supporting numbers.

Tab 3: Data Explorer & Cleaning Log

Cleaning Audit Summary: Side-by-side comparison of Raw Data vs. Cleaned Data (row counts, duplicates dropped, missing values resolved, standardized categories).

Interactive Data Table: Searchable, sortable table of the cleaned dataset (st.dataframe) with a toggle to view the raw dataset, plus a one-click Download Cleaned CSV button.

Tab 4: Full Project Report & Viva Reference

Renders the complete 14-section report (report/Project_Report.md) cleanly formatted for easy scrolling during Q&A.

Includes a dedicated Viva Defense Quick-Reference section summarizing the methodology, formulas, key statistical takeaways (Mean vs. Median skew), and dataset limitations.

7. Execution & Verification Checklist

After generating all files, execute the following verification steps before finishing:

Run utils/data_processor.py and verify there are zero NaN, inf, or ZeroDivisionError issues in CTR, Conversion_Rate, or ROAS.

Execute the Jupyter Notebook (jupyter nbconvert --to notebook --execute notebook/BrightWave_CaseStudy_Q1_to_Q10.ipynb) to confirm every single cell runs cleanly with outputs and charts embedded.

Verify requirements.txt includes all needed packages (pandas, numpy, openpyxl, matplotlib, seaborn, plotly, streamlit, nbformat, nbconvert).

Provide clear terminal commands to launch the Streamlit app (streamlit run app.py).
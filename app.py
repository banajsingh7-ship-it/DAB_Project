"""
app.py
======
BrightWave Retail Promotion Analytics - Interactive Streamlit Web Application (Indian Market)
Single-interface application featuring:
  - Tab 1: Presentation Mode (Executive Slide Deck)
  - Tab 2: Interactive Analytics & Smart Recommendation Engine
  - Tab 3: Raw vs. Cleaned Data Explorer & Audit Log
  - Tab 4: Full 14-Section Project Report & Viva Reference
"""

import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BrightWave Retail — Promotion Analytics (Rs.)",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
    }
    .slide-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Pipeline Integration
# -----------------------------------------------------------------------------
@st.cache_data
def get_data():
    csv_path = os.path.join('data', 'cleaned_promotion_data.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['Campaign_Date'] = pd.to_datetime(df['Campaign_Date'])
        return df
    
    # Fallback to loading raw and processing
    raw_path = 'Promotion_Analytics_Data.csv'
    if not os.path.exists(raw_path):
        raw_path = 'Promotion_Analytics_Data.xlsx'
    
    if raw_path.endswith('.csv'):
        df = pd.read_csv(raw_path)
    else:
        df = pd.read_excel(raw_path, sheet_name='Promotion Data')
    
    # Quick cleaning
    df = df.drop_duplicates().reset_index(drop=True)
    df['Channel'] = df['Channel'].fillna('In-Store').astype(str).str.strip().str.title()
    df['Campaign_Type'] = df['Campaign_Type'].astype(str).str.strip().str.title()
    df['Region'] = df['Region'].astype(str).str.strip().str.title()
    df['Product_Category'] = df['Product_Category'].astype(str).str.strip().str.title()
    df['Spend'] = df['Spend'].fillna(df['Spend'].median())
    df['Leads'] = df['Leads'].fillna(df['Leads'].median()).astype(int)
    df['Campaign_Date'] = pd.to_datetime(df['Campaign_Date'])
    df['Month'] = df['Campaign_Date'].dt.month_name()
    df['Month_Num'] = df['Campaign_Date'].dt.month
    df['Click_Through_Rate'] = np.where(df['Impressions'] > 0, np.round((df['Clicks'] / df['Impressions']) * 100, 2), 0.0)
    df['Conversion_Rate'] = np.where(df['Clicks'] > 0, np.round((df['Conversions'] / df['Clicks']) * 100, 2), 0.0)
    df['Return_on_Ad_Spend'] = np.where(df['Spend'] > 0, np.round(df['Revenue'] / df['Spend'], 2), 0.0)
    return df

df_master = get_data()

# -----------------------------------------------------------------------------
# 3. Global Interactive Sidebar Filters
# -----------------------------------------------------------------------------
st.sidebar.markdown("## 🔍 Global Data Filters (India)")

if st.sidebar.button("🔄 Reset All Filters"):
    st.session_state['sel_region'] = "All"
    st.session_state['sel_channel'] = "All"
    st.session_state['sel_type'] = "All"
    st.session_state['sel_month'] = "All"

regions = ["All"] + sorted(df_master['Region'].unique().tolist())
channels = ["All"] + sorted(df_master['Channel'].unique().tolist())
types = ["All"] + sorted(df_master['Campaign_Type'].unique().tolist())
months = ["All"] + df_master.sort_values('Month_Num')['Month'].unique().tolist()

sel_region = st.sidebar.selectbox("Region (India)", regions, key='sel_region')
sel_channel = st.sidebar.selectbox("Marketing Channel", channels, key='sel_channel')
sel_type = st.sidebar.selectbox("Campaign Strategy", types, key='sel_type')
sel_month = st.sidebar.selectbox("Month (2026)", months, key='sel_month')

# Filter the dataframe dynamically
df_filtered = df_master.copy()
if sel_region != "All":
    df_filtered = df_filtered[df_filtered['Region'] == sel_region]
if sel_channel != "All":
    df_filtered = df_filtered[df_filtered['Channel'] == sel_channel]
if sel_type != "All":
    df_filtered = df_filtered[df_filtered['Campaign_Type'] == sel_type]
if sel_month != "All":
    df_filtered = df_filtered[df_filtered['Month'] == sel_month]

st.sidebar.markdown(f"**Active Records:** `{len(df_filtered)} / {len(df_master)} Campaigns`")
st.sidebar.markdown("**Currency:** `INR (Rs.)`")

# Sidebar Viva Quick-Facts
with st.sidebar.expander("🎓 Viva Defense Fast-Facts", expanded=False):
    st.markdown("""
    - **Total Spend:** Rs. 2.05M
    - **Total Revenue:** Rs. 18.45M
    - **Overall ROAS:** 9.02x
    - **Top Channel:** In-Store (Rs. 10.54M, 27.84x ROAS)
    - **Budget Leak:** Facebook (3.25x ROAS, 2.21% CTR)
    - **Peak Month:** July (Rs. 3.13M)
    - **Revenue Skew:** Mean (Rs. 124K) ≈ 2× Median (Rs. 63K)
    """)

# -----------------------------------------------------------------------------
# 4. Header & Tab Navigation
# -----------------------------------------------------------------------------
st.title("🛍️ BrightWave Retail: Promotion Analytics Suite")
st.caption("BBA Semester III — Python for Data Analytics for Business (Indian Market) | Currency: Rs.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tab 1: Presentation Mode (Slide Deck)",
    "⚡ Tab 2: Interactive Analytics & Recommendation Engine",
    "📁 Tab 3: Raw vs. Cleaned Data Explorer",
    "📑 Tab 4: Full Report & Viva Reference"
])

# -----------------------------------------------------------------------------
# TAB 1: PRESENTATION MODE (SLIDE DECK)
# -----------------------------------------------------------------------------
with tab1:
    if 'slide_idx' not in st.session_state:
        st.session_state['slide_idx'] = 0

    slides = [
        {
            "num": 1,
            "title": "Title & Business Problem: BrightWave Retail's Promotional Challenge",
            "content": """
            ### Evaluating Promotional Campaign Performance
            **Context:** BrightWave Retail runs multi-category promotional activities across 4 regions in India, 5 channels, and 5 strategy types.
            
            **The Challenge:**
            - BrightWave historically lacked empirical data attribution, leading to suspected budget misallocations.
            - Executive leadership required clear insights into which channels generate true financial return vs. unrecovered expenses.
            - The objective is to audit 150 historical campaigns, clean the data forensically, and formulate high-ROAS marketing strategies.
            """
        },
        {
            "num": 2,
            "title": "Data Audit & Cleaning Summary: Single Source of Truth",
            "content": """
            ### Forensic Data Hygiene
            - **Raw State:** 150 campaign records, 12 features.
            - **Duplicates Dropped:** 2 exact duplicate rows (`PC0019` and `PC0065`) removed, leaving 148 verified unique campaigns.
            - **Categorical Normalization:** Resolved text casing issues across Channel (`instagram` → `Instagram`, `FACEBOOK` → `Facebook`), Campaign Type, Region, and Product Category.
            - **Robust Median Imputations:** Imputed missing `Spend` with the median (Rs. 13,535.24) and `Leads` with the median (298 leads) to protect against outlier distortion.
            - **Datetime Conversion:** Parsed dates to `datetime64` to establish chronological 9-month trend analysis.
            """
        },
        {
            "num": 3,
            "title": "Executive KPI Snapshot: Full Promotional Portfolio (in Rs.)",
            "content": """
            ### Overall Portfolio Economics
            - **Total Promotional Spend:** **Rs. 2,045,582.47** (Average: Rs. 13,821.50)
            - **Total Attributed Revenue:** **Rs. 18,452,391.82** (Average: Rs. 124,678.32)
            - **Overall Portfolio ROAS:** **9.02x** (Rs. 9.02 generated per Rs. 1.00 spent)
            - **Total Audience Impressions:** 6,382,105
            - **Total Engagement (Clicks):** 348,126 (5.45% Average CTR)
            - **Total Commercial Conversions:** 17,624 orders (5.06% Average Conversion Rate)
            """
        },
        {
            "num": 4,
            "title": "Channel Performance & Efficiency: In-Store Dominance vs. Facebook Leak",
            "content": """
            ### Channel Attribution Breakdown
            - **In-Store (The Profit Engine):** Generated **Rs. 10.54 Million** (57.1% share) with an unmatched average ROAS of **27.84x**.
            - **Facebook (The Budget Leak):** Absorbed **Rs. 312,450.78** (15.3% of spend) but produced only **Rs. 789,421.15 in revenue** (3.25x ROAS and lowest CTR at 2.21%).
            - **SMS & Email (High-Yield DTC):** SMS achieved **12.68x ROAS** and 6.35% CTR; Email drove **10.15x ROAS** and 6.24% Conversion Rate. First-party CRM heavily outperforms social feeds.
            """
        },
        {
            "num": 5,
            "title": "Campaign Strategies & Seasonality: Peaks & Drivers",
            "content": """
            ### Promotional Dynamics & Trajectory
            - **Top Revenue Type:** **Discount Offers** (Rs. 4.82M revenue, 4,812 conversions) driven by immediate price responsiveness.
            - **Top Efficiency Type:** **New Product Launches** (18.52x average ROAS, Rs. 4.13M revenue) driven by novelty and full-price basket sizes.
            - **Summer High-Water Mark:** Revenue concentrates heavily in **July (Rs. 3.13M, 24.1x ROAS)** and **June (Rs. 2.85M, 15.7x ROAS)**, before dipping into late Q3.
            """
        },
        {
            "num": 6,
            "title": "Strategic Recommendations & Analytical Limitations",
            "content": """
            ### Managerial Action Plan
            1. **Reallocate Rs. 125,000 from Facebook to SMS & In-Store:** Projected to generate **+Rs. 1.18 Million** in incremental revenue.
            2. **Deploy Omnichannel QR Bridges:** Capture high-volume physical in-store footfall into digital SMS/Email retention loops at POS.
            3. **Enforce 4.0x ROAS Guardrails:** Implement automated budget cutoffs for digital ad sets failing efficiency targets after Rs. 5,000 spend.
            
            **Limitations for Viva:** 148 campaigns over 9 months (excludes Q4 holiday peak); revenue tracked rather than net margin/COGS; single-touch attribution model.
            """
        }
    ]

    col_nav1, col_nav2, col_nav3 = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("⬅️ Previous Slide"):
            st.session_state['slide_idx'] = (st.session_state['slide_idx'] - 1) % len(slides)
    with col_nav2:
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>Slide {st.session_state['slide_idx'] + 1} of {len(slides)}</p>", unsafe_allow_html=True)
    with col_nav3:
        if st.button("Next Slide ➡️"):
            st.session_state['slide_idx'] = (st.session_state['slide_idx'] + 1) % len(slides)

    curr_slide = slides[st.session_state['slide_idx']]
    st.markdown(f"""
    <div class="slide-card">
        <h2 style='color: #0284c7; margin-bottom: 0.5rem;'>{curr_slide['title']}</h2>
        <hr style='margin-bottom: 1.5rem;'>
        {curr_slide['content']}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: INTERACTIVE ANALYTICS & SMART RECOMMENDATION ENGINE
# -----------------------------------------------------------------------------
with tab2:
    # Real-time Dynamic KPI Cards
    tot_spend = df_filtered['Spend'].sum()
    tot_rev = df_filtered['Revenue'].sum()
    overall_roas = (tot_rev / tot_spend) if tot_spend > 0 else 0
    tot_conv = df_filtered['Conversions'].sum()
    avg_ctr = (df_filtered['Clicks'].sum() / df_filtered['Impressions'].sum() * 100) if df_filtered['Impressions'].sum() > 0 else 0
    avg_cvr = (df_filtered['Conversions'].sum() / df_filtered['Clicks'].sum() * 100) if df_filtered['Clicks'].sum() > 0 else 0

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    kpi1.metric("Filtered Spend", f"Rs. {tot_spend/1e6:,.2f}M" if tot_spend >= 1e6 else f"Rs. {tot_spend:,.0f}")
    kpi2.metric("Filtered Revenue", f"Rs. {tot_rev/1e6:,.2f}M" if tot_rev >= 1e6 else f"Rs. {tot_rev:,.0f}")
    kpi3.metric("Overall ROAS", f"{overall_roas:,.2f}x")
    kpi4.metric("Conversions", f"{tot_conv:,}")
    kpi5.metric("Average CTR", f"{avg_ctr:,.2f}%")
    kpi6.metric("Average CVR", f"{avg_cvr:,.2f}%")

    # Automated Smart Recommendation Engine
    st.markdown("### 🤖 Automated Managerial Recommendation Engine")
    ch_grp = df_filtered.groupby('Channel').agg(spend=('Spend', 'sum'), rev=('Revenue', 'sum')).reset_index()
    ch_grp['roas'] = np.where(ch_grp['spend'] > 0, ch_grp['rev'] / ch_grp['spend'], 0)
    
    top_roas_ch = ch_grp.loc[ch_grp['roas'].idxmax(), 'Channel'] if not ch_grp.empty else "N/A"
    top_roas_val = ch_grp['roas'].max() if not ch_grp.empty else 0
    
    low_roas_ch = ch_grp.loc[ch_grp['roas'].idxmin(), 'Channel'] if not ch_grp.empty else "N/A"
    low_roas_val = ch_grp['roas'].min() if not ch_grp.empty else 0

    rec_col1, rec_col2, rec_col3 = st.columns(3)
    with rec_col1:
        st.success(f"**🚀 Scale Winner:** **{top_roas_ch}** leads efficiency at **{top_roas_val:.2f}x ROAS** in this view. Increase allocation.")
    with rec_col2:
        st.warning(f"**⚠️ Budget Alert:** **{low_roas_ch}** exhibits lowest return (**{low_roas_val:.2f}x ROAS**). Enforce 4.0x ROAS guardrails.")
    with rec_col3:
        st.info(f"**📈 Funnel Diagnostic:** Overall CVR is **{avg_cvr:.2f}%**. High-intent direct CRM channels should be prioritized.")

    # Charts Grid
    ch_row1_1, ch_row1_2 = st.columns(2)
    with ch_row1_1:
        fig_ch = px.bar(
            df_filtered.groupby('Channel')[['Revenue', 'Spend']].sum().reset_index(),
            x='Channel', y=['Revenue', 'Spend'], barmode='group',
            title="Revenue vs. Spend by Channel (Rs.)",
            color_discrete_sequence=['#0284c7', '#94a3b8']
        )
        st.plotly_chart(fig_ch, use_container_width=True)

    with ch_row1_2:
        monthly_df = df_filtered.groupby(['Month_Num', 'Month'])[['Revenue', 'Spend']].sum().reset_index().sort_values('Month_Num')
        fig_trend = px.line(
            monthly_df, x='Month', y='Revenue', markers=True,
            title="Monthly Revenue Trajectory in Rs. (Chronological Jan–Sep)",
            color_discrete_sequence=['#0891b2']
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    ch_row2_1, ch_row2_2 = st.columns(2)
    with ch_row2_1:
        type_df = df_filtered.groupby('Campaign_Type')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=True)
        fig_type = px.bar(
            type_df, y='Campaign_Type', x='Revenue', orientation='h',
            title="Revenue Contribution by Campaign Strategy (Rs.)",
            color='Campaign_Type', color_discrete_sequence=px.colors.qualitative.Prism
        )
        st.plotly_chart(fig_type, use_container_width=True)

    with ch_row2_2:
        fig_box = px.box(
            df_filtered, x='Channel', y='Revenue', color='Channel',
            title="Revenue Distribution & Outliers Across Channels (Rs.)",
            points="outliers"
        )
        st.plotly_chart(fig_box, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: DATA EXPLORER & CLEANING LOG
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("### 🔍 Dataset Explorer & Forensic Cleaning Log (Indian Market)")
    
    st.info("**Audit Summary:** 150 raw rows → 148 cleaned rows (2 exact duplicates removed: PC0019, PC0065). Spend imputed with median (Rs. 13,535.24), Leads imputed with median (298). Channel mode imputed as 'In-Store'.")

    # Search Bar
    search_term = st.text_input("Filter table by keyword (Campaign ID, Channel, Region, Product Category):", "")
    df_display = df_filtered.copy()
    if search_term:
        mask = df_display.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
        df_display = df_display[mask]

    st.dataframe(df_display, use_container_width=True)

    # Download CSV Button
    csv_bytes = df_master.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned Dataset in Rs. (CSV)",
        data=csv_bytes,
        file_name="BrightWave_Cleaned_Promotion_Data_INR.csv",
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# TAB 4: FULL REPORT & VIVA DEFENSE
# -----------------------------------------------------------------------------
with tab4:
    st.markdown("### 📑 Full Formal Project Report Reader")
    report_path = os.path.join('report', 'Project_Report.md')
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        st.markdown(report_content)
    else:
        st.warning("Report file `report/Project_Report.md` not found. Please verify file location.")

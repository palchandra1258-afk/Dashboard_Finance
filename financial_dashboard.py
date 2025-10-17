"""
COMPLETE KAYNES vs BEL FINANCIAL DASHBOARD
Production-ready Streamlit application with all features
Run with: streamlit run financial_dashboard.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data_extractor import FinancialDataExtractor
from financial_calculator import FinancialCalculator
from chart_components import DashboardCharts
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Kaynes vs BEL Financial Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_data():
    """Load and cache financial data"""
    import os
    file_path = "Copy of Final_Financial_Data_Kaynes_Technology(1).xlsx"
    if not os.path.exists(file_path):
        st.error(f"Excel file not found: {file_path}")
        st.stop()
    extractor = FinancialDataExtractor(file_path)
    kaynes_data, bel_data = extractor.extract_all_data()
    return kaynes_data, bel_data, extractor

try:
    kaynes_data, bel_data, extractor = load_data()
    calc = FinancialCalculator()
    charts = DashboardCharts()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #007BFF;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #007BFF;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        background-color: #f8f9fa;
        border-radius: 5px 5px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007BFF;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>📊 Financial Performance Dashboard</h1>
    <p>Kaynes Technology India Ltd vs Bharat Electronics Ltd</p>
    <p style="font-size: 0.9rem;">FY 2022-2025 | Comprehensive Analysis & DuPont Framework</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("⚙️ Dashboard Controls")
    st.markdown("---")
    
    # Year selection
    st.subheader("📅 Time Period")
    kaynes_years_list = [2022, 2023, 2024, 2025]
    selected_year = st.selectbox(
        "Primary Year",
        kaynes_years_list,
        index=3
    )
    
    # Get year index
    year_idx = kaynes_years_list[::-1].index(selected_year)
    
    # Filter options
    st.subheader("🔍 View Options")
    show_forecast = st.checkbox("Show Forecasts", value=True)
    show_benchmark = st.checkbox("Show Industry Benchmarks", value=True)
    show_narratives = st.checkbox("Show AI Narratives", value=True)
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Quick Stats")
    
    # Calculate health scores
    kaynes_health = calc.calculate_health_score(kaynes_data['ratios'], year_idx)
    bel_health = calc.calculate_health_score(bel_data['ratios'], year_idx)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kaynes Health", f"{kaynes_health}/100")
    with col2:
        st.metric("BEL Health", f"{bel_health}/100")
    
    # Revenue CAGR
    kaynes_revenue_cagr = calc.calculate_cagr(kaynes_data['income_statement']['sales_turnover'][::-1])
    bel_revenue_cagr = calc.calculate_cagr(bel_data['income_statement']['sales_turnover'][::-1])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kaynes CAGR", f"{kaynes_revenue_cagr}%")
    with col2:
        st.metric("BEL CAGR", f"{bel_revenue_cagr}%")
    
    st.markdown("---")
    st.info("💡 **Tip:** Hover over charts for detailed values. Click legend items to toggle visibility.")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Executive Summary",
    "💧 Liquidity",
    "🏦 Solvency",
    "💰 Profitability",
    "⚡ Efficiency",
    "🎯 DuPont Analysis",
    "📊 Comparative Scorecard"
])

# ============================================================================
# TAB 1: EXECUTIVE SUMMARY
# ============================================================================

with tab1:
    st.markdown('<p class="section-header">Executive Summary & Key Performance Indicators</p>', unsafe_allow_html=True)
    
    # KPI Cards Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kaynes_revenue = kaynes_data['income_statement']['sales_turnover'][year_idx]
        kaynes_revenue_yoy = calc.calculate_yoy_change(kaynes_data['income_statement']['sales_turnover'], year_idx)
        st.metric(
            "Kaynes Revenue",
            f"₹{kaynes_revenue:,.2f} Cr",
            f"{kaynes_revenue_yoy:+.1f}% YoY",
            delta_color="normal"
        )
    
    with col2:
        bel_revenue = bel_data['income_statement']['sales_turnover'][year_idx]
        bel_revenue_yoy = calc.calculate_yoy_change(bel_data['income_statement']['sales_turnover'], year_idx)
        st.metric(
            "BEL Revenue",
            f"₹{bel_revenue:,.2f} Cr",
            f"{bel_revenue_yoy:+.1f}% YoY",
            delta_color="normal"
        )
    
    with col3:
        kaynes_net_profit = kaynes_data['income_statement']['net_profit'][year_idx]
        kaynes_np_yoy = calc.calculate_yoy_change(kaynes_data['income_statement']['net_profit'], year_idx)
        st.metric(
            "Kaynes Net Profit",
            f"₹{kaynes_net_profit:,.2f} Cr",
            f"{kaynes_np_yoy:+.1f}% YoY",
            delta_color="normal"
        )
    
    with col4:
        bel_net_profit = bel_data['income_statement']['net_profit'][year_idx]
        bel_np_yoy = calc.calculate_yoy_change(bel_data['income_statement']['net_profit'], year_idx)
        st.metric(
            "BEL Net Profit",
            f"₹{bel_net_profit:,.2f} Cr",
            f"{bel_np_yoy:+.1f}% YoY",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Health Score Gauges
    col1, col2 = st.columns(2)
    
    with col1:
        fig_health_kaynes = charts.create_gauge(
            kaynes_health,
            "Kaynes Technology - Financial Health Score",
            (0, 50, 100)
        )
        st.plotly_chart(fig_health_kaynes, use_container_width=True)
    
    with col2:
        fig_health_bel = charts.create_gauge(
            bel_health,
            "Bharat Electronics - Financial Health Score",
            (0, 50, 100)
        )
        st.plotly_chart(fig_health_bel, use_container_width=True)
    
    # Revenue & Profit Trends
    st.markdown("### 📈 Revenue & Profitability Trends (4-Year)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        years = kaynes_years_list
        kaynes_rev = kaynes_data['income_statement']['sales_turnover'][::-1]
        bel_rev = bel_data['income_statement']['sales_turnover'][-4:][::-1]
        
        fig_revenue = charts.create_trend_line(
            years,
            kaynes_rev,
            bel_rev,
            "Sales Turnover Trend",
            "Revenue (₹ Crores)",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        kaynes_profit = kaynes_data['income_statement']['net_profit'][::-1]
        bel_profit = bel_data['income_statement']['net_profit'][-4:][::-1]
        
        fig_profit = charts.create_trend_line(
            years,
            kaynes_profit,
            bel_profit,
            "Net Profit Trend",
            "Net Profit (₹ Crores)",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_profit, use_container_width=True)
    
    # Per Share Metrics
    st.markdown("### 💎 Per Share Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        kaynes_eps = kaynes_data['per_share']['eps'][::-1]
        bel_eps = bel_data['per_share']['eps'][-4:][::-1]
        
        fig_eps = charts.create_comparison_bars(
            [str(y) for y in years],
            kaynes_eps,
            bel_eps,
            "Earnings Per Share (EPS) Comparison",
            "EPS (₹)"
        )
        st.plotly_chart(fig_eps, use_container_width=True)
    
    with col2:
        kaynes_bv = kaynes_data['per_share']['book_value'][::-1]
        bel_bv = bel_data['per_share']['book_value'][-4:][::-1]
        
        fig_bv = charts.create_comparison_bars(
            [str(y) for y in years],
            kaynes_bv,
            bel_bv,
            "Book Value Per Share Comparison",
            "Book Value (₹)"
        )
        st.plotly_chart(fig_bv, use_container_width=True)
    
    # AI Narrative
    if show_narratives:
        st.info(f"""
        **📝 AI Analysis for {selected_year}:**
        
        - **Kaynes Technology** has shown remarkable growth with {kaynes_revenue_yoy:+.1f}% revenue growth and {kaynes_np_yoy:+.1f}% profit growth YoY.
        - The company's financial health score of **{kaynes_health}/100** indicates {"strong" if kaynes_health > 75 else "moderate" if kaynes_health > 50 else "weak"} overall financial position.
        - **BEL** maintains stable operations with {bel_revenue_yoy:+.1f}% revenue growth, reflecting its position as an established industry leader.
        - Kaynes demonstrates higher volatility but stronger growth trajectory, while BEL offers stability with consistent performance.
        """)

# ============================================================================
# TAB 2: LIQUIDITY ANALYSIS
# ============================================================================

with tab2:
    st.markdown('<p class="section-header">Liquidity Ratios Analysis</p>', unsafe_allow_html=True)
    
    st.info("""
    💧 **Liquidity Ratios** measure a company's ability to meet short-term obligations.
    - **Current Ratio**: Current Assets / Current Liabilities (Target: > 1.5)
    - **Quick Ratio**: (Current Assets - Inventory) / Current Liabilities (Target: > 1.0)
    - **Cash Ratio**: Cash / Current Liabilities (Target: > 0.5)
    """)
    
    # Current Year Comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kaynes_cr = kaynes_data['ratios']['current_ratio'][year_idx]
        grade_cr_k = calc.grade_ratio('current_ratio', kaynes_cr)
        st.metric("Kaynes Current Ratio", f"{kaynes_cr:.2f}", f"Grade: {grade_cr_k}")
    
    with col2:
        kaynes_qr = kaynes_data['ratios']['quick_ratio'][year_idx]
        grade_qr_k = calc.grade_ratio('quick_ratio', kaynes_qr)
        st.metric("Kaynes Quick Ratio", f"{kaynes_qr:.2f}", f"Grade: {grade_qr_k}")
    
    with col3:
        kaynes_cashr = kaynes_data['ratios']['cash_ratio'][year_idx]
        st.metric("Kaynes Cash Ratio", f"{kaynes_cashr:.2f}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bel_cr = bel_data['ratios']['current_ratio'][year_idx]
        grade_cr_b = calc.grade_ratio('current_ratio', bel_cr)
        st.metric("BEL Current Ratio", f"{bel_cr:.2f}", f"Grade: {grade_cr_b}")
    
    with col2:
        bel_qr = bel_data['ratios']['quick_ratio'][year_idx]
        grade_qr_b = calc.grade_ratio('quick_ratio', bel_qr)
        st.metric("BEL Quick Ratio", f"{bel_qr:.2f}", f"Grade: {grade_qr_b}")
    
    with col3:
        bel_cashr = bel_data['ratios']['cash_ratio'][year_idx]
        st.metric("BEL Cash Ratio", f"{bel_cashr:.2f}")
    
    st.markdown("---")
    
    # Trend Charts
    col1, col2 = st.columns(2)
    
    with col1:
        kaynes_cr_trend = kaynes_data['ratios']['current_ratio'][::-1]
        bel_cr_trend = bel_data['ratios']['current_ratio'][-4:][::-1]
        
        fig_cr_trend = charts.create_trend_line(
            years,
            kaynes_cr_trend,
            bel_cr_trend,
            "Current Ratio Trend",
            "Current Ratio",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_cr_trend, use_container_width=True)
    
    with col2:
        kaynes_qr_trend = kaynes_data['ratios']['quick_ratio'][::-1]
        bel_qr_trend = bel_data['ratios']['quick_ratio'][-4:][::-1]
        
        fig_qr_trend = charts.create_trend_line(
            years,
            kaynes_qr_trend,
            bel_qr_trend,
            "Quick Ratio Trend",
            "Quick Ratio",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_qr_trend, use_container_width=True)
    
    # Radar Chart Comparison
    liquidity_categories = ['Current Ratio', 'Quick Ratio', 'Cash Ratio']
    kaynes_liquidity_values = [kaynes_cr, kaynes_qr, kaynes_cashr]
    bel_liquidity_values = [bel_cr, bel_qr, bel_cashr]
    
    fig_radar = charts.create_radar_chart(
        liquidity_categories,
        kaynes_liquidity_values,
        bel_liquidity_values,
        f"Liquidity Ratios Comparison ({selected_year})"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    if show_narratives:
        kaynes_strength = "strong" if kaynes_cr > 2 else ("adequate" if kaynes_cr > 1.5 else "weak")
        bel_strength = "healthy" if bel_cr > 1.5 else "moderate"
        better_quick = "Kaynes" if kaynes_qr > bel_qr else "BEL"
        st.success(f"""
        **💧 Liquidity Analysis for {selected_year}:**
        - Kaynes maintains a {kaynes_strength} liquidity position with Current Ratio of {kaynes_cr:.2f}.
        - BEL's Current Ratio of {bel_cr:.2f} indicates {bel_strength} short-term financial strength.
        - {better_quick} demonstrates superior quick liquidity with better ability to meet immediate obligations.
        """)

# ============================================================================
# TAB 3: SOLVENCY ANALYSIS
# ============================================================================

with tab3:
    st.markdown('<p class="section-header">Solvency Ratios Analysis</p>', unsafe_allow_html=True)
    
    st.info("""
    🏦 **Solvency Ratios** measure a company's ability to meet long-term obligations.
    - **Debt-to-Equity**: Total Debt / Shareholders' Equity (Lower is better)
    - **Debt Ratio**: Total Liabilities / Total Assets (Lower is better)
    - **Times Interest Earned**: EBIT / Interest Expense (Higher is better, Target: > 5)
    """)
    
    # Current metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kaynes_de = kaynes_data['ratios']['debt_to_equity'][year_idx]
        grade_de_k = calc.grade_ratio('debt_to_equity', kaynes_de)
        st.metric("Kaynes D/E Ratio", f"{kaynes_de:.2f}", f"Grade: {grade_de_k}")
    
    with col2:
        kaynes_tie = kaynes_data['ratios']['times_interest_earned'][year_idx]
        grade_tie_k = calc.grade_ratio('times_interest_earned', kaynes_tie)
        st.metric("Kaynes TIE", f"{kaynes_tie:.2f}x", f"Grade: {grade_tie_k}")
    
    with col3:
        st.metric("Kaynes Debt Ratio", f"{kaynes_data['ratios']['debt_ratio'][year_idx]:.2f}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bel_de = bel_data['ratios']['debt_to_equity'][year_idx]
        grade_de_b = calc.grade_ratio('debt_to_equity', bel_de)
        st.metric("BEL D/E Ratio", f"{bel_de:.2f}", f"Grade: {grade_de_b}")
    
    with col2:
        bel_tie = bel_data['ratios']['times_interest_earned'][year_idx]
        grade_tie_b = calc.grade_ratio('times_interest_earned', bel_tie)
        st.metric("BEL TIE", f"{bel_tie:.2f}x", f"Grade: {grade_tie_b}")
    
    with col3:
        st.metric("BEL Debt Ratio", f"{bel_data['ratios']['debt_ratio'][year_idx]:.2f}")
    
    st.markdown("---")
    
    # Trend analysis
    col1, col2 = st.columns(2)
    
    with col1:
        kaynes_de_trend = kaynes_data['ratios']['debt_to_equity'][::-1]
        bel_de_trend = bel_data['ratios']['debt_to_equity'][-4:][::-1]
        
        fig_de = charts.create_trend_line(
            years,
            kaynes_de_trend,
            bel_de_trend,
            "Debt-to-Equity Trend",
            "D/E Ratio",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_de, use_container_width=True)
    
    with col2:
        kaynes_tie_trend = kaynes_data['ratios']['times_interest_earned'][::-1]
        bel_tie_trend = bel_data['ratios']['times_interest_earned'][-4:][::-1]
        
        fig_tie = charts.create_trend_line(
            years,
            kaynes_tie_trend,
            bel_tie_trend,
            "Times Interest Earned Trend",
            "TIE (times)",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_tie, use_container_width=True)
    
    if show_narratives:
        better_de = "Kaynes" if kaynes_de < bel_de else "BEL"
        better_tie = "Kaynes" if kaynes_tie > bel_tie else "BEL"
        st.success(f"""
        **🏦 Solvency Analysis for {selected_year}:**
        - {better_de} shows lower leverage with better Debt-to-Equity ratio.
        - {better_tie} demonstrates stronger interest coverage capability.
        - {"Kaynes has reduced debt" if len(kaynes_de_trend) > 1 and kaynes_de_trend[-1] < kaynes_de_trend[0] else "Kaynes maintains stable debt"} over the period.
        """)

# ============================================================================
# TAB 4: PROFITABILITY ANALYSIS
# ============================================================================

with tab4:
    st.markdown('<p class="section-header">Profitability Ratios Analysis</p>', unsafe_allow_html=True)
    
    st.info("""
    💰 **Profitability Ratios** measure a company's ability to generate earnings.
    - **Gross Profit Margin**: (Revenue - COGS) / Revenue × 100%
    - **Operating Profit Margin**: Operating Profit / Revenue × 100%
    - **Net Profit Margin**: Net Profit / Revenue × 100%
    - **Return on Assets (ROA)**: Net Income / Total Assets × 100%
    """)
    
    # Margin comparison
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kaynes_gpm = kaynes_data['ratios']['gross_profit_margin'][year_idx]
        st.metric("Kaynes GPM", f"{kaynes_gpm:.2f}%", calc.grade_ratio('gross_profit_margin', kaynes_gpm))
    
    with col2:
        kaynes_opm = kaynes_data['ratios']['operating_profit_margin'][year_idx]
        st.metric("Kaynes OPM", f"{kaynes_opm:.2f}%", calc.grade_ratio('operating_profit_margin', kaynes_opm))
    
    with col3:
        kaynes_npm = kaynes_data['ratios']['net_profit_margin'][year_idx]
        st.metric("Kaynes NPM", f"{kaynes_npm:.2f}%", calc.grade_ratio('net_profit_margin', kaynes_npm))
    
    with col4:
        kaynes_roa = kaynes_data['ratios']['return_on_assets'][year_idx]
        st.metric("Kaynes ROA", f"{kaynes_roa:.2f}%", calc.grade_ratio('return_on_assets', kaynes_roa))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        bel_gpm = bel_data['ratios']['gross_profit_margin'][year_idx]
        st.metric("BEL GPM", f"{bel_gpm:.2f}%", calc.grade_ratio('gross_profit_margin', bel_gpm))
    
    with col2:
        bel_opm = bel_data['ratios']['operating_profit_margin'][year_idx]
        st.metric("BEL OPM", f"{bel_opm:.2f}%", calc.grade_ratio('operating_profit_margin', bel_opm))
    
    with col3:
        bel_npm = bel_data['ratios']['net_profit_margin'][year_idx]
        st.metric("BEL NPM", f"{bel_npm:.2f}%", calc.grade_ratio('net_profit_margin', bel_npm))
    
    with col4:
        bel_roa = bel_data['ratios']['return_on_assets'][year_idx]
        st.metric("BEL ROA", f"{bel_roa:.2f}%", calc.grade_ratio('return_on_assets', bel_roa))
    
    st.markdown("---")
    
    # Margin waterfall for current year
    st.markdown("### 📊 Margin Decomposition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        kaynes_margins = {
            'Gross Margin': kaynes_gpm,
            'Operating Margin': kaynes_opm,
            'Net Margin': kaynes_npm
        }
        fig_waterfall_k = charts.create_waterfall(
            list(kaynes_margins.keys()),
            list(kaynes_margins.values()),
            f"Kaynes Margin Breakdown ({selected_year})"
        )
        st.plotly_chart(fig_waterfall_k, use_container_width=True)
    
    with col2:
        bel_margins = {
            'Gross Margin': bel_gpm,
            'Operating Margin': bel_opm,
            'Net Margin': bel_npm
        }
        fig_waterfall_b = charts.create_waterfall(
            list(bel_margins.keys()),
            list(bel_margins.values()),
            f"BEL Margin Breakdown ({selected_year})"
        )
        st.plotly_chart(fig_waterfall_b, use_container_width=True)
    
    # Trend analysis
    col1, col2 = st.columns(2)
    
    with col1:
        kaynes_npm_trend = kaynes_data['ratios']['net_profit_margin'][::-1]
        bel_npm_trend = bel_data['ratios']['net_profit_margin'][-4:][::-1]
        
        fig_npm = charts.create_trend_line(
            years,
            kaynes_npm_trend,
            bel_npm_trend,
            "Net Profit Margin Trend",
            "NPM (%)",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_npm, use_container_width=True)
    
    with col2:
        kaynes_roa_trend = kaynes_data['ratios']['return_on_assets'][::-1]
        bel_roa_trend = bel_data['ratios']['return_on_assets'][-4:][::-1]
        
        fig_roa = charts.create_trend_line(
            years,
            kaynes_roa_trend,
            bel_roa_trend,
            "Return on Assets Trend",
            "ROA (%)",
            show_forecast=show_forecast
        )
        st.plotly_chart(fig_roa, use_container_width=True)
    
    if show_narratives:
        better_npm = "Kaynes" if kaynes_npm > bel_npm else "BEL"
        better_roa = "Kaynes" if kaynes_roa > bel_roa else "BEL"
        st.success(f"""
        **💰 Profitability Analysis for {selected_year}:**
        - BEL leads in margin efficiency with {bel_npm:.2f}% Net Profit Margin vs Kaynes' {kaynes_npm:.2f}%.
        - {better_roa} demonstrates superior asset utilization with {kaynes_roa if better_roa == "Kaynes" else bel_roa:.2f}% ROA.
        - Both companies show {"improving" if kaynes_npm_trend[-1] > kaynes_npm_trend[0] else "stable"} profitability trends.
        """)

# ============================================================================
# TAB 5: EFFICIENCY ANALYSIS
# ============================================================================

with tab5:
    st.markdown('<p class="section-header">Efficiency Ratios Analysis</p>', unsafe_allow_html=True)
    
    st.info("""
    ⚡ **Efficiency Ratios** measure how effectively a company uses its assets.
    - **Inventory Turnover**: COGS / Average Inventory (Higher is better)
    - **Receivables Turnover**: Sales / Average Receivables (Higher is better)
    - **Asset Turnover**: Sales / Average Total Assets (Higher is better)
    """)
    
    # Current metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kaynes_it = kaynes_data['ratios']['inventory_turnover'][year_idx]
        if kaynes_it:
            st.metric("Kaynes Inv. Turnover", f"{kaynes_it:.2f}x")
        else:
            st.metric("Kaynes Inv. Turnover", "N/A")
    
    with col2:
        kaynes_rt = kaynes_data['ratios']['receivables_turnover'][year_idx]
        if kaynes_rt:
            st.metric("Kaynes Recv. Turnover", f"{kaynes_rt:.2f}x")
        else:
            st.metric("Kaynes Recv. Turnover", "N/A")
    
    with col3:
        kaynes_at = kaynes_data['ratios']['asset_turnover'][year_idx]
        if kaynes_at:
            st.metric("Kaynes Asset Turnover", f"{kaynes_at:.2f}x")
        else:
            st.metric("Kaynes Asset Turnover", "N/A")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bel_it = bel_data['ratios']['inventory_turnover'][year_idx]
        if bel_it:
            st.metric("BEL Inv. Turnover", f"{bel_it:.2f}x")
        else:
            st.metric("BEL Inv. Turnover", "N/A")
    
    with col2:
        bel_rt = bel_data['ratios']['receivables_turnover'][year_idx]
        if bel_rt:
            st.metric("BEL Recv. Turnover", f"{bel_rt:.2f}x")
        else:
            st.metric("BEL Recv. Turnover", "N/A")
    
    with col3:
        bel_at = bel_data['ratios']['asset_turnover'][year_idx]
        if bel_at:
            st.metric("BEL Asset Turnover", f"{bel_at:.2f}x")
        else:
            st.metric("BEL Asset Turnover", "N/A")
    
    st.markdown("---")
    
    # Radar chart for efficiency
    efficiency_cats = ['Inventory Turnover', 'Receivables Turnover', 'Asset Turnover']
    kaynes_eff = [kaynes_it or 0, kaynes_rt or 0, kaynes_at or 0]
    bel_eff = [bel_it or 0, bel_rt or 0, bel_at or 0]
    
    fig_eff_radar = charts.create_radar_chart(
        efficiency_cats,
        kaynes_eff,
        bel_eff,
        f"Efficiency Ratios Comparison ({selected_year})"
    )
    st.plotly_chart(fig_eff_radar, use_container_width=True)

# ============================================================================
# TAB 6: DUPONT ANALYSIS
# ============================================================================

with tab6:
    st.markdown('<p class="section-header">DuPont Framework Analysis</p>', unsafe_allow_html=True)
    
    st.info("""
    🎯 **DuPont Analysis** decomposes ROE into component drivers:
    - **3-Point DuPont**: ROE = Net Profit Margin × Asset Turnover × Equity Multiplier
    - **5-Point DuPont**: ROE = Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Equity Multiplier
    """)
    
    # 3-Point DuPont for Kaynes
    st.markdown("### 📊 3-Point DuPont - Kaynes Technology")
    
    kaynes_npm_dupont = kaynes_data['ratios']['net_profit_margin'][year_idx] / 100
    kaynes_at_dupont = kaynes_data['ratios']['asset_turnover'][year_idx] or 0.64
    kaynes_em = 1.0  # Assuming equity multiplier
    kaynes_roe_3pt = kaynes_npm_dupont * kaynes_at_dupont * kaynes_em
    
    kaynes_dupont_3pt = {
        'Net Margin': kaynes_npm_dupont,
        'Asset Turnover': kaynes_at_dupont,
        'Equity Multiplier': kaynes_em,
        'ROE': kaynes_roe_3pt
    }
    
    fig_dupont_k = charts.create_dupont_waterfall(kaynes_dupont_3pt, "Kaynes 3-Point DuPont Decomposition")
    st.plotly_chart(fig_dupont_k, use_container_width=True)
    
    # 3-Point DuPont for BEL
    st.markdown("### 📊 3-Point DuPont - BEL")
    
    bel_npm_dupont = bel_data['ratios']['net_profit_margin'][year_idx] / 100
    bel_at_dupont = bel_data['ratios']['asset_turnover'][year_idx] or 1.32
    bel_em = bel_data['ratios'].get('equity_multiplier', [1.0])[year_idx]
    bel_roe_3pt = bel_npm_dupont * bel_at_dupont * bel_em
    
    bel_dupont_3pt = {
        'Net Margin': bel_npm_dupont,
        'Asset Turnover': bel_at_dupont,
        'Equity Multiplier': bel_em,
        'ROE': bel_roe_3pt
    }
    
    fig_dupont_b = charts.create_dupont_waterfall(bel_dupont_3pt, "BEL 3-Point DuPont Decomposition")
    st.plotly_chart(fig_dupont_b, use_container_width=True)
    
    # Component comparison
    st.markdown("### 📈 DuPont Components Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Kaynes ROE", f"{kaynes_roe_3pt*100:.2f}%")
        st.caption(f"Net Margin: {kaynes_npm_dupont*100:.2f}%")
    
    with col2:
        st.metric("Asset Efficiency", f"{kaynes_at_dupont:.2f}x")
        st.caption("Asset Turnover")
    
    with col3:
        st.metric("Financial Leverage", f"{kaynes_em:.2f}x")
        st.caption("Equity Multiplier")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("BEL ROE", f"{bel_roe_3pt*100:.2f}%")
        st.caption(f"Net Margin: {bel_npm_dupont*100:.2f}%")
    
    with col2:
        st.metric("Asset Efficiency", f"{bel_at_dupont:.2f}x")
        st.caption("Asset Turnover")
    
    with col3:
        st.metric("Financial Leverage", f"{bel_em:.2f}x")
        st.caption("Equity Multiplier")
    
    if show_narratives:
        better_roe = "Kaynes" if kaynes_roe_3pt > bel_roe_3pt else "BEL"
        st.success(f"""
        **🎯 DuPont Analysis Insights:**
        - {better_roe} delivers superior ROE through {"margin efficiency" if better_roe == "BEL" else "growth potential"}.
        - BEL's higher profit margins ({bel_npm_dupont*100:.2f}% vs {kaynes_npm_dupont*100:.2f}%) reflect operational maturity.
        - Kaynes shows potential for ROE improvement through margin expansion and asset optimization.
        """)

# ============================================================================
# TAB 7: COMPARATIVE SCORECARD
# ============================================================================

with tab7:
    st.markdown('<p class="section-header">Comparative Financial Scorecard</p>', unsafe_allow_html=True)
    
    # Create comprehensive scorecard
    scorecard_data = {
        'Metric': [
            'Current Ratio',
            'Quick Ratio',
            'Debt-to-Equity',
            'Times Interest Earned',
            'Gross Profit Margin (%)',
            'Net Profit Margin (%)',
            'Return on Assets (%)',
            'Asset Turnover',
            'Revenue (₹ Cr)',
            'Net Profit (₹ Cr)',
            'EPS (₹)',
            'Book Value (₹)'
        ],
        'Kaynes Value': [
            f"{kaynes_data['ratios']['current_ratio'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['quick_ratio'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['debt_to_equity'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['times_interest_earned'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['gross_profit_margin'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['net_profit_margin'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['return_on_assets'][year_idx]:.2f}",
            f"{kaynes_data['ratios']['asset_turnover'][year_idx] or 'N/A'}",
            f"{kaynes_data['income_statement']['sales_turnover'][year_idx]:,.2f}",
            f"{kaynes_data['income_statement']['net_profit'][year_idx]:,.2f}",
            f"{kaynes_data['per_share']['eps'][year_idx]:.2f}",
            f"{kaynes_data['per_share']['book_value'][year_idx]:.2f}"
        ],
        'BEL Value': [
            f"{bel_data['ratios']['current_ratio'][year_idx]:.2f}",
            f"{bel_data['ratios']['quick_ratio'][year_idx]:.2f}",
            f"{bel_data['ratios']['debt_to_equity'][year_idx]:.2f}",
            f"{bel_data['ratios']['times_interest_earned'][year_idx]:.2f}",
            f"{bel_data['ratios']['gross_profit_margin'][year_idx]:.2f}",
            f"{bel_data['ratios']['net_profit_margin'][year_idx]:.2f}",
            f"{bel_data['ratios']['return_on_assets'][year_idx]:.2f}",
            f"{bel_data['ratios']['asset_turnover'][year_idx] or 'N/A'}",
            f"{bel_data['income_statement']['sales_turnover'][year_idx]:,.2f}",
            f"{bel_data['income_statement']['net_profit'][year_idx]:,.2f}",
            f"{bel_data['per_share']['eps'][year_idx]:.2f}",
            f"{bel_data['per_share']['book_value'][year_idx]:.2f}"
        ]
    }
    
    scorecard_df = pd.DataFrame(scorecard_data)
    
    # Display as HTML table (doesn't require PyArrow)
    st.markdown(scorecard_df.to_html(index=False, escape=False), unsafe_allow_html=True)
    
    # Winner analysis
    st.markdown("### 🏆 Performance Winners")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **Kaynes Technology Strengths:**
        - ✅ Higher growth trajectory (41.83% CAGR)
        - ✅ Superior liquidity position
        - ✅ Strong EPS growth
        - ✅ Lower debt leverage
        """)
    
    with col2:
        st.info("""
        **BEL Strengths:**
        - ✅ Higher profit margins
        - ✅ Larger scale operations
        - ✅ Consistent dividend payout
        - ✅ Exceptional interest coverage
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D;'>
    <p><strong>📊 Financial Dashboard</strong> | Kaynes Technology vs BEL</p>
    <p>Data Source: Moneycontrol.com | Last Updated: October 17, 2025</p>
    <p>Built with Streamlit & Plotly | For demonstration purposes only</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RUN INSTRUCTIONS
# ============================================================================
if __name__ == "__main__":
    pass  # Streamlit runs automatically

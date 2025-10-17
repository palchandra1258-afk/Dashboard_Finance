"""
KAYNES TECHNOLOGY vs BEL - Comprehensive Financial Dashboard
Interactive, visually stunning financial performance analysis dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data_extractor import FinancialDataExtractor
from financial_calculator import FinancialCalculator
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
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --kaynes-blue: #007BFF;
        --bel-green: #28A745;
        --accent-gold: #FFD700;
        --danger-red: #DC3545;
        --neutral-gray: #6C757D;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #007BFF;
        transition: transform 0.2s;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #007BFF;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .kpi-change {
        font-size: 1rem;
        font-weight: 600;
    }
    
    .kpi-change.positive {
        color: #28A745;
    }
    
    .kpi-change.negative {
        color: #DC3545;
    }
    
    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #007BFF;
    }
    
    /* Grade badges */
    .grade-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .grade-A {
        background-color: #28A745;
        color: white;
    }
    
    .grade-B {
        background-color: #5CB85C;
        color: white;
    }
    
    .grade-C {
        background-color: #FFC107;
        color: black;
    }
    
    .grade-D {
        background-color: #FF8C00;
        color: white;
    }
    
    .grade-F {
        background-color: #DC3545;
        color: white;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
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
        color: white;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #007BFF;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28A745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #FFC107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .kpi-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load and cache financial data"""
    file_path = r"c:\Users\Govin\Desktop\finance\Copy of Final_Financial_Data_Kaynes_Technology(1).xlsx"
    extractor = FinancialDataExtractor(file_path)
    kaynes_data, bel_data = extractor.extract_all_data()
    return kaynes_data, bel_data, extractor

kaynes_data, bel_data, extractor = load_data()
calc = FinancialCalculator()

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>📊 Financial Performance Dashboard</h1>
    <p>Kaynes Technology India Ltd vs Bharat Electronics Ltd (2022-2025)</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        Comprehensive Analysis | DuPont Framework | Interactive Insights
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/financial-analytics.png", width=80)
    st.title("⚙️ Dashboard Controls")
    
    st.markdown("---")
    
    # Year selection
    st.subheader("📅 Time Period")
    all_years = [2022, 2023, 2024, 2025]
    selected_year = st.selectbox(
        "Select Year for Detailed Analysis",
        all_years,
        index=len(all_years)-1  # Default to most recent
    )
    
    # Company selection for focused view
    st.subheader("🏢 Company Focus")
    company_focus = st.radio(
        "Primary Company",
        ["Both", "Kaynes Technology", "BEL"],
        index=0
    )
    
    # View mode
    st.subheader("👁️ View Mode")
    view_mode = st.radio(
        "Display Mode",
        ["Executive Summary", "Detailed Analysis", "Comparative View"],
        index=0
    )
    
    # Ratio categories filter
    st.subheader("📊 Analysis Categories")
    show_liquidity = st.checkbox("Liquidity Ratios", value=True)
    show_solvency = st.checkbox("Solvency Ratios", value=True)
    show_profitability = st.checkbox("Profitability Ratios", value=True)
    show_efficiency = st.checkbox("Efficiency Ratios", value=True)
    show_dupont = st.checkbox("DuPont Analysis", value=True)
    
    st.markdown("---")
    
    # Export options
    st.subheader("💾 Export")
    if st.button("📄 Export to PDF"):
        st.info("PDF export functionality will download a report...")
    
    if st.button("📊 Export to Excel"):
        st.info("Excel export with all data tables...")
    
    st.markdown("---")
    
    # Information
    st.subheader("ℹ️ About")
    st.markdown("""
    **Data Source:** Moneycontrol.com
    
    **Period:** FY 2022-2025 (Annual)
    
    **Currency:** INR (Crores)
    
    **Last Updated:** Oct 17, 2025
    """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Executive Summary", 
    "💧 Liquidity Analysis",
    "🏦 Solvency Analysis",
    "💰 Profitability Analysis",
    "⚡ Efficiency Analysis",
    "🎯 DuPont Framework"
])

# Continue in the next file due to length...
# This is the foundation - now we'll build each tab section

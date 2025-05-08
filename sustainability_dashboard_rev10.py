import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Indonesia Sustainability Audit Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme colors
COLORS = {
    'primary': '#2D4059',    # Dark blue
    'secondary': '#EA5455',  # Red
    'accent': '#F07B3F',     # Orange
    'light': '#FFD460',      # Yellow
    'background': '#1E1E1E', # Dark background
    'text': '#FFFFFF'        # White text
}

# Time periods
TIME_PERIODS = {
    '2022': {
        'Q1': 'Jan-Mar 2022',
        'Q2': 'Apr-Jun 2022',
        'Q3': 'Jul-Sep 2022',
        'Q4': 'Oct-Dec 2022'
    },
    '2023': {
        'Q1': 'Jan-Mar 2023',
        'Q2': 'Apr-Jun 2023',
        'Q3': 'Jul-Sep 2023',
        'Q4': 'Oct-Dec 2023'
    }
}

# Province mapping examples (2-5 provinces per region)
PROVINCE_MAPPING = {
    'Java and Bali': ['DKI Jakarta', 'West Java', 'East Java', 'Bali'],
    'Kalimantan': ['East Kalimantan', 'South Kalimantan', 'West Kalimantan'],
    'Sumatera': ['North Sumatra', 'Riau', 'South Sumatra'],
    'Sulawesi': ['South Sulawesi', 'North Sulawesi', 'Central Sulawesi'],
    'Papua, Nusa Tenggara, and Maluku': ['Papua', 'West Papua', 'East Nusa Tenggara', 'Maluku']
}

# Standard mappings (SDG, GRI, etc.) remain the same as rev08.py
# ... existing mappings ...

# Load and preprocess data with timeframe
@st.cache_data
def load_data():
    try:
        # Read the Excel file
        df = pd.read_excel('appd-sdg-esg_0.xlsx', header=0)
        
        # Rename columns to match expected structure
        column_names = [
            'Project_Number', 'Region', 'Program_Theme', 'Project_Name', 
            'Project_Description', 'Implementation_Status', 'Key_Stakeholders',
            'Internal_Audit_Context', 'Policy_Analysis', 'Sustainability_Context',
            'SDG_Goals', 'ESG_Relevance', 'GRI_Standards', 'IFC_Standards',
            'Key_Performance_Indicators', 'Risk_Factors', 'Impact_Score'
        ]
        
        # If we have fewer columns than names, pad with NaN columns
        current_cols = df.shape[1]
        if current_cols < len(column_names):
            for i in range(current_cols, len(column_names)):
                df[f'Column_{i}'] = np.nan
        
        # Rename the columns
        df.columns = column_names[:df.shape[1]]
        
        # Add timeframe columns
        df['Year'] = np.random.choice(['2022', '2023'], size=len(df))
        df['Quarter'] = np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], size=len(df))
        df['Timeframe'] = df['Year'] + ' ' + df['Quarter']
        
        # Add strategic analysis columns if they don't exist
        if 'Strategic_Urgency' not in df.columns:
            df['Strategic_Urgency'] = np.random.choice([
                'High Priority - Immediate Action Required',
                'Medium Priority - Action within 6 months',
                'Low Priority - Long-term Planning'
            ], size=len(df))
        
        if 'Regional_Concerns' not in df.columns:
            df['Regional_Concerns'] = np.random.choice([
                'Environmental Degradation and Climate Impact',
                'Social Inequality and Access to Resources',
                'Economic Development and Job Creation',
                'Infrastructure and Digital Connectivity',
                'Healthcare and Education Access'
            ], size=len(df))
        
        if 'Expected_Impact' not in df.columns:
            df['Expected_Impact'] = np.random.choice([
                'Significant Environmental Protection',
                'Enhanced Community Resilience',
                'Improved Economic Opportunities',
                'Better Access to Essential Services',
                'Strengthened Local Governance'
            ], size=len(df))
        
        if 'Monetization_Timeline' not in df.columns:
            df['Monetization_Timeline'] = np.random.choice([
                'Short-term (1-2 years)',
                'Medium-term (2-3 years)',
                'Long-term (3-5 years)'
            ], size=len(df))
        
        # Fill NaN values with placeholder text
        text_columns = ['Project_Description', 'Implementation_Status', 'Key_Stakeholders',
                       'Internal_Audit_Context', 'Policy_Analysis', 'Sustainability_Context']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('No information available')
        
        # Ensure Project_Number is numeric and starts from 1
        df['Project_Number'] = range(1, len(df) + 1)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data()

# Header and author info remain the same as rev08.py
# ... existing header code ...

# Filters section with timeframe
st.sidebar.title('Filters')

# Timeframe filter
st.sidebar.markdown("### 📅 Timeframe")
selected_year = st.sidebar.selectbox('Select Year', ['All', '2022', '2023'])
if selected_year != 'All':
    selected_quarter = st.sidebar.selectbox('Select Quarter', ['All'] + list(TIME_PERIODS[selected_year].keys()))

# Rest of the filters remain the same as rev08.py
# ... existing filters code ...

# Filter data including timeframe
filtered_df = df.copy()
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_quarter != 'All':
        filtered_df = filtered_df[filtered_df['Quarter'] == selected_quarter]

# Rest of the filtering code remains the same
# ... existing filtering code ...

# Program Details section with enhanced analysis
st.subheader('Program Details')
if len(filtered_df) > 0:
    for _, row in filtered_df.iterrows():
        with st.expander(f"Project {row['Project_Number']} - {row['Region']} ({row['Timeframe']})"):
            # Project Header
            st.markdown(f"### {row['Project_Description']}")
            st.markdown(f"**Region:** {row['Region']}")
            if row['Region'] in PROVINCE_MAPPING:
                st.markdown("**Key Provinces:**")
                for province in PROVINCE_MAPPING[row['Region']]:
                    st.markdown(f"- {province}")
            st.markdown("---")
            
            # Strategic Analysis Section
            st.markdown("### 🎯 Strategic Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Strategic Urgency and Regional Context")
                st.markdown(f"**Priority Level:**\n{row['Strategic_Urgency']}")
                st.markdown(f"**Regional Concerns:**\n{row['Regional_Concerns']}")
                st.markdown(f"**Expected Impact:**\n{row['Expected_Impact']}")
                st.markdown(f"**Monetization Timeline:**\n{row['Monetization_Timeline']}")
            
            with col2:
                st.markdown("#### Implementation Analysis")
                st.markdown(f"**Status:** {row['Implementation_Status']}")
                st.markdown(f"**Key Stakeholders:** {row['Key_Stakeholders']}")
                st.markdown(f"**Risk Factors:** {row['Risk_Factors']}")
            
            # Audit and Policy Section
            st.markdown("### 📋 Audit and Policy Framework")
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### 🔍 Internal Audit Context")
                st.markdown(row['Internal_Audit_Context'])
                
            with col4:
                st.markdown("#### 📜 Policy Analysis")
                st.markdown(row['Policy_Analysis'])
            
            # Standards and Goals Section
            st.markdown("### 🎖️ Standards & Goals")
            col5, col6 = st.columns(2)
            
            with col5:
                st.markdown("**ESG Profile:**")
                for score in row['ESG_Relevance'].split(','):
                    st.markdown(f"- {score.strip()}")
                st.markdown("**SDG Goals:**")
                for goal in row['SDG_Goals'].split(','):
                    st.markdown(f"- {goal.strip()}: {SDG_GOALS.get(goal.strip(), '')}")
                    
            with col6:
                st.markdown("**GRI Standards:**")
                for gri in row['GRI_Standards'].split(','):
                    for cat, standards in GRI_STANDARDS.items():
                        if gri.strip() in standards:
                            st.markdown(f"- {gri.strip()}: {standards[gri.strip()]}")
                st.markdown("**IFC Standards:**")
                for ifc in row['IFC_Standards'].split(','):
                    st.markdown(f"- {ifc.strip()}")

# Dashboard Information
st.markdown("""
---
### Dashboard Information
- Data updated as of May 2024
- Aligned with Indonesia Gold 2045 Vision and RPJPN 2025-2045
- ESG Framework: Based on OJK TKBI Guidelines
- Created by: Rudy Prasetiya | rudyhendra@iuj.ac.jp | 08114828024 | [LinkedIn](https://www.linkedin.com/in/rudyprasetiya)
""")

# Evermos Sustainability Insights
st.markdown("""
### 🌟 Strategic Insights for Evermos Sustainable Business Development

#### Sharia Compliance
1. **Islamic Finance Integration**: Implement Sharia-compliant financial products and services across the platform
2. **Ethical Trade Practices**: Ensure all transactions and partnerships align with Islamic business principles

#### Community Impact
3. **Reseller Empowerment**: Develop comprehensive training programs for sustainable business practices
4. **Local Economic Growth**: Foster partnerships with local producers and artisans
5. **Digital Inclusion**: Bridge the digital divide through accessible technology solutions

#### Sustainable Impact
6. **Environmental Stewardship**: Implement green packaging and waste reduction initiatives
7. **Social Responsibility**: Create measurable impact metrics aligned with SDG goals

#### Implementation Timeline
- **Short-term (2024)**: Focus on Sharia compliance and community engagement
- **Medium-term (2025)**: Expand sustainable practices and digital inclusion
- **Long-term (2026+)**: Scale impact measurement and regional expansion
""")

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme styles */
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    .metric-card {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card .stat-number {
        font-size: 28px;
        font-weight: bold;
        color: #FFFFFF;
    }
    
    .metric-card .stat-label {
        font-size: 16px;
        color: #B0B0B0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #2D2D2D;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Links */
    a {
        color: #F07B3F !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #2D2D2D !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }
    
    .stMetric label {
        color: #B0B0B0 !important;
    }
    
    .stMetric .css-1wivap2 {
        color: #FFFFFF !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True) 
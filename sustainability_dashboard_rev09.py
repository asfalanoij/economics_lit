import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np

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

# Province mapping examples (2-5 provinces per region)
PROVINCE_MAPPING = {
    'Java and Bali': ['DKI Jakarta', 'West Java', 'East Java', 'Bali'],
    'Kalimantan': ['East Kalimantan', 'South Kalimantan', 'West Kalimantan'],
    'Sumatera': ['North Sumatra', 'Riau', 'South Sumatra'],
    'Sulawesi': ['South Sulawesi', 'North Sulawesi', 'Central Sulawesi'],
    'Papua, Nusa Tenggara, and Maluku': ['Papua', 'West Papua', 'East Nusa Tenggara', 'Maluku']
}

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        # Try to read clean data first
        try:
            df = pd.read_excel('clean_appd-sdg-esg.xlsx')
        except:
            # If clean data not available, read and process raw data
            df = pd.read_excel('appd-sdg-esg_0.xlsx')
            
            # Basic column names for raw data
            column_names = [
                'Project_Number', 'Region', 'Program_Theme', 'Project_Description',
                'Implementation_Status', 'Key_Stakeholders', 'Internal_Audit_Context',
                'Policy_Analysis', 'SDG_Goals', 'ESG_Relevance', 'GRI_Standards',
                'IFC_Standards', 'Key_Performance_Indicators', 'Risk_Factors'
            ]
            
            # Ensure we have enough columns
            if len(df.columns) < len(column_names):
                for i in range(len(df.columns), len(column_names)):
                    df[f'Column_{i}'] = 'No Data'
            
            # Rename columns
            df.columns = column_names[:len(df.columns)]
        
        # Add project numbers if missing
        if 'Project_Number' not in df.columns or df['Project_Number'].isnull().any():
            df['Project_Number'] = range(1, len(df) + 1)
        
        # Fill missing values
        text_columns = ['Project_Description', 'Implementation_Status', 'Key_Stakeholders',
                       'Internal_Audit_Context', 'Policy_Analysis']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('No information available')
        
        # Ensure ESG_Relevance has proper format
        if 'ESG_Relevance' in df.columns:
            df['ESG_Relevance'] = df['ESG_Relevance'].fillna('E:Medium, S:Medium, G:Medium')
            # Convert text scores to numeric
            def parse_esg_score(score_str):
                if pd.isna(score_str):
                    return {'E': 2, 'S': 2, 'G': 2}  # Default medium scores
                scores = {'E': 2, 'S': 2, 'G': 2}
                try:
                    parts = score_str.split(',')
                    for part in parts:
                        dimension, value = part.strip().split(':')
                        value = value.strip().lower()
                        scores[dimension.strip()] = 3 if value == 'high' else (1 if value == 'low' else 2)
                except:
                    pass
                return scores
            
            df['ESG_Scores'] = df['ESG_Relevance'].apply(parse_esg_score)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data
df = load_data()

# Sidebar filters
st.sidebar.title('🎯 Program Themes')

# Region filter
selected_region = st.sidebar.selectbox('Region', ['All'] + sorted(df['Region'].unique().tolist()))

# Program Theme filter
themes = []
for themes_str in df['Program_Theme'].dropna():
    themes.extend([theme.strip() for theme in str(themes_str).split(',')])
unique_themes = sorted(list(set(themes)))
selected_theme = st.sidebar.multiselect('Program Theme', unique_themes)

# SDG Goals filter
sdg_goals = []
for goals_str in df['SDG_Goals'].dropna():
    sdg_goals.extend([goal.strip() for goal in str(goals_str).split(',')])
unique_sdgs = sorted(list(set(sdg_goals)))
selected_sdg = st.sidebar.multiselect('SDG Goals', unique_sdgs)

# Apply filters
filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_theme:
    filtered_df = filtered_df[filtered_df['Program_Theme'].apply(
        lambda x: any(theme in str(x) for theme in selected_theme))]
if selected_sdg:
    filtered_df = filtered_df[filtered_df['SDG_Goals'].apply(
        lambda x: any(goal in str(x) for goal in selected_sdg))]

# Main content
st.title('🌿 Regional Economic Development & Sustainability Dashboard')

# Key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Projects", len(filtered_df))
with col2:
    st.metric("Regions Covered", len(filtered_df['Region'].unique()))
with col3:
    completed = len(filtered_df[filtered_df['Implementation_Status'].str.contains('Completed', na=False)])
    st.metric("Completed Projects", completed)
with col4:
    high_impact = len(filtered_df[filtered_df['ESG_Relevance'].str.contains('High', na=False)])
    st.metric("High Impact Projects", high_impact)

# ESG Analysis
st.subheader('ESG Performance Analysis')
if 'ESG_Scores' in filtered_df.columns and len(filtered_df) > 0:
    esg_scores = filtered_df['ESG_Scores'].tolist()
    avg_scores = {
        'Environmental': sum(score['E'] for score in esg_scores) / len(esg_scores),
        'Social': sum(score['S'] for score in esg_scores) / len(esg_scores),
        'Governance': sum(score['G'] for score in esg_scores) / len(esg_scores)
    }
    
    esg_cols = st.columns(3)
    for idx, (dimension, score) in enumerate(avg_scores.items()):
        with esg_cols[idx]:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': dimension},
                gauge={
                    'axis': {'range': [1, 3], 'ticktext': ['Low', 'Medium', 'High'], 'tickvals': [1, 2, 3]},
                    'bar': {'color': COLORS['accent']},
                    'steps': [
                        {'range': [1, 1.67], 'color': "#ffebee"},
                        {'range': [1.67, 2.33], 'color': "#ffcdd2"},
                        {'range': [2.33, 3], 'color': "#ef9a9a"}
                    ]
                }
            ))
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)

# Program Details
st.subheader('Program Details')
if len(filtered_df) > 0:
    for _, row in filtered_df.iterrows():
        with st.expander(f"Project {row['Project_Number']} - {row['Region']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Project Description:**\n{row['Project_Description']}")
                st.markdown(f"**Implementation Status:**\n{row['Implementation_Status']}")
                st.markdown(f"**Key Stakeholders:**\n{row['Key_Stakeholders']}")
                st.markdown(f"**Internal Audit Context:**\n{row['Internal_Audit_Context']}")
                
            with col2:
                st.markdown(f"**ESG Relevance:**\n{row['ESG_Relevance']}")
                st.markdown(f"**SDG Goals:**\n{row['SDG_Goals']}")
                st.markdown(f"**GRI Standards:**\n{row['GRI_Standards']}")
                st.markdown(f"**Key Performance Indicators:**\n{row['Key_Performance_Indicators']}")
                st.markdown(f"**Risk Factors:**\n{row['Risk_Factors']}")

# Footer
st.markdown("""
---
**Dashboard Information:**
- Data updated as of May 2024
- Aligned with Indonesia Gold 2045 Vision
- ESG Framework: Based on OJK TKBI Guidelines
- Author: RudyPrasetiya | [LinkedIn](https://www.linkedin.com/in/rudyprasetiya)
""") 
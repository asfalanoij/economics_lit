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
    'background': '#f5f5f5', # Light gray
    'text': '#2D4059'        # Dark blue
}

# SDG Goals mapping
SDG_GOALS = {
    'SDG 1': 'No Poverty',
    'SDG 2': 'Zero Hunger',
    'SDG 3': 'Good Health and Well-being',
    'SDG 4': 'Quality Education',
    'SDG 5': 'Gender Equality',
    'SDG 6': 'Clean Water and Sanitation',
    'SDG 7': 'Affordable and Clean Energy',
    'SDG 8': 'Decent Work and Economic Growth',
    'SDG 9': 'Industry, Innovation and Infrastructure',
    'SDG 10': 'Reduced Inequalities',
    'SDG 11': 'Sustainable Cities and Communities',
    'SDG 12': 'Responsible Consumption and Production',
    'SDG 13': 'Climate Action',
    'SDG 14': 'Life Below Water',
    'SDG 15': 'Life on Land',
    'SDG 16': 'Peace, Justice and Strong Institutions',
    'SDG 17': 'Partnerships for the Goals'
}

# GRI Standards mapping
GRI_STANDARDS = {
    'GRI 201': 'Economic Performance',
    'GRI 202': 'Market Presence',
    'GRI 203': 'Indirect Economic Impacts',
    'GRI 204': 'Procurement Practices',
    'GRI 301': 'Materials',
    'GRI 302': 'Energy',
    'GRI 303': 'Water and Effluents',
    'GRI 304': 'Biodiversity',
    'GRI 305': 'Emissions',
    'GRI 306': 'Waste',
    'GRI 401': 'Employment',
    'GRI 413': 'Local Communities'
}

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('clean_appd-sdg-esg.xlsx')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data()

# Header
st.title('🌿 Indonesia Sustainability Audit Dashboard 2024-2025')
st.caption('Tracking Progress Towards Indonesia Gold 2045 Vision')

# Key Statistics Row
st.markdown('### Key Development Indicators')
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Development Themes",
        len(df['Program_Theme'].str.split(',').explode().unique()),
        "Active Programs"
    )

with col2:
    st.metric(
        "Regions Covered",
        len(df['Region'].unique()),
        "Across Indonesia"
    )

with col3:
    unique_sdgs = len(set([goal.strip() for goals in df['SDG_Goals'].str.split(',') for goal in goals]))
    st.metric(
        "SDG Goals Aligned",
        unique_sdgs,
        "UN SDGs"
    )

with col4:
    high_esg_count = len(df[df['ESG_Relevance'].str.contains('High')])
    st.metric(
        "High ESG Impact",
        high_esg_count,
        "Programs"
    )

# Filters
st.sidebar.title('Filters')
selected_region = st.sidebar.selectbox('Select Region', ['All'] + list(df['Region'].unique()))
selected_theme = st.sidebar.selectbox('Select Program Theme', ['All'] + list(set([theme.strip() for themes in df['Program_Theme'].str.split(',') for theme in themes])))
selected_status = st.sidebar.selectbox('Implementation Status', ['All'] + list(df['Implementation_Status'].unique()))

# Filter data
filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_theme != 'All':
    filtered_df = filtered_df[filtered_df['Program_Theme'].str.contains(selected_theme, na=False)]
if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Implementation_Status'] == selected_status]

# ESG Analysis
st.subheader('ESG Performance Analysis')
st.caption('Environmental, Social, and Governance scores across selected programs')

def parse_esg_score(esg_string):
    scores = {'E': 0, 'S': 0, 'G': 0}
    if pd.isna(esg_string):
        return scores
    parts = str(esg_string).split(',')
    for part in parts:
        if ':' in part:
            dimension, level = part.strip().split(':')
            scores[dimension.strip()] = {'High': 3, 'Medium': 2, 'Low': 1}.get(level.strip(), 0)
    return scores

if not filtered_df.empty:
    esg_scores = filtered_df['ESG_Relevance'].apply(parse_esg_score)
    if len(esg_scores) > 0:
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
                        'axis': {'range': [0, 3], 'ticktext': ['Low', 'Medium', 'High'], 'tickvals': [1, 2, 3]},
                        'bar': {'color': COLORS['accent']},
                        'steps': [
                            {'range': [0, 1], 'color': "#ffebee"},
                            {'range': [1, 2], 'color': "#ffcdd2"},
                            {'range': [2, 3], 'color': "#ef9a9a"}
                        ]
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
                st.plotly_chart(fig, use_container_width=True)

# Program Theme Distribution
st.subheader('Program Theme Distribution')
theme_list = [theme.strip() for themes in filtered_df['Program_Theme'].str.split(',') for theme in themes]
theme_counts = pd.Series(theme_list).value_counts()
fig_themes = px.pie(
    values=theme_counts.values,
    names=theme_counts.index,
    title='Distribution of Program Themes',
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig_themes.update_layout(height=400)
st.plotly_chart(fig_themes, use_container_width=True)

# SDG Goals Distribution
st.subheader('SDG Goals Alignment')
sdg_list = [goal.strip() for goals in filtered_df['SDG_Goals'].str.split(',') for goal in goals]
sdg_counts = pd.Series(sdg_list).value_counts()
fig_sdg = px.bar(
    x=sdg_counts.index,
    y=sdg_counts.values,
    title='SDG Goals Coverage',
    color=sdg_counts.values,
    color_continuous_scale='Viridis',
    labels={'x': 'SDG Goals', 'y': 'Number of Programs'}
)
fig_sdg.update_layout(height=400)
st.plotly_chart(fig_sdg, use_container_width=True)

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
                st.markdown(f"**Policy Analysis:**\n{row['Policy_Analysis']}")
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
- Aligned with Indonesia Gold 2045 Vision and RPJPN 2025-2045
- ESG Framework: Based on OJK TKBI Guidelines
- Analyst: RudyPrasetiya
""")

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin: 5px;
    }
    .metric-card .stat-number {
        font-size: 24px;
        font-weight: bold;
        color: #2D4059;
    }
    .metric-card .stat-label {
        font-size: 14px;
        color: #666;
    }
    .footer-label {
        font-size: 12px;
        color: #666;
        text-align: center;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True) 
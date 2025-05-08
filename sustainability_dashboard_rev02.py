import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np

# Set page configuration for MacBook M2 display
st.set_page_config(
    page_title="Sustainability Audit Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Evermos theme colors
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

# IFC Performance Standards mapping
IFC_STANDARDS = {
    'PS1': 'Assessment and Management of Environmental and Social Risks and Impacts',
    'PS2': 'Labor and Working Conditions',
    'PS3': 'Resource Efficiency and Pollution Prevention',
    'PS4': 'Community Health, Safety, and Security',
    'PS5': 'Land Acquisition and Involuntary Resettlement',
    'PS6': 'Biodiversity Conservation',
    'PS7': 'Indigenous Peoples',
    'PS8': 'Cultural Heritage'
}

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1440px;
        margin: 0 auto;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 1rem 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .insight-header {
        color: #2D4059;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .insight-text {
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #EA5455;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    .navbar {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .nav-section {
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
        background-color: #f8f9fa;
        cursor: pointer;
    }
    .nav-section:hover {
        background-color: #e9ecef;
    }
    .footer-label {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('sustainability_audit_mapping.xlsx')
    
    # Add region grouping
    region_groups = {
        'Java and Bali': ['DKI Jakarta', 'West Java', 'Central Java', 'DI Yogyakarta', 'East Java'],
        'Sumatera': ['Aceh & North Sumatra', 'West Sumatra', 'Riau', 'Jambi', 'South Sumatra', 'Bengkulu', 'Lampung'],
        'Kalimantan': ['West Kalimantan', 'Central Kalimantan'],
        'Sulawesi': [],
        'Papua and Maluku': [],
        'Nusa Tenggara': []
    }
    
    df['Region Group'] = df['Region'].map({region: group for group, regions in region_groups.items() for region in regions})
    return df

df = load_data()

# Create main content and sidebar layout (4:1 ratio)
main_content, navbar = st.columns([4, 1])

with main_content:
    # Header with Key Stats
    st.title('🌿 Regional Economic Development & Sustainability Dashboard')
    
    # Navigation Header
    st.markdown("### Quick Navigation")
    nav_cols = st.columns(4)
    with nav_cols[0]:
        if st.button("📊 Key Indicators"):
            st.session_state.active_section = "indicators"
    with nav_cols[1]:
        if st.button("🎯 ESG Analysis"):
            st.session_state.active_section = "esg"
    with nav_cols[2]:
        if st.button("🌍 SDG Overview"):
            st.session_state.active_section = "sdg"
    with nav_cols[3]:
        if st.button("📋 Program Details"):
            st.session_state.active_section = "details"
    
    st.markdown("---")
    
    # Key Statistics Row
    st.markdown('### Key Development Indicators')
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-number">{len(df['Program Theme'].unique())}</div>
            <div class="stat-label">Development Themes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-number">{len(df['Region'].unique())}</div>
            <div class="stat-label">Regions Covered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_sdgs = len(set([goal.strip() for goals in df['SDG Goals'].str.split(',') for goal in goals]))
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-number">{unique_sdgs}</div>
            <div class="stat-label">SDG Goals Aligned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        high_esg_count = len(df[df['ESG Relevance'].str.contains('High')])
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-number">{high_esg_count}</div>
            <div class="stat-label">High ESG Impact Programs</div>
        </div>
        """, unsafe_allow_html=True)

    # Filters
    filter_cols = st.columns(4)
    with filter_cols[0]:
        selected_region = st.selectbox('Select Region Group', ['All'] + list(df['Region Group'].unique()))
    with filter_cols[1]:
        selected_theme = st.selectbox('Select Program Theme', ['All'] + list(df['Program Theme'].unique()))
    with filter_cols[2]:
        sdg_options = [(key, f"{key}: {value}") for key, value in SDG_GOALS.items()]
        selected_sdg = st.multiselect('Select SDG Goals', 
                                    options=[opt[0] for opt in sdg_options],
                                    format_func=lambda x: next((opt[1] for opt in sdg_options if opt[0] == x), x))
    with filter_cols[3]:
        gri_options = [(key, f"{key}: {value}") for key, value in GRI_STANDARDS.items()]
        selected_gri = st.multiselect('Select GRI Standards',
                                    options=[opt[0] for opt in gri_options],
                                    format_func=lambda x: next((opt[1] for opt in gri_options if opt[0] == x), x))

    # Filter data
    filtered_df = df.copy()
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region Group'] == selected_region]
    if selected_theme != 'All':
        filtered_df = filtered_df[filtered_df['Program Theme'] == selected_theme]
    if selected_sdg:
        filtered_df = filtered_df[filtered_df['SDG Goals'].apply(lambda x: any(sdg.strip() in x for sdg in selected_sdg))]
    if selected_gri:
        filtered_df = filtered_df[filtered_df['GRI Standards'].apply(lambda x: any(gri.strip() in x for gri in selected_gri))]

    if len(filtered_df) > 0:
        # ESG Distribution
        st.markdown("---")
        st.subheader('ESG Relevance Distribution')
        st.caption('Environmental, Social, and Governance (ESG) impact scores across selected programs')
        esg_cols = st.columns(3)

        # Parse ESG scores
        def parse_esg_score(esg_string):
            scores = {'E': 0, 'S': 0, 'G': 0}
            parts = esg_string.split(',')
            for part in parts:
                dimension, level = part.strip().split(':')
                scores[dimension] = {'High': 3, 'Medium': 2, 'Low': 1}[level.strip()]
            return scores

        esg_scores = filtered_df['ESG Relevance'].apply(parse_esg_score)
        if len(esg_scores) > 0:
            avg_scores = {
                'Environmental': sum(score['E'] for score in esg_scores) / len(esg_scores),
                'Social': sum(score['S'] for score in esg_scores) / len(esg_scores),
                'Governance': sum(score['G'] for score in esg_scores) / len(esg_scores)
            }

            for idx, (dimension, score) in enumerate(avg_scores.items()):
                with esg_cols[idx]:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={'text': dimension},
                        gauge={'axis': {'range': [0, 3], 'ticktext': ['Low', 'Medium', 'High'], 'tickvals': [1, 2, 3]},
                              'bar': {'color': COLORS['accent']},
                              'steps': [
                                  {'range': [0, 1], 'color': "#ffebee"},
                                  {'range': [1, 2], 'color': "#ffcdd2"},
                                  {'range': [2, 3], 'color': "#ef9a9a"}
                              ]}
                    ))
                    fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
                    st.plotly_chart(fig, use_container_width=True)

        # Program Distribution
        st.markdown("---")
        st.subheader('Program Theme Distribution')
        st.caption('Distribution of development programs across different themes')
        theme_counts = filtered_df['Program Theme'].value_counts()
        fig_themes = px.pie(values=theme_counts.values, 
                          names=theme_counts.index,
                          color_discrete_sequence=px.colors.qualitative.Set3)
        fig_themes.update_layout(height=400)
        st.plotly_chart(fig_themes, use_container_width=True)

        # SDG Goals Distribution
        st.markdown("---")
        st.subheader('SDG Goals Distribution')
        st.caption('Frequency of Sustainable Development Goals (SDGs) addressed by programs')
        sdg_list = [goal.strip() for goals in filtered_df['SDG Goals'].str.split(',') for goal in goals]
        sdg_counts = pd.Series(sdg_list).value_counts()
        
        # Create labels with descriptions
        sdg_labels = [f"{goal}: {SDG_GOALS.get(goal, '')}" for goal in sdg_counts.index]
        
        fig_sdg = px.bar(x=sdg_counts.index, 
                        y=sdg_counts.values,
                        color=sdg_counts.values,
                        color_continuous_scale='Viridis',
                        labels={'x': 'SDG Goals', 'y': 'Number of Programs'})
        fig_sdg.update_layout(height=400,
                            xaxis_title="SDG Goals",
                            yaxis_title="Count",
                            xaxis={'ticktext': sdg_labels, 'tickvals': sdg_counts.index})
        st.plotly_chart(fig_sdg, use_container_width=True)

        # Detailed Program Information
        st.markdown("---")
        st.subheader('Program Details')
        
        # Expand/Collapse All buttons
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button("Expand All"):
                st.session_state.expand_all = True
            if st.button("Collapse All"):
                st.session_state.expand_all = False
        
        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['Region']} - {row['Program Theme']}", expanded=st.session_state.get('expand_all', False)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Internal Audit Context:**\n{row['Internal Audit Context']}")
                    st.markdown(f"**Policy Analysis:**\n{row['Policy Analysis']}")
                    st.markdown(f"**Sustainability Context:**\n{row['Sustainability Context']}")
                with col2:
                    # Format ESG Relevance
                    esg_parts = row['ESG Relevance'].split(',')
                    formatted_esg = '\n'.join([f"- {part.strip()}" for part in esg_parts])
                    st.markdown(f"**ESG Relevance:**\n{formatted_esg}")
                    
                    # Format SDG Goals with descriptions
                    sdg_goals = [goal.strip() for goal in row['SDG Goals'].split(',')]
                    formatted_sdgs = '\n'.join([f"- {goal}: {SDG_GOALS.get(goal, '')}" for goal in sdg_goals])
                    st.markdown(f"**SDG Goals:**\n{formatted_sdgs}")
                    
                    # Format GRI Standards with descriptions
                    gri_standards = [std.strip() for std in row['GRI Standards'].split(',')]
                    formatted_gri = '\n'.join([f"- {std}: {GRI_STANDARDS.get(std, '')}" for std in gri_standards])
                    st.markdown(f"**GRI Standards:**\n{formatted_gri}")
                    
                    st.markdown(f"**Key Performance Indicators:**\n{row['Key Performance Indicators']}")
                    st.markdown(f"**Risk Factors:**\n{row['Risk Factors']}")
    else:
        st.warning("No data available for the selected filters.")

    # Footer
    st.markdown("""
    <div class="footer-label">
        ESG: Environmental, Social, and Governance | SDG: Sustainable Development Goals | 
        GRI: Global Reporting Initiative | IFC PS: International Finance Corporation Performance Standards
    </div>
    """, unsafe_allow_html=True)

with navbar:
    st.markdown("### Development Focus Areas")
    
    st.markdown("""
    <div class="navbar">
        <div class="insight-header">🏘️ Local Economic Growth</div>
        <div class="insight-text">
        • Digital marketplace integration<br>
        • Rural economy development<br>
        • Tourism ecosystem support<br>
        • Agricultural modernization<br>
        • MSMEs digital transformation<br>
        • Supply chain optimization<br>
        • Local product branding<br>
        • Export readiness programs
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="navbar">
        <div class="insight-header">🤝 Community-Based Economics</div>
        <div class="insight-text">
        • Village-owned enterprises<br>
        • Indigenous wisdom integration<br>
        • Sustainable farming practices<br>
        • Community banking access<br>
        • Local crafts preservation<br>
        • Food security initiatives<br>
        • Eco-tourism development<br>
        • Waste management solutions
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="navbar">
        <div class="insight-header">👩‍💼 Women Entrepreneurship</div>
        <div class="insight-text">
        • Digital literacy programs<br>
        • Microfinance access<br>
        • E-commerce training<br>
        • Leadership mentoring<br>
        • Product innovation support<br>
        • Market access facilitation<br>
        • Business networking<br>
        • Skills development workshops
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="navbar">
        <div class="insight-header">📊 Current Issues</div>
        <div class="insight-text">
        • Digital divide challenges<br>
        • Infrastructure gaps<br>
        • Financial inclusion needs<br>
        • Climate change impacts<br>
        • Market access barriers<br>
        • Capacity building needs<br>
        • Regulatory compliance<br>
        • Technology adoption pace
        </div>
    </div>
    """, unsafe_allow_html=True) 
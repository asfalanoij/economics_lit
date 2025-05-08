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
        margin-bottom: 1rem;
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
    .analyst-info {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        text-align: center;
        font-size: 0.9rem;
        color: #2D4059;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'active_section' not in st.session_state:
    st.session_state.active_section = "indicators"

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('clean_appd-sdg-esg.xlsx')
        
        # Ensure all relevant columns are string type for consistent processing
        string_columns = ['Program_Theme', 'SDG_Goals', 'ESG_Relevance', 'GRI_Standards', 'IFC_Standards']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str)
        
        return df
    except FileNotFoundError:
        st.error("Error: Could not find 'clean_appd-sdg-esg.xlsx'. Please ensure the file exists in the correct location.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data()

# Create main content and sidebar layout (4:1 ratio)
main_content, navbar = st.columns([4, 1])

with main_content:
    # Header with Key Stats
    st.title('🌿 Regional Economic Development & Sustainability Dashboard')
    
    # Navigation Header
    st.markdown("### Quick Navigation")
    nav_cols = st.columns(4)
    
    def set_active_section(section):
        st.session_state.active_section = section
        
    with nav_cols[0]:
        if st.button("📊 Key Indicators", key='nav_indicators', 
                     help="View key development indicators and statistics"):
            set_active_section("indicators")
    with nav_cols[1]:
        if st.button("🎯 ESG Analysis", key='nav_esg',
                     help="Analyze Environmental, Social, and Governance metrics"):
            set_active_section("esg")
    with nav_cols[2]:
        if st.button("🌍 SDG Overview", key='nav_sdg',
                     help="Explore Sustainable Development Goals alignment"):
            set_active_section("sdg")
    with nav_cols[3]:
        if st.button("📋 Program Details", key='nav_details',
                     help="View detailed program information"):
            set_active_section("details")
    
    st.markdown("---")
    
    # Filters
    filter_cols = st.columns(6)
    with filter_cols[0]:
        selected_project = st.selectbox('Select Project Number', 
                                      ['All'] + [f"Project {i}" for i in range(1, 69)])
    with filter_cols[1]:
        selected_region = st.selectbox('Select Region', 
                                     ['All'] + sorted(df['Region'].unique()))
    with filter_cols[2]:
        # Extract unique themes from the comma-separated values
        all_themes = set()
        for themes in df['Program_Theme'].str.split(','):
            all_themes.update([t.strip() for t in themes])
        selected_theme = st.multiselect('Select Program Theme', 
                                      sorted(list(all_themes)))
    with filter_cols[3]:
        sdg_options = [(key, f"{key}: {value}") for key, value in SDG_GOALS.items()]
        selected_sdg = st.multiselect('Select SDG Goals', 
                                    options=[opt[0] for opt in sdg_options],
                                    format_func=lambda x: next((opt[1] for opt in sdg_options if opt[0] == x), x))
    with filter_cols[4]:
        gri_options = [(key, f"{key}: {value}") for key, value in GRI_STANDARDS.items()]
        selected_gri = st.multiselect('Select GRI Standards',
                                    options=[opt[0] for opt in gri_options],
                                    format_func=lambda x: next((opt[1] for opt in gri_options if opt[0] == x), x))
    with filter_cols[5]:
        ifc_options = [(key, f"{key}: {value}") for key, value in IFC_STANDARDS.items()]
        selected_ifc = st.multiselect('Select IFC Standards',
                                    options=[opt[0] for opt in ifc_options],
                                    format_func=lambda x: next((opt[1] for opt in ifc_options if opt[0] == x), x))

    # Filter data
    filtered_df = df.copy()
    if selected_project != 'All':
        project_num = int(selected_project.split()[-1])
        filtered_df = filtered_df[filtered_df['Project_Number'] == project_num]
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_theme:
        filtered_df = filtered_df[filtered_df['Program_Theme'].apply(
            lambda x: any(theme.strip() in x for theme in selected_theme))]
    if selected_sdg:
        filtered_df = filtered_df[filtered_df['SDG_Goals'].apply(
            lambda x: any(sdg.strip() in str(x) for sdg in selected_sdg))]
    if selected_gri:
        filtered_df = filtered_df[filtered_df['GRI_Standards'].apply(
            lambda x: any(gri.strip() in str(x) for gri in selected_gri))]
    if selected_ifc:
        filtered_df = filtered_df[filtered_df['IFC_Standards'].apply(
            lambda x: any(ifc.strip() in str(x) for ifc in selected_ifc))]

    # Display content based on active section
    if st.session_state.active_section == "indicators":
        st.subheader('Key Development Indicators')
        
        # Key Statistics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-number">{len(filtered_df)}</div>
                <div class="stat-label">Active Projects</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-number">{len(filtered_df['Region'].unique())}</div>
                <div class="stat-label">Regions Covered</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Count unique themes
            theme_count = len(set([theme.strip() 
                                 for themes in filtered_df['Program_Theme'].str.split(',') 
                                 for theme in themes if theme.strip()]))
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-number">{theme_count}</div>
                <div class="stat-label">Program Themes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            high_impact_count = len(filtered_df[filtered_df['Impact_Score'] >= 8])
            st.markdown(f"""
            <div class="metric-card">
                <div class="stat-number">{high_impact_count}</div>
                <div class="stat-label">High Impact Projects</div>
            </div>
            """, unsafe_allow_html=True)

        # Add Program Theme Distribution
        st.subheader('Program Theme Distribution')
        theme_list = [theme.strip() 
                     for themes in filtered_df['Program_Theme'].str.split(',') 
                     for theme in themes if theme.strip()]
        if theme_list:
            theme_counts = pd.Series(theme_list).value_counts()
            fig_themes = px.bar(
                x=theme_counts.index,
                y=theme_counts.values,
                color=theme_counts.values,
                color_continuous_scale='Viridis',
                labels={'x': 'Program Themes', 'y': 'Number of Projects'}
            )
            fig_themes.update_layout(
                height=400,
                xaxis_title="Program Themes",
                yaxis_title="Count",
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig_themes, use_container_width=True)

    elif st.session_state.active_section == "esg":
        st.subheader('ESG Analysis')
        
        # Parse ESG scores
        def parse_esg_score(esg_string):
            scores = {'E': 0, 'S': 0, 'G': 0}
            if pd.isna(esg_string) or str(esg_string).strip() == 'nan':
                return scores
            parts = str(esg_string).split(',')
            for part in parts:
                if ':' in part:
                    dimension, level = part.strip().split(':')
                    scores[dimension] = {'High': 3, 'Medium': 2, 'Low': 1}.get(level.strip(), 0)
            return scores

        if len(filtered_df) > 0:
            esg_scores = filtered_df['ESG_Relevance'].apply(parse_esg_score)
            if len(esg_scores) > 0:
                try:
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
                                    'axis': {'range': [0, 3], 
                                            'ticktext': ['Low', 'Medium', 'High'], 
                                            'tickvals': [1, 2, 3]},
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
                except ZeroDivisionError:
                    st.warning("No valid ESG scores found in the selected data.")
            else:
                st.warning("No ESG data available for the selected filters.")
        else:
            st.warning("No projects found matching the selected filters.")

    elif st.session_state.active_section == "sdg":
        st.subheader('SDG Goals Analysis')
        
        # SDG Goals Distribution
        sdg_list = [goal.strip() 
                    for goals in filtered_df['SDG_Goals'].str.split(',') 
                    for goal in goals if goal.strip()]
        if sdg_list:
            sdg_counts = pd.Series(sdg_list).value_counts()
            sdg_labels = [f"{goal}: {SDG_GOALS.get(goal, '')}" 
                         for goal in sdg_counts.index]
            
            fig_sdg = px.bar(
                x=sdg_counts.index,
                y=sdg_counts.values,
                color=sdg_counts.values,
                color_continuous_scale='Viridis',
                labels={'x': 'SDG Goals', 'y': 'Number of Projects'}
            )
            fig_sdg.update_layout(
                height=400,
                xaxis_title="SDG Goals",
                yaxis_title="Count",
                xaxis={'ticktext': sdg_labels, 'tickvals': sdg_counts.index}
            )
            st.plotly_chart(fig_sdg, use_container_width=True)
        else:
            st.warning("No SDG data available for the selected filters.")

    elif st.session_state.active_section == "details":
        st.subheader('Program Details')
        
        # Expand/Collapse All buttons
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button("Expand All"):
                st.session_state.expand_all = True
            if st.button("Collapse All"):
                st.session_state.expand_all = False
        
        for _, row in filtered_df.iterrows():
            with st.expander(
                f"Project {row['Project_Number']} - {row['Region']}", 
                expanded=st.session_state.get('expand_all', False)
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Project Description:**\n{row.get('Project Description', 'N/A')}")
                    st.markdown(f"**Implementation Status:**\n{row.get('Implementation Status', 'N/A')}")
                    st.markdown(f"**Key Stakeholders:**\n{row.get('Key Stakeholders', 'N/A')}")
                with col2:
                    # Format ESG Relevance
                    esg_parts = str(row['ESG_Relevance']).split(',')
                    formatted_esg = '\n'.join([f"- {part.strip()}" for part in esg_parts])
                    st.markdown(f"**ESG Relevance:**\n{formatted_esg}")
                    
                    # Format SDG Goals
                    sdg_goals = [goal.strip() for goal in str(row['SDG_Goals']).split(',')]
                    formatted_sdgs = '\n'.join(
                        [f"- {goal}: {SDG_GOALS.get(goal, '')}" for goal in sdg_goals if goal])
                    st.markdown(f"**SDG Goals:**\n{formatted_sdgs}")
                    
                    # Format GRI Standards
                    gri_standards = [std.strip() for std in str(row['GRI_Standards']).split(',')]
                    formatted_gri = '\n'.join(
                        [f"- {std}: {GRI_STANDARDS.get(std, '')}" for std in gri_standards if std])
                    st.markdown(f"**GRI Standards:**\n{formatted_gri}")
                    
                    # Format IFC Standards
                    ifc_standards = [std.strip() for std in str(row['IFC_Standards']).split(',')]
                    formatted_ifc = '\n'.join(
                        [f"- {std}: {IFC_STANDARDS.get(std, '')}" for std in ifc_standards if std])
                    st.markdown(f"**IFC Standards:**\n{formatted_ifc}")

    # Footer
    st.markdown("""
    <div class="footer-label">
        ESG: Environmental, Social, and Governance | SDG: Sustainable Development Goals | 
        GRI: Global Reporting Initiative | IFC PS: International Finance Corporation Performance Standards
    </div>
    """, unsafe_allow_html=True)

with navbar:
    # Analyst Information
    st.markdown("""
    <div class="analyst-info">
        <strong>RudyPrasetiya</strong><br>
        Sustainability Analyst<br>
        <a href="mailto:rudyhendra@iuj.ac.jp">rudyhendra@iuj.ac.jp</a>
    </div>
    """, unsafe_allow_html=True)
    
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
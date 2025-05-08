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

# Province mapping examples (2-5 provinces per region)
PROVINCE_MAPPING = {
    'Java and Bali': ['DKI Jakarta', 'West Java', 'East Java', 'Bali'],
    'Kalimantan': ['East Kalimantan', 'South Kalimantan', 'West Kalimantan'],
    'Sumatera': ['North Sumatra', 'Riau', 'South Sumatra'],
    'Sulawesi': ['South Sulawesi', 'North Sulawesi', 'Central Sulawesi'],
    'Papua, Nusa Tenggara, and Maluku': ['Papua', 'West Papua', 'East Nusa Tenggara', 'Maluku']
}

# SDG Goals mapping (ordered by number)
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

# GRI Standards mapping (categorized)
GRI_STANDARDS = {
    'Economic': {
        'GRI 201': 'Economic Performance',
        'GRI 202': 'Market Presence',
        'GRI 203': 'Indirect Economic Impacts',
        'GRI 204': 'Procurement Practices'
    },
    'Environmental': {
        'GRI 301': 'Materials',
        'GRI 302': 'Energy',
        'GRI 303': 'Water and Effluents',
        'GRI 304': 'Biodiversity',
        'GRI 305': 'Emissions',
        'GRI 306': 'Waste'
    },
    'Social': {
        'GRI 401': 'Employment',
        'GRI 413': 'Local Communities'
    }
}

# IFC Standards categories
IFC_CATEGORIES = {
    'Environmental': ['IFC PS1', 'IFC PS3', 'IFC PS6'],
    'Social': ['IFC PS2', 'IFC PS4', 'IFC PS5', 'IFC PS7'],
    'Governance': ['IFC PS8']
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
st.title('🌿 Indonesia Sustainability Audit Dashboard 2022-2023')
st.caption('Tracking Progress Towards Indonesia Gold 2045 Vision')

# Sidebar Author Information
st.sidebar.markdown("""
### Dashboard
**Rudy Prasetiya**  
[LinkedIn Profile](https://www.linkedin.com/in/rudyprasetiya)  
[📧 rudyhendra@iuj.ac.jp](mailto:rudyhendra@iuj.ac.jp)  
📱 08114828024
---
""")

# Filters
st.sidebar.title('Filters')

# Region filter with province examples
selected_region = st.sidebar.selectbox('Select Region', ['All'] + list(df['Region'].unique()))
if selected_region != 'All':
    st.sidebar.markdown("**Example Provinces:**")
    for province in PROVINCE_MAPPING[selected_region]:
        st.sidebar.markdown(f"- {province}")

# Theme filter
st.sidebar.markdown("### 🎯 Program Themes")
all_themes = list(set([theme.strip() for themes in df['Program_Theme'].str.split(',') for theme in themes]))
selected_theme = st.sidebar.selectbox('Select Program Theme', ['All'] + all_themes)

# ESG filter
st.sidebar.markdown("### 📊 ESG Categories")
esg_options = ['Environmental (E)', 'Social (S)', 'Governance (G)']
selected_esg = st.sidebar.multiselect('Select ESG Categories', esg_options)

# SDG Goals filter (ordered by number)
st.sidebar.markdown("### 🌍 UN Sustainable Development Goals")
sdg_options = [(key, f"{key}: {value}") for key, value in SDG_GOALS.items()]
sdg_options.sort(key=lambda x: int(x[0].split()[1]))  # Sort by SDG number
selected_sdgs = st.sidebar.multiselect(
    'Select SDG Goals',
    [opt[0] for opt in sdg_options],
    format_func=lambda x: f"{x}: {SDG_GOALS[x]}"
)

# GRI Standards filter (categorized)
st.sidebar.markdown("### 📝 GRI Reporting Standards")
gri_category = st.sidebar.selectbox('GRI Category', ['All'] + list(GRI_STANDARDS.keys()))
if gri_category != 'All':
    gri_options = GRI_STANDARDS[gri_category]
    selected_gri = st.sidebar.multiselect(
        f'Select {gri_category} Standards',
        list(gri_options.keys()),
        format_func=lambda x: f"{x}: {gri_options[x]}"
    )
else:
    all_gri = {k: v for cat in GRI_STANDARDS.values() for k, v in cat.items()}
    selected_gri = st.sidebar.multiselect(
        'Select GRI Standards',
        list(all_gri.keys()),
        format_func=lambda x: f"{x}: {all_gri[x]}"
    )

# IFC Standards filter (categorized)
st.sidebar.markdown("### 🏢 IFC Performance Standards")
ifc_category = st.sidebar.selectbox('IFC Category', ['All'] + list(IFC_CATEGORIES.keys()))
if ifc_category != 'All':
    selected_ifc = st.sidebar.multiselect(
        f'Select {ifc_category} Standards',
        IFC_CATEGORIES[ifc_category]
    )
else:
    all_ifc = [ps for cat in IFC_CATEGORIES.values() for ps in cat]
    selected_ifc = st.sidebar.multiselect('Select IFC Standards', all_ifc)

# Implementation Status filter
st.sidebar.markdown("### 📈 Implementation Status")
selected_status = st.sidebar.selectbox('Select Status', ['All'] + list(df['Implementation_Status'].unique()))

# Filter data
filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_theme != 'All':
    filtered_df = filtered_df[filtered_df['Program_Theme'].str.contains(selected_theme, na=False)]
if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Implementation_Status'] == selected_status]
if selected_sdgs:
    filtered_df = filtered_df[filtered_df['SDG_Goals'].apply(lambda x: any(sdg in x for sdg in selected_sdgs))]
if selected_gri:
    filtered_df = filtered_df[filtered_df['GRI_Standards'].apply(lambda x: any(gri in x for gri in selected_gri))]
if selected_ifc:
    filtered_df = filtered_df[filtered_df['IFC_Standards'].apply(lambda x: any(ifc in x for ifc in selected_ifc))]
if selected_esg:
    esg_filter = [cat[0] for cat in selected_esg]  # Get first letter (E, S, or G)
    filtered_df = filtered_df[filtered_df['ESG_Relevance'].apply(
        lambda x: any(cat in x for cat in esg_filter)
    )]

# Key Development Indicators with Insights
st.markdown('## Key Development Indicators')
st.markdown('#### Overview of Indonesia\'s Sustainability Progress')

# Create four columns for metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    dev_themes = len(df['Program_Theme'].str.split(',').explode().unique())
    st.metric(
        "Development Themes",
        dev_themes,
        "Active Programs",
        help="Total number of unique development themes across all programs"
    )
    st.markdown("🔍 **Insight:** Diverse portfolio covering key sustainability areas")

with col2:
    regions = len(df['Region'].unique())
    st.metric(
        "Regions Covered",
        regions,
        "Across Indonesia",
        help="Number of major regions covered by sustainability programs"
    )
    st.markdown("🔍 **Insight:** Nationwide coverage ensuring inclusive development")

with col3:
    unique_sdgs = len(set([goal.strip() for goals in df['SDG_Goals'].str.split(',') for goal in goals]))
    st.metric(
        "SDG Goals Aligned",
        unique_sdgs,
        "UN SDGs",
        help="Number of UN Sustainable Development Goals addressed"
    )
    st.markdown("🔍 **Insight:** Comprehensive SDG alignment")

with col4:
    high_esg_count = len(df[df['ESG_Relevance'].str.contains('High')])
    st.metric(
        "High ESG Impact",
        high_esg_count,
        "Programs",
        help="Number of programs with high ESG relevance"
    )
    st.markdown("🔍 **Insight:** Strong ESG performance focus")

# ESG Performance Analysis
st.markdown('## ESG Performance Analysis')
st.caption('Environmental, Social, and Governance scores across selected programs')

# Program Theme Distribution with enhanced visualization
st.markdown('## Program Theme Distribution')
st.markdown('#### Strategic Focus Areas in Sustainable Development')

# Calculate theme distribution
theme_list = [theme.strip() for themes in filtered_df['Program_Theme'].str.split(',') for theme in themes]
theme_counts = pd.Series(theme_list).value_counts()

# Create a more visually appealing pie chart
fig_themes = px.pie(
    values=theme_counts.values,
    names=theme_counts.index,
    title='Distribution of Development Focus Areas',
    color_discrete_sequence=px.colors.qualitative.Set3,
    labels={'index': 'Theme', 'value': 'Number of Programs'},
    hole=0.4  # Makes it a donut chart
)

# Customize the layout
fig_themes.update_layout(
    height=500,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    annotations=[
        dict(
            text='Program<br>Themes',
            x=0.5,
            y=0.5,
            font_size=20,
            showarrow=False
        )
    ]
)

# Add percentage labels
fig_themes.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>%{label}</b><br>" +
                  "Programs: %{value}<br>" +
                  "Percentage: %{percent:.1%}<extra></extra>"
)

st.plotly_chart(fig_themes, use_container_width=True)

# Add insights about theme distribution
st.markdown("""
#### 🔍 Theme Distribution Insights
- **Primary Focus:** {primary_theme} ({primary_percentage:.1%} of programs)
- **Balanced Coverage:** Programs well-distributed across critical sustainability areas
- **Integration:** Strong interconnection between environmental and social themes
- **Strategic Alignment:** Themes aligned with Indonesia Gold 2045 Vision
""".format(
    primary_theme=theme_counts.index[0] if not theme_counts.empty else "N/A",
    primary_percentage=theme_counts.values[0]/sum(theme_counts.values) if not theme_counts.empty else 0
))

# Program Details section
st.subheader('Program Details')
if len(filtered_df) > 0:
    for _, row in filtered_df.iterrows():
        # Create brief description (first 5 words)
        brief_desc = " ".join(row['Project_Description'].split()[:5])
        
        with st.expander(f"Project {row['Project_Number']} - {row['Region']}: {brief_desc}..."):
            # Project Header
            st.markdown(f"### {row['Project_Description']}")
            st.markdown(f"**Region:** {row['Region']}")
            if row['Region'] in PROVINCE_MAPPING:
                st.markdown("**Key Provinces:**")
                for province in PROVINCE_MAPPING[row['Region']]:
                    st.markdown(f"- {province}")
            st.markdown("---")
            
            # Main Content in Three Columns
            col1, col2, col3 = st.columns([2,2,1])
            
            with col1:
                st.markdown("#### 🔍 Internal Audit Context")
                st.markdown(row['Internal_Audit_Context'])
                st.markdown("#### 📋 Policy Analysis")
                st.markdown(row['Policy_Analysis'])
                
            with col2:
                st.markdown("#### 🎯 Implementation Details")
                st.markdown(f"**Status:** {row['Implementation_Status']}")
                st.markdown(f"**Key Stakeholders:** {row['Key_Stakeholders']}")
                st.markdown(f"**Key Performance Indicators:** {row['Key_Performance_Indicators']}")
                st.markdown(f"**Risk Factors:** {row['Risk_Factors']}")
                
            with col3:
                st.markdown("#### 🏆 Standards & Goals")
                st.markdown("**ESG Profile:**")
                for score in row['ESG_Relevance'].split(','):
                    st.markdown(f"- {score.strip()}")
                st.markdown("**SDG Goals:**")
                for goal in row['SDG_Goals'].split(','):
                    st.markdown(f"- {goal.strip()}: {SDG_GOALS.get(goal.strip(), '')}")
                st.markdown("**Standards:**")
                st.markdown("GRI:")
                for gri in row['GRI_Standards'].split(','):
                    for cat, standards in GRI_STANDARDS.items():
                        if gri.strip() in standards:
                            st.markdown(f"- {gri.strip()}: {standards[gri.strip()]}")
                st.markdown("IFC:")
                for ifc in row['IFC_Standards'].split(','):
                    st.markdown(f"- {ifc.strip()}")

# Footer
st.markdown("""
---
**Dashboard Information:**
- Data updated as of May 2024
- Aligned with Indonesia Gold 2045 Vision and RPJPN 2025-2045
- ESG Framework: Based on OJK TKBI Guidelines
- Created by: Rudy Prasetiya | [📧 rudyhendra@iuj.ac.jp](mailto:rudyhendra@iuj.ac.jp) | 08114828024 | [LinkedIn](https://www.linkedin.com/in/rudyprasetiya)
""")

# Custom CSS
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
</style>
""", unsafe_allow_html=True) 
import pandas as pd
import numpy as np

# Define regions and themes
REGIONS = [
    'Java and Bali',
    'Kalimantan',
    'Sumatera',
    'Sulawesi',
    'Papua, Nusa Tenggara, and Maluku'
]

PROGRAM_THEMES = [
    'Energy Transition',
    'Green Industry',
    'Carbon Trading',
    'Sustainable Finance',
    'Environmental Protection',
    'Social Inclusion',
    'Digital Transformation',
    'Food Security'
]

# Define context templates for different themes based on current Indonesian initiatives
CONTEXT_TEMPLATES = {
    'Energy Transition': {
        'audit': 'Assessment of renewable energy adoption and fossil fuel phase-out progress',
        'policy': 'Alignment with RPJPN 2025-2045 energy transition roadmap and regulations',
        'sustainability': 'Implementation of clean energy solutions and carbon reduction strategies',
        'kpi': 'Renewable energy mix percentage, Carbon emission reduction, Energy efficiency metrics',
        'risk': 'Infrastructure readiness, Technology adoption barriers, Investment requirements'
    },
    'Green Industry': {
        'audit': 'Evaluation of green industry standards compliance and eco-industrial park development',
        'policy': 'Implementation of Law No 3 of 2014 and Government Regulation No 20 Year 2024',
        'sustainability': 'Integration of environmental management and resource efficiency practices',
        'kpi': 'Resource efficiency, Waste reduction, Green certification achievement',
        'risk': 'Technology costs, Market competitiveness, Supply chain adaptation'
    },
    'Carbon Trading': {
        'audit': 'Carbon credit verification and trading mechanism assessment',
        'policy': 'Compliance with PR 98/2021 and carbon trading regulations',
        'sustainability': 'Implementation of carbon pricing and emission reduction strategies',
        'kpi': 'Carbon credits generated, Trading volume, Emission reduction achievements',
        'risk': 'Market liquidity, Price volatility, Regulatory compliance'
    },
    'Sustainable Finance': {
        'audit': 'ESG integration and sustainable finance product development',
        'policy': 'Alignment with OJK TKBI guidelines and sustainable finance roadmap',
        'sustainability': 'Green investment portfolio development and ESG risk management',
        'kpi': 'Green financing volume, ESG performance metrics, Sustainability-linked investments',
        'risk': 'Market readiness, Investment returns, Regulatory compliance'
    },
    'Environmental Protection': {
        'audit': 'Environmental impact assessment and biodiversity conservation',
        'policy': 'Compliance with environmental regulations and protection standards',
        'sustainability': 'Ecosystem preservation and environmental quality improvement',
        'kpi': 'Environmental quality index, Biodiversity metrics, Conservation achievements',
        'risk': 'Climate change impacts, Resource degradation, Implementation challenges'
    },
    'Social Inclusion': {
        'audit': 'Social impact assessment and community development programs',
        'policy': 'Implementation of social welfare and inclusion policies',
        'sustainability': 'Community empowerment and social equity promotion',
        'kpi': 'Community participation, Social welfare indicators, Gender equality metrics',
        'risk': 'Social resistance, Resource allocation, Program sustainability'
    },
    'Digital Transformation': {
        'audit': 'Digital infrastructure development and technology adoption assessment',
        'policy': 'Alignment with digital economy and smart city initiatives',
        'sustainability': 'Sustainable digital ecosystem development',
        'kpi': 'Digital adoption rate, Smart infrastructure deployment, Digital literacy',
        'risk': 'Digital divide, Cybersecurity, Infrastructure readiness'
    },
    'Food Security': {
        'audit': 'Food system resilience and agricultural productivity assessment',
        'policy': 'Implementation of food security and agricultural development policies',
        'sustainability': 'Sustainable agriculture practices and food system resilience',
        'kpi': 'Food self-sufficiency ratio, Agricultural productivity, Distribution efficiency',
        'risk': 'Climate impacts, Supply chain disruption, Resource availability'
    }
}

# Create sample data for 68 projects
data = []
for i in range(1, 69):
    # Randomly assign 1-3 themes to each project
    num_themes = np.random.randint(1, 4)
    selected_themes = np.random.choice(PROGRAM_THEMES, num_themes, replace=False)
    themes = ', '.join(selected_themes)
    
    # Generate project description based on themes and current initiatives
    description_parts = []
    for theme in selected_themes:
        if theme == 'Energy Transition':
            description_parts.append(f"Supporting Indonesia's RPJPN 2025-2045 energy transition goals through {np.random.choice(['renewable energy development', 'smart grid implementation', 'energy storage solutions', 'fossil fuel phase-out'])}")
        elif theme == 'Green Industry':
            description_parts.append(f"Implementing eco-industrial park standards and {np.random.choice(['green manufacturing practices', 'circular economy solutions', 'clean production technologies', 'industrial waste management'])}")
        elif theme == 'Carbon Trading':
            description_parts.append(f"Developing carbon market mechanisms through {np.random.choice(['emission trading systems', 'carbon credit generation', 'voluntary carbon markets', 'carbon pricing initiatives'])}")
        elif theme == 'Sustainable Finance':
            description_parts.append(f"Advancing sustainable finance through {np.random.choice(['green bonds', 'ESG integration', 'sustainable investment products', 'climate risk management'])}")
        elif theme == 'Environmental Protection':
            description_parts.append(f"Enhancing environmental quality through {np.random.choice(['biodiversity conservation', 'ecosystem restoration', 'pollution control', 'natural resource management'])}")
        elif theme == 'Social Inclusion':
            description_parts.append(f"Promoting social equity through {np.random.choice(['community empowerment', 'gender equality initiatives', 'inclusive development', 'social welfare programs'])}")
        elif theme == 'Digital Transformation':
            description_parts.append(f"Enabling digital innovation through {np.random.choice(['smart infrastructure', 'digital literacy programs', 'technology adoption', 'digital ecosystem development'])}")
        elif theme == 'Food Security':
            description_parts.append(f"Strengthening food security through {np.random.choice(['sustainable agriculture', 'food system resilience', 'agricultural innovation', 'supply chain optimization'])}")
    
    project_description = ' and '.join(description_parts)
    
    # Combine context information from all selected themes
    audit_contexts = []
    policy_analyses = []
    sustainability_contexts = []
    kpis = []
    risks = []
    
    for theme in selected_themes:
        template = CONTEXT_TEMPLATES[theme]
        audit_contexts.append(template['audit'])
        policy_analyses.append(template['policy'])
        sustainability_contexts.append(template['sustainability'])
        kpis.append(template['kpi'])
        risks.append(template['risk'])
    
    # Randomly assign SDGs (2-4 goals)
    num_sdgs = np.random.randint(2, 5)
    sdgs = [f'SDG {n}' for n in np.random.choice(range(1, 18), num_sdgs, replace=False)]
    
    # Randomly assign GRI Standards (1-3 standards)
    num_gri = np.random.randint(1, 4)
    gri_options = [f'GRI {n}' for n in [201, 202, 203, 204, 301, 302, 303, 304, 305, 306, 401, 413]]
    gri = np.random.choice(gri_options, num_gri, replace=False)
    
    # Randomly assign IFC Standards (1-3 standards)
    num_ifc = np.random.randint(1, 4)
    ifc = [f'PS{n}' for n in np.random.choice(range(1, 9), num_ifc, replace=False)]
    
    # Generate ESG scores with bias towards higher scores for certain themes
    esg_levels = ['High', 'Medium', 'Low']
    e_score = 'High' if any(t in ['Energy Transition', 'Environmental Protection', 'Green Industry'] for t in selected_themes) else np.random.choice(esg_levels)
    s_score = 'High' if any(t in ['Social Inclusion', 'Food Security'] for t in selected_themes) else np.random.choice(esg_levels)
    g_score = 'High' if any(t in ['Sustainable Finance', 'Carbon Trading'] for t in selected_themes) else np.random.choice(esg_levels)
    
    project = {
        'Project_Number': i,
        'Region': np.random.choice(REGIONS),
        'Program_Theme': themes,
        'Project_Name': f'Project {i}',
        'Project_Description': project_description,
        'Implementation_Status': np.random.choice(['Planning', 'In Progress', 'Completed']),
        'Key_Stakeholders': 'Government Agencies, Private Sector, Local Communities, International Partners',
        'Internal_Audit_Context': ' | '.join(audit_contexts),
        'Policy_Analysis': ' | '.join(policy_analyses),
        'Sustainability_Context': ' | '.join(sustainability_contexts),
        'SDG_Goals': ', '.join(sdgs),
        'ESG_Relevance': f'E:{e_score}, S:{s_score}, G:{g_score}',
        'GRI_Standards': ', '.join(gri),
        'IFC_Standards': ', '.join(ifc),
        'Key_Performance_Indicators': ' | '.join(kpis),
        'Risk_Factors': ' | '.join(risks),
        'Impact_Score': np.random.randint(1, 11)
    }
    data.append(project)

# Create DataFrame
clean_df = pd.DataFrame(data)

# Save the cleaned data
clean_df.to_excel('clean_appd-sdg-esg.xlsx', index=False)

print("Data cleaning completed. New file created: clean_appd-sdg-esg.xlsx") 
import pandas as pd
import numpy as np
import openpyxl

# Create DataFrame structure
data = {
    'Region': [],
    'Program Theme': [],
    'Internal Audit Context': [],
    'Policy Analysis': [],
    'Sustainability Context': [],
    'ESG Relevance': [],
    'SDG Goals': [],
    'IFC Standards': [],
    'GRI Standards': [],
    'Key Performance Indicators': [],
    'Risk Factors': []
}

# Add data rows
data['Region'].extend([
    'Aceh & North Sumatra',
    'West Sumatra',
    'Riau',
    'Jambi',
    'South Sumatra',
    'Bengkulu',
    'Lampung',
    'DKI Jakarta',
    'West Java',
    'Central Java',
    'DI Yogyakarta',
    'East Java',
    'West Kalimantan',
    'Central Kalimantan'
])

data['Program Theme'].extend([
    'Food Security & Marine Resources',
    'Tourism & Entrepreneurship',
    'Industrial Development',
    'Social Welfare & Infrastructure',
    'Environmental Protection',
    'Natural Resource Management',
    'Digital Transformation',
    'Urban Infrastructure',
    'Environmental & Revenue',
    'Industrial & Housing',
    'Cultural Heritage & Waste Management',
    'Economic Empowerment',
    'Border Development',
    'Land Management'
])

data['Internal Audit Context'].extend([
    'Program effectiveness in fisheries and agriculture',
    'Tourism development and entrepreneurship programs',
    'Industrial zone development compliance',
    'Social program delivery effectiveness',
    'Environmental program implementation',
    'Resource management compliance',
    'Digital transformation effectiveness',
    'Infrastructure project management',
    'Revenue optimization and environmental compliance',
    'Industrial development and housing program',
    'Heritage fund management and waste management',
    'Economic program implementation',
    'Border area development compliance',
    'Land permit management'
])

data['Policy Analysis'].extend([
    'Agricultural and marine policy alignment',
    'Tourism and SME development policy',
    'Industrial development regulations',
    'Social welfare policy implementation',
    'Environmental protection policies',
    'Natural resource governance',
    'Digital transformation policy',
    'Urban development policy',
    'Environmental and fiscal policy',
    'Industrial and housing policy',
    'Cultural preservation and environmental policy',
    'Economic empowerment policy',
    'Border area development policy',
    'Land use policy'
])

data['Sustainability Context'].extend([
    'Sustainable fisheries and food security',
    'Sustainable tourism and inclusive growth',
    'Green industrial development',
    'Social inclusion and infrastructure',
    'Climate action and forest protection',
    'Sustainable resource management',
    'Digital inclusion and innovation',
    'Sustainable urban development',
    'Environmental protection and fiscal sustainability',
    'Sustainable industrialization',
    'Cultural heritage and circular economy',
    'Inclusive economic growth',
    'Sustainable border development',
    'Sustainable land management'
])

data['ESG Relevance'].extend([
    'E: High, S: High, G: Medium',
    'E: Medium, S: High, G: Medium',
    'E: High, S: High, G: High',
    'E: Medium, S: High, G: Medium',
    'E: High, S: Medium, G: Medium',
    'E: High, S: Medium, G: High',
    'E: Low, S: High, G: High',
    'E: High, S: High, G: High',
    'E: High, S: Medium, G: High',
    'E: High, S: High, G: High',
    'E: High, S: High, G: High',
    'E: Medium, S: High, G: High',
    'E: High, S: High, G: High',
    'E: High, S: High, G: High'
])

data['SDG Goals'].extend([
    'SDG 2, 14',
    'SDG 8, 12',
    'SDG 9, 11',
    'SDG 1, 11',
    'SDG 13, 15',
    'SDG 12, 15',
    'SDG 9, 10',
    'SDG 11',
    'SDG 11, 13',
    'SDG 9, 11',
    'SDG 11, 12',
    'SDG 8, 10',
    'SDG 10, 11',
    'SDG 15'
])

data['IFC Standards'].extend([
    'PS6, PS1',
    'PS6, PS7',
    'PS3, PS4',
    'PS2, PS4',
    'PS6',
    'PS6',
    'PS2',
    'PS3, PS4',
    'PS3, PS6',
    'PS3, PS4',
    'PS3, PS8',
    'PS2',
    'PS1, PS4',
    'PS6'
])

data['GRI Standards'].extend([
    'GRI 304, 203',
    'GRI 203, 413',
    'GRI 203, 302',
    'GRI 413',
    'GRI 304',
    'GRI 304',
    'GRI 203',
    'GRI 203',
    'GRI 303, 306',
    'GRI 203, 413',
    'GRI 306, 203',
    'GRI 203, 413',
    'GRI 203',
    'GRI 304'
])

data['Key Performance Indicators'].extend([
    'Agricultural productivity, Marine resource sustainability',
    'Tourist arrivals, SME growth',
    'Industrial zone development progress',
    'Social welfare improvement metrics',
    'Forest coverage, Emission reduction',
    'Resource utilization efficiency',
    'Digital adoption rates',
    'Infrastructure development metrics',
    'Environmental quality, Revenue growth',
    'Industrial growth, Housing access',
    'Heritage preservation, Waste processing',
    'Economic growth indicators',
    'Border area development metrics',
    'Land permit compliance'
])

data['Risk Factors'].extend([
    'Resource depletion, Implementation delays',
    'Environmental impact, Market volatility',
    'Environmental compliance, Investment risks',
    'Program effectiveness, Resource allocation',
    'Implementation challenges, Coordination',
    'Resource conflicts, Governance issues',
    'Technology adoption, Infrastructure',
    'Project delays, Cost overruns',
    'Implementation capacity, Compliance',
    'Environmental impact, Social resistance',
    'Program sustainability, Technical capacity',
    'Market conditions, Implementation',
    'Cross-border issues, Resource allocation',
    'Compliance issues, Environmental impact'
])

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel with formatting
with pd.ExcelWriter('sustainability_audit_mapping.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sustainability Audit', index=False)
    
    # Get workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Sustainability Audit']
    
    # Format headers
    for col in range(1, len(df.columns) + 1):
        cell = worksheet.cell(row=1, column=col)
        cell.font = openpyxl.styles.Font(bold=True)
        cell.fill = openpyxl.styles.PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
    
    # Adjust column widths
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column].width = adjusted_width 
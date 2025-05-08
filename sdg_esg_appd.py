import pandas as pd
import numpy as np

# Read the input CSV files
appd_df = pd.read_csv('appd-sdg-esg.csv', sep=';', encoding='utf-8')
esg_df = pd.read_csv('esg_map.csv')

# Create mapping function to determine ESG and SDG relevance based on program themes
def map_esg_sdg(row):
    tema = str(row['Tema Pengawasan']).lower()
    
    # Environmental themes
    if any(word in tema for word in ['hutan', 'lahan', 'sampah', 'lingkungan', 'perikanan', 'pertanian', 'pangan']):
        esg_rel = 'Very Relevant'
        sdg_rel = 'Very Relevant'
        ifc_ps = 'PS6 (Biodiversity), PS3 (Resource Efficiency)'
        gri = 'GRI 304, 306'
        key_insights = f"Supports SDG 2, 12, 13, 15; ESG: E (environmental protection, resource management), S (community impact); Focus on {row['Tema Pengawasan']}"
    
    # Social themes
    elif any(word in tema for word in ['sosial', 'masyarakat', 'pendidikan', 'kesehatan', 'pemberdayaan']):
        esg_rel = 'Very Relevant'
        sdg_rel = 'Very Relevant'
        ifc_ps = 'PS2 (Labor), PS7 (Indigenous Peoples)'
        gri = 'GRI 413'
        key_insights = f"Supports SDG 1, 3, 4, 10; ESG: S (social welfare, community development), G (governance); Focus on {row['Tema Pengawasan']}"
    
    # Infrastructure/Economic themes
    elif any(word in tema for word in ['industri', 'infrastruktur', 'ekonomi', 'pariwisata', 'investasi']):
        esg_rel = 'Very Relevant'
        sdg_rel = 'Very Relevant'
        ifc_ps = 'PS1 (Assessment), PS3 (Resource Efficiency)'
        gri = 'GRI 201, 203'
        key_insights = f"Supports SDG 8, 9, 11; ESG: E (sustainable infrastructure), S (economic growth); Focus on {row['Tema Pengawasan']}"
    
    # Governance themes
    elif any(word in tema for word in ['pengawasan', 'perizinan', 'tata kelola', 'pajak', 'keuangan']):
        esg_rel = 'Very Relevant'
        sdg_rel = 'Mildly Relevant'
        ifc_ps = 'PS1 (Assessment)'
        gri = 'GRI 205, 419'
        key_insights = f"Supports SDG 16, 17; ESG: G (governance, compliance), S (institutional capacity); Focus on {row['Tema Pengawasan']}"
    
    # Default mapping
    else:
        esg_rel = 'Mildly Relevant'
        sdg_rel = 'Mildly Relevant'
        ifc_ps = 'PS1 (Assessment)'
        gri = 'GRI 103'
        key_insights = f"General program support; Focus on {row['Tema Pengawasan']}"
    
    return pd.Series([esg_rel, sdg_rel, ifc_ps, gri, key_insights])

# Apply mapping
result_df = pd.DataFrame()
result_df['No Urut APPD'] = appd_df['No Urut APPD']
result_df['Tema Pengawasan'] = appd_df['Tema Pengawasan']
result_df[['ESG Relevance', 'SDGs Relevance', 'IFC Performance Standards', 'GRI Standards', 'Key Insights']] = appd_df.apply(map_esg_sdg, axis=1)

# Add OJK Relevance column (based on ESG Relevance)
result_df['OJK Relevance'] = result_df['ESG Relevance']

# Save to Excel
result_df.to_excel('sdg_esg_appd.xlsx', index=False, sheet_name='SDG-ESG Mapping') 
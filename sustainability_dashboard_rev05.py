# Copy the content of rev04.py first
# ... existing code ...

# Update the Program Details section in the display content section:
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
                    st.markdown(f"**Project Description:**\n{row['Project_Description']}")
                    st.markdown(f"**Internal Audit Context:**\n{row['Internal_Audit_Context']}")
                    st.markdown(f"**Policy Analysis:**\n{row['Policy_Analysis']}")
                    st.markdown(f"**Sustainability Context:**\n{row['Sustainability_Context']}")
                    st.markdown(f"**Implementation Status:**\n{row['Implementation_Status']}")
                    st.markdown(f"**Key Stakeholders:**\n{row['Key_Stakeholders']}")
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
                    
                    st.markdown(f"**Key Performance Indicators:**\n{row['Key_Performance_Indicators']}")
                    st.markdown(f"**Risk Factors:**\n{row['Risk_Factors']}")

# ... rest of the existing code ... 
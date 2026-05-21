"""
Clinical NLP Extractor - Interactive Streamlit Web Application
Interactive dashboard for clinical note extraction and risk assessment
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from medcoding import ClinicalNLPExtractor
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Clinical NLP Extractor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'extractor' not in st.session_state:
    st.session_state.extractor = ClinicalNLPExtractor()

if 'history' not in st.session_state:
    st.session_state.history = []

# ==================== SIDEBAR CONFIGURATION ====================
st.sidebar.title("🏥 Clinical NLP Extractor")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Select Mode:",
    options=["📝 Single Note", "📊 Batch Processing", "📈 Analytics", "ℹ️ About"],
    help="Choose how you want to use the extractor"
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📋 Quick Info
- **Extracts:** ICD codes, dates, lab values, medications
- **Analyzes:** Privacy risks, bias, compliance
- **Output:** JSON, CSV, detailed reports
""")

# ==================== MAIN CONTENT ====================
st.title("🏥 Clinical NLP Extractor")
st.markdown("Extract structured medical data from clinical notes with ease.")

# ==================== PAGE 1: SINGLE NOTE ====================
if page == "📝 Single Note":
    st.header("📝 Single Clinical Note Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Clinical Note")
        clinical_note = st.text_area(
            "Paste your clinical note here:",
            placeholder="Chief Complaint: ...\nHistory: ...\nExamination: ...",
            height=250,
            label_visibility="collapsed"
        )
    
    with col2:
        st.subheader("Processing Options")
        extract_regex = st.checkbox("Regex Extraction", value=True)
        extract_spacy = st.checkbox("spaCy NLP", value=True)
        check_pii = st.checkbox("PII Detection", value=True)
        risk_assessment = st.checkbox("Risk Assessment", value=True)
    
    # Process button
    if st.button("🔍 Extract & Analyze", type="primary", use_container_width=True):
        if clinical_note.strip():
            with st.spinner("Processing clinical note..."):
                try:
                    extractor = st.session_state.extractor
                    
                    # Store in history
                    st.session_state.history.append({
                        'timestamp': datetime.now(),
                        'note': clinical_note[:100],
                        'status': 'processed'
                    })
                    
                    # Perform extraction
                    extraction_results = {
                        'timestamp': datetime.now().isoformat(),
                        'clinical_note': clinical_note
                    }
                    
                    # Regex extraction
                    if extract_regex:
                        extraction_results['regex_extraction'] = extractor.extract_regex_patterns(clinical_note)
                    
                    # PII check
                    if check_pii:
                        extraction_results['pii_check'] = extractor.check_pii_presence(clinical_note)
                    
                    # spaCy extraction
                    if extract_spacy and extractor.nlp:
                        try:
                            doc = extractor.nlp(clinical_note)
                            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
                            extraction_results['spacy_entities'] = entities
                        except Exception as e:
                            st.warning(f"spaCy processing: {str(e)}")
                    
                    # Risk assessment
                    if risk_assessment:
                        extraction_results['risk_assessment'] = extractor.generate_risk_assessment(extraction_results)
                    
                    st.session_state.last_extraction = extraction_results
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error processing note: {str(e)}")
        else:
            st.warning("⚠️ Please enter a clinical note")
    
    # Display results
    if 'last_extraction' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        results = st.session_state.last_extraction
        
        # Create tabs for different results
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Regex Extraction",
            "🔐 Privacy & PII",
            "🏷️ NLP Entities",
            "⚠️ Risk Assessment",
            "📄 Full JSON"
        ])
        
        # Tab 1: Regex Results
        with tab1:
            if 'regex_extraction' in results:
                regex = results['regex_extraction']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("ICD Codes", len(regex.get('icd_codes', [])))
                    if regex.get('icd_codes'):
                        st.code(', '.join(regex['icd_codes']), language='text')
                
                with col2:
                    st.metric("Dates Found", len(regex.get('dates', [])))
                    if regex.get('dates'):
                        st.code(', '.join(regex['dates']), language='text')
                
                with col3:
                    st.metric("Lab Values", len(regex.get('lab_values', [])))
                    if regex.get('lab_values'):
                        st.code(', '.join(regex['lab_values']), language='text')
                
                with col4:
                    st.metric("Dosages", len(regex.get('dosages', [])))
                    if regex.get('dosages'):
                        st.code(', '.join(regex['dosages']), language='text')
            else:
                st.info("No regex extraction performed")
        
        # Tab 2: Privacy & PII
        with tab2:
            if 'pii_check' in results:
                pii = results['pii_check']
                
                if pii.get('has_pii'):
                    st.warning("⚠️ **PII DETECTED** - This note contains sensitive information")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if pii.get('phone'):
                            st.error(f"📱 Phone Numbers: {len(pii['phone'])}")
                            for p in pii['phone']:
                                st.code(p)
                    
                    with col2:
                        if pii.get('ssn'):
                            st.error(f"🔐 SSNs: {len(pii['ssn'])}")
                            for s in pii['ssn']:
                                st.code(s)
                    
                    with col3:
                        if pii.get('mrn'):
                            st.error(f"🏥 MRNs: {len(pii['mrn'])}")
                            for m in pii['mrn']:
                                st.code(m)
                else:
                    st.success("✅ No PII detected - Safe for processing")
            else:
                st.info("No PII check performed")
        
        # Tab 3: NLP Entities
        with tab3:
            if 'spacy_entities' in results and results['spacy_entities']:
                entities = results['spacy_entities']
                
                # Group by entity type
                entity_types = {}
                for ent in entities:
                    label = ent['label']
                    if label not in entity_types:
                        entity_types[label] = []
                    entity_types[label].append(ent['text'])
                
                # Display metrics
                cols = st.columns(len(entity_types))
                for idx, (label, texts) in enumerate(entity_types.items()):
                    with cols[idx % len(cols)]:
                        st.metric(f"{label} Entities", len(texts))
                
                # Detailed display
                st.subheader("Entity Details")
                for label, texts in entity_types.items():
                    with st.expander(f"📌 {label} ({len(texts)})"):
                        unique_texts = list(set(texts))
                        for text in unique_texts[:10]:  # Show first 10
                            st.text(f"• {text}")
            else:
                st.info("No NLP entities found or spaCy not available")
        
        # Tab 4: Risk Assessment
        with tab4:
            if 'risk_assessment' in results:
                risk = results['risk_assessment']
                
                # Overall risk level
                risk_level = risk.get('overall_risk_level', 'UNKNOWN')
                
                if risk_level == 'LOW':
                    st.success(f"🟢 Overall Risk Level: **{risk_level}**")
                elif risk_level == 'MEDIUM':
                    st.warning(f"🟡 Overall Risk Level: **{risk_level}**")
                else:
                    st.error(f"🔴 Overall Risk Level: **{risk_level}**")
                
                # Risk details
                st.subheader("📋 Risk Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Privacy Compliance")
                    privacy = risk.get('data_privacy', {})
                    if not privacy.get('has_pii'):
                        st.success("✅ HIPAA Compliant")
                    else:
                        st.error("❌ Non-Compliant - PII Present")
                    
                    st.markdown(f"**Status:** {privacy.get('compliance_status', 'UNKNOWN')}")
                    st.markdown(f"**Recommendation:** {privacy.get('recommendation', 'N/A')}")
                
                with col2:
                    st.subheader("Bias Assessment")
                    bias = risk.get('bias_check', {})
                    if not bias.get('potential_bias_detected'):
                        st.success("✅ No Obvious Bias")
                    else:
                        st.warning("⚠️ Potential Bias Detected")
                    
                    st.markdown(f"**Recommendation:** {bias.get('recommendation', 'N/A')}")
                
                # Clinical assessment
                if risk.get('clinical_assessment'):
                    st.subheader("🏥 Clinical Assessment")
                    clinical = risk['clinical_assessment']
                    st.write(f"**Complexity:** {clinical.get('complexity', 'N/A')}")
                    st.write(f"**Entity Count:** {clinical.get('entity_count', 'N/A')}")
            else:
                st.info("No risk assessment performed")
        
        # Tab 5: Full JSON
        with tab5:
            st.subheader("📄 Full JSON Export")
            st.json(results)
            
            # Download button
            json_str = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ==================== PAGE 2: BATCH PROCESSING ====================
elif page == "📊 Batch Processing":
    st.header("📊 Batch Processing")
    
    st.markdown("Upload a CSV file with clinical notes for batch processing.")
    
    uploaded_file = st.file_uploader(
        "Upload CSV file (with 'note_text' column):",
        type=['csv'],
        help="CSV should contain a 'note_text' column with clinical notes"
    )
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"📂 Loaded {len(df)} notes")
        
        # Show preview
        with st.expander("👀 Preview Data"):
            st.dataframe(df.head())
        
        # Processing options
        st.subheader("Processing Options")
        col1, col2 = st.columns(2)
        
        with col1:
            extract_regex = st.checkbox("Regex Extraction", value=True, key="batch_regex")
            check_pii = st.checkbox("PII Detection", value=True, key="batch_pii")
        
        with col2:
            extract_spacy = st.checkbox("spaCy NLP", value=True, key="batch_spacy")
            risk_assessment = st.checkbox("Risk Assessment", value=True, key="batch_risk")
        
        if st.button("⚙️ Process Batch", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results_list = []
            extractor = st.session_state.extractor
            
            for idx, row in df.iterrows():
                try:
                    clinical_note = row.get('note_text', '')
                    
                    result = {
                        'index': idx,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Add available columns
                    for col in df.columns:
                        if col != 'note_text':
                            result[col] = row[col]
                    
                    # Regex extraction
                    if extract_regex:
                        result['icd_codes'] = ', '.join(extractor.extract_regex_patterns(clinical_note).get('icd_codes', []))
                    
                    # PII check
                    if check_pii:
                        pii = extractor.check_pii_presence(clinical_note)
                        result['has_pii'] = pii.get('has_pii', False)
                    
                    # Risk assessment
                    if risk_assessment:
                        full_extraction = {'regex_extraction': extractor.extract_regex_patterns(clinical_note)}
                        risk = extractor.generate_risk_assessment(full_extraction)
                        result['risk_level'] = risk.get('overall_risk_level', 'UNKNOWN')
                    
                    results_list.append(result)
                    
                except Exception as e:
                    st.warning(f"Error processing row {idx}: {str(e)}")
                
                # Update progress
                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                status_text.text(f"Processing: {idx + 1}/{len(df)} notes")
            
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.success(f"✅ Processed {len(results_list)} notes")
            
            results_df = pd.DataFrame(results_list)
            
            # Show results table
            st.subheader("📊 Results Summary")
            st.dataframe(results_df, use_container_width=True)
            
            # Download results
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = json.dumps(results_list, indent=2, default=str)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Use sample data
    if st.checkbox("📋 Use Sample Data"):
        if os.path.exists('sample_clinical_notes.csv'):
            df = pd.read_csv('sample_clinical_notes.csv')
            st.write(f"📂 Sample data: {len(df)} notes")
            st.dataframe(df)

# ==================== PAGE 3: ANALYTICS ====================
elif page == "📈 Analytics":
    st.header("📈 Analytics & Statistics")
    
    st.markdown("View extraction statistics and processing history.")
    
    # History stats
    if st.session_state.history:
        st.subheader("📊 Processing History")
        
        history_df = pd.DataFrame(st.session_state.history)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Processed", len(st.session_state.history))
        
        with col2:
            st.metric("Successful", len([h for h in st.session_state.history if h['status'] == 'processed']))
        
        with col3:
            st.metric("Session Started", datetime.now().strftime('%H:%M:%S'))
        
        st.dataframe(history_df)
    else:
        st.info("No processing history yet. Process some notes to see statistics.")
    
    # General information
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Extraction Modules:**")
        st.write("✅ Regex Pattern Extraction")
        st.write("✅ PII Detection")
        if st.session_state.extractor.nlp:
            st.write("✅ spaCy NLP")
        else:
            st.write("❌ spaCy NLP (not available)")
    
    with col2:
        st.write("**Capabilities:**")
        st.write("✅ ICD Code Extraction")
        st.write("✅ Risk Assessment")
        st.write("✅ Bias Detection")

# ==================== PAGE 4: ABOUT ====================
elif page == "ℹ️ About":
    st.header("ℹ️ About Clinical NLP Extractor")
    
    st.markdown("""
    ### 🏥 Overview
    
    The Clinical NLP Extractor is a comprehensive clinical text extraction pipeline that demonstrates
    the use of **Regex**, **spaCy NLP**, and **LLMs** for extracting structured medical data from
    unstructured clinical notes.
    
    ### ✨ Key Features
    
    - **📋 Regex Pattern Extraction** - Extract structured data (ICD codes, dates, lab values)
    - **🏷️ Entity Recognition** - Identify clinical entities using spaCy NLP
    - **🔐 Privacy Detection** - Detect PII and ensure HIPAA compliance
    - **⚠️ Risk Assessment** - Comprehensive risk and compliance evaluation
    - **🎯 Bias Detection** - Identify potential demographic biases
    - **📊 Batch Processing** - Process multiple notes efficiently
    
    ### 📊 Extraction Patterns
    
    - **ICD-10 Codes**: E11.65, K25.4, J18.9
    - **Dates**: Multiple formats (MM/DD/YYYY, YYYY-MM-DD, month names)
    - **Lab Values**: 185 mg/dL, 145 mmHg, 12.5 units
    - **Dosages**: 500mg, 2.5g, 10 units
    - **PII**: Phone numbers, SSNs, MRNs
    
    ### 🚀 Getting Started
    
    1. **Single Note Mode** - Analyze individual clinical notes
    2. **Batch Processing** - Process multiple notes from a CSV file
    3. **Analytics** - View processing statistics and history
    
    ### 📚 Documentation
    
    For more information, check the project documentation:
    - README.md - Full project documentation
    - QUICK_START.md - Quick start guide
    - LLM_INTEGRATION_GUIDE.md - LLM integration instructions
    
    ### ⚠️ Privacy & Compliance
    
    This application is designed with privacy in mind:
    - ✅ Detects and flags PII
    - ✅ Checks HIPAA compliance
    - ✅ Maintains audit trails
    - ✅ Generates compliance reports
    
    **Note**: Always review results and comply with your organization's data handling policies.
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ for healthcare professionals")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Clinical NLP Extractor v1.0 | 🔒 Privacy-First Medical NLP | 🏥 HIPAA-Aware Extraction</small>
</div>
""", unsafe_allow_html=True)

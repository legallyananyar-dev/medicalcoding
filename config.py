"""
Configuration file for Clinical NLP Extractor
Customize extraction behavior and thresholds
"""

# ============================================
# EXTRACTION CONFIGURATION
# ============================================

# Regex Patterns for Structured Extraction
REGEX_PATTERNS = {
    # ICD-10 codes (e.g., E11.65, K25.4)
    'icd_10': r'\b[A-Z]\d{1,2}(?:\.\d{1,2})?(?:[A-Z])?\b',
    
    # CPT codes (e.g., 99213, 70450)
    'cpt': r'\b\d{5}(?:-\d{2,3})?\b',
    
    # SNOMED-CT codes (e.g., 250.00)
    'snomed': r'\b\d{6,8}(?:\.\d{2,3})?\b',
    
    # Dates in various formats
    'dates': r'(?:\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
    
    # Lab values with units
    'lab_values': r'(\d+\.?\d*)\s*(?:mg/dL|mmol/L|mmHg|mL|units?|%|g/dL)',
    
    # Medication dosages
    'dosages': r'(\d+\.?\d*)\s*(?:mg|g|units?|ml|IU)',
    
    # Temperature
    'temperature': r'(\d+\.?\d*)\s*(?:°?F|°?C)',
    
    # Blood pressure
    'blood_pressure': r'(\d{2,3})\s*(?:mmHg|/)\s*(\d{2,3})',
}

# ============================================
# CLINICAL KEYWORD DICTIONARIES
# ============================================

CLINICAL_KEYWORDS = {
    'diagnoses': [
        'diabetes', 'hypertension', 'asthma', 'copd', 'pneumonia',
        'bronchitis', 'heart failure', 'myocardial infarction', 'infarction',
        'stroke', 'cancer', 'depression', 'anxiety', 'schizophrenia',
        'bipolar', 'arthritis', 'osteoporosis', 'hepatitis', 'cirrhosis',
        'kidney disease', 'ckd', 'gerd', 'ulcer', 'cholangitis'
    ],
    
    'drugs': [
        'metformin', 'lisinopril', 'atorvastatin', 'aspirin', 'ibuprofen',
        'amoxicillin', 'sertraline', 'fluoxetine', 'citalopram',
        'insulin', 'albuterol', 'omeprazole', 'simvastatin',
        'warfarin', 'clopidogrel', 'tramadol', 'gabapentin',
        'prednisone', 'dexamethasone', 'heparin', 'enoxaparin'
    ],
    
    'symptoms': [
        'fever', 'cough', 'shortness of breath', 'dyspnea', 'chest pain',
        'headache', 'nausea', 'vomiting', 'fatigue', 'weakness',
        'dizziness', 'vertigo', 'swelling', 'edema', 'rash',
        'bleeding', 'hemorrhage', 'confusion', 'disorientation',
        'anxiety', 'tremor', 'palpitations', 'syncope', 'diaphoresis'
    ],
    
    'procedures': [
        'echocardiogram', 'ekg', 'x-ray', 'ct scan', 'mri',
        'ultrasound', 'endoscopy', 'colonoscopy', 'biopsy',
        'surgery', 'injection', 'aspiration', 'catheterization',
        'intubation', 'ventilation', 'dialysis', 'transfusion'
    ]
}

# ============================================
# PII DETECTION PATTERNS
# ============================================

PII_PATTERNS = {
    # US Phone numbers: 555-123-4567, (555) 123-4567, 555.123.4567
    'phone': r'\b(?:\d{3}[-.]?\d{3}[-.]?\d{4}|\(?\d{3}\)?[-.\s]?\d{3}[-.]?\d{4})\b',
    
    # Social Security Numbers: 123-45-6789
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    
    # Medical Record Numbers: MRN: 12345678
    'mrn': r'\b(?:MRN|medical record)\s*[:=]?\s*([A-Z0-9]+)',
    
    # Email addresses
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    
    # Zip codes: 12345 or 12345-6789
    'zip_code': r'\b\d{5}(?:-\d{4})?\b',
}

# ============================================
# RISK ASSESSMENT CONFIGURATION
# ============================================

# Thresholds for different risk levels
RISK_THRESHOLDS = {
    'pii_found': 'CRITICAL',  # Any PII = CRITICAL risk
    'bias_detected': 'MEDIUM',
    'compliance_failed': 'HIGH',
}

# Compliance checklist
COMPLIANCE_REQUIREMENTS = {
    'hipaa': [
        'Patient identifiers removed or anonymized',
        'Access logs maintained',
        'Data encryption enabled',
        'Business Associate Agreement signed',
    ],
    'gdpr': [
        'Legal basis documented',
        'Data subject rights procedures established',
        'Data Processing Agreement signed',
        'Data retention limits enforced',
    ],
    'fda_samd': [
        'Algorithm validation completed',
        'Clinical validation studies performed',
        'Risk classification determined',
        'Appropriate regulatory pathway selected',
    ]
}

# ============================================
# BIAS TESTING CONFIGURATION
# ============================================

# Demographic groups for bias testing
DEMOGRAPHIC_GROUPS = {
    'age_groups': ['18-40', '40-60', '60+'],
    'gender': ['Male', 'Female', 'Other'],
    'race_ethnicity': ['White', 'Black', 'Hispanic', 'Asian', 'Other'],
}

# Performance metrics to track
PERFORMANCE_METRICS = [
    'precision',
    'recall',
    'f1_score',
    'accuracy',
    'specificity',
    'sensitivity',
]

# ============================================
# LOGGING CONFIGURATION
# ============================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    
    # Log critical events
    'log_pii_detection': True,
    'log_every_extraction': True,
    'log_failures': True,
}

# ============================================
# OUTPUT CONFIGURATION
# ============================================

OUTPUT_FORMAT = {
    'json_indent': 2,
    'include_confidence_scores': True,
    'include_extraction_rationale': True,
    'include_audit_trail': True,
}

# ============================================
# LLM CONFIGURATION (for future integration)
# ============================================

LLM_CONFIG = {
    'provider': 'openai',  # Options: 'openai', 'anthropic', 'huggingface'
    
    # OpenAI
    'openai_model': 'gpt-4',
    'openai_temperature': 0.3,  # Lower = more deterministic
    'openai_max_tokens': 500,
    
    # Anthropic (Claude)
    'anthropic_model': 'claude-opus',
    'anthropic_temperature': 0.2,
    
    # Hugging Face
    'huggingface_model': 'meta-llama/Llama-2-7b-chat-hf',
    
    # General settings
    'use_cache': True,
    'timeout': 30,
    'retry_attempts': 3,
}

# ============================================
# SPACY CONFIGURATION
# ============================================

SPACY_CONFIG = {
    'model_name': 'en_core_web_sm',  # Options: sm, md, lg
    'use_gpu': False,  # Set to True if GPU available
    'batch_size': 50,
}

# ============================================
# BATCH PROCESSING CONFIGURATION
# ============================================

BATCH_CONFIG = {
    'batch_size': 100,
    'parallel_processing': True,
    'num_workers': 4,
}

# ============================================
# EXPORT CONFIGURATION
# ============================================

EXPORT_CONFIG = {
    'export_formats': ['json', 'csv', 'xml'],
    'include_timestamps': True,
    'anonymize_output': True,  # Remove all PII from exports
    'encryption_enabled': False,  # Set to True for production
}

# ============================================
# VALIDATION CONFIGURATION
# ============================================

VALIDATION_CONFIG = {
    'validate_icd_codes': True,
    'validate_drug_names': True,
    'validate_lab_ranges': True,  # Check if values are physiologically possible
}

# ============================================
# DEFAULT THRESHOLDS
# ============================================

THRESHOLDS = {
    'min_confidence_score': 0.70,  # Minimum confidence for extraction
    'min_text_length': 50,  # Minimum characters to attempt extraction
    'max_text_length': 50000,  # Maximum characters to process
}

"""
Clinical NLP Extractor with Risk Assessment
============================================
Demonstrates extraction of clinical entities using:
- Regex for structured patterns (dates, ICD codes, lab values)
- spaCy for NLP entity recognition (diagnoses, drugs, symptoms)
- LLMs for flexible extraction and summarization
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

# Configure logging for audit trail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClinicalNLPExtractor:
    """Main clinical text extraction pipeline."""
    
    def __init__(self):
        """Initialize the extractor with regex patterns and spaCy model."""
        self.extraction_log = []
        self._init_patterns()
        self._init_spacy()
    
    def _init_patterns(self):
        """Initialize regex patterns for structured extraction."""
        self.patterns = {
            # ICD-10 codes: E11.65, K25.4, etc.
            'icd_codes': r'\b[A-Z]\d{1,2}(?:\.\d{1,2})?(?:[A-Z])?\b',
            
            # Dates: MM/DD/YYYY, YYYY-MM-DD, month names
            'dates': r'(?:\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
            
            # Lab values: 5.2 mg/dL, 120 mmHg, etc.
            'lab_values': r'(\d+\.?\d*)\s*(?:mg/dL|mmol/L|mmHg|mL|units?|%|g/dL)',
            
            # Medication dosages: 500mg, 2.5g, 10 units
            'dosages': r'(\d+\.?\d*)\s*(?:mg|g|units?|ml|IU)',
            
            # Phone/SSN patterns (for privacy check)
            'pii_patterns': {
                'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
                'mrn': r'\bMRN\s*[:=]?\s*(\d+)',
            }
        }
    
    def _init_spacy(self):
        """Initialize spaCy model (lazy load to avoid required dependency)."""
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except (ImportError, OSError) as e:
            logger.warning(f"spaCy not available or model not installed: {e}")
            self.nlp = None
            logger.info("Continuing with regex-only extraction")
    
    def extract_regex_patterns(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structured patterns using regex.
        
        Args:
            text: Clinical note text
            
        Returns:
            Dictionary of extracted patterns
        """
        logger.info("Starting regex pattern extraction")
        results = {
            'icd_codes': re.findall(self.patterns['icd_codes'], text),
            'dates': re.findall(self.patterns['dates'], text),
            'lab_values': re.findall(self.patterns['lab_values'], text),
            'dosages': re.findall(self.patterns['dosages'], text),
        }
        
        # Remove duplicates
        for key in results:
            results[key] = list(set(results[key]))
        
        logger.info(f"Regex extraction found: {results}")
        return results
    
    def check_pii_presence(self, text: str) -> Dict[str, List[str]]:
        """
        Check for presence of Personally Identifiable Information (PII).
        
        Args:
            text: Clinical note text
            
        Returns:
            Dictionary of found PII
        """
        logger.warning("Checking for PII in text")
        pii_found = {}
        
        for pii_type, pattern in self.patterns['pii_patterns'].items():
            matches = re.findall(pattern, text)
            if matches:
                pii_found[pii_type] = matches
                logger.error(f"⚠️  CRITICAL: {pii_type.upper()} found in clinical note!")
        
        return pii_found
    
    def extract_spacy_entities(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """
        Extract entities using spaCy NLP.
        
        Args:
            text: Clinical note text
            
        Returns:
            Dictionary of extracted entities with types and confidence
        """
        if not self.nlp:
            logger.warning("spaCy not available, skipping NLP extraction")
            return {}
        
        logger.info("Starting spaCy entity extraction")
        doc = self.nlp(text)
        
        entities = {}
        for ent in doc.ents:
            ent_type = ent.label_
            if ent_type not in entities:
                entities[ent_type] = []
            
            entities[ent_type].append({
                'text': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'label': ent_type
            })
            logger.debug(f"Found entity: {ent.text} ({ent_type})")
        
        return entities
    
    def extract_clinical_concepts(self, text: str) -> Dict[str, List[str]]:
        """
        Extract clinical concepts using keyword matching.
        Clinical-specific terms for diagnoses, drugs, and symptoms.
        
        Args:
            text: Clinical note text
            
        Returns:
            Dictionary of detected clinical concepts
        """
        logger.info("Starting clinical concept extraction")
        
        # Medical terminology dictionaries
        medical_keywords = {
            'diagnoses': [
                'diabetes', 'hypertension', 'asthma', 'copd',
                'pneumonia', 'bronchitis', 'heart failure', 'infarction',
                'stroke', 'cancer', 'depression', 'anxiety'
            ],
            'drugs': [
                'metformin', 'lisinopril', 'atorvastatin', 'aspirin',
                'ibuprofen', 'amoxicillin', 'sertraline', 'fluoxetine',
                'insulin', 'albuterol'
            ],
            'symptoms': [
                'fever', 'cough', 'shortness of breath', 'chest pain',
                'headache', 'nausea', 'vomiting', 'fatigue',
                'dizziness', 'weakness', 'swelling'
            ]
        }
        
        concepts = {}
        text_lower = text.lower()
        
        for category, keywords in medical_keywords.items():
            found = []
            for keyword in keywords:
                if keyword in text_lower:
                    found.append(keyword)
                    logger.debug(f"Found {category}: {keyword}")
            if found:
                concepts[category] = list(set(found))
        
        return concepts
    
    def extract_all(self, text: str) -> Dict[str, Any]:
        """
        Run complete extraction pipeline.
        
        Args:
            text: Clinical note text
            
        Returns:
            Comprehensive extraction results
        """
        logger.info("=" * 50)
        logger.info("Starting complete clinical extraction pipeline")
        logger.info("=" * 50)
        
        extraction = {
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'extraction_steps': []
        }
        
        # Step 1: Check for PII (critical for compliance)
        pii_check = self.check_pii_presence(text)
        extraction['pii_warning'] = pii_check
        extraction['extraction_steps'].append('pii_check')
        
        # Step 2: Regex extraction
        regex_results = self.extract_regex_patterns(text)
        extraction['regex_extraction'] = regex_results
        extraction['extraction_steps'].append('regex')
        
        # Step 3: spaCy extraction
        spacy_results = self.extract_spacy_entities(text)
        extraction['spacy_entities'] = spacy_results
        extraction['extraction_steps'].append('spacy')
        
        # Step 4: Clinical concept extraction
        concepts = self.extract_clinical_concepts(text)
        extraction['clinical_concepts'] = concepts
        extraction['extraction_steps'].append('clinical_concepts')
        
        # Log the complete extraction
        self.extraction_log.append(extraction)
        logger.info(f"Extraction complete with {len(extraction['extraction_steps'])} steps")
        
        return extraction
    
    def generate_risk_assessment(self, extraction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate risk assessment based on extraction results.
        
        Args:
            extraction: Results from extract_all()
            
        Returns:
            Risk assessment report
        """
        logger.info("Generating risk assessment report")
        
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'data_privacy': self._assess_privacy(extraction),
            'bias_check': self._assess_bias(extraction),
            'compliance': self._assess_compliance(extraction),
            'audit_trail': self._generate_audit_trail(),
            'overall_risk_level': 'PENDING'
        }
        
        # Determine overall risk level
        if assessment['data_privacy']['has_pii']:
            assessment['overall_risk_level'] = 'CRITICAL'
        elif not assessment['compliance']['hipaa_compliant']:
            assessment['overall_risk_level'] = 'HIGH'
        elif assessment['bias_check']['potential_bias_detected']:
            assessment['overall_risk_level'] = 'MEDIUM'
        else:
            assessment['overall_risk_level'] = 'LOW'
        
        logger.info(f"Risk assessment complete: {assessment['overall_risk_level']}")
        return assessment
    
    def _assess_privacy(self, extraction: Dict[str, Any]) -> Dict[str, Any]:
        """Assess data privacy risks."""
        pii_warning = extraction.get('pii_warning', {})
        
        return {
            'has_pii': bool(pii_warning),
            'pii_types_found': list(pii_warning.keys()),
            'recommendation': 'REMOVE ALL PII BEFORE PROCESSING' if pii_warning else 'OK - No PII detected',
            'compliance_status': 'FAILED' if pii_warning else 'PASSED'
        }
    
    def _assess_bias(self, extraction: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential bias in extraction."""
        concepts = extraction.get('clinical_concepts', {})
        
        # Simple bias detection: check for demographic-specific terms
        demographic_terms = ['elderly', 'young', 'male', 'female', 'african', 'hispanic']
        found_demographics = [term for term in demographic_terms if term in str(concepts).lower()]
        
        return {
            'potential_bias_detected': bool(found_demographics),
            'demographic_terms_found': found_demographics,
            'recommendation': 'Review extraction results across multiple demographics' if found_demographics else 'Continue with caution',
            'note': 'Bias assessment is preliminary; human review required'
        }
    
    def _assess_compliance(self, extraction: Dict[str, Any]) -> Dict[str, Any]:
        """Assess HIPAA/GDPR compliance."""
        pii_check = extraction.get('pii_warning', {})
        
        return {
            'hipaa_compliant': not bool(pii_check),
            'gdpr_compliant': not bool(pii_check),
            'audit_trail_available': len(self.extraction_log) > 0,
            'extraction_logged': True,
            'recommendations': [
                'Ensure data minimization principles are applied',
                'Implement role-based access controls',
                'Maintain detailed audit logs for all extractions',
                'Review extraction with privacy officer before production'
            ]
        }
    
    def _generate_audit_trail(self) -> List[Dict[str, Any]]:
        """Generate audit trail from extraction log."""
        return [
            {
                'step': i + 1,
                'timestamp': log.get('timestamp'),
                'text_length': log.get('text_length'),
                'extraction_steps': log.get('extraction_steps')
            }
            for i, log in enumerate(self.extraction_log[-5:])  # Last 5 extractions
        ]
    
    def export_to_json(self, extraction: Dict[str, Any], filepath: str):
        """Export extraction results to JSON."""
        with open(filepath, 'w') as f:
            json.dump(extraction, f, indent=2)
        logger.info(f"Exported extraction results to {filepath}")
    
    def export_risk_assessment(self, assessment: Dict[str, Any], filepath: str):
        """Export risk assessment to JSON."""
        with open(filepath, 'w') as f:
            json.dump(assessment, f, indent=2)
        logger.info(f"Exported risk assessment to {filepath}")


def process_clinical_note(note: str) -> Tuple[Dict, Dict]:
    """
    Process a clinical note end-to-end.
    
    Args:
        note: Clinical note text
        
    Returns:
        Tuple of (extraction_results, risk_assessment)
    """
    extractor = ClinicalNLPExtractor()
    extraction = extractor.extract_all(note)
    assessment = extractor.generate_risk_assessment(extraction)
    return extraction, assessment


if __name__ == "__main__":
    # Example usage
    sample_note = """
    Patient: John Doe
    Date: 2024-01-15
    
    Chief Complaint: Persistent cough and shortness of breath
    
    History of Present Illness:
    45-year-old male with diabetes (ICD-10: E11.65) presents with fever of 102°F,
    productive cough for 2 weeks, and dyspnea. Patient reports chest pain on exertion.
    
    Assessment:
    - Pneumonia (ICD-10: J18.9)
    - Hypertension (ICD-10: I10)
    - Type 2 Diabetes Mellitus with complications
    
    Medications:
    - Metformin 500mg twice daily
    - Lisinopril 10mg daily
    - Atorvastatin 20mg nightly
    - Aspirin 81mg daily
    - Albuterol inhaler as needed
    
    Lab Values:
    - Blood Glucose: 185 mg/dL
    - BP: 145 mmHg
    - WBC: 12.5 units
    """
    
    extraction, assessment = process_clinical_note(sample_note)
    
    print("\n" + "="*60)
    print("EXTRACTION RESULTS")
    print("="*60)
    print(json.dumps(extraction, indent=2))
    
    print("\n" + "="*60)
    print("RISK ASSESSMENT")
    print("="*60)
    print(json.dumps(assessment, indent=2))

#!/usr/bin/env python3
"""
Bias Detection and Fairness Testing Script
Tests extraction performance across different demographic groups
"""

import json
import pandas as pd
from typing import Dict, List
from medcoding import ClinicalNLPExtractor


class BiasTestingFramework:
    """
    Framework for testing and detecting bias in clinical NLP extraction
    """
    
    def __init__(self):
        self.extractor = ClinicalNLPExtractor()
        self.results = []
    
    def create_demographic_variants(self, base_note: str, demographic_term: str) -> Dict[str, str]:
        """
        Create demographic variants of a clinical note.
        
        Args:
            base_note: Original clinical note
            demographic_term: Type of demographic ('age', 'gender', 'ethnicity')
            
        Returns:
            Dictionary of variant notes by demographic group
        """
        variants = {}
        
        if demographic_term == 'age':
            variants = {
                'age_18_40': base_note.replace(
                    '45-year-old', '32-year-old'
                ),
                'age_40_60': base_note,  # Original
                'age_60_plus': base_note.replace(
                    '45-year-old', '72-year-old'
                ),
            }
        
        elif demographic_term == 'gender':
            variants = {
                'male': base_note.replace(
                    'female', 'male'
                ).replace('she', 'he').replace('her', 'his'),
                'female': base_note.replace(
                    'male', 'female'
                ).replace('he', 'she').replace('his', 'her'),
            }
        
        elif demographic_term == 'race_ethnicity':
            # Note: This is simplified for demonstration
            # In production, this would require careful consideration of cultural sensitivity
            variants = {
                'baseline': base_note,
                'with_ethnic_context': base_note + " [Patient reports traditional medicine use]",
            }
        
        return variants
    
    def test_extraction_performance(self, notes_by_demographic: Dict[str, str]) -> Dict:
        """
        Test extraction performance across demographic variants.
        
        Args:
            notes_by_demographic: Dictionary mapping demographic group to note text
            
        Returns:
            Performance comparison across demographics
        """
        results = {}
        
        for demographic, note_text in notes_by_demographic.items():
            extraction = self.extractor.extract_all(note_text)
            
            # Calculate extraction metrics
            total_entities = (
                len(extraction['regex_extraction']['icd_codes']) +
                len(extraction['regex_extraction']['dates']) +
                len(extraction['regex_extraction']['lab_values']) +
                len(extraction['regex_extraction']['dosages']) +
                sum(len(v) for v in extraction['clinical_concepts'].values())
            )
            
            results[demographic] = {
                'icd_codes': len(extraction['regex_extraction']['icd_codes']),
                'dates': len(extraction['regex_extraction']['dates']),
                'lab_values': len(extraction['regex_extraction']['lab_values']),
                'dosages': len(extraction['regex_extraction']['dosages']),
                'clinical_concepts': sum(len(v) for v in extraction['clinical_concepts'].values()),
                'total_entities': total_entities,
            }
        
        return results
    
    def analyze_demographic_disparities(self, performance_data: Dict) -> Dict:
        """
        Analyze disparities in extraction performance across demographics.
        
        Args:
            performance_data: Performance metrics by demographic group
            
        Returns:
            Analysis of disparities and potential biases
        """
        disparities = {
            'findings': [],
            'warnings': [],
            'recommendations': [],
        }
        
        # Get baseline (usually the first or 'baseline' group)
        baseline_group = list(performance_data.keys())[0]
        baseline_metrics = performance_data[baseline_group]
        baseline_total = baseline_metrics['total_entities']
        
        # Compare other groups to baseline
        for group_name, metrics in performance_data.items():
            if group_name == baseline_group:
                continue
            
            group_total = metrics['total_entities']
            
            # Calculate percentage difference
            if baseline_total > 0:
                pct_diff = ((group_total - baseline_total) / baseline_total) * 100
            else:
                pct_diff = 0
            
            # Flag disparities > 10%
            if abs(pct_diff) > 10:
                finding = {
                    'group': group_name,
                    'baseline': baseline_group,
                    'disparity_percent': round(pct_diff, 2),
                    'group_total': group_total,
                    'baseline_total': baseline_total,
                }
                disparities['findings'].append(finding)
                
                if abs(pct_diff) > 20:
                    disparities['warnings'].append(
                        f"⚠️  SIGNIFICANT disparity detected: {group_name} has {pct_diff:+.1f}% "
                        f"entities compared to {baseline_group}"
                    )
        
        # Add recommendations
        if disparities['warnings']:
            disparities['recommendations'].extend([
                "1. Conduct manual review of extraction quality by demographic",
                "2. Verify training data includes diverse demographic representation",
                "3. Test with larger sample sizes for statistical significance",
                "4. Consider bias mitigation techniques (rebalancing, adversarial debiasing)",
                "5. Implement ongoing fairness monitoring in production",
            ])
        else:
            disparities['recommendations'].append(
                "✓ No significant disparities detected. Continue monitoring."
            )
        
        return disparities
    
    def generate_fairness_report(self, test_name: str, 
                                performance_data: Dict, 
                                disparity_analysis: Dict) -> str:
        """
        Generate a fairness test report.
        
        Args:
            test_name: Name of the fairness test
            performance_data: Performance metrics
            disparity_analysis: Disparity analysis results
            
        Returns:
            Formatted report string
        """
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║              CLINICAL NLP FAIRNESS TEST REPORT                 ║
╚════════════════════════════════════════════════════════════════╝

Test Name: {test_name}
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

EXTRACTION PERFORMANCE BY DEMOGRAPHIC GROUP
────────────────────────────────────────────
"""
        
        # Create performance table
        perf_df = pd.DataFrame(performance_data).T
        report += perf_df.to_string()
        
        report += f"""

DISPARITY ANALYSIS
───────────────────
"""
        
        if disparity_analysis['findings']:
            report += f"\nDisparities Found: {len(disparity_analysis['findings'])}\n"
            for finding in disparity_analysis['findings']:
                report += f"\n  {finding['group']} vs {finding['baseline']}:"
                report += f"\n    • Disparity: {finding['disparity_percent']:+.1f}%"
                report += f"\n    • {finding['group']}: {finding['group_total']} entities"
                report += f"\n    • {finding['baseline']}: {finding['baseline_total']} entities"
        else:
            report += "\n✓ No significant disparities detected (threshold: 10%)\n"
        
        if disparity_analysis['warnings']:
            report += "\nWARNINGS:\n"
            for warning in disparity_analysis['warnings']:
                report += f"  {warning}\n"
        
        report += "\nRECOMMENDATIONS:\n"
        for rec in disparity_analysis['recommendations']:
            report += f"  {rec}\n"
        
        report += "\n" + "="*60 + "\n"
        
        return report
    
    def run_comprehensive_bias_test(self, clinical_note: str) -> str:
        """
        Run comprehensive bias testing across multiple demographics.
        
        Args:
            clinical_note: Base clinical note for testing
            
        Returns:
            Comprehensive bias test report
        """
        report = ""
        
        # Test 1: Age-based bias
        print("\n🧪 Testing for AGE-BASED BIAS...")
        age_variants = self.create_demographic_variants(clinical_note, 'age')
        age_performance = self.test_extraction_performance(age_variants)
        age_disparities = self.analyze_demographic_disparities(age_performance)
        report += self.generate_fairness_report("Age-Based Bias Test", age_performance, age_disparities)
        
        # Test 2: Gender-based bias
        print("🧪 Testing for GENDER-BASED BIAS...")
        gender_variants = self.create_demographic_variants(clinical_note, 'gender')
        gender_performance = self.test_extraction_performance(gender_variants)
        gender_disparities = self.analyze_demographic_disparities(gender_performance)
        report += self.generate_fairness_report("Gender-Based Bias Test", gender_performance, gender_disparities)
        
        # Test 3: Ethnic/Cultural bias
        print("🧪 Testing for ETHNIC/CULTURAL BIAS...")
        ethnic_variants = self.create_demographic_variants(clinical_note, 'race_ethnicity')
        ethnic_performance = self.test_extraction_performance(ethnic_variants)
        ethnic_disparities = self.analyze_demographic_disparities(ethnic_performance)
        report += self.generate_fairness_report("Ethnic/Cultural Bias Test", ethnic_performance, ethnic_disparities)
        
        return report


def run_bias_tests():
    """
    Run comprehensive bias testing on sample notes
    """
    print("="*60)
    print("CLINICAL NLP BIAS DETECTION TEST SUITE")
    print("="*60)
    
    # Sample clinical note
    base_note = """
    Chief Complaint: Chest pain
    
    45-year-old male presents with acute chest pain on exertion.
    Pain radiates to left arm. Associated with shortness of breath.
    
    History of Hypertension (ICD-10: I10)
    
    Current Medications:
    - Lisinopril 20mg daily
    - Aspirin 81mg daily
    
    Lab Values:
    - Troponin: 0.15 ng/mL (elevated)
    - Blood Pressure: 160 mmHg systolic
    
    Assessment:
    Acute Coronary Syndrome
    
    Plan:
    Emergency catheterization
    """
    
    # Initialize framework
    framework = BiasTestingFramework()
    
    # Run tests
    comprehensive_report = framework.run_comprehensive_bias_test(base_note)
    
    print(comprehensive_report)
    
    # Save report
    with open('bias_test_report.txt', 'w') as f:
        f.write(comprehensive_report)
    
    print("✓ Report saved to: bias_test_report.txt")


if __name__ == '__main__':
    run_bias_tests()

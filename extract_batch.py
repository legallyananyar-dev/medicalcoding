#!/usr/bin/env python3
"""
Batch Processing Script for Clinical Notes
Demonstrates how to process multiple clinical notes using the extractor
"""

import json
import pandas as pd
from pathlib import Path
import argparse
from medcoding import ClinicalNLPExtractor, process_clinical_note


def process_csv_notes(csv_filepath: str, output_dir: str = 'output'):
    """
    Process clinical notes from CSV file.
    
    Args:
        csv_filepath: Path to CSV file with clinical notes
        output_dir: Directory to save output files
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"📂 Reading clinical notes from: {csv_filepath}")
    
    # Load CSV
    df = pd.read_csv(csv_filepath)
    print(f"✓ Loaded {len(df)} clinical notes\n")
    
    # Initialize extractor
    extractor = ClinicalNLPExtractor()
    
    # Process each note
    results = []
    risk_assessments = []
    
    for idx, row in df.iterrows():
        note_id = row['note_id']
        note_text = row['note_text']
        
        print(f"🔄 Processing {note_id} ({idx+1}/{len(df)})...", end=" ")
        
        try:
            # Extract and assess
            extraction = extractor.extract_all(note_text)
            assessment = extractor.generate_risk_assessment(extraction)
            
            # Store results
            results.append({
                'note_id': note_id,
                'extraction': extraction,
                'risk_level': assessment['overall_risk_level']
            })
            
            risk_assessments.append({
                'note_id': note_id,
                'risk_level': assessment['overall_risk_level'],
                'has_pii': assessment['data_privacy']['has_pii'],
                'hipaa_compliant': assessment['compliance']['hipaa_compliant'],
                'gdpr_compliant': assessment['compliance']['gdpr_compliant'],
            })
            
            print(f"✓ Risk Level: {assessment['overall_risk_level']}")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append({
                'note_id': note_id,
                'error': str(e),
                'extraction': None
            })
    
    # Save results
    print("\n" + "="*60)
    print("SAVING RESULTS")
    print("="*60)
    
    # Save extraction results
    with open(output_path / 'extraction_results.json', 'w') as f:
        for r in results:
            if r['extraction']:
                json.dump(r, f, indent=2, default=str)
                f.write('\n')
    print(f"✓ Saved extraction results to: {output_path / 'extraction_results.json'}")
    
    # Save risk assessment summary
    risk_df = pd.DataFrame(risk_assessments)
    risk_df.to_csv(output_path / 'risk_assessment_summary.csv', index=False)
    print(f"✓ Saved risk assessment summary to: {output_path / 'risk_assessment_summary.csv'}")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    
    risk_counts = risk_df['risk_level'].value_counts()
    print(f"\nRisk Level Distribution:")
    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = risk_counts.get(level, 0)
        print(f"  {level}: {count} notes")
    
    pii_count = risk_df['has_pii'].sum()
    print(f"\nPII Detection:")
    print(f"  Notes with PII: {pii_count}")
    print(f"  Notes without PII: {len(risk_df) - pii_count}")
    
    hipaa_count = risk_df['hipaa_compliant'].sum()
    gdpr_count = risk_df['gdpr_compliant'].sum()
    print(f"\nCompliance:")
    print(f"  HIPAA Compliant: {hipaa_count}/{len(risk_df)}")
    print(f"  GDPR Compliant: {gdpr_count}/{len(risk_df)}")
    
    return risk_df


def process_single_note(note_text: str, export_json: bool = False):
    """
    Process a single clinical note.
    
    Args:
        note_text: Clinical note text
        export_json: Whether to export results to JSON
    """
    print("="*60)
    print("CLINICAL EXTRACTION ANALYSIS")
    print("="*60)
    
    extraction, assessment = process_clinical_note(note_text)
    
    # Display results
    print("\n📋 EXTRACTION RESULTS")
    print("-"*60)
    
    regex_data = extraction['regex_extraction']
    print(f"\nStructured Data (Regex):")
    print(f"  • ICD Codes: {regex_data['icd_codes']}")
    print(f"  • Dates: {regex_data['dates']}")
    print(f"  • Lab Values: {regex_data['lab_values']}")
    print(f"  • Dosages: {regex_data['dosages']}")
    
    clinical_data = extraction['clinical_concepts']
    if clinical_data:
        print(f"\nClinical Concepts:")
        for category, items in clinical_data.items():
            print(f"  • {category.title()}: {', '.join(items)}")
    
    # Risk assessment
    print(f"\n\n⚠️  RISK ASSESSMENT")
    print("-"*60)
    
    privacy = assessment['data_privacy']
    print(f"\nData Privacy:")
    print(f"  • PII Found: {'🔴 YES' if privacy['has_pii'] else '🟢 NO'}")
    print(f"  • Compliance: {privacy['compliance_status']}")
    
    bias = assessment['bias_check']
    print(f"\nBias Detection:")
    print(f"  • Bias Detected: {'⚠️  YES' if bias['potential_bias_detected'] else '✓ NO'}")
    
    compliance = assessment['compliance']
    print(f"\nCompliance:")
    print(f"  • HIPAA: {'✓ YES' if compliance['hipaa_compliant'] else '✗ NO'}")
    print(f"  • GDPR: {'✓ YES' if compliance['gdpr_compliant'] else '✗ NO'}")
    
    print(f"\n🚨 Overall Risk Level: {assessment['overall_risk_level']}")
    
    # Export if requested
    if export_json:
        with open('extraction_output.json', 'w') as f:
            json.dump({
                'extraction': extraction,
                'risk_assessment': assessment
            }, f, indent=2, default=str)
        print(f"\n✓ Results exported to: extraction_output.json")
    
    return extraction, assessment


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Clinical NLP Extractor - Batch Processing'
    )
    parser.add_argument(
        '--csv', 
        help='Process CSV file with clinical notes',
        type=str
    )
    parser.add_argument(
        '--output',
        help='Output directory for results',
        default='output',
        type=str
    )
    parser.add_argument(
        '--example',
        help='Run example on sample note',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    if args.csv:
        # Process CSV file
        risk_df = process_csv_notes(args.csv, args.output)
        
    elif args.example:
        # Run example
        example_note = """
        Chief Complaint: Follow-up for hypertension
        
        Patient: 55-year-old male
        Date: 2024-01-20
        
        History:
        Patient with hypertension (ICD-10: I10) and type 2 diabetes (ICD-10: E11.9)
        reports good medication compliance.
        
        Medications:
        - Lisinopril 20mg daily
        - Atorvastatin 40mg at night
        - Metformin 1000mg twice daily
        
        Lab Values:
        - BP: 138 mmHg
        - FBS: 120 mg/dL
        
        Assessment:
        Hypertension - controlled
        Diabetes - stable
        
        Plan:
        Continue current medications
        Follow-up in 3 months
        """
        
        process_single_note(example_note, export_json=True)
        
    else:
        print("Clinical NLP Extractor - Batch Processing Tool")
        print("\nUsage:")
        print("  python extract_batch.py --csv <path_to_csv> [--output <output_dir>]")
        print("  python extract_batch.py --example")
        print("\nExample:")
        print("  python extract_batch.py --csv sample_clinical_notes.csv --output results/")

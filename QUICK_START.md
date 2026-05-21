# Quick Start Guide - Clinical NLP Extractor

Get started with clinical NLP extraction in 5 minutes!

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd medcoding.py

# Create virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 2: Try the Example (1 minute)

```python
from medcoding import ClinicalNLPExtractor

# Initialize extractor
extractor = ClinicalNLPExtractor()

# Sample clinical note
note = """
Chief Complaint: Cough and fever
45-year-old male with diabetes (ICD-10: E11.65)
Temperature: 102°F
Medications: Metformin 500mg twice daily
Lab: Blood Glucose: 185 mg/dL
"""

# Extract and assess
extraction = extractor.extract_all(note)
risk_assessment = extractor.generate_risk_assessment(extraction)

# View results
print(f"ICD Codes: {extraction['regex_extraction']['icd_codes']}")
print(f"Risk Level: {risk_assessment['overall_risk_level']}")
```

### Step 3: Run Interactive Notebook (2 minutes)

```bash
jupyter notebook clinical_extraction.ipynb
```

---

## 🎯 Common Use Cases

### Use Case 1: Extract from Single Note

```python
from medcoding import process_clinical_note

clinical_note = "Your clinical note text here..."

extraction, assessment = process_clinical_note(clinical_note)

# Check for PII
if assessment['data_privacy']['has_pii']:
    print("⚠️  PII DETECTED - Do not use in production!")
else:
    print("✓ Safe for processing")
    print(f"Risk Level: {assessment['overall_risk_level']}")
```

### Use Case 2: Batch Process CSV File

```bash
python extract_batch.py --csv sample_clinical_notes.csv --output results/
```

**Output:**
- `results/extraction_results.json` - Detailed results
- `results/risk_assessment_summary.csv` - Risk summary

### Use Case 3: Check for Bias

```bash
python bias_testing.py
```

**Output:**
- `bias_test_report.txt` - Fairness analysis across demographics

### Use Case 4: Compliance Review

1. Download template: [RISK_ASSESSMENT_TEMPLATE.md](RISK_ASSESSMENT_TEMPLATE.md)
2. Fill out each section (Data Privacy, Bias, Compliance, etc.)
3. Get sign-off from team leads
4. Submit for approval

---

## 📊 What You Get

### 1. Structured Extraction
```json
{
  "icd_codes": ["E11.65", "J18.9"],
  "dates": ["2024-01-15"],
  "lab_values": ["185 mg/dL", "102°F"],
  "clinical_concepts": {
    "diagnoses": ["diabetes", "pneumonia"],
    "drugs": ["metformin"],
    "symptoms": ["cough", "fever"]
  }
}
```

### 2. Risk Assessment
```
🟢 LOW RISK
✓ No PII detected
✓ HIPAA compliant  
✓ GDPR compliant
✓ Bias assessment: OK
```

### 3. Compliance Report
- Data privacy status
- Regulatory alignment (HIPAA, GDPR)
- Audit trail
- Recommendations

---

## 🔍 Key Features at a Glance

| Feature | Status | Use Case |
|---------|--------|----------|
| **Regex Extraction** | ✅ Ready | Quick structured data extraction |
| **spaCy NLP** | ✅ Ready | Entity recognition (requires model) |
| **PII Detection** | ✅ Ready | Privacy compliance checking |
| **Risk Assessment** | ✅ Ready | Compliance & bias evaluation |
| **LLM Integration** | 📖 Guide | Advanced contextual extraction |
| **Batch Processing** | ✅ Ready | Process 100s of notes |
| **Bias Testing** | ✅ Ready | Fairness across demographics |

---

## 📚 Documentation Map

```
START HERE
    ↓
Quick Start Guide (this file)
    ↓
Choose your path:
    ├─ Clinical Users → README.md
    ├─ Developers → medcoding.py code
    ├─ Compliance → RISK_ASSESSMENT_TEMPLATE.md
    ├─ Advanced → LLM_INTEGRATION_GUIDE.md
    ├─ Reference → PROJECT_STRUCTURE.md
    └─ Demo → clinical_extraction.ipynb
```

---

## 🚨 Important Before Using

### ⚠️ Clinical Use Limitations
- **NOT** for autonomous clinical decision-making
- Always requires human clinician review
- Cannot replace clinical judgment
- Must comply with FDA, HIPAA, GDPR regulations

### ⚠️ Data Privacy
Before processing real patient data:
1. ✅ Implement de-identification procedures
2. ✅ Get institutional IRB/ethics approval
3. ✅ Sign HIPAA Business Associate Agreements
4. ✅ Implement access controls
5. ✅ Maintain audit logs

### ⚠️ Bias Awareness
- Extraction may perform differently across demographics
- Regular fairness testing required
- Human review recommended for high-risk cases
- Ongoing monitoring essential for production

---

## ❓ Quick Troubleshooting

### Issue: "No module named 'spacy'"
```bash
pip install -r requirements.txt
```

### Issue: "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### Issue: Extraction seems to miss entities
- Check PII detection (may filter sensitive data)
- Review clinical_extraction.ipynb for examples
- Verify clinical note format and completeness
- Run bias_testing.py to check performance

### Issue: "Too many entities extracted"
- May include false positives
- Always have human review for clinical use
- Consider filtering by confidence scores
- Customize patterns in config.py

---

## 🎓 Learning Exercises

### Exercise 1: Basic Extraction (5 min)
```python
from medcoding import ClinicalNLPExtractor

extractor = ClinicalNLPExtractor()

# Write a clinical note and extract from it
my_note = """Your clinical note here"""

results = extractor.extract_all(my_note)
```

### Exercise 2: Batch Processing (10 min)
```bash
# Add your notes to sample_clinical_notes.csv
# Then process batch:
python extract_batch.py --csv sample_clinical_notes.csv
```

### Exercise 3: Bias Analysis (10 min)
```bash
# Run bias tests
python bias_testing.py

# Review results in bias_test_report.txt
```

### Exercise 4: Compliance Review (20 min)
1. Open RISK_ASSESSMENT_TEMPLATE.md
2. Fill out Data Privacy section
3. Document bias testing results
4. Evaluate regulatory compliance

---

## 💡 Pro Tips

1. **De-identify first**: Remove patient names before processing
2. **Validate results**: Always have a clinician review
3. **Monitor costs**: Track LLM API usage if using advanced features
4. **Test locally**: Validate on sample data before production
5. **Regular audits**: Re-run bias tests quarterly
6. **Update models**: Keep spaCy and dependencies current

---

## 🔗 Related Resources

- [spaCy Documentation](https://spacy.io)
- [HIPAA Guide](https://www.hhs.gov/hipaa/)
- [GDPR Overview](https://gdpr-info.eu/)
- [FDA SaMD Guidance](https://www.fda.gov/medical-devices/software-medical-device-samd/)
- [Clinical NLP Papers](https://www.nlm.nih.gov/)

---

## 📞 Next Steps

1. ✅ **Install**: Complete Step 1 above
2. ✅ **Try**: Run the example in Step 2
3. ✅ **Explore**: Open `clinical_extraction.ipynb`
4. ✅ **Read**: Study [README.md](README.md) for full docs
5. ✅ **Validate**: Fill out [RISK_ASSESSMENT_TEMPLATE.md](RISK_ASSESSMENT_TEMPLATE.md)
6. ✅ **Deploy**: Follow [LLM_INTEGRATION_GUIDE.md](LLM_INTEGRATION_GUIDE.md) for production

---

## 📋 Checklist

Before deploying to production:

- [ ] Dependencies installed
- [ ] Tested on sample notes
- [ ] Clinical validation completed
- [ ] Bias testing results reviewed
- [ ] HIPAA compliance verified
- [ ] GDPR compliance verified
- [ ] PII detection working
- [ ] Audit logging implemented
- [ ] Human review process defined
- [ ] Emergency response plan documented
- [ ] Compliance team approved
- [ ] Clinical team trained

---

**Ready to get started? Run this command:**
```bash
python extract_batch.py --example
```

**Questions?** See the [README.md](README.md) or specific guide files.

---

*Last Updated: January 2024*  
*Clinical NLP Extractor v1.0*

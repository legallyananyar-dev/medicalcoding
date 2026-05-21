# Clinical Extraction Risk Assessment Template

This template provides a structured approach for compliance teams to review AI-driven clinical NLP extraction systems.

---

## 1. Data Privacy Assessment

### Patient Identifiers
- [ ] **PII Removal Check**: Are all PHI (Protected Health Information) elements removed from input before processing?
  - [ ] Names removed or anonymized
  - [ ] SSN/MRN removed or anonymized
  - [ ] Phone numbers removed or anonymized
  - [ ] Email addresses removed or anonymized
  - [ ] Address information removed or anonymized

### Data Storage
- [ ] Extracted data encrypted at rest
- [ ] Extracted data encrypted in transit
- [ ] Access logs maintained for all data access
- [ ] Data retention policies documented and enforced

### Compliance Checklist
- [ ] HIPAA Business Associate Agreement (BAA) signed if required
- [ ] GDPR Data Processing Agreement (DPA) signed for EU data
- [ ] State privacy laws (CCPA, etc.) addressed

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 2. Bias and Fairness Assessment

### Demographic Testing
- [ ] Extraction tested across demographics (age, gender, race, ethnicity)
- [ ] Performance metrics tracked by demographic group
- [ ] Disparities identified and documented

### Bias Detection Results

| Demographic | Extraction Accuracy | Issues Identified | Mitigation |
|---|---|---|---|
| Age 18-40 | ___% | | |
| Age 40-60 | ___% | | |
| Age 60+ | ___% | | |
| Male | ___% | | |
| Female | ___% | | |
| Other | ___% | | |

### Potential Bias Sources
- [ ] Training data biases documented
- [ ] Annotation bias reviewed
- [ ] Language model bias assessed
- [ ] Clinical guideline bias considered

### Mitigation Strategies
- [ ] Retraining with balanced datasets
- [ ] Regular performance audits
- [ ] Fairness constraints applied
- [ ] Human-in-the-loop review process

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 3. Regulatory Compliance Assessment

### HIPAA Requirements
- [ ] Minimum necessary principle applied (only extract needed data)
- [ ] Access controls implemented
- [ ] Audit controls in place
- [ ] Transmission security enabled
- [ ] Business Associate Agreement reviewed

### GDPR Requirements (if processing EU data)
- [ ] Lawful basis documented (consent, contract, legal obligation, etc.)
- [ ] Data subject rights procedures established
- [ ] Data Protection Impact Assessment (DPIA) completed
- [ ] Data Processing Agreement signed
- [ ] Data retention limits enforced

### FDA Compliance (if clinical decision support)
- [ ] Algorithm validation and verification completed
- [ ] Clinical validation studies performed
- [ ] Risk classification determined
- [ ] Appropriate regulatory pathway selected

### Other Regulatory Requirements
- [ ] State privacy laws reviewed and addressed
- [ ] International data transfer restrictions assessed
- [ ] Industry-specific regulations identified

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 4. Audit Trail and Transparency

### System Logging
- [ ] All extraction operations logged with timestamps
- [ ] User/system identity recorded for each operation
- [ ] Extraction parameters documented
- [ ] Data lineage tracked

### Audit Trail Contents
- [ ] Date and time of extraction
- [ ] User/system identifier
- [ ] Clinical note identifier
- [ ] Extraction method used
- [ ] Extracted entities and confidence scores
- [ ] Risk assessment results
- [ ] Any manual overrides or corrections

### Audit Trail Review
- [ ] Logs retained for minimum legal hold period (typically 6-7 years)
- [ ] Regular audit trail reviews conducted (frequency: ______)
- [ ] Anomalies detected and investigated
- [ ] Access to audit logs restricted to authorized personnel

### Transparency Documentation
- [ ] Algorithm documentation available to clinicians
- [ ] Confidence scores provided with extractions
- [ ] Model limitations clearly stated
- [ ] Update history maintained

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 5. Clinical Validation

### Accuracy Assessment
- [ ] Precision (% of extractions correct): ____%
- [ ] Recall (% of actual entities found): ____%
- [ ] F1-Score (harmonic mean): ____%
- [ ] Accuracy targets met: ☐ Yes ☐ No

### Comparative Validation
- [ ] Performance vs. clinician manual extraction: ✓ Acceptable ☐ Unacceptable
- [ ] Performance vs. competing systems: ✓ Acceptable ☐ Unacceptable
- [ ] Domain-specific validation completed: ✓ Yes ☐ No

### Edge Cases
- [ ] Rare conditions tested: ✓ Yes ☐ No
- [ ] Contradictory/conflicting information handled: ✓ Yes ☐ No
- [ ] Incomplete clinical notes processed: ✓ Yes ☐ No
- [ ] Multiple medical conditions extracted correctly: ✓ Yes ☐ No

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 6. Model Interpretability

### Explainability
- [ ] System provides reasoning for extractions
- [ ] Confidence scores provided with all extractions
- [ ] Contributing factors identified (which words/phrases drove the decision)
- [ ] Model behavior documented

### Clinician Understanding
- [ ] Clinicians trained on system outputs
- [ ] Limitations clearly communicated
- [ ] Override procedures established and documented
- [ ] Human review process defined

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 7. Incident Response

### Procedures in Place
- [ ] Incident response plan documented
- [ ] Emergency contact information established
- [ ] System rollback procedures defined
- [ ] Patient notification procedures established

### Adverse Events
- [ ] Adverse event reporting mechanism in place
- [ ] Regular review of adverse events
- [ ] Corrective actions implemented
- [ ] FDA MedWatch reporting considered if applicable

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## 8. Vendor Management (if using third-party systems)

- [ ] Vendor security certifications reviewed (SOC 2, ISO 27001, etc.)
- [ ] Contracts include data protection provisions
- [ ] Subprocessors identified and approved
- [ ] Regular security assessments conducted
- [ ] Business continuity and disaster recovery plans reviewed

**Risk Level**: ☐ Low ☐ Medium ☐ High ☐ Critical

**Notes**:
```
[Add assessment notes here]
```

---

## Summary Risk Assessment

### Overall Risk Level Determination

| Section | Risk Level | Critical Issues |
|---|---|---|
| Data Privacy | | |
| Bias & Fairness | | |
| Regulatory Compliance | | |
| Audit Trail | | |
| Clinical Validation | | |
| Interpretability | | |
| Incident Response | | |
| Vendor Management | | |

### Overall Risk Rating

**OVERALL RISK LEVEL: ☐ LOW ☐ MEDIUM ☐ HIGH ☐ CRITICAL**

### Recommended Actions

**Before Production Deployment:**
- [ ] Action 1: _________________________________
- [ ] Action 2: _________________________________
- [ ] Action 3: _________________________________

**Ongoing Monitoring:**
- [ ] Monitoring 1: _________________________________
- [ ] Monitoring 2: _________________________________
- [ ] Monitoring 3: _________________________________

---

## Sign-Off

| Role | Name | Signature | Date |
|---|---|---|---|
| Clinical Informatics Lead | | | |
| Compliance Officer | | | |
| Privacy Officer | | | |
| IT Security Lead | | | |
| Clinical Department Head | | | |

---

## Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | | Initial assessment |
| | | | |

---

## References

- HIPAA Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/
- GDPR: https://gdpr-info.eu/
- FDA Software as a Medical Device (SaMD): https://www.fda.gov/medical-devices/software-medical-device-samd
- NIH Bias in AI: https://www.nih.gov/about-nih/what-we-do/nih-health-equity-research-policy
- CMS Guidelines: https://www.cms.gov/

---

**Document Classification**: [Confidential / Internal Use / Public]

**Effective Date**: ____________________

**Next Review Date**: ____________________

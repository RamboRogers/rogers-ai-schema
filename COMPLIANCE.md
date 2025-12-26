# Rogers-AI-Schema - Compliance Mapping Guide

**Author**: Matthew Rogers, CISSP
**Title**: Field CTO for AI and Security at VAST Data
**License**: GNU General Public License v3.0
**Links**: [LinkedIn](https://www.linkedin.com/in/matthewrogerscissp/) | [Twitter/X](https://x.com/Matthewrogers) | [GitHub](https://github.com/RamboRogers/) | [Website](https://matthewrogers.org)

This document maps each field in the Rogers-AI-Schema to specific regulatory requirements from NIST AI-600 (AI Risk Management Framework), EU AI Act, and GDPR.

## Table of Contents

1. [Compliance Overview](#compliance-overview)
2. [NIST AI-600 Mapping](#nist-ai-600-mapping)
3. [EU AI Act Mapping](#eu-ai-act-mapping)
4. [GDPR Mapping](#gdpr-mapping)
5. [Compliance Workflows](#compliance-workflows)
6. [Audit and Reporting](#audit-and-reporting)
7. [Privacy Impact Assessment](#privacy-impact-assessment)

---

## Compliance Overview

**Schema Version:** 1.0.0-tier1
**Regulatory Frameworks Addressed:**
- NIST AI Risk Management Framework (AI-600)
- EU Artificial Intelligence Act (Regulation 2024/1689)
- General Data Protection Regulation (GDPR) (Regulation 2016/679)

**Compliance Posture:**

| Framework | Coverage Level | Notes |
|-----------|---------------|-------|
| NIST AI-600 | Tier 1 Complete | GOVERN, MAP, MEASURE, MANAGE functions addressed |
| EU AI Act Articles 10-14 | Tier 1 Complete | Data governance, transparency, logging, human oversight (basic) |
| GDPR | Tier 1 Complete | Data subject rights, legal basis, retention, erasure |

---

## NIST AI-600 Mapping

The NIST AI Risk Management Framework organizes AI risk management into four functions: GOVERN, MAP, MEASURE, and MANAGE.

### GOVERN Function - Data Governance & Accountability

**GOVERN 1.1**: Legal and regulatory requirements are understood and managed

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| LegalBasisForProcessing | Document legal justification for data processing | Aligns with regulatory requirements |
| CopyrightStatus | Track IP and licensing requirements | Legal compliance |
| LicenseType | Specific license tracking | Ensure legal use |
| UsageRestrictions | Document legal restrictions | Prevent unauthorized use |
| ApplicableJurisdictions (Tier 2) | Track regulatory jurisdictions | Future enhancement |

**GOVERN 1.2**: Organizational roles and responsibilities are defined and documented

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| InsertUser | User accountability for data creation | Responsibility tracking |
| UpdateUser | User accountability for modifications | Change responsibility |
| DataValidatedBy | Quality assurance responsibility | Validation accountability |
| AllowedRoles | Role-based access control | Define who can access data |

**GOVERN 1.3**: Processes and procedures are in place for third-party risk management

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| OriginalSourceType | Track data provenance from third parties | Third-party data tracking |
| DataLineageChain | Full chain of custody | Supplier risk management |
| DocumentEmbeddingURL01-05 | Track third-party AI services | Vendor management |

**GOVERN 1.6**: Policies and procedures are in place for data governance

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| DatasetType | Categorize data by purpose | Policy enforcement |
| DatasetPurpose | Document intended use | Purpose limitation |
| DataQualityScore | Track data quality metrics | Quality governance |
| DataValidationStatus | Validation workflow | Quality assurance process |
| DataRetentionPeriod | Retention policy enforcement | Data lifecycle governance |
| DeletionScheduledDate | Scheduled deletion per policy | Automated compliance |

### MAP Function - Risk Identification

**MAP 1.1**: Context is established and understood

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| SourceDocumentAuthor | Understand data creator | Context establishment |
| SourceDocumentOrganization | Organizational context | Provenance |
| DatasetPurpose | Intended use case | Purpose documentation |

**MAP 1.2**: Categorization of the AI system

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| RiskLevel | Risk classification of data | Low, Medium, High, Critical |
| SensitiveDataClassification | Data sensitivity categorization | Risk-based approach |
| AccessControlLevel | Access restrictions based on sensitivity | Security categorization |

**MAP 1.5**: Impacts to individuals, groups, communities, and society are characterized

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| ContainsPII | Identify impact on individuals | Personal data indicator |
| PIITypes | Specific types of personal data | Granular impact assessment |
| SensitiveDataClassification | Level of sensitivity | Impact severity |

### MEASURE Function - Performance and Risk Metrics

**MEASURE 2.1**: Test datasets are developed and applied to evaluate AI system performance

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| DatasetType | Distinguish Training/Validation/Testing | Dataset separation |
| DataQualityScore | Quantitative quality metric | Performance measurement |

**MEASURE 2.3**: AI system performance is evaluated, and results are documented

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| DataValidationStatus | Track validation outcomes | Performance documentation |
| DataValidationDate | When evaluation occurred | Temporal tracking |
| ContentSafetyScore | Safety performance metric | Safety measurement |

### MANAGE Function - Risk Response and Monitoring

**MANAGE 1.1**: Risk treatment is prioritized and implemented

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| RiskLevel | Identify priority for treatment | Risk prioritization |
| ContentSafetyStatus | Track content moderation actions | Safety risk management |
| AccessControlLevel | Implement access restrictions | Risk mitigation control |

**MANAGE 2.1**: Mechanisms are in place for addressing AI risks

| Field | Purpose | Compliance Notes |
|-------|---------|------------------|
| PIIDetectionMethod | Automated privacy risk detection | Privacy risk mechanism |
| AnonymizationStatus | Privacy protection mechanism | De-identification tracking |
| DeletionStatus | Data deletion mechanism | Erasure capability |

---

## EU AI Act Mapping

The EU Artificial Intelligence Act establishes harmonized rules for AI systems, with specific requirements for high-risk AI systems.

### Article 9 - Risk Management System

**Requirement**: Establish and maintain a risk management system

| Field | Purpose | Article 9 Compliance |
|-------|---------|---------------------|
| RiskLevel | Risk classification per system | Section 9.2(a) - Risk identification |
| ContentSafetyStatus | Monitor content risks | Section 9.2(b) - Risk estimation |
| ContentSafetyScore | Quantify safety risks | Section 9.2(b) - Risk evaluation |
| SensitiveDataClassification | Data-related risks | Section 9.2(a) - Identify risks |

### Article 10 - Data and Data Governance

**Section 10.2**: Training, validation, and testing datasets shall be relevant, representative, and free of errors

| Field | Purpose | Article 10 Compliance |
|-------|---------|----------------------|
| DatasetType | Distinguish dataset purposes | Section 10.2 - Dataset categorization |
| DataQualityScore | Measure data quality | Section 10.2 - Error-free requirement |
| DataValidationStatus | Track validation | Section 10.2 - Validation requirement |
| DataValidationDate | When validation occurred | Section 10.2 - Validation documentation |
| DataValidatedBy | Who performed validation | Section 10.2 - Accountability |

**Section 10.3**: Datasets shall be relevant, representative, and free from bias

| Field | Purpose | Article 10 Compliance |
|-------|---------|----------------------|
| DatasetPurpose | Ensure relevance | Section 10.3 - Relevance requirement |
| DataLineageChain | Provenance tracking | Section 10.3 - Understand data characteristics |
| OriginalSourceType | Source transparency | Section 10.3 - Data properties |
| BiasAssessmentPerformed (Tier 2) | Bias detection | Section 10.3 - Bias-free requirement |

**Section 10.5**: Processing of special categories of personal data

| Field | Purpose | Article 10 Compliance |
|-------|---------|----------------------|
| ContainsPII | Identify personal data | Section 10.5 - Special category detection |
| PIITypes | Specific PII categories | Section 10.5 - Granular classification |
| SensitiveDataClassification | Sensitivity level | Section 10.5 - Special data protection |
| LegalBasisForProcessing | Legal justification | Section 10.5 - Lawful processing |

### Article 11 - Technical Documentation

**Requirement**: Technical documentation shall be drawn up and kept up to date

| Field | Purpose | Article 11 Compliance |
|-------|---------|----------------------|
| Rogers-AI-Schema-Version | Schema version tracking | Annex IV - System version |
| DocumentEmbeddingModel01-05 | AI model documentation | Annex IV - AI model specifications |
| DocumentEmbeddingURL01-05 | Service endpoints | Annex IV - Technical specifications |
| DataLineageChain | Data processing documentation | Annex IV - Data flow |
| InsertDateTime, UpdateDateTime | Change history | Annex IV - Modification tracking |
| DocumentVersion | Content versioning | Annex IV - Version control |
| DocumentStatus | Lifecycle documentation | Annex IV - System lifecycle |

### Article 12 - Record-Keeping

**Section 12.1**: High-risk AI systems shall have logging capabilities

| Field | Purpose | Article 12 Compliance |
|-------|---------|----------------------|
| InsertDateTime | Creation timestamp | Section 12.1 - Automatic logging |
| UpdateDateTime | Modification timestamp | Section 12.1 - Change logging |
| InsertUser | User who created record | Section 12.1 - User identification |
| UpdateUser | User who modified record | Section 12.1 - Modification tracking |
| LastModifiedReason | Justification for changes | Section 12.1 - Event documentation |

**Note**: Access logging (read operations) should be handled via separate AUDIT_LOG table at the database layer for Section 12.1 usage logging and access accountability requirements.

**Section 12.2**: Logging shall enable traceability

| Field | Purpose | Article 12 Compliance |
|-------|---------|----------------------|
| UUID | Unique record identifier | Section 12.2 - Traceability |
| DataLineageChain | Full data lineage | Section 12.2 - Input data tracing |
| SourceDocumentHash | Immutable source reference | Section 12.2 - Traceability to source |
| DocumentChunkNumber | Chunk traceability | Section 12.2 - Data transformation tracking |

### Article 13 - Transparency and Information to Users

**Section 13.1**: High-risk AI systems shall be designed to be sufficiently transparent

| Field | Purpose | Article 13 Compliance |
|-------|---------|----------------------|
| DatasetPurpose | Explain data purpose | Section 13.1 - Purpose transparency |
| SourceDocumentSummary | Content description | Section 13.1 - Input transparency |
| DocumentEmbeddingModel01-05 | Model transparency | Section 13.1 - AI model disclosure |
| LicenseType | Usage rights transparency | Section 13.1 - Legal transparency |
| UsageRestrictions | Limitation disclosure | Section 13.1 - Restriction transparency |

### Article 14 - Human Oversight

**Section 14.4**: Measures shall enable individuals to whom human oversight is assigned to:
- (a) Fully understand AI system capabilities
- (b) Properly interpret outputs
- (c) Decide not to use the AI system

| Field | Purpose | Article 14 Compliance |
|-------|---------|----------------------|
| DataValidationStatus | Human validation tracking | Section 14.4(a) - Human review |
| DataValidatedBy | Who performed oversight | Section 14.4(a) - Oversight accountability |
| ContentModerationDate | When human review occurred | Section 14.4(b) - Output review |
| ContentSafetyStatus | Human safety determination | Section 14.4(c) - Human decision |
| LastModifiedReason | Human decision rationale | Section 14.4 - Decision documentation |

**Note**: Tier 2 fields (HumanReviewRequired, HumanReviewStatus) provide enhanced Article 14 compliance

---

## GDPR Mapping

The General Data Protection Regulation establishes requirements for processing personal data in the EU.

### Article 5 - Principles Relating to Processing

**Article 5(1)(a) - Lawfulness, Fairness, and Transparency**

| Field | Purpose | GDPR Compliance |
|-------|---------|-----------------|
| LegalBasisForProcessing | Document lawful basis | Article 6 legal basis |
| DatasetPurpose | Transparent purpose | Purpose transparency |
| PIITypes | Identify personal data | Data transparency |

**Article 5(1)(b) - Purpose Limitation**

| Field | Purpose | GDPR Compliance |
|-------|---------|-----------------|
| DatasetPurpose | Define specific purpose | Purpose limitation |
| UsageRestrictions | Limit incompatible uses | Purpose compliance |

**Article 5(1)(c) - Data Minimization**

| Field | Purpose | GDPR Compliance |
|-------|---------|-----------------|
| DatasetPurpose | Ensure data is adequate and relevant | Minimization principle |
| ContainsPII | Identify unnecessary PII | Minimize personal data |

**Article 5(1)(e) - Storage Limitation**

| Field | Purpose | GDPR Compliance |
|-------|---------|-----------------|
| DataRetentionPeriod | Enforce retention limits | Storage limitation |
| DeletionScheduledDate | Schedule deletion | Automated retention |
| DeletionStatus | Track deletion process | Retention compliance |

**Article 5(1)(f) - Integrity and Confidentiality**

| Field | Purpose | GDPR Compliance |
|-------|---------|-----------------|
| SourceDocumentHash | Data integrity verification | Integrity protection |
| AccessControlLevel | Confidentiality controls | Security measures |
| AllowedRoles | Access restrictions | Confidentiality |

### Article 6 - Lawfulness of Processing

**Requirement**: Processing must have a legal basis

| Field | Purpose | Article 6 Compliance |
|-------|---------|---------------------|
| LegalBasisForProcessing | Document legal basis | Article 6(1) - Legal grounds |
| DatasetPurpose | Specific purpose for each legal basis | Basis justification |

**Legal Basis Values:**
- Consent (6.1.a)
- Contract (6.1.b)
- Legal Obligation (6.1.c)
- Vital Interests (6.1.d)
- Public Task (6.1.e)
- Legitimate Interests (6.1.f)

### Article 9 - Processing of Special Categories

**Requirement**: Special protection for sensitive personal data

| Field | Purpose | Article 9 Compliance |
|-------|---------|---------------------|
| SensitiveDataClassification | Identify special category data | Article 9 detection |
| PIITypes | Specific sensitive data types | Granular classification |
| LegalBasisForProcessing | Additional legal basis for Article 9 | Special category justification |

### Article 17 - Right to Erasure ("Right to be Forgotten")

**Requirement**: Data subjects can request deletion

| Field | Purpose | Article 17 Compliance |
|-------|---------|----------------------|
| DeletionStatus | Track erasure requests | Erasure workflow |
| DeletionScheduledDate | Schedule deletion | Deletion timeline |
| DataRetentionPeriod | Automatic deletion | Proactive erasure |
| AnonymizationStatus | Alternative to deletion | Anonymization option |

**Erasure Workflow:**
1. Request received → DeletionStatus = 'Pending'
2. Approved → DeletionStatus = 'Scheduled', DeletionScheduledDate set
3. Executed → DeletionStatus = 'Deleted', DocumentStatus = 'Deleted'

### Article 30 - Records of Processing Activities

**Requirement**: Maintain records of all processing activities

| Field | Purpose | Article 30 Compliance |
|-------|---------|----------------------|
| InsertDateTime | When processing began | Processing timestamp |
| UpdateDateTime | When data was modified | Processing changes |
| InsertUser | Controller/processor identity | Accountability |
| UpdateUser | Who performed processing | Processing responsibility |
| DatasetPurpose | Purpose of processing | Article 30(1)(b) |
| DataRetentionPeriod | Retention timeline | Article 30(1)(f) |
| LegalBasisForProcessing | Legal basis documentation | Article 30(1)(a) |
| PIITypes | Categories of data | Article 30(1)(c) |

### Article 32 - Security of Processing

**Requirement**: Appropriate technical and organizational measures

| Field | Purpose | Article 32 Compliance |
|-------|---------|----------------------|
| AccessControlLevel | Access restrictions | Article 32(1)(b) - Confidentiality |
| AllowedRoles | Role-based access | Access control measures |
| SourceDocumentHash | Integrity verification | Article 32(1)(b) - Integrity |
| AnonymizationStatus | Pseudonymization | Article 32(1)(a) - Security measure |

---

## Compliance Workflows

### GDPR Data Subject Rights Workflow

#### Right to Access (Article 15)

**Query to retrieve all personal data for a data subject:**

```sql
SELECT *
FROM ai_documents
WHERE ContainsPII = TRUE
  AND DocumentChunkText LIKE '%subject_identifier%'
  AND DocumentStatus != 'Deleted';
```

**Required information to provide:**
- All fields where PIITypes contains relevant categories
- DatasetPurpose - why we're processing their data
- LegalBasisForProcessing - legal justification
- DataRetentionPeriod - how long we keep it
- AllowedRoles - who has access

#### Right to Erasure (Article 17)

**Step 1**: Mark for deletion
```sql
UPDATE ai_documents
SET DeletionStatus = 'Pending',
    UpdateDateTime = CURRENT_TIMESTAMP,
    UpdateUser = 'gdpr_compliance_system'
WHERE UUID = ?
  AND ContainsPII = TRUE;
```

**Step 2**: Schedule deletion (after verification)
```sql
UPDATE ai_documents
SET DeletionStatus = 'Scheduled',
    DeletionScheduledDate = CURRENT_TIMESTAMP + INTERVAL '30 days',
    UpdateDateTime = CURRENT_TIMESTAMP,
    UpdateUser = 'gdpr_compliance_officer'
WHERE UUID = ?;
```

**Step 3**: Execute deletion
```sql
UPDATE ai_documents
SET DeletionStatus = 'Deleted',
    DocumentStatus = 'Deleted',
    DocumentChunkText = NULL,  -- Redact content
    PIITypes = NULL,
    UpdateDateTime = CURRENT_TIMESTAMP,
    UpdateUser = 'automated_deletion_job'
WHERE DeletionScheduledDate <= CURRENT_TIMESTAMP
  AND DeletionStatus = 'Scheduled';
```

### NIST AI RMF Risk Assessment Workflow

#### Step 1: Identify Risks (MAP)

```sql
-- Find unassessed data
SELECT UUID, SourceDocumentName, DatasetType
FROM ai_documents
WHERE RiskLevel IS NULL
   OR RiskLevel = 'Unassessed'
ORDER BY InsertDateTime DESC;
```

#### Step 2: Classify Risks

```sql
UPDATE ai_documents
SET RiskLevel = CASE
    WHEN ContainsPII = TRUE AND SensitiveDataClassification IN ('High', 'Critical') THEN 'High'
    WHEN ContainsPII = TRUE THEN 'Medium'
    WHEN ContentSafetyScore < 50 THEN 'High'
    WHEN ContentSafetyScore < 75 THEN 'Medium'
    ELSE 'Low'
END,
UpdateDateTime = CURRENT_TIMESTAMP,
UpdateUser = 'risk_assessment_system'
WHERE RiskLevel IS NULL;
```

#### Step 3: Apply Controls (MANAGE)

```sql
-- Apply access controls based on risk
UPDATE ai_documents
SET AccessControlLevel = CASE
    WHEN RiskLevel = 'Critical' THEN 'Classified'
    WHEN RiskLevel = 'High' THEN 'Restricted'
    WHEN RiskLevel = 'Medium' THEN 'Confidential'
    ELSE AccessControlLevel  -- Keep existing
END,
AllowedRoles = CASE
    WHEN RiskLevel IN ('Critical', 'High') THEN '["admin", "compliance_officer"]'::jsonb
    ELSE AllowedRoles
END
WHERE RiskLevel IN ('Critical', 'High')
  AND AccessControlLevel NOT IN ('Classified', 'Restricted');
```

### EU AI Act Compliance Reporting

#### Article 12 - Generate Audit Log

```sql
-- Extract audit trail for specific time period
SELECT
    UUID,
    InsertDateTime,
    UpdateDateTime,
    InsertUser,
    UpdateUser,
    LastAccessedDateTime,
    LastAccessedBy,
    LastModifiedReason,
    DocumentStatus,
    DataValidationStatus
FROM ai_documents
WHERE UpdateDateTime BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY UpdateDateTime DESC;
```

#### Article 10 - Data Quality Report

```sql
-- Data quality compliance report
SELECT
    DatasetType,
    COUNT(*) as total_records,
    AVG(DataQualityScore) as avg_quality_score,
    COUNT(CASE WHEN DataValidationStatus = 'Validated' THEN 1 END) as validated_records,
    COUNT(CASE WHEN DataValidationStatus = 'Failed' THEN 1 END) as failed_validation,
    COUNT(CASE WHEN DataQualityScore >= 80 THEN 1 END) as high_quality_records
FROM ai_documents
WHERE DocumentStatus = 'Active'
GROUP BY DatasetType;
```

---

## Audit and Reporting

### Compliance Dashboards

#### Privacy Compliance Dashboard (GDPR)

**Key Metrics:**
1. **PII Inventory**: COUNT(ContainsPII = TRUE)
2. **Pending Deletions**: COUNT(DeletionStatus = 'Pending')
3. **Overdue Deletions**: COUNT(DeletionScheduledDate < TODAY AND DeletionStatus != 'Deleted')
4. **Unclassified Sensitivity**: COUNT(SensitiveDataClassification IS NULL AND ContainsPII = TRUE)
5. **Missing Legal Basis**: COUNT(LegalBasisForProcessing IS NULL AND ContainsPII = TRUE)

**Note**: Access metrics should be queried from separate AUDIT_LOG table.

**SQL Query:**
```sql
SELECT
    COUNT(*) FILTER (WHERE ContainsPII = TRUE) as pii_records,
    COUNT(*) FILTER (WHERE DeletionStatus = 'Pending') as pending_deletions,
    COUNT(*) FILTER (WHERE DeletionScheduledDate < CURRENT_TIMESTAMP AND DeletionStatus != 'Deleted') as overdue_deletions,
    COUNT(*) FILTER (WHERE SensitiveDataClassification IS NULL AND ContainsPII = TRUE) as unclassified_sensitive,
    COUNT(*) FILTER (WHERE LegalBasisForProcessing IS NULL AND ContainsPII = TRUE) as missing_legal_basis
FROM ai_documents
WHERE DocumentStatus = 'Active';
```

#### Risk Management Dashboard (NIST AI RMF)

**Key Metrics:**
1. **Risk Distribution**: COUNT by RiskLevel
2. **Unassessed Risks**: COUNT(RiskLevel IS NULL OR 'Unassessed')
3. **High-Risk Data**: COUNT(RiskLevel IN ('High', 'Critical'))
4. **Content Safety Issues**: COUNT(ContentSafetyStatus IN ('Flagged', 'Unsafe'))
5. **Data Quality**: AVG(DataQualityScore) by DatasetType

**SQL Query:**
```sql
SELECT
    RiskLevel,
    COUNT(*) as record_count,
    AVG(DataQualityScore) as avg_quality,
    COUNT(CASE WHEN ContentSafetyStatus IN ('Flagged', 'Unsafe') THEN 1 END) as safety_issues
FROM ai_documents
WHERE DocumentStatus = 'Active'
GROUP BY RiskLevel
ORDER BY
    CASE RiskLevel
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5
    END;
```

#### EU AI Act Article 10 Data Governance Report

```sql
SELECT
    DatasetType,
    COUNT(*) as total_records,
    COUNT(CASE WHEN DataValidationStatus = 'Validated' THEN 1 END) as validated,
    AVG(DataQualityScore) as avg_quality,
    COUNT(CASE WHEN DataLineageChain IS NOT NULL THEN 1 END) as with_lineage,
    COUNT(CASE WHEN ContainsPII = TRUE THEN 1 END) as contains_pii
FROM ai_documents
WHERE DocumentStatus = 'Active'
GROUP BY DatasetType;
```

### Automated Compliance Checks

#### Daily Compliance Validation

```sql
-- Find compliance gaps requiring attention
SELECT
    'Missing Legal Basis for PII' as issue_type,
    UUID,
    SourceDocumentName
FROM ai_documents
WHERE ContainsPII = TRUE
  AND LegalBasisForProcessing IS NULL
  AND DocumentStatus = 'Active'

UNION ALL

SELECT
    'Overdue Deletion' as issue_type,
    UUID,
    SourceDocumentName
FROM ai_documents
WHERE DeletionScheduledDate < CURRENT_TIMESTAMP
  AND DeletionStatus != 'Deleted'

UNION ALL

SELECT
    'Unvalidated High-Risk Data' as issue_type,
    UUID,
    SourceDocumentName
FROM ai_documents
WHERE RiskLevel IN ('High', 'Critical')
  AND DataValidationStatus != 'Validated'
  AND DocumentStatus = 'Active'

UNION ALL

SELECT
    'Missing Data Quality Score' as issue_type,
    UUID,
    SourceDocumentName
FROM ai_documents
WHERE DataQualityScore IS NULL
  AND DocumentStatus = 'Active'
  AND InsertDateTime < CURRENT_TIMESTAMP - INTERVAL '7 days';
```

---

## Privacy Impact Assessment

### GDPR Article 35 - Data Protection Impact Assessment (DPIA)

When is a DPIA required for AI systems using this schema?

**Triggers:**
1. **Systematic monitoring**: If LastAccessedDateTime shows continuous tracking
2. **Large-scale processing of special categories**: If PIITypes includes sensitive data at scale
3. **Automated decision-making**: If AI system makes decisions affecting individuals

**Schema Fields Supporting DPIA:**

| DPIA Section | Supporting Fields |
|-------------|-------------------|
| Nature of processing | DatasetType, DatasetPurpose, DocumentEmbeddingModel01-05 |
| Scope of processing | COUNT(records), PIITypes distribution |
| Context | OriginalSourceType, DataLineageChain |
| Purposes | DatasetPurpose, LegalBasisForProcessing |
| Data categories | PIITypes, SensitiveDataClassification |
| Recipients | AllowedRoles, AccessControlLevel |
| Storage period | DataRetentionPeriod, DeletionScheduledDate |
| Security measures | AccessControlLevel, AnonymizationStatus, SourceDocumentHash |
| Risks to rights | RiskLevel, ContentSafetyStatus |

**DPIA Query Template:**

```sql
-- Generate DPIA data summary
SELECT
    DatasetPurpose,
    COUNT(*) as total_records,
    COUNT(CASE WHEN ContainsPII = TRUE THEN 1 END) as pii_records,
    jsonb_agg(DISTINCT PIITypes) as pii_categories,
    AVG(DataRetentionPeriod) as avg_retention_days,
    jsonb_agg(DISTINCT AllowedRoles) as recipients,
    COUNT(CASE WHEN RiskLevel IN ('High', 'Critical') THEN 1 END) as high_risk_records
FROM ai_documents
WHERE DatasetType = 'Production'
  AND DocumentStatus = 'Active'
GROUP BY DatasetPurpose;
```

---

## Compliance Checklist

### Pre-Production Checklist

Before deploying AI system to production, verify:

- [ ] **GDPR Article 6**: All records with ContainsPII=TRUE have LegalBasisForProcessing set
- [ ] **GDPR Article 17**: DeletionScheduledDate set for all records per retention policy
- [ ] **GDPR Article 30**: InsertUser, UpdateUser, timestamps populated for all records
- [ ] **GDPR Article 32**: AccessControlLevel set appropriately for all records
- [ ] **EU AI Act Article 10**: DataValidationStatus = 'Validated' for all training data
- [ ] **EU AI Act Article 10**: DataQualityScore >= 70 for production datasets
- [ ] **EU AI Act Article 11**: DocumentEmbeddingModel fields populated with version info
- [ ] **EU AI Act Article 12**: Audit logging enabled (InsertDateTime, UpdateDateTime auto-populated)
- [ ] **NIST AI RMF MAP**: RiskLevel assigned to all records
- [ ] **NIST AI RMF MEASURE**: DataQualityScore calculated for all active records
- [ ] **Data Lineage**: DataLineageChain populated for traceability
- [ ] **Content Safety**: ContentSafetyStatus assessed for public-facing content

### Ongoing Compliance Maintenance

**Daily:**
- [ ] Process pending deletion requests (DeletionStatus = 'Pending')
- [ ] Execute scheduled deletions (DeletionScheduledDate < TODAY)
- [ ] Review content safety flags (ContentSafetyStatus = 'Flagged')

**Weekly:**
- [ ] Validate data quality scores (DataQualityScore < 70)
- [ ] Review unvalidated records (DataValidationStatus = 'Pending')
- [ ] Audit access logs (LastAccessedDateTime, LastAccessedBy)

**Monthly:**
- [ ] Generate GDPR Article 30 processing records report
- [ ] Review and update risk classifications (RiskLevel)
- [ ] Compliance dashboard review (PII inventory, deletion backlog)
- [ ] License compliance audit (LicenseType, UsageRestrictions)

**Quarterly:**
- [ ] Data Protection Impact Assessment (DPIA) review
- [ ] NIST AI RMF risk assessment update
- [ ] EU AI Act Article 10 data quality report
- [ ] Audit trail completeness verification

---

## Related Documentation

- [DESIGN.md](DESIGN.md) - Complete schema specification (single table, 52 fields)
- [future/TIER2_TIER3_ROADMAP.md](future/TIER2_TIER3_ROADMAP.md) - Future enhancements

### Database Platform Guides

- [platforms/POSTGRESQL.md](platforms/POSTGRESQL.md) - PostgreSQL implementation
- [platforms/SQLITE_VECTOR.md](platforms/SQLITE_VECTOR.md) - SQLite with sqlite-vec extension

# Rogers-AI-Schema - Tier 2 & Tier 3 Enhancement Roadmap

**Author**: Matthew Rogers, CISSP
**Title**: Field CTO for AI and Security at VAST Data
**License**: GNU General Public License v3.0
**Repository**: [github.com/RamboRogers/rogers-ai-schema](https://github.com/RamboRogers/rogers-ai-schema)

This document outlines future enhancements to the Rogers-AI-Schema beyond the Tier 1 implementation, providing a phased approach to comprehensive AI compliance and operational excellence.

## Table of Contents

1. [Overview](#overview)
2. [Tier 2 Enhancements](#tier-2-enhancements)
3. [Tier 3 Enhancements](#tier-3-enhancements)
4. [Implementation Strategy](#implementation-strategy)
5. [Migration Planning](#migration-planning)

---

## Overview

### Current State: Tier 1 (54 fields)

**Focus**: Core compliance and privacy protection
- Privacy & PII protection (GDPR compliant)
- Data governance & lineage (NIST AI RMF)
- Legal & licensing tracking
- Risk management & content safety
- Basic access control
- Enhanced audit trail
- Document lifecycle management

**Coverage**:
- ✅ NIST AI-600: GOVERN, MAP, MEASURE, MANAGE (basic)
- ✅ EU AI Act: Articles 10-14 (core requirements)
- ✅ GDPR: Data subject rights, legal basis, retention

### Future State Goals

**Tier 2** (~30 additional fields → ~84 total):
- Enhanced RAG-specific metadata
- Improved human oversight capabilities
- Performance and retrieval tracking
- Bias detection and fairness metrics
- Advanced embedding management

**Tier 3** (~30 additional fields → ~114 total):
- Advanced analytics and monitoring
- Cost tracking and optimization
- Jurisdictional and cross-border compliance
- Explainability and interpretability
- Business context and operational metadata

---

## Tier 2 Enhancements

### Priority: Operational Excellence & Enhanced Compliance

**Target**: Production RAG systems requiring performance monitoring and enhanced oversight

**Total New Fields**: ~30 (bringing total to ~84 fields)

---

### Category 1: RAG-Specific Chunking Metadata (8 fields)

**Business Value**: Optimize retrieval quality, enable chunk strategy experimentation, improve reconstruction

| Field Name | Type | Description | Use Case |
|------------|------|-------------|----------|
| ChunkingStrategy | VARCHAR(50) | Fixed, Semantic, SlidingWindow, Recursive | Track chunking approach for A/B testing |
| ChunkSize | INTEGER | Size in characters or tokens | Optimize chunk size per use case |
| ChunkOverlap | INTEGER | Overlap between chunks in chars/tokens | Tune for context preservation |
| ChunkingAlgorithm | VARCHAR(100) | Specific algorithm used | Reproducibility and debugging |
| ChunkingAlgorithmVersion | VARCHAR(20) | Algorithm version | Track algorithm changes |
| TotalChunksInDocument | INTEGER | Total chunks from source document | Document reconstruction |
| ChunkSequenceNumber | INTEGER | Position in overall document sequence | Maintain order for reconstruction |
| ChunkContext | TEXT | Surrounding context for this chunk | Improve retrieval relevance |

**Compliance Mapping**:
- EU AI Act Article 11: Technical documentation of processing methods
- NIST AI RMF MEASURE: Document processing metrics

**Example Values**:
```json
{
  "ChunkingStrategy": "Semantic",
  "ChunkSize": 512,
  "ChunkOverlap": 128,
  "ChunkingAlgorithm": "langchain.text_splitter.RecursiveCharacterTextSplitter",
  "ChunkingAlgorithmVersion": "0.1.0",
  "TotalChunksInDocument": 47,
  "ChunkSequenceNumber": 12,
  "ChunkContext": "Previous: ...introduction to AI systems. Next: ...regulatory frameworks..."
}
```

---

### Category 2: Enhanced Embedding Management (10 fields)

**Business Value**: Track embedding costs, quality, and versioning across providers

**Pattern**: 5 providers × 2 fields each

| Field Pattern | Type | Description | Use Case |
|--------------|------|-------------|----------|
| EmbeddingGenerationDate0X | TIMESTAMP | When embedding was created | Track embedding freshness |
| EmbeddingModelVersion0X | VARCHAR(50) | Specific version of model | Handle model deprecation |

**Additional Fields** (not provider-specific):

| Field Name | Type | Description | Use Case |
|------------|------|-------------|----------|
| PrimaryEmbeddingProvider | VARCHAR(10) | Which provider is primary (01-05) | Identify main embedding for retrieval |
| EmbeddingRefreshRequired | BOOLEAN | Whether re-embedding is needed | Trigger batch re-embedding jobs |
| EmbeddingRefreshReason | TEXT | Why refresh is needed | Track model upgrades |

**Compliance Mapping**:
- EU AI Act Article 11: AI model versioning and documentation
- NIST AI RMF MANAGE: Model lifecycle management

**Example Values**:
```json
{
  "EmbeddingGenerationDate01": "2025-01-15T14:30:00Z",
  "EmbeddingModelVersion01": "text-embedding-ada-002-v2",
  "EmbeddingGenerationDate02": "2025-01-15T14:35:00Z",
  "EmbeddingModelVersion02": "embed-english-v3.0",
  "PrimaryEmbeddingProvider": "01",
  "EmbeddingRefreshRequired": false,
  "EmbeddingRefreshReason": null
}
```

---

### Category 3: Human Oversight & Validation (6 fields)

**Business Value**: Enhanced EU AI Act Article 14 compliance, quality assurance

| Field Name | Type | Description | Compliance Mapping |
|------------|------|-------------|-------------------|
| HumanReviewRequired | BOOLEAN | Whether human review is required | EU AI Act Article 14 |
| HumanReviewStatus | VARCHAR(30) | Pending, InProgress, Completed, NotRequired | Oversight workflow |
| HumanReviewDate | TIMESTAMP | When human review was performed | Audit trail |
| HumanReviewedBy | VARCHAR(100) | User who performed review | Accountability |
| HumanReviewNotes | TEXT | Review notes and findings | Quality documentation |
| ValidationMethod | VARCHAR(50) | Automated, Manual, Hybrid | Process transparency |

**Allowed Values**:
- `HumanReviewStatus`: "Pending", "InProgress", "Completed", "NotRequired", "Failed"
- `ValidationMethod`: "Automated", "Manual", "Hybrid", "PeerReview", "ExpertReview"

**Compliance Mapping**:
- EU AI Act Article 14: Human oversight measures
- NIST AI RMF MEASURE: Validation documentation

**Workflow Example**:
1. High-risk content → HumanReviewRequired = TRUE, HumanReviewStatus = 'Pending'
2. Assigned to reviewer → HumanReviewStatus = 'InProgress', HumanReviewedBy set
3. Review complete → HumanReviewStatus = 'Completed', HumanReviewDate, HumanReviewNotes

---

### Category 4: Performance & Retrieval Tracking (4 fields)

**Business Value**: Measure RAG effectiveness, identify underperforming content

| Field Name | Type | Description | Use Case |
|------------|------|-------------|----------|
| RetrievalCount | INTEGER | Times this chunk was retrieved | Popularity tracking |
| SuccessfulRetrievalCount | INTEGER | Times retrieval led to actual use | Quality metric |
| AverageRelevanceScore | DECIMAL(5,2) | Average relevance when retrieved | Effectiveness measure |
| LastRetrievalDateTime | TIMESTAMP | When last retrieved | Recency tracking |

**Compliance Mapping**:
- EU AI Act Article 12: Usage logging
- NIST AI RMF MEASURE: Performance metrics

**Use Cases**:
- Identify "dead" content (low RetrievalCount) for archival
- Find high-value content (high SuccessfulRetrievalCount) for promotion
- Tune chunking strategy based on AverageRelevanceScore
- Cache frequently retrieved content (high RetrievalCount)

**Example Analytics**:
```sql
-- Find underperforming content
SELECT UUID, SourceDocumentName, RetrievalCount, AverageRelevanceScore
FROM ai_documents
WHERE RetrievalCount > 100
  AND AverageRelevanceScore < 50
  AND DocumentStatus = 'Active'
ORDER BY AverageRelevanceScore ASC;
```

---

### Category 5: Bias Detection & Fairness (5 fields)

**Business Value**: EU AI Act Article 10 bias requirements, ethical AI

| Field Name | Type | Description | Compliance Mapping |
|------------|------|-------------|-------------------|
| BiasAssessmentPerformed | BOOLEAN | Whether bias detection was run | EU AI Act Article 10 |
| BiasAssessmentDate | TIMESTAMP | When bias assessment occurred | Audit trail |
| BiasAssessedBy | VARCHAR(100) | Who/what performed assessment | Accountability |
| DetectedBiasTypes | TEXT/JSON | Types of bias detected | Transparency |
| BiasScore | DECIMAL(5,2) | Overall bias score 0-100 (lower = better) | Quantitative metric |

**DetectedBiasTypes JSON Example**:
```json
{
  "gender_bias": {"score": 12.5, "severity": "low"},
  "geographic_bias": {"score": 45.2, "severity": "medium"},
  "age_bias": {"score": 8.1, "severity": "low"}
}
```

**Compliance Mapping**:
- EU AI Act Article 10.3: Bias-free datasets
- NIST AI RMF MAP 1.x: Bias identification
- NIST AI RMF MEASURE: Fairness metrics

**Workflow**:
1. Automated bias detection → BiasAssessmentPerformed = TRUE
2. Results logged → DetectedBiasTypes, BiasScore
3. High bias flagged → RiskLevel elevated, HumanReviewRequired = TRUE

---

## Tier 3 Enhancements

### Priority: Advanced Operations & International Compliance

**Target**: Enterprise-scale systems, multi-jurisdiction deployments, cost optimization

**Total New Fields**: ~30 (bringing total to ~114 fields)

---

### Category 1: Advanced Analytics & Monitoring (6 fields)

**Business Value**: Performance optimization, anomaly detection, predictive maintenance

| Field Name | Type | Description | Use Case |
|------------|------|-------------|----------|
| PerformanceMetrics | TEXT/JSON | Various performance indicators | System optimization |
| StatisticalProperties | TEXT/JSON | Statistical characteristics of data | Data profiling |
| PerformanceAnomalies | TEXT/JSON | Detected performance anomalies | Proactive issue detection |
| ErrorRate | DECIMAL(5,2) | Percentage of errors | Quality monitoring |
| LatencyMetrics | TEXT/JSON | Response time data | Performance tuning |
| MonitoringStatus | VARCHAR(20) | Active, Paused, Disabled | Monitoring control |

**PerformanceMetrics JSON Example**:
```json
{
  "avg_retrieval_time_ms": 45.2,
  "p95_retrieval_time_ms": 120.5,
  "embedding_generation_time_ms": 230.1,
  "cache_hit_rate": 0.67,
  "error_rate": 0.002
}
```

**Use Cases**:
- SLA monitoring and alerting
- Identify slow-performing embeddings
- Optimize caching strategy
- Predictive scaling

---

### Category 2: Cost Tracking & Optimization (7 fields)

**Business Value**: ROI analysis, budget management, cost allocation

| Field Name | Type | Description | Use Case |
|------------|------|-------------|----------|
| ProcessingCost | DECIMAL(10,4) | Cost to process this record | Budget tracking |
| StorageCost | DECIMAL(10,4) | Monthly storage cost | Cost optimization |
| EmbeddingCost01-05 | DECIMAL(10,4) | Cost per embedding provider | Provider comparison |
| TotalLifetimeCost | DECIMAL(10,4) | Cumulative cost since creation | ROI calculation |
| CostCenter | VARCHAR(50) | Cost allocation | Chargeback |

**Use Cases**:
- Compare embedding provider costs
- Identify expensive low-value content for archival
- Departmental chargeback
- Budget forecasting

**Example Analytics**:
```sql
-- Cost analysis by dataset type
SELECT
    DatasetType,
    COUNT(*) as records,
    SUM(ProcessingCost) as total_processing_cost,
    SUM(StorageCost) as total_storage_cost,
    AVG(TotalLifetimeCost) as avg_lifetime_cost
FROM ai_documents
WHERE DocumentStatus = 'Active'
GROUP BY DatasetType
ORDER BY total_storage_cost DESC;
```

---

### Category 3: Jurisdictional & Cross-Border (8 fields)

**Business Value**: International compliance, data sovereignty, GDPR cross-border rules

| Field Name | Type | Description | Compliance Mapping |
|------------|------|-------------|-------------------|
| DataOriginCountry | VARCHAR(2) | ISO country code of origin | Data sovereignty |
| DataProcessingCountry | VARCHAR(2) | Where data is processed | Processing location |
| DataStorageCountry | VARCHAR(2) | Where data is stored | Storage location |
| CrossBorderTransfer | BOOLEAN | Whether data crosses borders | GDPR Chapter V |
| TransferMechanism | VARCHAR(50) | Standard Contractual Clauses, BCR, etc. | GDPR compliance |
| ApplicableJurisdictions | TEXT/JSON | All applicable legal jurisdictions | Multi-jurisdiction compliance |
| DataLocalizationRequirements | TEXT/JSON | Requirements for data location | Sovereignty compliance |
| ExportRestrictions | TEXT/JSON | Export control restrictions | Trade compliance |

**Compliance Mapping**:
- GDPR Chapter V: International transfers
- EU AI Act Article 10: Geographic considerations
- Data sovereignty laws (China, Russia, etc.)

**ApplicableJurisdictions JSON Example**:
```json
{
  "jurisdictions": ["EU", "US-CA", "US-NY", "UK"],
  "primary_jurisdiction": "EU",
  "compliance_required": ["GDPR", "CCPA", "UK-GDPR"]
}
```

---

### Category 4: Explainability & Interpretability (4 fields)

**Business Value**: AI transparency, regulatory compliance, user trust

| Field Name | Type | Description | Compliance Mapping |
|------------|------|-------------|-------------------|
| ExplainabilityLevel | VARCHAR(20) | None, Low, Medium, High | Transparency indicator |
| InterpretabilityMethods | TEXT/JSON | Methods for interpretation | Technical transparency |
| ExplanationAvailable | BOOLEAN | Whether explanation can be provided | User rights |
| TransparencyScore | DECIMAL(5,2) | Overall transparency score 0-100 | Compliance metric |

**Compliance Mapping**:
- EU AI Act Article 13: Transparency requirements
- NIST AI RMF GOVERN: Transparency documentation

**InterpretabilityMethods JSON Example**:
```json
{
  "methods": ["SHAP", "LIME", "attention_weights"],
  "explanation_format": "natural_language",
  "technical_details_available": true
}
```

---

### Category 5: Business Context & Operational Metadata (5 fields)

**Business Value**: Organizational governance, ownership clarity, operational efficiency

| Field Name | Type | Description | Use Case |
|------------|------|-------------|----------|
| DataOwner | VARCHAR(100) | Business owner of this data | Ownership clarity |
| DataSteward | VARCHAR(100) | Data steward responsible for quality | Quality accountability |
| BusinessUnit | VARCHAR(100) | Business unit this data belongs to | Organizational context |
| ProjectID | VARCHAR(100) | Project this data is part of | Project tracking |
| UseCase | VARCHAR(200) | Specific use case for this data | Purpose documentation |

**Use Cases**:
- Contact data owner for questions
- Assign stewardship responsibilities
- Cost allocation by business unit
- Project-based data lifecycle management

---

## Implementation Strategy

### Phased Rollout Approach

#### Phase 1: Tier 1 Foundation (Current)
**Timeline**: Immediate
**Focus**: Core compliance, privacy protection, basic governance
**Fields**: 54
**Effort**: 2-3 weeks implementation + testing

#### Phase 2A: Tier 2 - RAG Operations (Recommended Next)
**Timeline**: 3-6 months after Tier 1 production
**Focus**: Chunking metadata, performance tracking, retrieval optimization
**New Fields**: ~12
**Effort**: 1-2 weeks

**Includes**:
- Category 1: RAG-Specific Chunking Metadata (8 fields)
- Category 4: Performance & Retrieval Tracking (4 fields)

**Trigger**: When RAG system is stable and needs optimization

#### Phase 2B: Tier 2 - Enhanced Compliance
**Timeline**: 6-12 months after Tier 1, or upon regulatory requirement
**Focus**: Human oversight, bias detection, advanced embedding management
**New Fields**: ~18
**Effort**: 2-3 weeks

**Includes**:
- Category 2: Enhanced Embedding Management (10 fields)
- Category 3: Human Oversight & Validation (6 fields)
- Category 5: Bias Detection & Fairness (5 fields)

**Trigger**: Regulatory audit, high-risk AI designation, or ethical AI initiative

#### Phase 3A: Tier 3 - Cost Optimization
**Timeline**: 12-18 months after Tier 1, when ROI becomes priority
**Focus**: Cost tracking, analytics, performance optimization
**New Fields**: ~13
**Effort**: 2 weeks

**Includes**:
- Category 1: Advanced Analytics & Monitoring (6 fields)
- Category 2: Cost Tracking & Optimization (7 fields)

**Trigger**: Budget pressure, cost optimization initiative

#### Phase 3B: Tier 3 - International Expansion
**Timeline**: When expanding to new jurisdictions
**Focus**: Cross-border compliance, jurisdictional requirements
**New Fields**: ~12
**Effort**: 2-3 weeks

**Includes**:
- Category 3: Jurisdictional & Cross-Border (8 fields)
- Category 4: Explainability & Interpretability (4 fields)

**Trigger**: International expansion, new market entry

#### Phase 3C: Tier 3 - Enterprise Maturity
**Timeline**: 18-24 months, enterprise-wide deployment
**Focus**: Business context, organizational governance
**New Fields**: ~5
**Effort**: 1 week

**Includes**:
- Category 5: Business Context & Operational Metadata (5 fields)

**Trigger**: Enterprise-wide standardization initiative

---

### Decision Framework: Which Tier Should I Implement?

#### Implement Tier 1 If:
- ✅ You're starting a new RAG project
- ✅ You need GDPR compliance
- ✅ You're handling personal data
- ✅ You need basic risk management
- ✅ You want future-proof foundation

**Effort**: Low to Medium
**ROI**: High (compliance, risk mitigation)

#### Add Tier 2 If:
- ✅ Your RAG system is in production
- ✅ You need to optimize retrieval quality
- ✅ You're facing EU AI Act high-risk designation
- ✅ You need human oversight capabilities
- ✅ You want to detect and mitigate bias
- ✅ You need to track embedding costs across providers

**Effort**: Medium
**ROI**: High (performance, compliance, quality)

#### Add Tier 3 If:
- ✅ You're operating at enterprise scale (1M+ documents)
- ✅ You need cost optimization and chargeback
- ✅ You're expanding to multiple countries
- ✅ You need advanced analytics and monitoring
- ✅ You require explainable AI capabilities
- ✅ You have complex organizational governance

**Effort**: Medium to High
**ROI**: Medium to High (depends on scale and requirements)

---

## Migration Planning

### Database Schema Evolution

#### Adding Tier 2/3 Fields

**PostgreSQL Migration Example**:

```sql
-- Tier 2A: RAG Operations
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ChunkingStrategy VARCHAR(50);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ChunkSize INTEGER;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ChunkOverlap INTEGER;
-- ... etc

-- Add constraints
ALTER TABLE ai_documents ADD CONSTRAINT chk_chunking_strategy
  CHECK (ChunkingStrategy IN ('Fixed', 'Semantic', 'SlidingWindow', 'Recursive'));

-- Add indexes
CREATE INDEX idx_chunking_strategy ON ai_documents(ChunkingStrategy)
  WHERE ChunkingStrategy IS NOT NULL;
```

**Backward Compatibility**:
- All new fields are NULLABLE
- Applications ignore unknown fields
- Rogers-AI-Schema-Version tracks capabilities
- Old applications continue to function

#### Backfill Strategy

**Option 1: Lazy Backfill** (Recommended)
- New fields remain NULL for existing records
- Populate on next update or access
- Low impact, gradual migration

**Option 2: Batch Backfill**
- Background job processes existing records
- Populate fields in batches (1000 records at a time)
- Monitor performance impact

**Option 3: Full Reprocessing**
- Re-run ingestion pipeline for all documents
- Generate new embeddings, recalculate metrics
- High effort but ensures consistency

---

### Performance Considerations

#### Index Strategy by Tier

**Tier 1 Indexes** (Already implemented):
- ContainsPII, AccessControlLevel, DocumentStatus, RiskLevel

**Tier 2 Indexes** (Add when implementing):
- ChunkingStrategy (for chunking analysis)
- HumanReviewStatus (for workflow queries)
- BiasAssessmentPerformed (for compliance reporting)
- RetrievalCount (for popularity queries)

**Tier 3 Indexes** (Add when implementing):
- DataOriginCountry (for jurisdictional queries)
- MonitoringStatus (for operational queries)
- CostCenter (for financial reporting)

#### Storage Impact

**Per-Record Overhead Estimate**:

| Tier | Fields | Avg Storage | Notes |
|------|--------|-------------|-------|
| Tier 1 | 54 | ~5 KB | Excluding vectors and large TEXT |
| Tier 2 | +30 | +2 KB | JSON fields for metrics |
| Tier 3 | +30 | +1.5 KB | Mostly small VARCHAR fields |

**For 1M records**:
- Tier 1: ~5 GB metadata (excluding vectors)
- Tier 2: ~7 GB metadata
- Tier 3: ~8.5 GB metadata

**Vector storage dominates** (1536-dim vectors = ~6KB each × 5 providers = 30KB per record)

---

### Testing Strategy

#### Tier 2/3 Testing Checklist

- [ ] **Schema Migration**: Run on test database, verify no data loss
- [ ] **Backward Compatibility**: Ensure old queries still work
- [ ] **Application Layer**: Update models, DAL, API endpoints
- [ ] **Performance Testing**: Query performance with new indexes
- [ ] **Data Validation**: New field constraints don't block existing workflows
- [ ] **Compliance Verification**: New fields improve compliance posture
- [ ] **Rollback Plan**: Tested rollback procedure
- [ ] **Documentation**: Updated SCHEMA.md, COMPLIANCE.md

---

## Success Metrics

### Tier 2 Success Indicators

**RAG Performance**:
- ↑ AverageRelevanceScore by 15%+
- ↑ SuccessfulRetrievalCount ratio
- ↓ Dead content (low RetrievalCount)

**Compliance**:
- 100% HumanReviewRequired records reviewed within SLA
- BiasScore < 30 for all production datasets
- EU AI Act Article 14 audit passed

### Tier 3 Success Indicators

**Cost Optimization**:
- ↓ TotalLifetimeCost per record by 20%
- Cost attribution to business units established
- Optimal embedding provider selection per use case

**International Compliance**:
- CrossBorderTransfer compliance at 100%
- Data localization requirements met
- Zero jurisdictional violations

---

## Recommendations

### For Most Users: Start with Tier 1

Tier 1 provides comprehensive compliance coverage and solid foundation. Only add Tier 2/3 when:

1. **Operational Need**: Production issues require optimization
2. **Regulatory Requirement**: Audit or new regulations demand it
3. **Scale Justification**: Volume justifies the added complexity
4. **Resource Availability**: Team has capacity for enhancement

### Quick Wins from Tier 2

If you can only add a few Tier 2 fields:

**Top 5 Most Valuable**:
1. RetrievalCount - Identify popular content
2. ChunkingStrategy - Experiment with chunking
3. HumanReviewStatus - Workflow management
4. BiasScore - Ethical AI minimum
5. EmbeddingGenerationDate01 - Track embedding freshness

### Enterprise Roadmap

**Year 1**: Tier 1 foundation
**Year 2**: Tier 2A (RAG ops) + Tier 2B (compliance)
**Year 3**: Tier 3A (cost) + Tier 3B (international) as needed

---

## Related Documentation

- [../DESIGN.md](../DESIGN.md) - Complete schema specification (Tier 1: single table, 52 fields)
- [../COMPLIANCE.md](../COMPLIANCE.md) - Regulatory mapping

### Database Platform Guides

- [../platforms/POSTGRESQL.md](../platforms/POSTGRESQL.md) - PostgreSQL implementation
- [../platforms/SQLITE_VECTOR.md](../platforms/SQLITE_VECTOR.md) - SQLite with sqlite-vec extension

### Future Platform Support

Planned database platforms (Tier 2+):
- **MySQL** - JSON and vector support via InnoDB, cloud deployments (AWS RDS/Aurora)
- **SQL Server** - Azure SQL integration, columnstore indexes, Always Encrypted
- **MongoDB** - Document-oriented variant for NoSQL workloads
- **Cassandra** - Distributed variant for high-scale deployments

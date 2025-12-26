![logo](media/logo.png)

# Rogers-AI-Schema

**Universal Schema for AI Workloads with NIST AI-600 and EU AI Act Compliance**

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Schema Version](https://img.shields.io/badge/Schema-v1.0.0--tier1-green.svg)](DESIGN.md)
[![Compliance](https://img.shields.io/badge/Compliance-NIST%20AI--600%20|%20EU%20AI%20Act%20|%20GDPR-orange.svg)](COMPLIANCE.md)

## Overview

Rogers-AI-Schema is a **production-ready, compliance-first database schema** for AI and RAG (Retrieval-Augmented Generation) workloads. Designed to be database-agnostic, it provides comprehensive metadata tracking, data governance, and regulatory compliance out of the box.

### Problem Statement

Every AI application reinvents the database schema wheel:
- ❌ Missing critical compliance fields (GDPR, NIST AI-600, EU AI Act)
- ❌ Inadequate data lineage and provenance tracking
- ❌ No standardized approach to PII handling
- ❌ Constant schema rework and technical debt
- ❌ Vendor lock-in to specific vector databases

### Solution

Rogers-AI-Schema provides a **single, unified table design** with:
- ✅ **52 Tier 1 fields** covering core compliance requirements
- ✅ **Multi-provider vector support** (5 simultaneous embedding providers)
- ✅ **Complete audit trail** for NIST AI-600 compliance
- ✅ **Privacy-first design** with GDPR Article 17 (right to erasure) support
- ✅ **Database independence** - works with PostgreSQL, MySQL, SQLite, SQL Server
- ✅ **Phased enhancement path** (Tier 2/3 roadmap for advanced features)

## Quick Start

### 1. Choose Your Database Platform

<table>
<tr>
<th>Database</th>
<th>Best For</th>
<th>Implementation Guide</th>
</tr>
<tr>
<td><strong>PostgreSQL</strong></td>
<td>Enterprise production, high-scale RAG systems, cloud deployments, multi-tenancy</td>
<td><a href="platforms/POSTGRESQL.md">📘 PostgreSQL Guide</a></td>
</tr>
<tr>
<td><strong>SQLite + sqlite-vec</strong></td>
<td>Edge AI, embedded applications, mobile RAG, offline-first, single-user systems</td>
<td><a href="platforms/SQLITE_VECTOR.md">📗 SQLite Guide</a></td>
</tr>
</table>

**Note**: MySQL and SQL Server implementations are planned for future releases. See [future/TIER2_TIER3_ROADMAP.md](future/TIER2_TIER3_ROADMAP.md) for details.

### 2. Deploy the Schema

```bash
# PostgreSQL
psql -U your_user -d your_database -f platforms/postgresql.sql

# SQLite with vector extension
sqlite3 ai_documents.db < platforms/sqlite_vector.sql
```

### 3. Start Ingesting AI Data

```python
# Example: Python with PostgreSQL + pgvector
import psycopg2
import numpy as np

conn = psycopg2.connect("postgresql://localhost/ai_db")
cursor = conn.cursor()

# Example embedding from Qwen/Qwen2.5-Coder-0.5B-Instruct (1024 dimensions)
embedding_vector = np.random.rand(1024).tolist()  # Replace with actual Qwen embeddings

cursor.execute("""
    INSERT INTO ai_documents (
        InsertUser, UpdateUser,
        SourceDocumentName, DocumentChunkText,
        DocumentEmbeddingModel01, DocumentEmbeddingURL01, DocumentEmbeddingVectors01,
        ContainsPII, AccessControlLevel, DocumentStatus
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    'data_ingestion_pipeline',
    'data_ingestion_pipeline',
    'technical_documentation.pdf',
    'RAG systems combine retrieval with generation...',
    'Qwen/Qwen2.5-Coder-0.5B-Instruct',
    'https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct',
    embedding_vector,  # pgvector automatically converts list to vector type
    False,  # No PII detected
    'Internal',
    'Active'
))

conn.commit()

# Vector similarity search with pgvector
query_vector = np.random.rand(1024).tolist()  # Your query embedding

cursor.execute("""
    SELECT
        ID, SourceDocumentName, DocumentChunkText,
        DocumentEmbeddingVectors01 <=> %s::vector AS distance
    FROM ai_documents
    WHERE DocumentStatus = 'Active'
      AND ContainsPII = FALSE
    ORDER BY DocumentEmbeddingVectors01 <=> %s::vector
    LIMIT 10
""", (query_vector, query_vector))

results = cursor.fetchall()
for row in results:
    print(f"Document: {row[1]}, Distance: {row[3]}")
```

## Architecture

### Single-Table Design Philosophy

**Why a single table?**
- ✅ **Simplicity**: No complex joins, easier to understand and maintain
- ✅ **Performance**: Optimized for read-heavy RAG workloads
- ✅ **Portability**: Easily replicate across databases and environments
- ✅ **Compliance**: All metadata co-located with content for audit trails
- ✅ **Scalability**: Partition by status, dataset type, or time period as needed

### Schema Structure (52 Fields)

```
┌─────────────────────────────────────────────────────────────┐
│ ai_documents                                                │
├─────────────────────────────────────────────────────────────┤
│ Core Identity & Audit (7)                                   │
│ ├─ ID, UUID, Schema Version, Timestamps, Users              │
│                                                             │
│ Source Document Metadata (7)                                │
│ ├─ Name, Path, Hash, Title, Summary, Author, Organization   │
│                                                             │
│ Content & Chunking (2)                                      │
│ ├─ Chunk Number, Chunk Text                                 │
│                                                             │
│ Vector Embeddings (15) - 5 Providers                        │
│ ├─ Model, URL, Vectors (×5)                                 │
│                                                             │
│ Privacy & PII Protection (10) - GDPR                        │
│ ├─ PII Detection, Classification, Legal Basis, Deletion     │
│                                                             │
│ Data Governance (8) - NIST AI RMF                           │
│ ├─ Dataset Type, Quality Score, Validation, Lineage         │
│                                                             │
│ Legal & Licensing (6)                                       │
│ ├─ Copyright, License, Usage Restrictions                   │
│                                                             │
│ Risk & Safety (4) - NIST AI RMF                             │
│ ├─ Risk Level, Content Safety, Moderation                   │
│                                                             │
│ Access Control (3) - Security                               │
│ ├─ Access Level, Classification, Allowed Roles              │
│                                                             │
│ Audit Trail (1) - EU AI Act Article 12                      │
│ ├─ Last Modified Reason                                     │
│                                                             │
│ Lifecycle Management (2)                                    │
│ ├─ Status, Version                                          │
└─────────────────────────────────────────────────────────────┘
```

## Documentation

### Core Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [DESIGN.md](DESIGN.md) | Complete schema specification - single table, 52 fields, database-agnostic | All - Developers, Architects, Product Managers |
| [COMPLIANCE.md](COMPLIANCE.md) | Regulatory mapping to NIST AI-600, EU AI Act, GDPR | Compliance Officers, Legal Teams |

### Database Platform Guides

| Platform | Guide | Features |
|----------|-------|----------|
| **PostgreSQL** | [platforms/POSTGRESQL.md](platforms/POSTGRESQL.md) | pgvector REQUIRED, HNSW indexes, native vector types, enterprise scale |
| **SQLite** | [platforms/SQLITE_VECTOR.md](platforms/SQLITE_VECTOR.md) | sqlite-vec extension, FTS5, edge deployments, offline-first |

### Roadmap & Planning

| Document | Description |
|----------|-------------|
| [future/TIER2_TIER3_ROADMAP.md](future/TIER2_TIER3_ROADMAP.md) | Future enhancements (82/112 total fields) for advanced RAG operations |

## Compliance Coverage

### NIST AI Risk Management Framework (AI-600)

| Function | Coverage | Key Fields |
|----------|----------|-----------|
| **GOVERN** | ✅ Complete | LegalBasisForProcessing, DatasetPurpose, AllowedRoles |
| **MAP** | ✅ Complete | RiskLevel, SensitiveDataClassification, DatasetType |
| **MEASURE** | ✅ Complete | DataQualityScore, DataValidationStatus, ContentSafetyScore |
| **MANAGE** | ✅ Complete | AccessControlLevel, AnonymizationStatus, DeletionStatus |

### EU AI Act (Regulation 2024/1689)

| Article | Requirement | Coverage | Key Fields |
|---------|-------------|----------|-----------|
| **Article 9** | Risk management system | ✅ Complete | RiskLevel, ContentSafetyStatus |
| **Article 10** | Data and data governance | ✅ Complete | DatasetType, DataQualityScore, DataLineageChain |
| **Article 11** | Technical documentation | ✅ Complete | DocumentEmbeddingModel, DataLineageChain, DocumentVersion |
| **Article 12** | Record-keeping | ✅ Complete | InsertUser, UpdateUser, Timestamps, LastModifiedReason |
| **Article 13** | Transparency | ✅ Complete | DatasetPurpose, LicenseType, UsageRestrictions |
| **Article 14** | Human oversight | ⚠️ Basic (Tier 2 enhances) | DataValidationStatus, DataValidatedBy |

### GDPR (General Data Protection Regulation)

| Article | Requirement | Coverage | Key Fields |
|---------|-------------|----------|-----------|
| **Article 5** | Data processing principles | ✅ Complete | LegalBasisForProcessing, DataRetentionPeriod |
| **Article 6** | Lawfulness of processing | ✅ Complete | LegalBasisForProcessing |
| **Article 17** | Right to erasure | ✅ Complete | DeletionStatus, DeletionScheduledDate |
| **Article 30** | Records of processing | ✅ Complete | All audit fields |
| **Article 32** | Security of processing | ✅ Complete | AccessControlLevel, AnonymizationStatus |

## Use Cases

### Enterprise RAG Systems

```sql
-- Production knowledge base with compliance filtering
SELECT DocumentChunkText, SourceDocumentName
FROM ai_documents
WHERE DocumentStatus = 'Active'
  AND AccessControlLevel IN ('Public', 'Internal')
  AND ContainsPII = FALSE
  AND DataQualityScore >= 80
ORDER BY InsertDateTime DESC;
```

### GDPR-Compliant Data Subject Access Request

```sql
-- Retrieve all personal data for data subject rights
SELECT *
FROM ai_documents
WHERE ContainsPII = TRUE
  AND DocumentChunkText LIKE '%john.doe@example.com%'
  AND DeletionStatus != 'Deleted';
```

### Automated Data Deletion Workflow

```sql
-- Find documents scheduled for deletion
SELECT UUID, SourceDocumentName, DeletionScheduledDate
FROM ai_documents
WHERE DeletionScheduledDate <= datetime('now')
  AND DeletionStatus = 'Scheduled';

-- Execute deletion
UPDATE ai_documents
SET DeletionStatus = 'Deleted',
    DocumentStatus = 'Deleted',
    DocumentChunkText = NULL  -- Redact content
WHERE DeletionScheduledDate <= datetime('now')
  AND DeletionStatus = 'Scheduled';
```

### Multi-Provider Embedding Comparison

```sql
-- Compare retrieval quality across embedding providers
SELECT
    SourceDocumentName,
    DocumentEmbeddingModel01,
    DocumentEmbeddingModel02,
    -- Calculate semantic similarity using different providers
    vector_similarity(DocumentEmbeddingVectors01, :query_vector) AS provider1_score,
    vector_similarity(DocumentEmbeddingVectors02, :query_vector) AS provider2_score
FROM ai_documents
WHERE DocumentStatus = 'Active';
```

## Best Practices

### Data Governance

1. **Always populate audit fields**: InsertUser, UpdateUser, timestamps
2. **Set ContainsPII conservatively**: Default to TRUE if uncertain, run PII detection
3. **Document data lineage**: Populate DataLineageChain for regulatory compliance
4. **Quality gates**: Require DataQualityScore >= 70 for production datasets
5. **Version control**: Use DocumentVersion for tracking content iterations

### Privacy & Security

1. **Access control by default**: Set AccessControlLevel = 'Internal' minimum
2. **PII detection pipeline**: Automated scanning on ingestion
3. **Retention policies**: Set DataRetentionPeriod based on legal requirements
4. **Deletion workflows**: Automated jobs to enforce DeletionScheduledDate
5. **Audit logging**: Implement separate AUDIT_LOG table for read operations (see POSTGRESQL.md)

### Performance Optimization

1. **Index strategically**: ContainsPII, DocumentStatus, AccessControlLevel, RiskLevel
2. **Partition large tables**: By DocumentStatus or InsertDateTime
3. **Vector indexing**: Use platform-specific vector indexes (IVFFlat, HNSW, sqlite-vec)
4. **Batch operations**: Use transactions for bulk inserts (100x speedup)
5. **Read replicas**: Separate read-heavy RAG queries from write operations

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas for contribution:**
- Additional database platform guides (MongoDB, Cassandra, Oracle)
- Tier 2/3 field implementations
- Industry-specific compliance mappings (HIPAA, SOC 2, ISO 27001)
- Language-specific SDKs and ORMs
- Vector database integration examples

## Roadmap

### Version 1.0.0 (Current - Tier 1)
- ✅ 52 core compliance fields
- ✅ PostgreSQL, SQLite, MySQL, SQL Server support
- ✅ NIST AI-600, EU AI Act, GDPR compliance
- ✅ Multi-provider vector embeddings (5 providers)

### Version 1.1.0 (Q2 2025 - Tier 2A)
- 🔄 RAG-specific chunking metadata (+12 fields)
- 🔄 Performance tracking and retrieval metrics (+4 fields)
- 🔄 MongoDB and Cassandra support

### Version 1.2.0 (Q3 2025 - Tier 2B)
- 📋 Enhanced embedding management (+10 fields)
- 📋 Human oversight and validation workflows (+6 fields)
- 📋 Bias detection and fairness metrics (+5 fields)

### Version 2.0.0 (Q4 2025 - Tier 3)
- 📋 Advanced analytics and monitoring (+30 fields)
- 📋 Cost tracking and optimization
- 📋 Multi-jurisdiction support
- 📋 Explainability and interpretability

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE) - Free for commercial and non-commercial use with GPLv3 terms.

---

### 👤 Author

**Matthew Rogers, CISSP**
*Field CTO for AI and Security at [VAST Data](https://vastdata.com)*

#### Connect & Follow

<table>
<tr>
<td align="center" width="25%">
<a href="https://www.linkedin.com/in/matthewrogerscissp/">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
</a>
</td>
<td align="center" width="25%">
<a href="https://x.com/Matthewrogers">
<img src="https://img.shields.io/badge/Twitter/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Twitter/X"/>
</a>
</td>
<td align="center" width="25%">
<a href="https://github.com/RamboRogers/">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
</a>
</td>
<td align="center" width="25%">
<a href="https://matthewrogers.org">
<img src="https://img.shields.io/badge/Website-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website"/>
</a>
</td>
</tr>
</table>

## Citation

If you use Rogers-AI-Schema in your research or production systems, please cite:

```bibtex
@software{rogers_ai_schema,
  title = {Rogers-AI-Schema: Universal Schema for AI Workloads},
  author = {Rogers, Matthew},
  year = {2025},
  version = {1.0.0-tier1},
  url = {https://github.com/RamboRogers/rogers-ai-schema},
  note = {Author: Matthew Rogers}
}
```

## Support

- 💬 Discussions: [GitHub Discussions](https://github.com/RamboRogers/rogers-ai-schema/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/RamboRogers/rogers-ai-schema/issues)
- 📧 Contact: [matthewrogers.org](https://matthewrogers.org)

---

**Built with ❤️ for the AI engineering community**

*Rogers-AI-Schema is designed to be the last database schema you'll need for AI workloads.*

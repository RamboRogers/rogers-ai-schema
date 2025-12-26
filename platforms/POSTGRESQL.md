# Rogers-AI-Schema - PostgreSQL Implementation Guide

**Author**: Matthew Rogers, CISSP
**Title**: Field CTO for AI and Security at VAST Data
**License**: GNU General Public License v3.0
**Repository**: [github.com/RamboRogers/rogers-ai-schema](https://github.com/RamboRogers/rogers-ai-schema)

Complete guide for implementing Rogers-AI-Schema Tier 1 on PostgreSQL with pgvector extension for enterprise vector search, RAG systems, and production AI workloads.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Migration Checklist](#pre-migration-checklist)
3. [PostgreSQL Migration](#postgresql-migration)
5. [Data Migration Strategies](#data-migration-strategies)
6. [Performance Optimization](#performance-optimization)
7. [Testing and Validation](#testing-and-validation)
8. [Rollback Procedures](#rollback-procedures)
9. [Application Layer Updates](#application-layer-updates)

---

## Prerequisites

### Required PostgreSQL Version

**Minimum:** PostgreSQL 12
**Recommended:** PostgreSQL 15+ (for improved vector performance)

```bash
# Check PostgreSQL version
psql --version

# Expected output:
# psql (PostgreSQL) 15.x
```

### Install pgvector Extension

**REQUIRED**: The pgvector extension must be installed for vector similarity search.

#### Option 1: Install from Package Manager (Recommended)

```bash
# Ubuntu/Debian
sudo apt install postgresql-15-pgvector

# macOS (Homebrew)
brew install pgvector

# Verify installation
psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

#### Option 2: Build from Source

```bash
# Clone pgvector repository
git clone --branch v0.7.4 https://github.com/pgvector/pgvector.git
cd pgvector

# Build and install
make
sudo make install

# Enable in your database
psql -U postgres -d your_database -c "CREATE EXTENSION vector;"
```

#### Verify pgvector Installation

```sql
-- Connect to your database
psql -U postgres -d your_database

-- Check if vector extension is available
SELECT * FROM pg_available_extensions WHERE name = 'vector';

-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify it's loaded
\dx

-- Test vector operations
SELECT '[1,2,3]'::vector;
```

### Supported Vector Dimensions

pgvector supports vectors up to **16,000 dimensions** (default limit: 2,000).

Common embedding model dimensions:
- **Qwen/Qwen2.5-Coder-0.5B-Instruct**: 1024 dimensions
- **OpenAI text-embedding-ada-002**: 1536 dimensions
- **sentence-transformers (base)**: 768 dimensions
- **all-MiniLM-L6-v2**: 384 dimensions
- **Custom/large models**: Up to 2048+ dimensions

---

## Pre-Migration Checklist

### Planning Phase

- [ ] **Backup Database**: Full backup before any schema changes
- [ ] **Document Current Schema**: Export current schema definition
- [ ] **Identify Dependencies**: Map all applications using the database
- [ ] **Downtime Window**: Schedule maintenance window if needed
- [ ] **Test Environment**: Set up identical test database
- [ ] **Rollback Plan**: Document rollback procedure
- [ ] **Team Communication**: Notify all stakeholders
- [ ] **Performance Baseline**: Capture current performance metrics

### Environment Assessment

- [ ] **Database Version**: PostgreSQL 12+ (15+ recommended)
- [ ] **Storage Available**: Ensure sufficient storage (estimate +20% for new fields + indexes + vector data)
- [ ] **Permissions**: Verify DDL permissions and CREATE EXTENSION privilege
- [ ] **pgvector Extension**: **REQUIRED** - Install pgvector extension (see [Prerequisites](#prerequisites))
- [ ] **Character Set**: Verify UTF-8 encoding for international character support

### Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Schema migration failure | High | Test on replica first, have rollback script ready |
| Performance degradation | Medium | Add indexes incrementally, monitor query performance |
| Application breaking changes | High | Update application layer before migration, use feature flags |
| Storage exhaustion | Medium | Monitor storage, provision additional capacity |
| Downtime exceeds window | Medium | Perform migration in phases, use online DDL where possible |

---

## PostgreSQL Migration

### Step 1: Create Table (New Installation)

**File**: `platforms/postgresql.sql`

```sql
-- Rogers-AI-Schema Tier 1 - PostgreSQL Implementation
-- Version: 1.0.0-tier1
-- Database: PostgreSQL 12+
-- Extension: pgvector REQUIRED for vector operations

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

BEGIN;

CREATE TABLE IF NOT EXISTS ai_documents (
    -- ============================================
    -- Core Identity & Audit (7 fields)
    -- ============================================
    ID BIGSERIAL PRIMARY KEY,
    UUID UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    "Rogers-AI-Schema-Version" VARCHAR(20) NOT NULL DEFAULT '1.0.0-tier1',
    InsertDateTime TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdateDateTime TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    InsertUser VARCHAR(100) NOT NULL,
    UpdateUser VARCHAR(100) NOT NULL,

    -- ============================================
    -- Source Document Metadata (7 fields)
    -- ============================================
    SourceDocumentName VARCHAR(500),
    SourceDocumentPath TEXT,
    SourceDocumentHash VARCHAR(128),
    SourceDocumentTitle VARCHAR(1000),
    SourceDocumentSummary TEXT,
    SourceDocumentAuthor VARCHAR(500),
    SourceDocumentOrganization VARCHAR(500),

    -- ============================================
    -- Document Content & Chunking (2 fields)
    -- ============================================
    DocumentChunkNumber INTEGER CHECK (DocumentChunkNumber >= 1),
    DocumentChunkText TEXT,

    -- ============================================
    -- Vector Embeddings - 5 Providers (15 fields)
    -- ============================================
    DocumentEmbeddingModel01 VARCHAR(200),
    DocumentEmbeddingURL01 TEXT,
    DocumentEmbeddingVectors01 vector(1024),  -- e.g., Qwen/Qwen2.5-Coder-0.5B-Instruct (1024 dims)

    DocumentEmbeddingModel02 VARCHAR(200),
    DocumentEmbeddingURL02 TEXT,
    DocumentEmbeddingVectors02 vector(1536),  -- e.g., OpenAI text-embedding-ada-002 (1536 dims)

    DocumentEmbeddingModel03 VARCHAR(200),
    DocumentEmbeddingURL03 TEXT,
    DocumentEmbeddingVectors03 vector(768),   -- e.g., sentence-transformers (768 dims)

    DocumentEmbeddingModel04 VARCHAR(200),
    DocumentEmbeddingURL04 TEXT,
    DocumentEmbeddingVectors04 vector(384),   -- e.g., all-MiniLM-L6-v2 (384 dims)

    DocumentEmbeddingModel05 VARCHAR(200),
    DocumentEmbeddingURL05 TEXT,
    DocumentEmbeddingVectors05 vector(2048),  -- e.g., custom/large models (2048 dims)

    -- ============================================
    -- Privacy & PII Protection (10 fields)
    -- ============================================
    ContainsPII BOOLEAN NOT NULL DEFAULT FALSE,
    PIITypes JSONB,
    PIIDetectionMethod VARCHAR(50) CHECK (PIIDetectionMethod IN ('automated', 'manual', 'both', 'not_detected')),
    PIIDetectionDate TIMESTAMP WITH TIME ZONE,
    SensitiveDataClassification VARCHAR(20) CHECK (SensitiveDataClassification IN ('None', 'Low', 'Medium', 'High', 'Critical')),
    LegalBasisForProcessing VARCHAR(50) CHECK (LegalBasisForProcessing IN ('Consent', 'Contract', 'LegalObligation', 'VitalInterests', 'PublicTask', 'LegitimateInterests')),
    DataRetentionPeriod INTEGER CHECK (DataRetentionPeriod > 0),
    DeletionScheduledDate TIMESTAMP WITH TIME ZONE,
    DeletionStatus VARCHAR(20) CHECK (DeletionStatus IN ('Pending', 'Scheduled', 'Deleted', 'Retained', 'AwaitingApproval')),
    AnonymizationStatus VARCHAR(30) CHECK (AnonymizationStatus IN ('NotAnonymized', 'Pseudonymized', 'FullyAnonymized')),

    -- ============================================
    -- Data Governance & Lineage (8 fields)
    -- ============================================
    DatasetType VARCHAR(30) CHECK (DatasetType IN ('Training', 'Validation', 'Testing', 'Production', 'KnowledgeBase', 'Archive')),
    DatasetPurpose TEXT,
    DataQualityScore NUMERIC(5,2) CHECK (DataQualityScore BETWEEN 0 AND 100),
    DataValidationStatus VARCHAR(20) CHECK (DataValidationStatus IN ('Pending', 'Validated', 'Failed', 'NeedsReview', 'InProgress')),
    DataValidationDate TIMESTAMP WITH TIME ZONE,
    DataValidatedBy VARCHAR(100),
    DataLineageChain JSONB,
    OriginalSourceType VARCHAR(50) CHECK (OriginalSourceType IN ('Web', 'Database', 'API', 'FileSystem', 'Manual', 'Email', 'S3', 'SharePoint', 'Other')),

    -- ============================================
    -- Legal & Licensing Tracking (6 fields)
    -- ============================================
    CopyrightStatus VARCHAR(30) CHECK (CopyrightStatus IN ('PublicDomain', 'Copyrighted', 'CreativeCommons', 'Unknown', 'ProprietaryInternal')),
    LicenseType VARCHAR(100),
    UsageRestrictions TEXT,
    CommercialUseAllowed BOOLEAN,
    AttributionRequired BOOLEAN,
    AttributionText TEXT,

    -- ============================================
    -- Risk Management & Content Safety (4 fields)
    -- ============================================
    RiskLevel VARCHAR(20) CHECK (RiskLevel IN ('Low', 'Medium', 'High', 'Critical', 'Unassessed')),
    ContentSafetyStatus VARCHAR(20) CHECK (ContentSafetyStatus IN ('Safe', 'Flagged', 'Unsafe', 'UnderReview', 'NotAssessed')),
    ContentSafetyScore NUMERIC(5,2) CHECK (ContentSafetyScore BETWEEN 0 AND 100),
    ContentModerationDate TIMESTAMP WITH TIME ZONE,

    -- ============================================
    -- Access Control & Security (3 fields)
    -- ============================================
    AccessControlLevel VARCHAR(20) NOT NULL DEFAULT 'Internal' CHECK (AccessControlLevel IN ('Public', 'Internal', 'Confidential', 'Restricted', 'Classified')),
    DataClassification VARCHAR(30),
    AllowedRoles JSONB,

    -- ============================================
    -- Enhanced Audit Trail (1 field)
    -- ============================================
    LastModifiedReason TEXT,

    -- ============================================
    -- Document Lifecycle Management (2 fields)
    -- ============================================
    DocumentStatus VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (DocumentStatus IN ('Draft', 'Active', 'Deprecated', 'Archived', 'Deleted', 'UnderReview')),
    DocumentVersion VARCHAR(20)
);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Unique indexes
CREATE UNIQUE INDEX IF NOT EXISTS idx_ai_documents_uuid ON ai_documents(UUID);

-- High-priority single-column indexes
CREATE INDEX IF NOT EXISTS idx_ai_documents_contains_pii ON ai_documents(ContainsPII);
CREATE INDEX IF NOT EXISTS idx_ai_documents_access_control ON ai_documents(AccessControlLevel);
CREATE INDEX IF NOT EXISTS idx_ai_documents_status ON ai_documents(DocumentStatus);
CREATE INDEX IF NOT EXISTS idx_ai_documents_risk_level ON ai_documents(RiskLevel);
CREATE INDEX IF NOT EXISTS idx_ai_documents_dataset_type ON ai_documents(DatasetType);
CREATE INDEX IF NOT EXISTS idx_ai_documents_deletion_scheduled ON ai_documents(DeletionScheduledDate)
    WHERE DeletionScheduledDate IS NOT NULL;

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_ai_documents_privacy_classification
    ON ai_documents(ContainsPII, SensitiveDataClassification)
    WHERE ContainsPII = TRUE;

CREATE INDEX IF NOT EXISTS idx_ai_documents_compliance_audit
    ON ai_documents(DocumentStatus, DataValidationStatus);

-- Temporal indexes for time-based queries
CREATE INDEX IF NOT EXISTS idx_ai_documents_insert_datetime ON ai_documents(InsertDateTime DESC);
CREATE INDEX IF NOT EXISTS idx_ai_documents_update_datetime ON ai_documents(UpdateDateTime DESC);

-- Vector indexes using HNSW for similarity search (cosine distance)
CREATE INDEX IF NOT EXISTS idx_ai_documents_vector01_hnsw ON ai_documents
    USING hnsw (DocumentEmbeddingVectors01 vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_ai_documents_vector02_hnsw ON ai_documents
    USING hnsw (DocumentEmbeddingVectors02 vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_ai_documents_vector03_hnsw ON ai_documents
    USING hnsw (DocumentEmbeddingVectors03 vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_ai_documents_vector04_hnsw ON ai_documents
    USING hnsw (DocumentEmbeddingVectors04 vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_ai_documents_vector05_hnsw ON ai_documents
    USING hnsw (DocumentEmbeddingVectors05 vector_cosine_ops);

-- ============================================
-- Triggers for Automatic Updates
-- ============================================

-- Auto-update UpdateDateTime on row modification
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.UpdateDateTime = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_ai_documents_modtime
    BEFORE UPDATE ON ai_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- ============================================
-- Comments for Documentation
-- ============================================

COMMENT ON TABLE ai_documents IS 'Rogers-AI-Schema v1.0.0-tier1: Universal schema for AI workloads with NIST AI-600, EU AI Act, and GDPR compliance';
COMMENT ON COLUMN ai_documents."Rogers-AI-Schema-Version" IS 'Schema version for feature detection and compatibility';
COMMENT ON COLUMN ai_documents.ContainsPII IS 'GDPR: Whether record contains personally identifiable information';
COMMENT ON COLUMN ai_documents.LegalBasisForProcessing IS 'GDPR Article 6: Legal basis for processing personal data';
COMMENT ON COLUMN ai_documents.DataRetentionPeriod IS 'GDPR Article 5(1)(e): Days to retain data before deletion';
COMMENT ON COLUMN ai_documents.RiskLevel IS 'NIST AI RMF MAP: Risk classification of data';
COMMENT ON COLUMN ai_documents.DataQualityScore IS 'NIST AI RMF MEASURE: Quality score 0-100';

COMMIT;

-- ============================================
-- Verify Installation
-- ============================================

SELECT
    'Rogers-AI-Schema v1.0.0-tier1 installed successfully' AS status,
    count(*) AS table_count
FROM information_schema.tables
WHERE table_name = 'ai_documents';
```

**Execution**:
```bash
psql -U your_user -d your_database -f platforms/postgresql.sql
```

---

### Step 2: Migrate Existing Table (Add Tier 1 Fields)

**File**: `migrate_to_tier1_postgresql.sql`

```sql
-- Migrate existing ai_documents table to Tier 1 compliance
-- IMPORTANT: Test on replica first, backup before running

BEGIN;

-- Add Rogers-AI-Schema-Version if not exists
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS "Rogers-AI-Schema-Version" VARCHAR(20) DEFAULT '1.0.0-tier1';

-- ============================================
-- Privacy & PII Protection (10 fields)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ContainsPII BOOLEAN DEFAULT FALSE NOT NULL;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS PIITypes JSONB;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS PIIDetectionMethod VARCHAR(50)
    CHECK (PIIDetectionMethod IN ('automated', 'manual', 'both', 'not_detected'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS PIIDetectionDate TIMESTAMP WITH TIME ZONE;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS SensitiveDataClassification VARCHAR(20)
    CHECK (SensitiveDataClassification IN ('None', 'Low', 'Medium', 'High', 'Critical'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS LegalBasisForProcessing VARCHAR(50)
    CHECK (LegalBasisForProcessing IN ('Consent', 'Contract', 'LegalObligation', 'VitalInterests', 'PublicTask', 'LegitimateInterests'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataRetentionPeriod INTEGER CHECK (DataRetentionPeriod > 0);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DeletionScheduledDate TIMESTAMP WITH TIME ZONE;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DeletionStatus VARCHAR(20)
    CHECK (DeletionStatus IN ('Pending', 'Scheduled', 'Deleted', 'Retained', 'AwaitingApproval'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS AnonymizationStatus VARCHAR(30)
    CHECK (AnonymizationStatus IN ('NotAnonymized', 'Pseudonymized', 'FullyAnonymized'));

-- ============================================
-- Data Governance & Lineage (8 fields)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DatasetType VARCHAR(30)
    CHECK (DatasetType IN ('Training', 'Validation', 'Testing', 'Production', 'KnowledgeBase', 'Archive'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DatasetPurpose TEXT;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataQualityScore NUMERIC(5,2) CHECK (DataQualityScore BETWEEN 0 AND 100);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataValidationStatus VARCHAR(20)
    CHECK (DataValidationStatus IN ('Pending', 'Validated', 'Failed', 'NeedsReview', 'InProgress'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataValidationDate TIMESTAMP WITH TIME ZONE;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataValidatedBy VARCHAR(100);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataLineageChain JSONB;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS OriginalSourceType VARCHAR(50)
    CHECK (OriginalSourceType IN ('Web', 'Database', 'API', 'FileSystem', 'Manual', 'Email', 'S3', 'SharePoint', 'Other'));

-- ============================================
-- Legal & Licensing Tracking (6 fields)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS CopyrightStatus VARCHAR(30)
    CHECK (CopyrightStatus IN ('PublicDomain', 'Copyrighted', 'CreativeCommons', 'Unknown', 'ProprietaryInternal'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS LicenseType VARCHAR(100);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS UsageRestrictions TEXT;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS CommercialUseAllowed BOOLEAN;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS AttributionRequired BOOLEAN;
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS AttributionText TEXT;

-- ============================================
-- Risk Management & Content Safety (4 fields)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS RiskLevel VARCHAR(20)
    CHECK (RiskLevel IN ('Low', 'Medium', 'High', 'Critical', 'Unassessed'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ContentSafetyStatus VARCHAR(20)
    CHECK (ContentSafetyStatus IN ('Safe', 'Flagged', 'Unsafe', 'UnderReview', 'NotAssessed'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ContentSafetyScore NUMERIC(5,2) CHECK (ContentSafetyScore BETWEEN 0 AND 100);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS ContentModerationDate TIMESTAMP WITH TIME ZONE;

-- ============================================
-- Access Control & Security (3 fields)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS AccessControlLevel VARCHAR(20) DEFAULT 'Internal' NOT NULL
    CHECK (AccessControlLevel IN ('Public', 'Internal', 'Confidential', 'Restricted', 'Classified'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DataClassification VARCHAR(30);
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS AllowedRoles JSONB;

-- ============================================
-- Enhanced Audit Trail (1 field)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS LastModifiedReason TEXT;

-- ============================================
-- Document Lifecycle Management (2 fields)
-- ============================================
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DocumentStatus VARCHAR(20) DEFAULT 'Active' NOT NULL
    CHECK (DocumentStatus IN ('Draft', 'Active', 'Deprecated', 'Archived', 'Deleted', 'UnderReview'));
ALTER TABLE ai_documents ADD COLUMN IF NOT EXISTS DocumentVersion VARCHAR(20);

-- ============================================
-- Create Indexes (if not exist)
-- ============================================

CREATE INDEX IF NOT EXISTS idx_ai_documents_contains_pii ON ai_documents(ContainsPII);
CREATE INDEX IF NOT EXISTS idx_ai_documents_access_control ON ai_documents(AccessControlLevel);
CREATE INDEX IF NOT EXISTS idx_ai_documents_status ON ai_documents(DocumentStatus);
CREATE INDEX IF NOT EXISTS idx_ai_documents_risk_level ON ai_documents(RiskLevel);
CREATE INDEX IF NOT EXISTS idx_ai_documents_dataset_type ON ai_documents(DatasetType);
CREATE INDEX IF NOT EXISTS idx_ai_documents_deletion_scheduled ON ai_documents(DeletionScheduledDate)
    WHERE DeletionScheduledDate IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_ai_documents_privacy_classification
    ON ai_documents(ContainsPII, SensitiveDataClassification)
    WHERE ContainsPII = TRUE;

CREATE INDEX IF NOT EXISTS idx_ai_documents_compliance_audit
    ON ai_documents(DocumentStatus, DataValidationStatus);

COMMIT;

-- ============================================
-- Post-Migration Validation
-- ============================================

SELECT
    'Migration to Tier 1 complete' AS status,
    COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_name = 'ai_documents';
```

**Execution**:
```bash
# Dry run on test database first
psql -U your_user -d test_database -f migrate_to_tier1_postgresql.sql

# After validation, run on production
psql -U your_user -d production_database -f migrate_to_tier1_postgresql.sql
```

---

**Note**: MySQL and SQL Server implementations are planned for future releases. See [../future/TIER2_TIER3_ROADMAP.md](../future/TIER2_TIER3_ROADMAP.md) for details.

---

## Data Migration Strategies

### Strategy 1: Clean Installation (Recommended for New Projects)

**When to use**: Starting from scratch, no existing data

**Steps**:
1. Run CREATE TABLE script for your database platform
2. Configure application to use new schema
3. Start ingesting data with full Tier 1 compliance from day 1

**Pros**:
- No migration complexity
- Full compliance from start
- No legacy data issues

**Cons**:
- Not applicable if you have existing data

---

### Strategy 2: Incremental Migration (Recommended for Existing Data)

**When to use**: Existing data, want to minimize downtime

**Phase 1: Add Columns (Low risk, minimal downtime)**
```sql
-- Add all Tier 1 columns with NULL defaults
ALTER TABLE ai_documents ADD COLUMN ContainsPII BOOLEAN DEFAULT FALSE;
ALTER TABLE ai_documents ADD COLUMN DatasetType VARCHAR(30);
-- ... etc (all Tier 1 fields)
```

**Phase 2: Backfill Critical Fields** (Done in batches)
```sql
-- Backfill in batches of 1000 records
DO $$
DECLARE
    batch_size INT := 1000;
    offset_val INT := 0;
BEGIN
    LOOP
        -- Update ContainsPII based on simple heuristics
        UPDATE ai_documents
        SET ContainsPII = (DocumentChunkText ~* '(email|phone|ssn|address)')::BOOLEAN,
            AccessControlLevel = 'Internal',
            DocumentStatus = 'Active',
            UpdateDateTime = CURRENT_TIMESTAMP,
            UpdateUser = 'migration_script'
        WHERE ID IN (
            SELECT ID FROM ai_documents
            WHERE ContainsPII IS NULL
            ORDER BY ID
            LIMIT batch_size
        );

        EXIT WHEN NOT FOUND;
        offset_val := offset_val + batch_size;

        -- Log progress
        RAISE NOTICE 'Processed % records', offset_val;

        -- Optional: sleep to reduce load
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;
```

**Phase 3: Add Indexes** (After backfill, during low-traffic period)
```sql
CREATE INDEX CONCURRENTLY idx_ai_documents_contains_pii ON ai_documents(ContainsPII);
CREATE INDEX CONCURRENTLY idx_ai_documents_access_control ON ai_documents(AccessControlLevel);
-- ... etc
```

**Phase 4: Make Fields NOT NULL** (After validation)
```sql
-- Only for fields that should be NOT NULL
ALTER TABLE ai_documents ALTER COLUMN ContainsPII SET NOT NULL;
ALTER TABLE ai_documents ALTER COLUMN AccessControlLevel SET NOT NULL;
ALTER TABLE ai_documents ALTER COLUMN DocumentStatus SET NOT NULL;
```

---

### Strategy 3: Shadow Table Migration (Zero downtime)

**When to use**: Large datasets, cannot afford downtime

**Steps**:

1. **Create new table with Tier 1 schema**
```sql
CREATE TABLE ai_documents_tier1 AS SELECT * FROM ai_documents WHERE 1=0;
-- Add all Tier 1 columns to ai_documents_tier1
```

2. **Dual-write to both tables** (application layer)
```python
# Every insert/update goes to both tables
def save_document(doc):
    save_to_original(doc)  # Old schema
    save_to_tier1(doc)     # New schema with Tier 1 fields
```

3. **Backfill historical data** (background job)
```sql
INSERT INTO ai_documents_tier1 (...)
SELECT ..., DEFAULT, DEFAULT, ...  -- Add Tier 1 defaults
FROM ai_documents
WHERE ID NOT IN (SELECT ID FROM ai_documents_tier1);
```

4. **Cutover** (rename tables)
```sql
BEGIN;
ALTER TABLE ai_documents RENAME TO ai_documents_old;
ALTER TABLE ai_documents_tier1 RENAME TO ai_documents;
COMMIT;
```

---

## Performance Optimization

### Index Creation Order

**Create indexes in this order to minimize performance impact:**

1. **Unique indexes first** (during migration, before data load)
```sql
CREATE UNIQUE INDEX idx_uuid ON ai_documents(UUID);
```

2. **Small selective indexes** (high cardinality, frequently queried)
```sql
CREATE INDEX idx_contains_pii ON ai_documents(ContainsPII);
CREATE INDEX idx_document_status ON ai_documents(DocumentStatus);
```

3. **Composite indexes** (after testing query patterns)
```sql
CREATE INDEX idx_privacy_classification ON ai_documents(ContainsPII, SensitiveDataClassification);
```

4. **Large indexes last** (text, JSONB GIN indexes)
```sql
CREATE INDEX idx_lineage_gin ON ai_documents USING GIN (DataLineageChain);
```

### PostgreSQL-Specific Optimizations

**Use CONCURRENTLY for production**:
```sql
CREATE INDEX CONCURRENTLY idx_ai_documents_dataset_type ON ai_documents(DatasetType);
```

**Analyze after migration**:
```sql
ANALYZE ai_documents;
```

**Vacuum after large updates**:
```sql
VACUUM ANALYZE ai_documents;
```

---

## Testing and Validation

### Pre-Migration Testing

**1. Test on Replica/Dev Database**
```bash
# PostgreSQL - restore production backup to test
pg_dump production_db > backup.sql
psql test_db < backup.sql
psql test_db < migrate_to_tier1_postgresql.sql
```

**2. Validate Schema**
```sql
-- Check all Tier 1 columns exist
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'ai_documents'
ORDER BY ordinal_position;

-- Verify count matches
SELECT COUNT(*) FROM ai_documents;  -- Should match original
```

**3. Test Application Queries**
```sql
-- Test common queries work
SELECT * FROM ai_documents WHERE ContainsPII = TRUE LIMIT 10;
SELECT * FROM ai_documents WHERE DocumentStatus = 'Active' LIMIT 10;
```

### Post-Migration Validation

**1. Data Integrity Checks**
```sql
-- Check for orphaned records
SELECT COUNT(*) FROM ai_documents WHERE UUID IS NULL;  -- Should be 0

-- Check constraints are enforced
SELECT COUNT(*) FROM ai_documents
WHERE DataQualityScore < 0 OR DataQualityScore > 100;  -- Should be 0

-- Verify indexes exist
SELECT indexname FROM pg_indexes WHERE tablename = 'ai_documents';
```

**2. Performance Benchmarking**
```sql
-- Benchmark common queries
EXPLAIN ANALYZE
SELECT * FROM ai_documents
WHERE ContainsPII = TRUE
  AND DocumentStatus = 'Active'
  AND RiskLevel = 'High'
LIMIT 100;
```

**3. Compliance Validation**
```sql
-- Check GDPR compliance fields populated
SELECT
    COUNT(*) as total,
    COUNT(CASE WHEN ContainsPII = TRUE AND LegalBasisForProcessing IS NULL THEN 1 END) as missing_legal_basis
FROM ai_documents;
-- missing_legal_basis should be 0 for production data
```

---

## Rollback Procedures

### Rollback Strategy 1: Immediate Rollback (During Migration)

**If migration fails mid-way**:

```sql
-- PostgreSQL
ROLLBACK;  -- If migration was in a transaction

-- If indexes were created with CONCURRENTLY (not in transaction)
DROP INDEX CONCURRENTLY IF EXISTS idx_ai_documents_contains_pii;
-- Drop all created indexes

-- Remove added columns
ALTER TABLE ai_documents DROP COLUMN IF EXISTS ContainsPII;
-- Drop all Tier 1 columns
```

### Rollback Strategy 2: Post-Migration Rollback

**If issues discovered after migration**:

**Option A: Keep schema, remove data from new columns**
```sql
-- Nullify Tier 1 fields but keep schema
UPDATE ai_documents SET
    ContainsPII = FALSE,
    PIITypes = NULL,
    DatasetType = NULL,
    -- ... all Tier 1 fields
    UpdateDateTime = CURRENT_TIMESTAMP;
```

**Option B: Full rollback from backup**
```bash
# PostgreSQL - restore from pre-migration backup
psql production_db < pre_migration_backup.sql
```

**Option C: Shadow table rollback**
```sql
-- If using shadow table strategy
BEGIN;
ALTER TABLE ai_documents RENAME TO ai_documents_tier1_failed;
ALTER TABLE ai_documents_old RENAME TO ai_documents;
COMMIT;
```

---

## Application Layer Updates

### TypeScript/JavaScript Example

**Before (Old Schema)**:
```typescript
interface AIDocument {
  id: number;
  uuid: string;
  insertDateTime: Date;
  updateDateTime: Date;
  insertUser: string;
  updateUser: string;
  sourceDocumentName?: string;
  documentChunkText?: string;
  // ... old fields only
}
```

**After (Tier 1 Schema)**:
```typescript
interface AIDocumentTier1 extends AIDocument {
  rogersAISchemaVersion: string;

  // Privacy & PII
  containsPII: boolean;
  piiTypes?: string[];
  piiDetectionMethod?: 'automated' | 'manual' | 'both' | 'not_detected';
  piiDetectionDate?: Date;
  sensitiveDataClassification?: 'None' | 'Low' | 'Medium' | 'High' | 'Critical';
  legalBasisForProcessing?: 'Consent' | 'Contract' | 'LegalObligation' | 'VitalInterests' | 'PublicTask' | 'LegitimateInterests';
  dataRetentionPeriod?: number;
  deletionScheduledDate?: Date;
  deletionStatus?: 'Pending' | 'Scheduled' | 'Deleted' | 'Retained' | 'AwaitingApproval';
  anonymizationStatus?: 'NotAnonymized' | 'Pseudonymized' | 'FullyAnonymized';

  // Data Governance
  datasetType?: 'Training' | 'Validation' | 'Testing' | 'Production' | 'KnowledgeBase' | 'Archive';
  datasetPurpose?: string;
  dataQualityScore?: number;
  dataValidationStatus?: 'Pending' | 'Validated' | 'Failed' | 'NeedsReview' | 'InProgress';
  dataValidationDate?: Date;
  dataValidatedBy?: string;
  dataLineageChain?: Record<string, any>;
  originalSourceType?: 'Web' | 'Database' | 'API' | 'FileSystem' | 'Manual' | 'Email' | 'S3' | 'SharePoint' | 'Other';

  // Legal & Licensing
  copyrightStatus?: 'PublicDomain' | 'Copyrighted' | 'CreativeCommons' | 'Unknown' | 'ProprietaryInternal';
  licenseType?: string;
  usageRestrictions?: string;
  commercialUseAllowed?: boolean;
  attributionRequired?: boolean;
  attributionText?: string;

  // Risk & Safety
  riskLevel?: 'Low' | 'Medium' | 'High' | 'Critical' | 'Unassessed';
  contentSafetyStatus?: 'Safe' | 'Flagged' | 'Unsafe' | 'UnderReview' | 'NotAssessed';
  contentSafetyScore?: number;
  contentModerationDate?: Date;

  // Access Control
  accessControlLevel: 'Public' | 'Internal' | 'Confidential' | 'Restricted' | 'Classified';
  dataClassification?: string;
  allowedRoles?: string[];

  // Audit
  lastModifiedReason?: string;

  // Lifecycle
  documentStatus: 'Draft' | 'Active' | 'Deprecated' | 'Archived' | 'Deleted' | 'UnderReview';
  documentVersion?: string;
}
```

### ORM Updates (Prisma Example)

```prisma
model AIDocument {
  id                          BigInt    @id @default(autoincrement())
  uuid                        String    @unique @default(uuid())
  rogersAISchemaVersion       String    @default("1.0.0-tier1") @map("Rogers-AI-Schema-Version")
  insertDateTime              DateTime  @default(now())
  updateDateTime              DateTime  @updatedAt
  insertUser                  String
  updateUser                  String

  // ... all Tier 1 fields

  containsPII                 Boolean   @default(false)
  piiTypes                    Json?
  datasetType                 String?
  accessControlLevel          String    @default("Internal")
  documentStatus              String    @default("Active")

  @@map("ai_documents")
}
```

---

## Migration Checklist

### Pre-Migration

- [ ] Full database backup completed
- [ ] Test migration on replica database
- [ ] Application code updated and tested
- [ ] Rollback procedure documented and tested
- [ ] Downtime window scheduled (if needed)
- [ ] Stakeholders notified
- [ ] Performance baseline captured

### During Migration

- [ ] Stop application writes (if not using online migration)
- [ ] Execute migration script
- [ ] Monitor for errors
- [ ] Validate column creation
- [ ] Create indexes
- [ ] Run post-migration tests

### Post-Migration

- [ ] Verify row count matches
- [ ] Test application queries
- [ ] Performance testing
- [ ] Compliance validation queries
- [ ] Resume application writes
- [ ] Monitor for 24 hours
- [ ] Document any issues

---

## Related Documentation

- [../DESIGN.md](../DESIGN.md) - Complete schema specification (single table, 52 fields)
- [../COMPLIANCE.md](../COMPLIANCE.md) - Regulatory mapping
- [../future/TIER2_TIER3_ROADMAP.md](../future/TIER2_TIER3_ROADMAP.md) - Future enhancements

### Database Platform Guides

- **[POSTGRESQL.md](POSTGRESQL.md)** (this document) - PostgreSQL implementation
- [SQLITE_VECTOR.md](SQLITE_VECTOR.md) - SQLite with sqlite-vec extension

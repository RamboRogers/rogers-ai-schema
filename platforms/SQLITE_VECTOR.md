# Rogers-AI-Schema - SQLite with sqlite-vec Extension

**Author**: Matthew Rogers, CISSP
**Title**: Field CTO for AI and Security at VAST Data
**License**: GNU General Public License v3.0
**Repository**: [github.com/RamboRogers/rogers-ai-schema](https://github.com/RamboRogers/rogers-ai-schema)

Complete implementation guide for deploying Rogers-AI-Schema Tier 1 on SQLite with the `sqlite-vec` vector extension for embedded AI workloads and edge computing deployments.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Schema Implementation](#schema-implementation)
4. [Vector Extension Setup](#vector-extension-setup)
5. [Performance Optimization](#performance-optimization)
6. [Data Migration Strategies](#data-migration-strategies)
7. [Deployment Patterns](#deployment-patterns)
8. [Testing and Validation](#testing-and-validation)

---

## Overview

### Why SQLite for AI Workloads?

**Schema Version:** Tier 1 Compliance
**Total Fields:** 52
**Compliance:** NIST AI-600, EU AI Act Articles 10-14, GDPR
**Vector Extension:** sqlite-vec (https://github.com/asg017/sqlite-vec)

**Use Cases:**
- **Edge AI Deployments**: On-device RAG systems for mobile and IoT
- **Embedded Applications**: Desktop AI applications, local-first software
- **Development & Testing**: Rapid prototyping, CI/CD pipelines
- **Small-Scale Production**: Single-user systems, offline-first applications
- **Data Sovereignty**: Keep sensitive data on-premises with zero-latency access

**Advantages:**
- Zero-configuration serverless database
- ACID compliance with WAL mode
- Excellent read performance for retrieval workloads
- File-based portability and easy backup/restore
- Low memory footprint suitable for edge devices
- Built-in full-text search (FTS5)
- Native JSON support (JSON1 extension)

**Limitations:**
- Single-writer concurrency model (suitable for read-heavy RAG workloads)
- Maximum database size: 281 TB (practical limit ~1-2 TB)
- No built-in network access (use application layer for distributed systems)
- Vector operations not hardware-accelerated (CPU-only)

---

## Prerequisites

### Required SQLite Version

**Minimum:** SQLite 3.38.0 (for JSON improvements)
**Recommended:** SQLite 3.42.0+ (for enhanced JSON and performance)

```bash
# Check SQLite version
sqlite3 --version

# Expected output format:
# 3.42.0 2023-05-16 12:36:15
```

### Install sqlite-vec Extension

**Option 1: Pre-compiled Binaries** (Recommended)
```bash
# Download from GitHub releases
wget https://github.com/asg017/sqlite-vec/releases/download/v0.0.1-alpha.1/vec0.so

# Place in SQLite extensions directory
# Linux/macOS
mkdir -p ~/.sqlite-extensions
mv vec0.so ~/.sqlite-extensions/

# Verify installation
sqlite3 << 'EOF'
.load ~/.sqlite-extensions/vec0
SELECT vec_version();
EOF
```

**Option 2: Build from Source**
```bash
git clone https://github.com/asg017/sqlite-vec.git
cd sqlite-vec
make
make install
```

### Enable Required Extensions

```sql
-- Enable JSON1 extension (built-in for most distributions)
-- Enable FTS5 for full-text search (optional but recommended)

-- Test JSON support
SELECT json_valid('{"test": true}');  -- Should return 1

-- Test vector extension
.load vec0
SELECT vec_version();
```

---

## Schema Implementation

### Create Table (New Installation)

**File**: `platforms/sqlite_vector.sql`

```sql
-- Rogers-AI-Schema Tier 1 - SQLite Implementation
-- Version: 1.0.0-tier1
-- Database: SQLite 3.38.0+
-- Extension: sqlite-vec for vector operations

-- Enable Write-Ahead Logging for better concurrency
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=-64000;  -- 64MB cache
PRAGMA temp_store=MEMORY;
PRAGMA mmap_size=30000000000;  -- 30GB memory-mapped I/O

-- Load required extensions
.load vec0  -- sqlite-vec extension

BEGIN TRANSACTION;

-- ============================================
-- Main AI Documents Table
-- ============================================

CREATE TABLE IF NOT EXISTS ai_documents (
    -- ============================================
    -- Core Identity & Audit (7 fields)
    -- ============================================
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UUID TEXT NOT NULL UNIQUE,
    RogersAISchemaVersion TEXT NOT NULL DEFAULT '1.0.0-tier1',
    InsertDateTime TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
    UpdateDateTime TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
    InsertUser TEXT NOT NULL,
    UpdateUser TEXT NOT NULL,

    -- ============================================
    -- Source Document Metadata (7 fields)
    -- ============================================
    SourceDocumentName TEXT,
    SourceDocumentPath TEXT,
    SourceDocumentHash TEXT,
    SourceDocumentTitle TEXT,
    SourceDocumentSummary TEXT,
    SourceDocumentAuthor TEXT,
    SourceDocumentOrganization TEXT,

    -- ============================================
    -- Document Content & Chunking (2 fields)
    -- ============================================
    DocumentChunkNumber INTEGER CHECK (DocumentChunkNumber >= 1),
    DocumentChunkText TEXT,

    -- ============================================
    -- Vector Embeddings Metadata (5 providers × 2 fields = 10 fields)
    -- Note: Actual vectors stored in separate vec0 virtual tables
    -- ============================================
    DocumentEmbeddingModel01 TEXT,
    DocumentEmbeddingURL01 TEXT,

    DocumentEmbeddingModel02 TEXT,
    DocumentEmbeddingURL02 TEXT,

    DocumentEmbeddingModel03 TEXT,
    DocumentEmbeddingURL03 TEXT,

    DocumentEmbeddingModel04 TEXT,
    DocumentEmbeddingURL04 TEXT,

    DocumentEmbeddingModel05 TEXT,
    DocumentEmbeddingURL05 TEXT,

    -- ============================================
    -- Privacy & PII Protection (10 fields)
    -- ============================================
    ContainsPII INTEGER NOT NULL DEFAULT 0 CHECK (ContainsPII IN (0, 1)),
    PIITypes TEXT,  -- JSON array
    PIIDetectionMethod TEXT CHECK (PIIDetectionMethod IN ('automated', 'manual', 'both', 'not_detected')),
    PIIDetectionDate TEXT,
    SensitiveDataClassification TEXT CHECK (SensitiveDataClassification IN ('None', 'Low', 'Medium', 'High', 'Critical')),
    LegalBasisForProcessing TEXT CHECK (LegalBasisForProcessing IN ('Consent', 'Contract', 'LegalObligation', 'VitalInterests', 'PublicTask', 'LegitimateInterests')),
    DataRetentionPeriod INTEGER CHECK (DataRetentionPeriod > 0),
    DeletionScheduledDate TEXT,
    DeletionStatus TEXT CHECK (DeletionStatus IN ('Pending', 'Scheduled', 'Deleted', 'Retained', 'AwaitingApproval')),
    AnonymizationStatus TEXT CHECK (AnonymizationStatus IN ('NotAnonymized', 'Pseudonymized', 'FullyAnonymized')),

    -- ============================================
    -- Data Governance & Lineage (8 fields)
    -- ============================================
    DatasetType TEXT CHECK (DatasetType IN ('Training', 'Validation', 'Testing', 'Production', 'KnowledgeBase', 'Archive')),
    DatasetPurpose TEXT,
    DataQualityScore REAL CHECK (DataQualityScore BETWEEN 0 AND 100),
    DataValidationStatus TEXT CHECK (DataValidationStatus IN ('Pending', 'Validated', 'Failed', 'NeedsReview', 'InProgress')),
    DataValidationDate TEXT,
    DataValidatedBy TEXT,
    DataLineageChain TEXT,  -- JSON object
    OriginalSourceType TEXT CHECK (OriginalSourceType IN ('Web', 'Database', 'API', 'FileSystem', 'Manual', 'Email', 'S3', 'SharePoint', 'Other')),

    -- ============================================
    -- Legal & Licensing Tracking (6 fields)
    -- ============================================
    CopyrightStatus TEXT CHECK (CopyrightStatus IN ('PublicDomain', 'Copyrighted', 'CreativeCommons', 'Unknown', 'ProprietaryInternal')),
    LicenseType TEXT,
    UsageRestrictions TEXT,
    CommercialUseAllowed INTEGER CHECK (CommercialUseAllowed IN (0, 1)),
    AttributionRequired INTEGER CHECK (AttributionRequired IN (0, 1)),
    AttributionText TEXT,

    -- ============================================
    -- Risk Management & Content Safety (4 fields)
    -- ============================================
    RiskLevel TEXT CHECK (RiskLevel IN ('Low', 'Medium', 'High', 'Critical', 'Unassessed')),
    ContentSafetyStatus TEXT CHECK (ContentSafetyStatus IN ('Safe', 'Flagged', 'Unsafe', 'UnderReview', 'NotAssessed')),
    ContentSafetyScore REAL CHECK (ContentSafetyScore BETWEEN 0 AND 100),
    ContentModerationDate TEXT,

    -- ============================================
    -- Access Control & Security (3 fields)
    -- ============================================
    AccessControlLevel TEXT NOT NULL DEFAULT 'Internal' CHECK (AccessControlLevel IN ('Public', 'Internal', 'Confidential', 'Restricted', 'Classified')),
    DataClassification TEXT,
    AllowedRoles TEXT,  -- JSON array

    -- ============================================
    -- Enhanced Audit Trail (1 field)
    -- ============================================
    LastModifiedReason TEXT,

    -- ============================================
    -- Document Lifecycle Management (2 fields)
    -- ============================================
    DocumentStatus TEXT NOT NULL DEFAULT 'Active' CHECK (DocumentStatus IN ('Draft', 'Active', 'Deprecated', 'Archived', 'Deleted', 'UnderReview')),
    DocumentVersion TEXT
);

-- ============================================
-- Vector Storage Tables (sqlite-vec virtual tables)
-- ============================================

-- Provider 01 vectors (e.g., OpenAI text-embedding-ada-002, 1536 dimensions)
CREATE VIRTUAL TABLE IF NOT EXISTS vec_embeddings_01 USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding FLOAT[1536]
);

-- Provider 02 vectors (e.g., Cohere embed-english-v3.0, 1024 dimensions)
CREATE VIRTUAL TABLE IF NOT EXISTS vec_embeddings_02 USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding FLOAT[1024]
);

-- Provider 03 vectors (e.g., HuggingFace all-MiniLM-L6-v2, 384 dimensions)
CREATE VIRTUAL TABLE IF NOT EXISTS vec_embeddings_03 USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding FLOAT[384]
);

-- Provider 04 vectors (e.g., Google textembedding-gecko, 768 dimensions)
CREATE VIRTUAL TABLE IF NOT EXISTS vec_embeddings_04 USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding FLOAT[768]
);

-- Provider 05 vectors (custom/internal model)
CREATE VIRTUAL TABLE IF NOT EXISTS vec_embeddings_05 USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding FLOAT[1536]  -- Adjust dimensions as needed
);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Unique index on UUID
CREATE UNIQUE INDEX IF NOT EXISTS idx_ai_documents_uuid ON ai_documents(UUID);

-- High-priority compliance indexes
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
    WHERE ContainsPII = 1;

CREATE INDEX IF NOT EXISTS idx_ai_documents_compliance_audit
    ON ai_documents(DocumentStatus, DataValidationStatus);

-- Temporal indexes
CREATE INDEX IF NOT EXISTS idx_ai_documents_insert_datetime ON ai_documents(InsertDateTime DESC);
CREATE INDEX IF NOT EXISTS idx_ai_documents_update_datetime ON ai_documents(UpdateDateTime DESC);

-- ============================================
-- Triggers for Automatic Updates
-- ============================================

-- Auto-update UpdateDateTime on modification
CREATE TRIGGER IF NOT EXISTS trg_ai_documents_update_datetime
AFTER UPDATE ON ai_documents
FOR EACH ROW
BEGIN
    UPDATE ai_documents
    SET UpdateDateTime = datetime('now', 'utc')
    WHERE ID = NEW.ID;
END;

-- Generate UUID on insert if not provided
CREATE TRIGGER IF NOT EXISTS trg_ai_documents_insert_uuid
AFTER INSERT ON ai_documents
FOR EACH ROW
WHEN NEW.UUID IS NULL
BEGIN
    UPDATE ai_documents
    SET UUID = (SELECT lower(hex(randomblob(16))))
    WHERE ID = NEW.ID;
END;

-- ============================================
-- Full-Text Search Index (Optional)
-- ============================================

-- FTS5 virtual table for semantic + keyword search
CREATE VIRTUAL TABLE IF NOT EXISTS ai_documents_fts USING fts5(
    DocumentChunkText,
    SourceDocumentTitle,
    SourceDocumentSummary,
    content=ai_documents,
    content_rowid=ID
);

-- Triggers to keep FTS index synchronized
CREATE TRIGGER IF NOT EXISTS trg_ai_documents_fts_insert
AFTER INSERT ON ai_documents
BEGIN
    INSERT INTO ai_documents_fts(rowid, DocumentChunkText, SourceDocumentTitle, SourceDocumentSummary)
    VALUES (NEW.ID, NEW.DocumentChunkText, NEW.SourceDocumentTitle, NEW.SourceDocumentSummary);
END;

CREATE TRIGGER IF NOT EXISTS trg_ai_documents_fts_delete
AFTER DELETE ON ai_documents
BEGIN
    DELETE FROM ai_documents_fts WHERE rowid = OLD.ID;
END;

CREATE TRIGGER IF NOT EXISTS trg_ai_documents_fts_update
AFTER UPDATE ON ai_documents
BEGIN
    DELETE FROM ai_documents_fts WHERE rowid = OLD.ID;
    INSERT INTO ai_documents_fts(rowid, DocumentChunkText, SourceDocumentTitle, SourceDocumentSummary)
    VALUES (NEW.ID, NEW.DocumentChunkText, NEW.SourceDocumentTitle, NEW.SourceDocumentSummary);
END;

COMMIT;

-- ============================================
-- Verify Installation
-- ============================================

SELECT 'Rogers-AI-Schema v1.0.0-tier1 for SQLite installed successfully' AS status;

-- Show table info
.schema ai_documents

-- Verify vector tables
SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'vec_embeddings_%';

-- Database stats
SELECT
    (SELECT COUNT(*) FROM ai_documents) AS total_documents,
    (SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()) / 1024.0 / 1024.0 AS db_size_mb;
```

**Execution**:
```bash
sqlite3 ai_documents.db < platforms/sqlite_vector.sql
```

---

## Vector Extension Setup

### Understanding sqlite-vec Architecture

**Key Concepts:**
- **Virtual Tables**: Vector embeddings stored in separate `vec0` virtual tables
- **Document Linkage**: `document_id` in vector tables references `ID` in main table
- **Dimension Flexibility**: Each provider can have different vector dimensions
- **Distance Metrics**: Supports L2 (Euclidean), cosine similarity, inner product

### Vector Similarity Search

**Cosine Similarity Search** (Most common for RAG):
```sql
-- Find top 10 most similar documents using Provider 01 embeddings
SELECT
    d.ID,
    d.SourceDocumentName,
    d.DocumentChunkText,
    vec_distance_cosine(v.embedding, ?) AS similarity_score
FROM ai_documents d
JOIN vec_embeddings_01 v ON d.ID = v.document_id
WHERE d.DocumentStatus = 'Active'
  AND d.AccessControlLevel IN ('Public', 'Internal')
ORDER BY similarity_score ASC  -- Lower is more similar for cosine distance
LIMIT 10;
```

**L2 Distance Search**:
```sql
SELECT
    d.ID,
    d.DocumentChunkText,
    vec_distance_l2(v.embedding, ?) AS l2_distance
FROM ai_documents d
JOIN vec_embeddings_01 v ON d.ID = v.document_id
ORDER BY l2_distance ASC
LIMIT 10;
```

### Hybrid Search (Vector + Full-Text)

```sql
-- Combine semantic vector search with keyword matching
WITH vector_results AS (
    SELECT
        d.ID,
        vec_distance_cosine(v.embedding, ?) AS vec_score
    FROM ai_documents d
    JOIN vec_embeddings_01 v ON d.ID = v.document_id
    ORDER BY vec_score ASC
    LIMIT 100
),
fts_results AS (
    SELECT
        rowid AS ID,
        rank AS fts_score
    FROM ai_documents_fts
    WHERE ai_documents_fts MATCH ?
    ORDER BY rank
    LIMIT 100
)
SELECT
    d.*,
    COALESCE(v.vec_score, 1.0) AS vector_score,
    COALESCE(f.fts_score, 0.0) AS keyword_score,
    -- Combine scores with weights
    (COALESCE(v.vec_score, 1.0) * 0.7) + (COALESCE(f.fts_score, 0.0) * 0.3) AS combined_score
FROM ai_documents d
LEFT JOIN vector_results v ON d.ID = v.ID
LEFT JOIN fts_results f ON d.ID = f.ID
WHERE v.ID IS NOT NULL OR f.ID IS NOT NULL
ORDER BY combined_score ASC
LIMIT 10;
```

### Insert Document with Embeddings

```sql
-- Insert main document
INSERT INTO ai_documents (
    UUID,
    InsertUser,
    UpdateUser,
    SourceDocumentName,
    DocumentChunkText,
    DocumentEmbeddingModel01,
    ContainsPII,
    AccessControlLevel,
    DocumentStatus
) VALUES (
    lower(hex(randomblob(16))),
    'import_system',
    'import_system',
    'technical_documentation.pdf',
    'RAG systems combine retrieval with generation...',
    'text-embedding-ada-002',
    0,
    'Internal',
    'Active'
);

-- Get the inserted ID
SELECT last_insert_rowid() AS new_id;

-- Insert corresponding vector embedding
INSERT INTO vec_embeddings_01 (document_id, embedding)
VALUES (
    last_insert_rowid(),
    vec_f32(?)  -- Pass embedding as binary blob or JSON array
);
```

---

## Performance Optimization

### SQLite Pragmas for AI Workloads

```sql
-- Production-optimized configuration
PRAGMA journal_mode=WAL;           -- Write-Ahead Logging for concurrency
PRAGMA synchronous=NORMAL;         -- Balance safety/performance
PRAGMA cache_size=-64000;          -- 64MB page cache
PRAGMA temp_store=MEMORY;          -- Temp tables in memory
PRAGMA mmap_size=30000000000;      -- 30GB memory-mapped I/O
PRAGMA page_size=4096;             -- Optimal for SSDs
PRAGMA auto_vacuum=INCREMENTAL;    -- Prevent file fragmentation
PRAGMA busy_timeout=5000;          -- 5 second timeout for locks
```

### Indexing Best Practices

**DO:**
- ✅ Index foreign keys (`document_id` in vector tables)
- ✅ Index frequently filtered columns (ContainsPII, DocumentStatus)
- ✅ Use partial indexes with WHERE clauses for sparse data
- ✅ Analyze tables after bulk inserts: `ANALYZE ai_documents;`

**DON'T:**
- ❌ Over-index - SQLite has limited query planner capabilities
- ❌ Index low-cardinality columns (BOOLEAN/INTEGER with few values)
- ❌ Create redundant indexes on columns already in composite indexes

### Query Performance Tips

**Use Query Planner**:
```sql
EXPLAIN QUERY PLAN
SELECT * FROM ai_documents
WHERE ContainsPII = 1 AND DocumentStatus = 'Active';

-- Look for "USING INDEX" in output
```

**Batch Operations**:
```sql
-- Batch inserts in transactions for 100x speed improvement
BEGIN TRANSACTION;
INSERT INTO ai_documents (...) VALUES (...);
INSERT INTO ai_documents (...) VALUES (...);
-- ... thousands of rows
COMMIT;
```

**Prepared Statements** (Application layer):
```python
# Python example
import sqlite3

conn = sqlite3.connect('ai_documents.db')
cursor = conn.cursor()

# Prepare statement once
stmt = cursor.prepare('''
    INSERT INTO ai_documents (UUID, InsertUser, DocumentChunkText, ...)
    VALUES (?, ?, ?, ...)
''')

# Execute many times with different parameters
for doc in documents:
    cursor.execute(stmt, (doc.uuid, doc.user, doc.text, ...))

conn.commit()
```

---

## Data Migration Strategies

### From PostgreSQL to SQLite

**Export from PostgreSQL**:
```bash
# Export as CSV
psql -d production_db -c "COPY ai_documents TO '/tmp/ai_docs.csv' CSV HEADER;"
```

**Import to SQLite**:
```sql
.mode csv
.import /tmp/ai_docs.csv ai_documents_temp

-- Transform and insert
INSERT INTO ai_documents
SELECT * FROM ai_documents_temp
WHERE ...; -- Apply any transformations

-- Clean up
DROP TABLE ai_documents_temp;
```

### From JSON Export

```sql
-- Import JSON data using JSON1 extension
CREATE TEMP TABLE json_import(data TEXT);
.import data.json json_import

INSERT INTO ai_documents (UUID, SourceDocumentName, DocumentChunkText, ...)
SELECT
    json_extract(data, '$.uuid'),
    json_extract(data, '$.source_name'),
    json_extract(data, '$.text'),
    ...
FROM json_import;
```

---

## Deployment Patterns

### Edge AI Application

**Use Case**: Mobile app with local RAG

```python
import sqlite3
import numpy as np

class LocalRAG:
    def __init__(self, db_path='ai_documents.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.enable_load_extension(True)
        self.conn.load_extension('vec0')

    def search(self, query_embedding, top_k=10):
        """Vector similarity search"""
        cursor = self.conn.cursor()

        # Convert numpy array to blob
        embedding_blob = query_embedding.tobytes()

        results = cursor.execute('''
            SELECT
                d.DocumentChunkText,
                d.SourceDocumentName,
                vec_distance_cosine(v.embedding, ?) AS score
            FROM ai_documents d
            JOIN vec_embeddings_01 v ON d.ID = v.document_id
            WHERE d.DocumentStatus = 'Active'
            ORDER BY score ASC
            LIMIT ?
        ''', (embedding_blob, top_k))

        return results.fetchall()
```

### Offline-First Desktop App

**File-based Distribution**:
```bash
# Package SQLite database with application
myapp/
├── bin/
│   └── myapp
├── data/
│   └── ai_documents.db  # Embedded knowledge base
└── extensions/
    └── vec0.so
```

**Read-Only Mode** (for distributed read-only knowledge bases):
```python
conn = sqlite3.connect('file:ai_documents.db?mode=ro', uri=True)
```

### Multi-Database Sharding

**Shard by Dataset Type**:
```bash
training_data.db     # DatasetType = 'Training'
production_rag.db    # DatasetType = 'Production'
archive.db           # DocumentStatus = 'Archived'
```

**Query Across Shards**:
```sql
ATTACH DATABASE 'training_data.db' AS training;
ATTACH DATABASE 'production_rag.db' AS production;

SELECT * FROM training.ai_documents
UNION ALL
SELECT * FROM production.ai_documents
WHERE DocumentStatus = 'Active';
```

---

## Testing and Validation

### Schema Validation

```sql
-- Verify all tables exist
SELECT name FROM sqlite_master
WHERE type='table' AND name IN (
    'ai_documents',
    'vec_embeddings_01',
    'vec_embeddings_02',
    'vec_embeddings_03',
    'vec_embeddings_04',
    'vec_embeddings_05',
    'ai_documents_fts'
);

-- Check constraints
PRAGMA table_info(ai_documents);

-- Verify indexes
SELECT name, tbl_name FROM sqlite_master
WHERE type='index' AND tbl_name='ai_documents';
```

### Data Integrity Tests

```sql
-- Check for orphaned vectors
SELECT COUNT(*) FROM vec_embeddings_01 v
WHERE NOT EXISTS (
    SELECT 1 FROM ai_documents d WHERE d.ID = v.document_id
);
-- Should return 0

-- Verify UUID uniqueness
SELECT UUID, COUNT(*)
FROM ai_documents
GROUP BY UUID
HAVING COUNT(*) > 1;
-- Should return no rows

-- Check GDPR compliance fields
SELECT COUNT(*) FROM ai_documents
WHERE ContainsPII = 1 AND LegalBasisForProcessing IS NULL;
-- Should be 0 in production
```

### Performance Benchmarks

```sql
-- Measure query performance
.timer ON

SELECT COUNT(*) FROM ai_documents;

SELECT * FROM ai_documents
WHERE ContainsPII = 1
  AND DocumentStatus = 'Active'
LIMIT 100;

-- Vector search performance
SELECT d.*, vec_distance_cosine(v.embedding, ?) AS score
FROM ai_documents d
JOIN vec_embeddings_01 v ON d.ID = v.document_id
ORDER BY score ASC
LIMIT 10;

.timer OFF
```

---

## SQLite-Specific Considerations

### Database Size Limits

| Metric | Limit | Notes |
|--------|-------|-------|
| Max DB Size | 281 TB | Practical limit: 1-2 TB |
| Max Row Size | 1 GB | TEXT/BLOB column limit |
| Max Columns | 2000 | Schema has 52 fields |
| Max Table Size | 2^64 rows | Effectively unlimited |

### Concurrency Model

**Single Writer, Multiple Readers** (WAL mode):
- ✅ Excellent for RAG (read-heavy workloads)
- ✅ Readers don't block readers
- ✅ Readers don't block writer
- ⚠️ Only one writer at a time
- ⚠️ Writer blocks briefly during checkpoints

**Solution for High Write Volume**:
```python
# Use connection pool with queue
import queue
import threading

write_queue = queue.Queue()

def writer_thread(db_path):
    conn = sqlite3.connect(db_path)
    while True:
        write_op = write_queue.get()
        conn.execute(write_op)
        conn.commit()

# Application code
write_queue.put("INSERT INTO ai_documents ...")
```

### Backup and Recovery

**Online Backup** (no downtime):
```python
import sqlite3

def backup_database(source_db, backup_db):
    source = sqlite3.connect(source_db)
    backup = sqlite3.connect(backup_db)

    with backup:
        source.backup(backup)

    source.close()
    backup.close()
```

**Incremental Backup** (WAL files):
```bash
# Backup main database
cp ai_documents.db ai_documents.db.backup

# Backup WAL file (if exists)
cp ai_documents.db-wal ai_documents.db-wal.backup

# Checkpoint WAL into main database
sqlite3 ai_documents.db "PRAGMA wal_checkpoint(FULL);"
```

---

## Related Documentation

- [../DESIGN.md](../DESIGN.md) - Complete schema specification (single table, 52 fields)
- [POSTGRESQL.md](POSTGRESQL.md) - PostgreSQL implementation guide
- [../COMPLIANCE.md](../COMPLIANCE.md) - Regulatory mapping
- [../future/TIER2_TIER3_ROADMAP.md](../future/TIER2_TIER3_ROADMAP.md) - Future enhancements

## External Resources

- [SQLite Official Documentation](https://www.sqlite.org/docs.html)
- [sqlite-vec Extension](https://github.com/asg017/sqlite-vec)
- [SQLite JSON1 Extension](https://www.sqlite.org/json1.html)
- [SQLite FTS5 Full-Text Search](https://www.sqlite.org/fts5.html)
- [SQLite Performance Tuning](https://www.sqlite.org/lang_analyze.html)

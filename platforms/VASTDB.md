# Rogers-AI-Schema - VAST Data Platform Implementation Guide

**Author**: Matthew Rogers, CISSP  
**Title**: Field CTO for AI and Security at VAST Data  
**License**: GNU General Public License v3.0  
**Repository**: [github.com/RamboRogers/rogers-ai-schema](https://github.com/RamboRogers/rogers-ai-schema)

Complete guide for implementing Rogers-AI-Schema Tier 1 on VAST Data Platform (VASTDB) for enterprise AI workloads, RAG systems, and vector similarity search at scale.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [VASTDB Capabilities and Limitations](#vastdb-capabilities-and-limitations)
5. [Schema Implementation](#schema-implementation)
6. [Data Operations](#data-operations)
7. [Vector Similarity Search](#vector-similarity-search)
8. [Application-Layer Requirements](#application-layer-requirements)
9. [Integration Examples](#integration-examples)
10. [Performance Considerations](#performance-considerations)

---

## Overview

VAST Data Platform provides a unified data foundation for AI workloads with native vector support. This implementation uses the `vastdb` Python SDK with PyArrow schemas to create the Rogers-AI-Schema Tier 1 table structure.

### Why VAST Data Platform?

- **Unified Data Foundation**: Store vectors alongside structured data and unstructured files
- **Native Vector Support**: Built-in distance functions (`array_cosine_distance`, `array_distance`)
- **Massive Scale**: Up to 256 trillion rows per table, 31,936+ columns
- **ACID Transactions**: Full transactional support for data integrity
- **Real-Time Analytics**: Sub-second queries without staging
- **S3-Compatible**: Standard S3 API for data access

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ VAST Data Platform                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Bucket    │  │   Schema    │  │    Table    │          │
│  │ ai_workloads│──│rogers_ai_   │──│ai_documents │          │
│  │             │  │   schema    │  │ (52 fields) │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                             │
│  Vector Columns (5 providers × 1024 dims):                  │
│  ├─ DocumentEmbeddingVectors01 (list<float32>[1024])        │
│  ├─ DocumentEmbeddingVectors02 (list<float32>[1024])        │
│  ├─ DocumentEmbeddingVectors03 (list<float32>[1024])        │
│  ├─ DocumentEmbeddingVectors04 (list<float32>[1024])        │
│  └─ DocumentEmbeddingVectors05 (list<float32>[1024])        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Required Software

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.8+ | Runtime environment |
| vastdb | Latest | VAST Data Platform SDK |
| pyarrow | Latest | Apache Arrow data structures |
| adbc_driver_manager | Latest | ADBC driver interface for SQL queries |
| libvastdb_adbc_driver.so | Latest | VAST ADBC binary driver (for vector search) |

### Installation

```bash
# Install required packages
pip install vastdb pyarrow adbc_driver_manager

# Verify installation
python -c "import vastdb; import pyarrow; from adbc_driver_manager import dbapi; print('Dependencies installed successfully')"
```

### ADBC Driver Binary

The VAST ADBC driver binary (`libvastdb_adbc_driver.so`) is required for SQL queries including vector search. Download from:
- VAST GitHub Releases
- VAST Support Portal

Set the path:
```bash
export VAST_ADBC_DRIVER_PATH="/path/to/libvastdb_adbc_driver.so"
```

### VAST Cluster Requirements

- VAST Data Platform cluster with VASTDB enabled
- Access credentials (access key and secret key)
- Network connectivity to cluster endpoint
- Sufficient storage quota for your AI workload

---

## Quick Start

### 1. Set Environment Variables

```bash
export VAST_ENDPOINT="your-vast-cluster.example.com"
export VAST_ACCESS_KEY="your-access-key"
export VAST_SECRET_KEY="your-secret-key"
export VAST_BUCKET="ai_workloads"
export VAST_SCHEMA="rogers_ai_schema"
```

### 2. View Schema Information

```bash
python platforms/vast_schema.py --info
```

### 3. Create the Table

```bash
python platforms/vast_schema.py --create
```

### 4. View Example Queries

```bash
python platforms/vast_schema.py --examples
```

### Custom Vector Dimensions

By default, vector columns use 1024 dimensions. To use different dimensions:

```bash
# Use 1536 dimensions (OpenAI text-embedding-ada-002)
python platforms/vast_schema.py --create --dims 1536

# Use 768 dimensions (sentence-transformers)
python platforms/vast_schema.py --create --dims 768
```

### Drop and Recreate Table (Development)

```bash
# Useful if schema changed during development
python platforms/vast_schema.py --create --drop
```

---

## VASTDB Capabilities and Limitations

### Supported Features

| Feature | VASTDB Support | Notes |
|---------|---------------|-------|
| Vector storage | ✅ Native | Fixed-dimension arrays |
| Cosine similarity | ✅ `array_cosine_distance()` | Built-in function |
| Euclidean distance | ✅ `array_distance()` | Built-in function |
| ACID transactions | ✅ Full support | Snapshot isolation |
| SQL queries | ✅ Via Trino connector | Standard SQL syntax |
| Large tables | ✅ 256 trillion rows | Enterprise scale |
| Many columns | ✅ 31,936 columns | Planned: 64,000 |

### Not Supported (Application-Layer Alternatives)

| Feature | PostgreSQL | VASTDB | Mitigation |
|---------|------------|--------|------------|
| **NOT NULL constraints** | `NOT NULL` | Not available | All columns nullable; validate in app |
| Vector indexes (HNSW) | `CREATE INDEX ... USING hnsw` | Not available | VAST's architecture optimizes brute-force |
| Triggers | `CREATE TRIGGER` | Not available | Set timestamps in application code |
| SERIAL/AUTOINCREMENT | `BIGSERIAL` | Not available | Generate IDs in application |
| CHECK constraints | `CHECK (...)` | Not available | Validate in application layer |
| gen_random_uuid() | Built-in | Not available | Use Python `uuid.uuid4()` |
| DEFAULT values | `DEFAULT 'value'` | Not available | Set defaults when inserting |
| JSONB | Native type | Not available | Store JSON as string |
| DISTINCT in aggregates | `COUNT(DISTINCT col)` | Limited | Use subqueries or GROUP BY |

---

## Schema Implementation

### PyArrow Schema (65 Fields)

The schema is defined in `platforms/vast_schema.py` using PyArrow types:

```python
import pyarrow as pa

# IMPORTANT: VASTDB does NOT support NOT NULL constraints
# All columns must be nullable (omit nullable parameter or set nullable=True)

# Vector field helper - VAST requires this specific format
def create_vector_field(name: str, dims: int) -> pa.Field:
    vector_type = pa.list_(
        pa.field(name="item", type=pa.float32(), nullable=False),
        dims
    )
    return pa.field(name, vector_type)

schema = pa.schema([
    # Core Identity & Audit (7 fields) - all nullable in VASTDB
    pa.field("ID", pa.int64()),
    pa.field("UUID", pa.string()),
    pa.field("RogersAISchemaVersion", pa.string()),
    pa.field("InsertDateTime", pa.timestamp('us', tz='UTC')),
    pa.field("UpdateDateTime", pa.timestamp('us', tz='UTC')),
    pa.field("InsertUser", pa.string()),
    pa.field("UpdateUser", pa.string()),
    
    # Source Document Metadata (7 fields)
    pa.field("SourceDocumentName", pa.string()),
    # ... additional metadata fields
    
    # Vector Embeddings (5 providers × 3 fields = 15 fields)
    pa.field("DocumentEmbeddingModel01", pa.string()),
    pa.field("DocumentEmbeddingURL01", pa.string()),
    create_vector_field("DocumentEmbeddingVectors01", 1024),  # VAST vector format
    # ... additional vector providers
    
    # Privacy & PII Protection (10 fields) - GDPR
    pa.field("ContainsPII", pa.bool_()),
    # ... additional privacy fields
    
    # ... remaining field groups
])
```

### Data Type Mapping

| Schema Type | PyArrow Type | Example |
|-------------|--------------|---------|
| BIGSERIAL/ID | `pa.int64()` | `12345678901` |
| UUID | `pa.string()` | `"550e8400-e29b-..."` |
| VARCHAR(n) | `pa.string()` | `"document.pdf"` |
| TEXT | `pa.string()` | `"Long text content..."` |
| TIMESTAMP | `pa.timestamp('us')` or `pa.timestamp('us', tz='UTC')` | `2025-01-02T12:00:00` |
| BOOLEAN | `pa.bool_()` | `True` / `False` |
| INTEGER | `pa.int32()` | `42` |
| NUMERIC(5,2) | `pa.float64()` | `95.50` |
| JSONB | `pa.string()` | `'{"key": "value"}'` |
| vector(N) | `pa.list_(pa.field("item", pa.float32(), False), N)` | `[0.1, 0.2, ...]` |

---

## Data Operations

### Connecting to VASTDB

```python
import vastdb

# Note: Parameters are 'access' and 'secret' (not 'access_key'/'secret_key')
session = vastdb.connect(
    endpoint="http://your-cluster.example.com:8081",
    access="your-access-key",
    secret="your-secret-key",
)
```

### Inserting Data

```python
import pyarrow as pa
from datetime import datetime, timezone
import uuid

# Prepare data as PyArrow Table
data = {
    "ID": [1],
    "UUID": [str(uuid.uuid4())],
    "RogersAISchemaVersion": ["1.0.0-tier1"],
    "InsertDateTime": [datetime.now(timezone.utc)],
    "UpdateDateTime": [datetime.now(timezone.utc)],
    "InsertUser": ["data_pipeline"],
    "UpdateUser": ["data_pipeline"],
    "SourceDocumentName": ["technical_doc.pdf"],
    "DocumentChunkText": ["RAG systems combine retrieval with generation..."],
    "DocumentEmbeddingModel01": ["Qwen/Qwen3-Embedding-0.6B"],
    "DocumentEmbeddingVectors01": [[0.1, 0.2, 0.3, ...]],  # 1024 floats
    "ContainsPII": [False],
    "AccessControlLevel": ["Internal"],
    "DocumentStatus": ["Active"],
    # ... remaining fields
}

table = pa.Table.from_pydict(data)

with session.transaction() as tx:
    bucket = tx.bucket("ai_workloads")
    # Use fail_if_missing=False to avoid exceptions
    schema = bucket.schema("rogers_ai_schema", fail_if_missing=False) or \
             bucket.create_schema("rogers_ai_schema")
    tbl = schema.table("ai_documents", fail_if_missing=False)
    if tbl:
        tbl.insert(table)
```

### Querying Data via ADBC Driver

For SQL queries including vector search, use the VAST ADBC driver:

```python
from adbc_driver_manager import dbapi

# ADBC driver path (download from VAST GitHub Releases or Support Portal)
driver_path = "/path/to/libvastdb_adbc_driver.so"

# Table name format for ADBC queries
full_table_name = '"ai_workloads/rogers_ai_schema"."ai_documents"'

with dbapi.connect(
    driver=driver_path,
    db_kwargs={
        "vast.db.endpoint": "http://your-cluster:8081",
        "vast.db.access_key": "your-access-key",
        "vast.db.secret_key": "your-secret-key"
    }
) as conn:
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT ID, UUID, SourceDocumentName, DocumentChunkText
            FROM {full_table_name}
            WHERE DocumentStatus = 'Active'
              AND ContainsPII = FALSE
            LIMIT 100
        """)
        result = cur.fetch_arrow_table().to_pandas()
```

### Querying via Trino Connector

VASTDB also integrates with Trino for SQL-based queries:

```sql
-- Basic SELECT (Trino syntax)
SELECT ID, UUID, SourceDocumentName, DocumentChunkText
FROM ai_workloads.rogers_ai_schema.ai_documents
WHERE DocumentStatus = 'Active'
  AND ContainsPII = FALSE
LIMIT 100;

-- GDPR compliance query
SELECT UUID, SourceDocumentName, DeletionScheduledDate
FROM ai_workloads.rogers_ai_schema.ai_documents
WHERE DeletionScheduledDate <= CURRENT_TIMESTAMP
  AND DeletionStatus = 'Scheduled';
```

---

## Vector Similarity Search

**Important**: Vector search queries should be executed via the ADBC driver for best performance.

### Cosine Similarity (Recommended for Embeddings)

```python
from adbc_driver_manager import dbapi

# Build query vector as SQL array with type cast
query_vec = [0.1, 0.2, 0.3, ...]  # Your 1024-dim embedding
vec_str = f"[{', '.join(map(str, query_vec))}]"
vec_sql = f"{vec_str}::FLOAT[1024]"  # Type cast required

full_table_name = '"ai_workloads/rogers_ai_schema"."ai_documents"'

query = f"""
SELECT 
    ID, 
    UUID,
    SourceDocumentName, 
    DocumentChunkText,
    array_cosine_distance(DocumentEmbeddingVectors01, {vec_sql}) AS distance
FROM {full_table_name}
WHERE DocumentStatus = 'Active'
  AND ContainsPII = FALSE
  AND DocumentEmbeddingVectors01 IS NOT NULL
ORDER BY distance ASC
LIMIT 10
"""

with dbapi.connect(driver=driver_path, db_kwargs={...}) as conn:
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetch_arrow_table().to_pandas()
```

### Euclidean Distance

```python
# Using array_distance() for Euclidean distance
vec_sql = f"[{', '.join(map(str, query_vec))}]::FLOAT[1024]"

query = f"""
SELECT 
    ID,
    SourceDocumentName,
    DocumentChunkText,
    array_distance(DocumentEmbeddingVectors01, {vec_sql}) AS distance
FROM "{bucket}/{schema}"."{table}"
WHERE DocumentStatus = 'Active'
  AND array_distance(DocumentEmbeddingVectors01, {vec_sql}) < 1.5
ORDER BY distance ASC
LIMIT 20
"""
```

### Filtered RAG Query with Compliance

```sql
-- Production RAG query with access control
SELECT 
    ID,
    UUID,
    SourceDocumentName,
    DocumentChunkText,
    array_cosine_distance(DocumentEmbeddingVectors01, ARRAY[...]) AS similarity
FROM ai_workloads.rogers_ai_schema.ai_documents
WHERE DocumentStatus = 'Active'
  AND ContainsPII = FALSE
  AND AccessControlLevel IN ('Public', 'Internal')
  AND RiskLevel IN ('Low', 'Medium')
  AND DataQualityScore >= 70
ORDER BY similarity ASC
LIMIT 10;
```

### Multi-Provider Comparison

```sql
-- Compare embeddings from different providers
SELECT 
    ID,
    SourceDocumentName,
    DocumentEmbeddingModel01,
    array_cosine_distance(DocumentEmbeddingVectors01, ARRAY[...]) AS dist_provider1,
    DocumentEmbeddingModel02,
    array_cosine_distance(DocumentEmbeddingVectors02, ARRAY[...]) AS dist_provider2
FROM ai_workloads.rogers_ai_schema.ai_documents
WHERE DocumentEmbeddingVectors01 IS NOT NULL
  AND DocumentEmbeddingVectors02 IS NOT NULL
ORDER BY dist_provider1 ASC
LIMIT 10;
```

---

## Application-Layer Requirements

Since VASTDB does not support certain database-level features, your application must handle:

### 1. ID Generation

```python
import threading

class IDGenerator:
    """Thread-safe ID generator for VASTDB."""
    
    def __init__(self, start_id: int = 1):
        self._counter = start_id
        self._lock = threading.Lock()
    
    def next_id(self) -> int:
        with self._lock:
            current = self._counter
            self._counter += 1
            return current

# Usage
id_gen = IDGenerator()
new_id = id_gen.next_id()
```

### 2. UUID Generation

```python
import uuid

def generate_uuid() -> str:
    return str(uuid.uuid4())
```

### 3. Timestamp Management

```python
from datetime import datetime, timezone

def get_current_timestamp() -> datetime:
    return datetime.now(timezone.utc)

# Set both InsertDateTime and UpdateDateTime on insert
record["InsertDateTime"] = get_current_timestamp()
record["UpdateDateTime"] = get_current_timestamp()

# Update only UpdateDateTime on modification
record["UpdateDateTime"] = get_current_timestamp()
```

### 4. Field Validation (CHECK Constraint Replacement)

```python
VALID_DOCUMENT_STATUS = ["Draft", "Active", "Deprecated", "Archived", "Deleted", "UnderReview"]
VALID_ACCESS_LEVELS = ["Public", "Internal", "Confidential", "Restricted", "Classified"]
VALID_RISK_LEVELS = ["Low", "Medium", "High", "Critical", "Unassessed"]

def validate_document(record: dict) -> None:
    """Validate record fields before insert."""
    
    # Required field validation
    if not record.get("DocumentStatus"):
        raise ValueError("DocumentStatus is required")
    if record["DocumentStatus"] not in VALID_DOCUMENT_STATUS:
        raise ValueError(f"Invalid DocumentStatus: {record['DocumentStatus']}")
    
    # Score range validation
    if record.get("DataQualityScore") is not None:
        score = record["DataQualityScore"]
        if score < 0 or score > 100:
            raise ValueError(f"DataQualityScore must be 0-100, got {score}")
    
    # Enum validation
    if record.get("AccessControlLevel"):
        if record["AccessControlLevel"] not in VALID_ACCESS_LEVELS:
            raise ValueError(f"Invalid AccessControlLevel")
```

### 5. JSON Field Handling

```python
import json

# Storing JSON as string
record["PIITypes"] = json.dumps(["email", "phone", "address"])
record["DataLineageChain"] = json.dumps({
    "source": "web_scraper",
    "transforms": ["clean", "chunk", "embed"]
})
record["AllowedRoles"] = json.dumps(["admin", "data_scientist"])

# Retrieving and parsing JSON
pii_types = json.loads(record["PIITypes"])  # Returns list
lineage = json.loads(record["DataLineageChain"])  # Returns dict
```

---

## Integration Examples

### Python RAG Pipeline

```python
import vastdb
import pyarrow as pa
from datetime import datetime, timezone
import uuid
import numpy as np

def ingest_document(
    session,  # vastdb session from vastdb.connect()
    document_name: str,
    chunks: list[str],
    embeddings: list[np.ndarray],
    bucket_name: str = "ai_workloads",
    schema_name: str = "rogers_ai_schema",
    user: str = "ingestion_pipeline"
) -> list[str]:
    """
    Ingest a document with its chunks and embeddings.
    
    Returns list of UUIDs for the inserted records.
    """
    now = datetime.now(timezone.utc)
    uuids = []
    
    records = []
    for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        doc_uuid = str(uuid.uuid4())
        uuids.append(doc_uuid)
        
        records.append({
            "ID": i + 1,  # In production, use a proper ID generator
            "UUID": doc_uuid,
            "RogersAISchemaVersion": "1.0.0-tier1",
            "InsertDateTime": now,
            "UpdateDateTime": now,
            "InsertUser": user,
            "UpdateUser": user,
            "SourceDocumentName": document_name,
            "DocumentChunkNumber": i + 1,
            "DocumentChunkText": chunk_text,
            "DocumentEmbeddingModel01": "Qwen/Qwen3-Embedding-0.6B",
            "DocumentEmbeddingVectors01": embedding.tolist(),
            "ContainsPII": False,
            "AccessControlLevel": "Internal",
            "DocumentStatus": "Active",
            # ... set remaining fields as needed
        })
    
    # Convert to PyArrow and insert
    table = pa.Table.from_pylist(records)
    
    with session.transaction() as tx:
        bucket = tx.bucket(bucket_name)
        # Use fail_if_missing=False pattern
        schema = bucket.schema(schema_name, fail_if_missing=False)
        if schema:
            tbl = schema.table("ai_documents", fail_if_missing=False)
            if tbl:
                tbl.insert(table)
    
    return uuids
```

### LangChain Integration

```python
from langchain.vectorstores.base import VectorStore
from langchain.embeddings.base import Embeddings
from typing import List, Tuple
import vastdb

class VASTDBVectorStore(VectorStore):
    """LangChain VectorStore implementation for VASTDB."""
    
    def __init__(
        self,
        session: vastdb.Session,
        embedding_function: Embeddings,
        bucket: str = "ai_workloads",
        schema: str = "rogers_ai_schema",
        table: str = "ai_documents",
    ):
        self.session = session
        self.embedding_function = embedding_function
        self.bucket = bucket
        self.schema = schema
        self.table = table
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        **kwargs
    ) -> List[Document]:
        # Get query embedding
        query_vector = self.embedding_function.embed_query(query)
        
        # Execute vector search via Trino
        sql = f"""
        SELECT DocumentChunkText, SourceDocumentName,
               array_cosine_distance(DocumentEmbeddingVectors01, ARRAY{query_vector}) AS distance
        FROM {self.bucket}.{self.schema}.{self.table}
        WHERE DocumentStatus = 'Active'
          AND ContainsPII = FALSE
        ORDER BY distance ASC
        LIMIT {k}
        """
        
        # Execute query and return results
        # ... implementation details
```

---

## Performance Considerations

### Vector Search Optimization

Since VASTDB doesn't support vector indexes (in 5.4 it does in 5.5 soon to be released), consider these strategies in the short term:

1. **Pre-filtering**: Use WHERE clauses to reduce the dataset before vector comparison
   ```sql
   WHERE DocumentStatus = 'Active' 
     AND DatasetType = 'Production'
     AND ContainsPII = FALSE
   ```

2. **Partitioning**: Organize data by dataset type, date, or access level

3. **Batch Processing**: Process large ingestion jobs in batches of 5MB (VAST row batch limit)

### Query Performance Tips

| Strategy | Impact | Example |
|----------|--------|---------|
| Filter early | High | Add WHERE before ORDER BY distance |
| Limit results | High | Always use LIMIT clause |
| Avoid SELECT * | Medium | Select only needed columns |
| Use appropriate types | Medium | Match vector dimensions exactly |

### Storage Considerations

| Limit | Value | Notes |
|-------|-------|-------|
| Max cell size | 126 KB | Chunk large documents |
| Row batch insert | 5 MB | Batch inserts for efficiency |
| Max columns | 31,936 | Plenty for 52-field schema |
| Max rows | 256 trillion | Enterprise scale |

---

## Related Documentation

- [../DESIGN.md](../DESIGN.md) - Complete schema specification
- [../COMPLIANCE.md](../COMPLIANCE.md) - Regulatory mapping
- [../future/TIER2_TIER3_ROADMAP.md](../future/TIER2_TIER3_ROADMAP.md) - Future enhancements

### Other Platform Guides

- [POSTGRESQL.md](POSTGRESQL.md) - PostgreSQL with pgvector
- [SQLITE_VECTOR.md](SQLITE_VECTOR.md) - SQLite with sqlite-vec

### External Resources

- [VAST Data Platform Documentation](https://vast-data.github.io/data-platform-field-docs/)
- [VASTDB Python SDK](https://pypi.org/project/vastdb/)
- [Apache Arrow/PyArrow](https://arrow.apache.org/docs/python/)

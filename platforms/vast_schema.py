#!/usr/bin/env python3
"""
Rogers-AI-Schema Tier 1 - VAST Data Platform Implementation
Version: 1.0.0-tier1
Platform: VAST Data Platform (VASTDB)

NOTE: This file is named 'vast_schema.py' (not 'vastdb.py') to avoid
shadowing the 'vastdb' Python package during import.

Copyright (C) 2025 Matthew Rogers, CISSP
Field CTO for AI and Security at VAST Data
Licensed under GNU General Public License v3.0
https://github.com/RamboRogers/rogers-ai-schema

This script creates the ai_documents table in VASTDB using PyArrow schemas.
VASTDB is the native database engine for the VAST Data Platform.

Prerequisites:
    pip install vastdb pyarrow

Usage:
    # Set environment variables
    export VAST_ENDPOINT="your-vast-cluster.example.com"
    export VAST_ACCESS_KEY="your-access-key"
    export VAST_SECRET_KEY="your-secret-key"
    export VAST_BUCKET="octo-db"
    export VAST_SCHEMA="rogers_ai_schema"
    export VECTOR_DIMENSIONS="1024"
    # Run the script
    python vast_schema.py

VASTDB Features & Limitations (handled by this implementation):
    
    vastdb_rowid Auto-Increment Support:
    - VAST provides native auto-incrementing row IDs via the 'vastdb_rowid' column
    - Two allocation modes (mode is locked on first insert):
      * Internal allocation: Omit vastdb_rowid on insert, VAST auto-generates IDs
      * External allocation: Provide vastdb_rowid values on insert (max: 2^48-1)
    - Filtering on vastdb_rowid enables efficient tree pruning for fast queries
    - Cannot update vastdb_rowid values after insert
    - Cannot add/drop/rename the vastdb_rowid column (except on empty tables)
    
    Limitations (application layer required):
    - No NOT NULL constraints - all columns must be nullable, validate in application
    - No vector indexes (HNSW, IVFFlat) - uses brute-force search with array_cosine_distance()
    - No triggers - timestamps must be set at application layer
    - No CHECK constraints - validation must be done at application layer
    - No DEFAULT values - must be set at application layer
    - No gen_random_uuid() - UUIDs must be generated in Python
    - No JSONB type - JSON stored as strings
    - DISTINCT limited - avoid COUNT(DISTINCT column) patterns
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

import pyarrow as pa

# Optional: Import vastdb SDK if available
try:
    import vastdb
    VASTDB_AVAILABLE = True
except ImportError:
    VASTDB_AVAILABLE = False
    print("Warning: vastdb SDK not installed. Install with: pip install vastdb")

# Optional: Import ADBC driver for SQL queries
try:
    from adbc_driver_manager import dbapi
    ADBC_AVAILABLE = True
except ImportError:
    ADBC_AVAILABLE = False
    dbapi = None


# =============================================================================
# Configuration
# =============================================================================

# VAST cluster connection settings (from environment variables)
VAST_ENDPOINT = os.environ.get("VAST_ENDPOINT", "localhost")
VAST_ACCESS_KEY = os.environ.get("VAST_ACCESS_KEY", "")
VAST_SECRET_KEY = os.environ.get("VAST_SECRET_KEY", "")

# Database/Bucket settings
BUCKET_NAME = os.environ.get("VAST_BUCKET", "octo-db")
SCHEMA_NAME = os.environ.get("VAST_SCHEMA", "rogers_ai_schema")
TABLE_NAME = "ai_documents"

# Vector embedding configuration
# Default: 1024 dimensions (compatible with Qwen, Cohere, and many other models)
# Modify as needed for your embedding provider
VECTOR_DIMENSIONS = int(os.environ.get("VECTOR_DIMENSIONS", "1024"))

# ADBC Driver path (required for SQL queries including vector search)
# Download from VAST GitHub Releases or Support Portal
ADBC_DRIVER_PATH = os.environ.get("VAST_ADBC_DRIVER_PATH", "")

# Schema version
ROGERS_AI_SCHEMA_VERSION = "1.0.0-tier1"


# =============================================================================
# PyArrow Schema Definition - Rogers-AI-Schema Tier 1 (52 Fields)
# =============================================================================

def create_vector_field(name: str, dims: int) -> pa.Field:
    """
    Create a properly formatted vector field for VASTDB.
    
    VASTDB requires vector columns to use the specific pattern:
    pa.list_(pa.field(name="item", type=pa.float32(), nullable=False), dims)
    
    Note: VASTDB does not support NOT NULL constraints, so column is always nullable.
    The inner "item" field is non-nullable per VAST's vector format requirement.
    
    Args:
        name: Column name
        dims: Vector dimensions
    
    Returns:
        PyArrow Field with correct VAST vector format
    """
    vector_type = pa.list_(
        pa.field(name="item", type=pa.float32(), nullable=False),
        dims
    )
    return pa.field(name, vector_type)


def create_ai_documents_schema(vector_dims: int = VECTOR_DIMENSIONS) -> pa.Schema:
    """
    Create the PyArrow schema for the ai_documents table.
    
    This schema implements all 52 Tier 1 fields from Rogers-AI-Schema,
    adapted for VASTDB's supported data types.
    
    Args:
        vector_dims: Dimension size for vector embedding columns (default: 1024)
    
    Returns:
        PyArrow Schema object for table creation
    """
    
    # NOTE: VASTDB does not support NOT NULL constraints on columns.
    # All columns must be nullable. Validation must be done at application layer.
    
    schema = pa.schema([
        # =============================================
        # Core Identity & Audit (7 fields)
        # Application must ensure these are populated (no NOT NULL in VASTDB)
        # =============================================
        # vastdb_rowid: VAST-managed auto-incrementing row ID
        # - Internal allocation: Omit value on insert, VAST auto-generates
        # - External allocation: Provide value on insert (max: 2^48-1)
        # - Allocation mode is locked on first insert to table
        # - Enables efficient filtering: WHERE vastdb_rowid > X AND vastdb_rowid < Y
        pa.field("vastdb_rowid", pa.int64()),
        # UUID: Application-generated string UUID
        pa.field("UUID", pa.string()),
        # Schema version for compatibility tracking
        pa.field("RogersAISchemaVersion", pa.string()),
        # Timestamps: Application must set these (no DEFAULT in VASTDB)
        pa.field("InsertDateTime", pa.timestamp('us', tz='UTC')),
        pa.field("UpdateDateTime", pa.timestamp('us', tz='UTC')),
        # Audit user tracking
        pa.field("InsertUser", pa.string()),
        pa.field("UpdateUser", pa.string()),
        
        # =============================================
        # Source Document Metadata (7 fields)
        # =============================================
        pa.field("SourceDocumentName", pa.string()),
        pa.field("SourceDocumentPath", pa.string()),
        pa.field("SourceDocumentHash", pa.string()),
        pa.field("SourceDocumentTitle", pa.string()),
        pa.field("SourceDocumentSummary", pa.string()),
        pa.field("SourceDocumentAuthor", pa.string()),
        pa.field("SourceDocumentOrganization", pa.string()),
        
        # =============================================
        # Document Content & Chunking (2 fields)
        # =============================================
        pa.field("DocumentChunkNumber", pa.int32()),
        pa.field("DocumentChunkText", pa.string()),
        
        # =============================================
        # Vector Embeddings - 5 Providers (15 fields)
        # Each provider has: Model name, URL, and Vector array
        # Using VAST-compatible fixed-size list format for vector columns
        # =============================================
        
        # Provider 01 (e.g., Qwen/Qwen3-Embedding-0.6B)
        pa.field("DocumentEmbeddingModel01", pa.string()),
        pa.field("DocumentEmbeddingURL01", pa.string()),
        create_vector_field("DocumentEmbeddingVectors01", vector_dims),
        
        # Provider 02 (e.g., OpenAI text-embedding-ada-002)
        pa.field("DocumentEmbeddingModel02", pa.string()),
        pa.field("DocumentEmbeddingURL02", pa.string()),
        create_vector_field("DocumentEmbeddingVectors02", vector_dims),
        
        # Provider 03 (e.g., sentence-transformers)
        pa.field("DocumentEmbeddingModel03", pa.string()),
        pa.field("DocumentEmbeddingURL03", pa.string()),
        create_vector_field("DocumentEmbeddingVectors03", vector_dims),
        
        # Provider 04 (e.g., all-MiniLM-L6-v2)
        pa.field("DocumentEmbeddingModel04", pa.string()),
        pa.field("DocumentEmbeddingURL04", pa.string()),
        create_vector_field("DocumentEmbeddingVectors04", vector_dims),
        
        # Provider 05 (e.g., custom/internal model)
        pa.field("DocumentEmbeddingModel05", pa.string()),
        pa.field("DocumentEmbeddingURL05", pa.string()),
        create_vector_field("DocumentEmbeddingVectors05", vector_dims),
        
        # =============================================
        # Privacy & PII Protection (10 fields) - GDPR Compliant
        # =============================================
        pa.field("ContainsPII", pa.bool_()),
        # PIITypes: JSON array stored as string (no JSONB in VASTDB)
        # Example: '["email", "phone", "address"]'
        pa.field("PIITypes", pa.string()),
        # Allowed values: 'automated', 'manual', 'both', 'not_detected'
        pa.field("PIIDetectionMethod", pa.string()),
        pa.field("PIIDetectionDate", pa.timestamp('us', tz='UTC')),
        # Allowed values: 'None', 'Low', 'Medium', 'High', 'Critical'
        pa.field("SensitiveDataClassification", pa.string()),
        # GDPR Article 6 legal basis
        # Allowed values: 'Consent', 'Contract', 'LegalObligation', 'VitalInterests', 'PublicTask', 'LegitimateInterests'
        pa.field("LegalBasisForProcessing", pa.string()),
        # Days to retain data before deletion
        pa.field("DataRetentionPeriod", pa.int32()),
        pa.field("DeletionScheduledDate", pa.timestamp('us', tz='UTC')),
        # Allowed values: 'Pending', 'Scheduled', 'Deleted', 'Retained', 'AwaitingApproval'
        pa.field("DeletionStatus", pa.string()),
        # Allowed values: 'NotAnonymized', 'Pseudonymized', 'FullyAnonymized'
        pa.field("AnonymizationStatus", pa.string()),
        
        # =============================================
        # Data Governance & Lineage (8 fields) - NIST AI RMF
        # =============================================
        # Allowed values: 'Training', 'Validation', 'Testing', 'Production', 'KnowledgeBase', 'Archive'
        pa.field("DatasetType", pa.string()),
        pa.field("DatasetPurpose", pa.string()),
        # Quality score 0-100 (application must validate range)
        pa.field("DataQualityScore", pa.float64()),
        # Allowed values: 'Pending', 'Validated', 'Failed', 'NeedsReview', 'InProgress'
        pa.field("DataValidationStatus", pa.string()),
        pa.field("DataValidationDate", pa.timestamp('us', tz='UTC')),
        pa.field("DataValidatedBy", pa.string()),
        # DataLineageChain: JSON object stored as string (no JSONB in VASTDB)
        # Example: '{"source": "web_scraper", "transforms": ["clean", "chunk"]}'
        pa.field("DataLineageChain", pa.string()),
        # Allowed values: 'Web', 'Database', 'API', 'FileSystem', 'Manual', 'Email', 'S3', 'SharePoint', 'Other'
        pa.field("OriginalSourceType", pa.string()),
        
        # =============================================
        # Legal & Licensing Tracking (6 fields)
        # =============================================
        # Allowed values: 'PublicDomain', 'Copyrighted', 'CreativeCommons', 'Unknown', 'ProprietaryInternal'
        pa.field("CopyrightStatus", pa.string()),
        pa.field("LicenseType", pa.string()),
        pa.field("UsageRestrictions", pa.string()),
        pa.field("CommercialUseAllowed", pa.bool_()),
        pa.field("AttributionRequired", pa.bool_()),
        pa.field("AttributionText", pa.string()),
        
        # =============================================
        # Risk Management & Content Safety (4 fields) - NIST AI RMF
        # =============================================
        # Allowed values: 'Low', 'Medium', 'High', 'Critical', 'Unassessed'
        pa.field("RiskLevel", pa.string()),
        # Allowed values: 'Safe', 'Flagged', 'Unsafe', 'UnderReview', 'NotAssessed'
        pa.field("ContentSafetyStatus", pa.string()),
        # Safety score 0-100 (application must validate range)
        pa.field("ContentSafetyScore", pa.float64()),
        pa.field("ContentModerationDate", pa.timestamp('us', tz='UTC')),
        
        # =============================================
        # Access Control & Security (3 fields)
        # =============================================
        # Allowed values: 'Public', 'Internal', 'Confidential', 'Restricted', 'Classified'
        pa.field("AccessControlLevel", pa.string()),
        pa.field("DataClassification", pa.string()),
        # AllowedRoles: JSON array stored as string
        # Example: '["admin", "data_scientist", "analyst"]'
        pa.field("AllowedRoles", pa.string()),
        
        # =============================================
        # Enhanced Audit Trail (1 field) - EU AI Act Article 12
        # =============================================
        pa.field("LastModifiedReason", pa.string()),
        
        # =============================================
        # Document Lifecycle Management (2 fields)
        # =============================================
        # Allowed values: 'Draft', 'Active', 'Deprecated', 'Archived', 'Deleted', 'UnderReview'
        pa.field("DocumentStatus", pa.string()),
        pa.field("DocumentVersion", pa.string()),
    ])
    
    return schema


# =============================================================================
# Helper Functions for Application-Layer Operations
# =============================================================================

def generate_uuid() -> str:
    """Generate a new UUID string for document identification."""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get the current UTC timestamp for insert/update times."""
    return datetime.now(timezone.utc)


def validate_enum_field(value: str, allowed_values: List[str], field_name: str) -> str:
    """
    Validate that a field value is one of the allowed enum values.
    
    VASTDB does not support CHECK constraints, so validation must be done
    at the application layer.
    
    Args:
        value: The value to validate
        allowed_values: List of allowed string values
        field_name: Name of the field (for error messages)
    
    Returns:
        The validated value
    
    Raises:
        ValueError: If value is not in allowed_values
    """
    if value not in allowed_values:
        raise ValueError(
            f"Invalid value '{value}' for {field_name}. "
            f"Allowed values: {allowed_values}"
        )
    return value


def validate_score_range(value: float, field_name: str, min_val: float = 0, max_val: float = 100) -> float:
    """
    Validate that a score is within the allowed range.
    
    Args:
        value: The score value to validate
        field_name: Name of the field (for error messages)
        min_val: Minimum allowed value (default: 0)
        max_val: Maximum allowed value (default: 100)
    
    Returns:
        The validated value
    
    Raises:
        ValueError: If value is outside the allowed range
    """
    if value < min_val or value > max_val:
        raise ValueError(
            f"Invalid value {value} for {field_name}. "
            f"Must be between {min_val} and {max_val}"
        )
    return value


# =============================================================================
# vastdb_rowid Allocation Modes
# =============================================================================
#
# VAST Data Platform supports two allocation modes for the vastdb_rowid column.
# The mode is determined by the first INSERT operation and is locked for the
# lifetime of the table.
#
# INTERNAL ALLOCATION (Recommended for most use cases)
# -----------------------------------------------------
# - Omit vastdb_rowid from INSERT or set to None/NULL
# - VAST automatically generates sequential row IDs
# - Similar to PostgreSQL BIGSERIAL or MySQL AUTO_INCREMENT
# - Example:
#     record = create_example_record(
#         insert_user="pipeline",
#         document_name="doc.pdf",
#         chunk_text="content...",
#         # vastdb_rowid omitted - VAST will auto-generate
#     )
#
# EXTERNAL ALLOCATION (For custom partitioning/ID schemes)
# ---------------------------------------------------------
# - Provide vastdb_rowid value on INSERT (must be <= 2^48-1)
# - User is responsible for ensuring uniqueness
# - Enables custom partitioning: group related rows in ID ranges
# - Useful for Splunk integration (UUID-like lookups)
# - Example:
#     record = create_example_record(
#         insert_user="pipeline",
#         document_name="doc.pdf",
#         chunk_text="content...",
#         vastdb_rowid=1000001,  # User-controlled ID
#     )
#
# KEY CONSTRAINTS:
# - Cannot mix allocation modes within a table
# - Cannot UPDATE vastdb_rowid values
# - Cannot ADD/DROP/RENAME vastdb_rowid column (except on empty tables)
# - Reinserting deleted row IDs may cause brief write conflicts with truncator
# - Max value: 2^48-1 (281,474,976,710,655)
#
# QUERY PERFORMANCE:
# - Filtering on vastdb_rowid enables efficient tree pruning
# - Range queries (vastdb_rowid > X AND vastdb_rowid < Y) are very fast
# - Single-record lookups by vastdb_rowid are extremely efficient
#
# =============================================================================


# =============================================================================
# Enum Value Definitions (for validation)
# =============================================================================

ENUM_VALUES = {
    "PIIDetectionMethod": ["automated", "manual", "both", "not_detected"],
    "SensitiveDataClassification": ["None", "Low", "Medium", "High", "Critical"],
    "LegalBasisForProcessing": [
        "Consent", "Contract", "LegalObligation", 
        "VitalInterests", "PublicTask", "LegitimateInterests"
    ],
    "DeletionStatus": ["Pending", "Scheduled", "Deleted", "Retained", "AwaitingApproval"],
    "AnonymizationStatus": ["NotAnonymized", "Pseudonymized", "FullyAnonymized"],
    "DatasetType": ["Training", "Validation", "Testing", "Production", "KnowledgeBase", "Archive"],
    "DataValidationStatus": ["Pending", "Validated", "Failed", "NeedsReview", "InProgress"],
    "OriginalSourceType": [
        "Web", "Database", "API", "FileSystem", "Manual", 
        "Email", "S3", "SharePoint", "Other"
    ],
    "CopyrightStatus": [
        "PublicDomain", "Copyrighted", "CreativeCommons", 
        "Unknown", "ProprietaryInternal"
    ],
    "RiskLevel": ["Low", "Medium", "High", "Critical", "Unassessed"],
    "ContentSafetyStatus": ["Safe", "Flagged", "Unsafe", "UnderReview", "NotAssessed"],
    "AccessControlLevel": ["Public", "Internal", "Confidential", "Restricted", "Classified"],
    "DocumentStatus": ["Draft", "Active", "Deprecated", "Archived", "Deleted", "UnderReview"],
}


# =============================================================================
# VASTDB Table Management Functions
# =============================================================================

def create_table_in_vastdb(
    endpoint: str = VAST_ENDPOINT,
    access_key: str = VAST_ACCESS_KEY,
    secret_key: str = VAST_SECRET_KEY,
    bucket_name: str = BUCKET_NAME,
    schema_name: str = SCHEMA_NAME,
    table_name: str = TABLE_NAME,
    vector_dims: int = VECTOR_DIMENSIONS,
    drop_existing: bool = False,
) -> bool:
    """
    Create the ai_documents table in VASTDB.
    
    This function connects to the VAST cluster, creates the bucket/schema
    if needed, and creates the ai_documents table with the full Tier 1 schema.
    
    Args:
        endpoint: VAST cluster endpoint
        access_key: Access key for authentication
        secret_key: Secret key for authentication
        bucket_name: Name of the bucket (database)
        schema_name: Name of the schema within the bucket
        table_name: Name of the table to create
        vector_dims: Dimension size for vector columns
        drop_existing: If True, drop existing table before creating (for dev/testing)
    
    Returns:
        True if table was created successfully
    
    Raises:
        RuntimeError: If vastdb SDK is not available
        Exception: If table creation fails
    """
    if not VASTDB_AVAILABLE:
        raise RuntimeError(
            "vastdb SDK is not installed. Install with: pip install vastdb"
        )
    
    # Get the PyArrow schema
    arrow_schema = create_ai_documents_schema(vector_dims)
    
    print(f"Connecting to VAST cluster at {endpoint}...")
    
    # Connect to VAST cluster
    # Note: vastdb.connect() uses 'access' and 'secret' parameter names
    session = vastdb.connect(
        endpoint=endpoint,
        access=access_key,
        secret=secret_key,
    )
    
    print(f"Connected successfully!")
    print(f"Accessing bucket: {bucket_name}")
    
    # Create or get bucket, schema, and table
    with session.transaction() as tx:
        # Get bucket (bucket must exist - created via VAST management console)
        bucket = tx.bucket(bucket_name)
        
        print(f"Creating/accessing schema: {schema_name}")
        
        # Get or create schema using VAST SDK pattern with fail_if_missing=False
        schema = bucket.schema(schema_name, fail_if_missing=False) or \
                 bucket.create_schema(schema_name)
        
        print(f"Creating/accessing table: {table_name}")
        
        # Check if table exists using fail_if_missing=False
        existing_table = schema.table(table_name, fail_if_missing=False)
        
        if existing_table:
            if drop_existing:
                print(f"Dropping existing table '{table_name}'...")
                existing_table.drop()
                print(f"Table dropped. Creating fresh table...")
            else:
                print(f"Table '{table_name}' already exists.")
                print(f"  (Use --drop to recreate)")
                print(f"")
                print(f"✓ Table '{table_name}' ready!")
                print(f"  Schema: {schema_name}")
                print(f"  Bucket: {bucket_name}")
                print(f"  Vector dimensions: {vector_dims}")
                print(f"  Total columns: {len(arrow_schema)}")
                return True
        
        # Create new table with PyArrow schema
        table = schema.create_table(table_name, arrow_schema)
        
        if table:
            print(f"")
            print(f"✓ Table '{table_name}' created successfully!")
            print(f"  Schema: {schema_name}")
            print(f"  Bucket: {bucket_name}")
            print(f"  Vector dimensions: {vector_dims}")
            print(f"  Total columns: {len(arrow_schema)}")
            return True
    
    return False


def print_schema_info(vector_dims: int = VECTOR_DIMENSIONS):
    """Print detailed information about the schema."""
    schema = create_ai_documents_schema(vector_dims)
    
    print("\n" + "=" * 70)
    print("Rogers-AI-Schema v1.0.0-tier1 - VASTDB Implementation")
    print("=" * 70)
    print(f"\nTotal fields: {len(schema)}")
    print(f"Vector dimensions: {vector_dims}")
    print("\nField Groups:")
    print("-" * 40)
    
    groups = [
        ("Core Identity & Audit", 7),
        ("Source Document Metadata", 7),
        ("Document Content & Chunking", 2),
        ("Vector Embeddings (5 providers)", 15),
        ("Privacy & PII Protection", 10),
        ("Data Governance & Lineage", 8),
        ("Legal & Licensing Tracking", 6),
        ("Risk Management & Content Safety", 4),
        ("Access Control & Security", 3),
        ("Enhanced Audit Trail", 1),
        ("Document Lifecycle Management", 2),
    ]
    
    for group_name, count in groups:
        print(f"  {group_name}: {count} fields")
    
    print("\n" + "-" * 40)
    print("Schema Fields:")
    print("-" * 40)
    
    for i, field in enumerate(schema):
        nullable = "NULL" if field.nullable else "NOT NULL"
        print(f"  {i+1:2}. {field.name}: {field.type} ({nullable})")
    
    print("\n" + "=" * 70)


# =============================================================================
# Example Usage Functions
# =============================================================================

def create_example_record(
    insert_user: str,
    document_name: str,
    chunk_text: str,
    embedding_vector: Optional[List[float]] = None,
    vastdb_rowid: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Create an example record dictionary with proper field values.
    
    This demonstrates how to properly populate all required fields
    when inserting data into VASTDB.
    
    Args:
        insert_user: Username performing the insert
        document_name: Name of the source document
        chunk_text: The text content of this chunk
        embedding_vector: Optional embedding vector (must match VECTOR_DIMENSIONS)
        vastdb_rowid: Optional row ID for external allocation mode.
            - If None (default): Uses internal allocation, VAST auto-generates the ID
            - If provided: Uses external allocation, must be <= 2^48-1
            NOTE: Allocation mode is locked on first insert to the table.
    
    Returns:
        Dictionary with all fields properly set
    """
    now = get_current_timestamp()
    
    record = {
        # Core Identity & Audit
        # vastdb_rowid: Omit for internal allocation (VAST auto-generates),
        # or provide value for external allocation (max: 2^48-1)
        "vastdb_rowid": vastdb_rowid,  # None = internal allocation (auto-increment)
        "UUID": generate_uuid(),
        "RogersAISchemaVersion": ROGERS_AI_SCHEMA_VERSION,
        "InsertDateTime": now,
        "UpdateDateTime": now,
        "InsertUser": insert_user,
        "UpdateUser": insert_user,
        
        # Source Document Metadata
        "SourceDocumentName": document_name,
        "SourceDocumentPath": None,
        "SourceDocumentHash": None,
        "SourceDocumentTitle": None,
        "SourceDocumentSummary": None,
        "SourceDocumentAuthor": None,
        "SourceDocumentOrganization": None,
        
        # Document Content & Chunking
        "DocumentChunkNumber": 1,
        "DocumentChunkText": chunk_text,
        
        # Vector Embeddings (set first provider if vector provided)
        "DocumentEmbeddingModel01": "example-model" if embedding_vector else None,
        "DocumentEmbeddingURL01": None,
        "DocumentEmbeddingVectors01": embedding_vector,
        "DocumentEmbeddingModel02": None,
        "DocumentEmbeddingURL02": None,
        "DocumentEmbeddingVectors02": None,
        "DocumentEmbeddingModel03": None,
        "DocumentEmbeddingURL03": None,
        "DocumentEmbeddingVectors03": None,
        "DocumentEmbeddingModel04": None,
        "DocumentEmbeddingURL04": None,
        "DocumentEmbeddingVectors04": None,
        "DocumentEmbeddingModel05": None,
        "DocumentEmbeddingURL05": None,
        "DocumentEmbeddingVectors05": None,
        
        # Privacy & PII Protection (defaults for non-PII content)
        "ContainsPII": False,
        "PIITypes": None,
        "PIIDetectionMethod": "not_detected",
        "PIIDetectionDate": now,
        "SensitiveDataClassification": "None",
        "LegalBasisForProcessing": None,
        "DataRetentionPeriod": None,
        "DeletionScheduledDate": None,
        "DeletionStatus": None,
        "AnonymizationStatus": "NotAnonymized",
        
        # Data Governance & Lineage
        "DatasetType": "Production",
        "DatasetPurpose": None,
        "DataQualityScore": None,
        "DataValidationStatus": "Pending",
        "DataValidationDate": None,
        "DataValidatedBy": None,
        "DataLineageChain": None,
        "OriginalSourceType": "FileSystem",
        
        # Legal & Licensing
        "CopyrightStatus": None,
        "LicenseType": None,
        "UsageRestrictions": None,
        "CommercialUseAllowed": None,
        "AttributionRequired": None,
        "AttributionText": None,
        
        # Risk Management
        "RiskLevel": "Low",
        "ContentSafetyStatus": "NotAssessed",
        "ContentSafetyScore": None,
        "ContentModerationDate": None,
        
        # Access Control
        "AccessControlLevel": "Internal",
        "DataClassification": None,
        "AllowedRoles": None,
        
        # Audit Trail
        "LastModifiedReason": "Initial insert",
        
        # Lifecycle
        "DocumentStatus": "Active",
        "DocumentVersion": "1.0",
    }
    
    return record


# =============================================================================
# Vector Search Query Examples (for documentation)
# =============================================================================

VECTOR_SEARCH_EXAMPLES = """
-- =============================================================================
-- VASTDB Vector Search Examples
-- =============================================================================
-- 
-- VASTDB provides built-in distance functions for vector similarity search.
-- Note: There are no vector indexes in VASTDB - searches perform brute-force
-- comparisons, which is optimized by VAST's architecture.
--
-- vastdb_rowid enables efficient tree pruning for range-based queries

-- Example 1: Cosine Similarity Search (recommended for embeddings)
-- Find the 10 most similar documents using cosine distance
SELECT 
    vastdb_rowid, 
    UUID,
    SourceDocumentName, 
    DocumentChunkText,
    array_cosine_distance(DocumentEmbeddingVectors01, ARRAY[0.1, 0.2, ...]) AS distance
FROM ai_documents
WHERE DocumentStatus = 'Active'
  AND ContainsPII = FALSE
ORDER BY distance ASC
LIMIT 10;

-- Example 2: Euclidean Distance Search
-- Find documents within a certain distance threshold
SELECT 
    vastdb_rowid,
    SourceDocumentName,
    DocumentChunkText,
    array_distance(DocumentEmbeddingVectors01, ARRAY[0.1, 0.2, ...]) AS distance
FROM ai_documents
WHERE DocumentStatus = 'Active'
  AND array_distance(DocumentEmbeddingVectors01, ARRAY[0.1, 0.2, ...]) < 1.5
ORDER BY distance ASC
LIMIT 20;

-- Example 3: Filtered Vector Search with Compliance Constraints
-- RAG query with access control and PII filtering
SELECT 
    vastdb_rowid,
    UUID,
    SourceDocumentName,
    DocumentChunkText,
    array_cosine_distance(DocumentEmbeddingVectors01, ARRAY[0.1, 0.2, ...]) AS similarity
FROM ai_documents
WHERE DocumentStatus = 'Active'
  AND ContainsPII = FALSE
  AND AccessControlLevel IN ('Public', 'Internal')
  AND RiskLevel IN ('Low', 'Medium')
ORDER BY similarity ASC
LIMIT 10;

-- Example 4: Multi-Provider Embedding Comparison
-- Compare results from different embedding providers
SELECT 
    vastdb_rowid,
    SourceDocumentName,
    DocumentEmbeddingModel01,
    array_cosine_distance(DocumentEmbeddingVectors01, ARRAY[...]) AS distance_provider1,
    DocumentEmbeddingModel02,
    array_cosine_distance(DocumentEmbeddingVectors02, ARRAY[...]) AS distance_provider2
FROM ai_documents
WHERE DocumentStatus = 'Active'
  AND DocumentEmbeddingVectors01 IS NOT NULL
  AND DocumentEmbeddingVectors02 IS NOT NULL
ORDER BY distance_provider1 ASC
LIMIT 10;

-- Example 5: Efficient Range Query using vastdb_rowid
-- Use vastdb_rowid for fast tree pruning - excellent for partitioning-like queries
-- This enables fast lookups by skipping irrelevant tree sections
SELECT 
    vastdb_rowid,
    UUID,
    SourceDocumentName,
    DocumentChunkText
FROM ai_documents
WHERE vastdb_rowid > 1000 AND vastdb_rowid < 2000
  AND DocumentStatus = 'Active';

-- Example 6: Single Record Lookup by vastdb_rowid
-- Extremely fast single-record retrieval using vastdb_rowid
SELECT *
FROM ai_documents
WHERE vastdb_rowid = 12345;
"""


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Rogers-AI-Schema VASTDB Implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Print schema information
    python vast_schema.py --info
    
    # Create table in VASTDB
    python vast_schema.py --create
    
    # Create table with custom vector dimensions
    python vast_schema.py --create --dims 1536
    
    # Drop and recreate table (for development/testing)
    python vast_schema.py --create --drop

Environment Variables:
    VAST_ENDPOINT         - VAST cluster endpoint (default: localhost)
    VAST_ACCESS_KEY       - Access key for authentication
    VAST_SECRET_KEY       - Secret key for authentication
    VAST_BUCKET           - Bucket name (default: octo-db)
    VAST_SCHEMA           - Schema name (default: rogers_ai_schema)
    VECTOR_DIMENSIONS     - Vector embedding dimensions (default: 1024)
    VAST_ADBC_DRIVER_PATH - Path to ADBC driver (for SQL queries)
        """
    )
    
    parser.add_argument(
        "--info", 
        action="store_true",
        help="Print schema information"
    )
    parser.add_argument(
        "--create", 
        action="store_true",
        help="Create the ai_documents table in VASTDB"
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop and recreate existing table (use with --create for dev/testing)"
    )
    parser.add_argument(
        "--dims",
        type=int,
        default=VECTOR_DIMENSIONS,
        help=f"Vector dimensions (default: {VECTOR_DIMENSIONS})"
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Print example vector search queries"
    )
    
    args = parser.parse_args()
    
    if args.info or (not args.create and not args.examples):
        print_schema_info(args.dims)
    
    if args.examples:
        print(VECTOR_SEARCH_EXAMPLES)
    
    if args.create:
        if not VAST_ACCESS_KEY or not VAST_SECRET_KEY:
            print("\nError: VAST_ACCESS_KEY and VAST_SECRET_KEY environment variables must be set.")
            print("Example:")
            print('  export VAST_ENDPOINT="your-cluster.example.com"')
            print('  export VAST_ACCESS_KEY="your-access-key"')
            print('  export VAST_SECRET_KEY="your-secret-key"')
            exit(1)
        
        if args.drop:
            print("\n⚠️  WARNING: --drop flag set. Existing table will be deleted!")
        
        try:
            success = create_table_in_vastdb(
                vector_dims=args.dims,
                drop_existing=args.drop
            )
            if success:
                print("\n✓ Table creation completed successfully!")
            else:
                print("\n✗ Table creation failed.")
                exit(1)
        except Exception as e:
            print(f"\n✗ Error creating table: {e}")
            exit(1)

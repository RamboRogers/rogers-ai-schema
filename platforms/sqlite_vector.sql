-- Rogers-AI-Schema Tier 1 - SQLite Implementation
-- Version: 1.0.0-tier1
-- Database: SQLite 3.38.0+
-- Extension: sqlite-vec for vector operations
-- NOTE: sqlite-vec requires separate vector storage tables for each provider, this is a limitation of the extension.
--
-- Copyright (C) 2025 Matthew Rogers, CISSP
-- Field CTO for AI and Security at VAST Data
-- Licensed under GNU General Public License v3.0
-- https://github.com/RamboRogers/rogers-ai-schema
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

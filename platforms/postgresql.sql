-- Rogers-AI-Schema Tier 1 - PostgreSQL Implementation
-- Version: 1.0.0-tier1
-- Database: PostgreSQL 12+
-- Extension: pgvector REQUIRED for vector operations
--
-- Copyright (C) 2025 Matthew Rogers, CISSP
-- Field CTO for AI and Security at VAST Data
-- Licensed under GNU General Public License v3.0
-- https://github.com/RamboRogers/rogers-ai-schema

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
    DocumentEmbeddingVectors01 vector(1024),  -- e.g., Qwen/Qwen3-Embedding-0.6B (1024 dims)

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
    DocumentEmbeddingVectors05 vector(2000),  -- e.g., custom/large models (2048 dims)

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

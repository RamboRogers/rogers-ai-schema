# Rogers-AI-Schema

**Author**: Matthew Rogers, CISSP
**Title**: Field CTO for AI and Security at VAST Data
**License**: GNU General Public License v3.0
**Links**: [LinkedIn](https://www.linkedin.com/in/matthewrogerscissp/) | [Twitter/X](https://x.com/Matthewrogers) | [GitHub](https://github.com/RamboRogers/) | [Website](https://matthewrogers.org)

## Purpose
Rogers-AI-Schema is a project to create a universal schema for AI workloads.  I wrote this as a standard for storing data for AI workloads to be independent of underlying Database technologies.  Each time I see a new AI App, the DB schema is confusing, missing key fields, missing important meta data and always requires constant rework.  This schema aims to solve this foundational problem, and is intended to be used with SQL databases to service both vector, text, and blob data at scale.

# Tables
A single simple table design with all the right fields to do proper AI data transcations at scale, ensuring all meta data is retained, verisioned and is setup for proper lineage in compliance with NIST best practices and EU AI Act requirements. If separate data stores are required in different namespaces or data realms they can simple use this table format.

# Schema Format - Tier 1 Compliance (52 Fields Total)

## Core Identity & Audit (7 fields)
- ID (Auto Incrementing)
- UUID
- Rogers-AI-Schema-Version
- InsertDateTime
- UpdateDateTime
- InsertUser
- UpdateUser

## Source Document Metadata (7 fields)
- SourceDocumentName
- SourceDocumentPath
- SourceDocumentHash
- SourceDocumentTitle
- SourceDocumentSummary
- SourceDocumentAuthor
- SourceDocumentOrganization

## Document Content & Chunking (2 fields)
- DocumentChunkNumber
- DocumentChunkText

## Vector Embeddings - 5 Providers (15 fields)
- DocumentEmbeddingModel01, DocumentEmbeddingURL01, DocumentEmbeddingVectors01
- DocumentEmbeddingModel02, DocumentEmbeddingURL02, DocumentEmbeddingVectors02
- DocumentEmbeddingModel03, DocumentEmbeddingURL03, DocumentEmbeddingVectors03
- DocumentEmbeddingModel04, DocumentEmbeddingURL04, DocumentEmbeddingVectors04
- DocumentEmbeddingModel05, DocumentEmbeddingURL05, DocumentEmbeddingVectors05

## Privacy & PII Protection - GDPR Compliant (10 fields)
- ContainsPII (BOOLEAN) - Whether record contains personally identifiable information
- PIITypes (TEXT/JSON) - Types detected: email, phone, SSN, address, etc.
- PIIDetectionMethod (VARCHAR 50) - How detected: automated, manual, both
- PIIDetectionDate (DATETIME) - When PII detection was performed
- SensitiveDataClassification (VARCHAR 20) - None, Low, Medium, High, Critical
- LegalBasisForProcessing (VARCHAR 50) - Consent, Contract, LegalObligation, etc. (GDPR Art 6)
- DataRetentionPeriod (INTEGER) - Days to retain data before deletion
- DeletionScheduledDate (DATETIME) - When data is scheduled for deletion
- DeletionStatus (VARCHAR 20) - Pending, Scheduled, Deleted, Retained
- AnonymizationStatus (VARCHAR 30) - NotAnonymized, Pseudonymized, FullyAnonymized

## Data Governance & Lineage - NIST AI RMF (8 fields)
- DatasetType (VARCHAR 30) - Training, Validation, Testing, Production, KnowledgeBase
- DatasetPurpose (TEXT) - Intended use and business purpose
- DataQualityScore (DECIMAL 5,2) - Overall quality score 0-100
- DataValidationStatus (VARCHAR 20) - Pending, Validated, Failed, NeedsReview
- DataValidationDate (DATETIME) - When validation was performed
- DataValidatedBy (VARCHAR 100) - User who validated the data
- DataLineageChain (TEXT/JSON) - Full provenance trail from original source
- OriginalSourceType (VARCHAR 50) - Web, Database, API, FileSystem, Manual, etc.

## Legal & Licensing Tracking (6 fields)
- CopyrightStatus (VARCHAR 30) - PublicDomain, Copyrighted, CreativeCommons, Unknown
- LicenseType (VARCHAR 100) - MIT, Apache, CC-BY, Proprietary, etc.
- UsageRestrictions (TEXT) - Specific restrictions on data usage
- CommercialUseAllowed (BOOLEAN) - Whether commercial use is permitted
- AttributionRequired (BOOLEAN) - Whether attribution is required
- AttributionText (TEXT) - Required attribution text if applicable

## Risk Management & Content Safety - NIST AI RMF (4 fields)
- RiskLevel (VARCHAR 20) - Low, Medium, High, Critical
- ContentSafetyStatus (VARCHAR 20) - Safe, Flagged, Unsafe, UnderReview
- ContentSafetyScore (DECIMAL 5,2) - Safety score 0-100
- ContentModerationDate (DATETIME) - When content was reviewed for safety

## Access Control & Security (3 fields)
- AccessControlLevel (VARCHAR 20) - Public, Internal, Confidential, Restricted, Classified
- DataClassification (VARCHAR 30) - Per organizational taxonomy
- AllowedRoles (TEXT/JSON) - Roles permitted to access this data

## Enhanced Audit Trail - EU AI Act Article 12 (1 field)
- LastModifiedReason (TEXT) - Reason for last modification

**Note:** Access logging (read operations) should be handled via separate AUDIT_LOG table/process at the database layer, not in this schema.

## Document Lifecycle Management (2 fields)
- DocumentStatus (VARCHAR 20) - Draft, Active, Deprecated, Archived, Deleted
- DocumentVersion (VARCHAR 20) - Version identifier for this document

**Note:** See [COMPLIANCE.md](COMPLIANCE.md) for regulatory mapping to NIST AI-600 and EU AI Act.
**Note:** See [future/TIER2_TIER3_ROADMAP.md](future/TIER2_TIER3_ROADMAP.md) for future enhancement roadmap.
**Note:** See [platforms/POSTGRESQL.md](platforms/POSTGRESQL.md) or [platforms/SQLITE_VECTOR.md](platforms/SQLITE_VECTOR.md) for database-specific SQL implementations.



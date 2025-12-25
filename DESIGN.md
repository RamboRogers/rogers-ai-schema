# Rogers-AI-Schema

## Purpose
Rogers-AI-Schema is a project to create a universal schema for AI workloads.  I wrote this as a standard for storing data for AI workloads to be independent of underlying Database technologies.  Each time I see a new AI App, the DB schema is confusing, missing key fields, missing important meta data and always requires constant rework.  This schema aims to solve this foundational problem, and is intended to be used with SQL databases to service both vector, text, and blob data at scale.

# Tables
A single simple table design with all the right fields to do proper AI data transcations at scale, ensuring all meta data is retained, verisioned and is setup for proper lineage in compliance with NIST best practices and EU AI Act requirements. If separate data stores are required in different namespaces or data realms they can simple use this table format.

# Schema Format
ID (Auto Incrementing), UUID, InsertDateTime, UpdateDateTime, InsertUser, UpdateUser,  SourceDocumentName, SourceDocumentPath, SouthDocumentHash, SourceDocumentTitle, SourceDocumentSummary, SourceDocumentAuthor, SourceDocumentOrganization, 

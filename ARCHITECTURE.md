# DefTech AI Document Assistant - Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                                                                     │
│  ┌──────────────────┐              ┌──────────────────┐           │
│  │   CLI Demo       │              │  Jupyter         │           │
│  │  (demo_queries)  │              │  Notebook        │           │
│  └────────┬─────────┘              └────────┬─────────┘           │
│           │                                  │                     │
└───────────┼──────────────────────────────────┼─────────────────────┘
            │                                  │
            └──────────────┬───────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DEFTECH AGENT (agent.py)                        │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Cohere Command-R+ Multi-Step Agent                          │  │
│  │                                                               │  │
│  │  • System Message: "You are a defense assistant..."          │  │
│  │  • Temperature: 0.1 (accuracy-focused)                       │  │
│  │  • Max Steps: 10                                             │  │
│  │  • Tool-aware reasoning                                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│                           │                                         │
│                           ▼                                         │
│                  ┌─────────────────┐                               │
│                  │  Tool Selection │                               │
│                  │   & Execution   │                               │
│                  └─────────────────┘                               │
│                           │                                         │
└───────────────────────────┼─────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ search_       │   │ search_       │   │ log_access    │
│ manuals       │   │ doctrine      │   │               │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│              DEFTECH TOOLS (tools.py)                    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Tool Implementations                              │ │
│  │                                                    │ │
│  │  • search_manuals(query, manual_type)            │ │
│  │  • search_doctrine(query, doctrine_area)         │ │
│  │  • log_access(doc_id, user_id, classification)   │ │
│  └────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│  Document    │ │   Vector    │ │ Audit Logger │
│  Processor   │ │   Store     │ │              │
└──────┬───────┘ └──────┬──────┘ └──────┬───────┘
       │                │               │
       ▼                ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                 DATA LAYER                               │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Cohere     │  │   Qdrant     │  │  Audit Logs  │  │
│  │   Embed v3   │  │  Vector DB   │  │  (JSON)      │  │
│  │              │  │              │  │              │  │
│  │  1024 dims   │  │  Cosine      │  │  ./audit_    │  │
│  │  Embedding   │  │  Similarity  │  │  logs/       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Document Ingestion Flow

```
PDF/DOCX Files (./sample_docs/)
         │
         ▼
┌─────────────────────┐
│ document_processor  │
│                     │
│ • Load PDF/DOCX     │
│ • Extract pages     │
│ • Chunk text        │
│ • Extract metadata  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Cohere Embed v3     │
│                     │
│ • embed-english-v3  │
│ • input_type:       │
│   "search_document" │
│ • Returns 1024-dim  │
│   vectors           │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Qdrant Vector Store │
│                     │
│ • Store vectors     │
│ • Store metadata:   │
│   - manual_name     │
│   - page            │
│   - section         │
│   - classification  │
│   - document_type   │
└─────────────────────┘
```

### 2. Query Processing Flow

```
User Query: "What is the equipment inspection procedure?"
         │
         ▼
┌──────────────────────────────────────────────┐
│ DefTech Agent (Cohere Command-R+)            │
│                                              │
│ Step 1: Analyze query                       │
│ Step 2: Decide to use search_manuals tool   │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ search_manuals(                              │
│   query="equipment inspection procedure",   │
│   manual_type=None                           │
│ )                                            │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Query Embedding Generation                   │
│                                              │
│ Cohere Embed v3                              │
│ input_type: "search_query"                   │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Vector Similarity Search                     │
│                                              │
│ Qdrant.search(                               │
│   query_vector=embedding,                    │
│   limit=5,                                   │
│   filter={document_type: "manual"}           │
│ )                                            │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Top 5 Results Returned:                      │
│                                              │
│ [                                            │
│   {                                          │
│     "manual_name": "Equipment Maintenance...",│
│     "page": 2,                               │
│     "section": "1.1 Visual Inspection",      │
│     "classification": "unclassified",        │
│     "text": "Begin with comprehensive...",   │
│     "score": 0.89                            │
│   },                                         │
│   ...                                        │
│ ]                                            │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Agent Synthesizes Answer                     │
│                                              │
│ "The equipment inspection procedure          │
│  consists of two main steps:                 │
│  1. Visual Inspection Protocol...            │
│  2. Functional Testing Requirements..."      │
│                                              │
│ With citations to:                           │
│ - Equipment Maintenance Manual v3.2, p.2     │
└──────────────────────────────────────────────┘
```

### 3. Classified Access Flow

```
User Query: "Show me tactical doctrine for urban operations"
         │
         ▼
┌──────────────────────────────────────────────┐
│ Agent calls search_doctrine tool             │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Results include SECRET document              │
│ classification: "secret"                     │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Agent recognizes classified access           │
│ Automatically calls log_access tool          │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ log_access(                                  │
│   document_id="Tactical Doctrine TD-2023-04",│
│   user_id="demo_user_001",                   │
│   classification_level="secret"              │
│ )                                            │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Audit Log Created                            │
│                                              │
│ {                                            │
│   "audit_id": "AUD-000001",                  │
│   "timestamp": "2024-10-20T14:30:00Z",       │
│   "document_id": "Tactical Doctrine...",     │
│   "user_id": "demo_user_001",                │
│   "classification_level": "SECRET",          │
│   "action": "DOCUMENT_ACCESS"                │
│ }                                            │
│                                              │
│ Saved to: ./audit_logs/audit_log_20241020.jsonl │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│ Agent returns answer with audit confirmation │
│                                              │
│ "Access logged with audit ID AUD-000001"     │
└──────────────────────────────────────────────┘
```

## Component Responsibilities

### Agent Layer (`agent.py`)
- **Purpose**: Orchestrate multi-step reasoning
- **Responsibilities**:
  - Parse user queries
  - Decide which tools to use
  - Execute tool calls in sequence
  - Synthesize final answers
  - Extract and format citations
- **Key Method**: `run(query, user_id)`

### Tools Layer (`tools.py`)
- **Purpose**: Provide capabilities to the agent
- **Components**:
  - `DefTechTools` class with 3 tools
  - Tool schema definitions for Cohere
  - Tool execution logic
- **Key Methods**:
  - `search_manuals(query, manual_type)`
  - `search_doctrine(query, doctrine_area)`
  - `log_access(document_id, user_id, classification)`

### Document Processing (`document_processor.py`)
- **Purpose**: Convert documents to searchable vectors
- **Responsibilities**:
  - Load PDF/DOCX files
  - Chunk text intelligently
  - Extract metadata (page, section)
  - Generate embeddings via Cohere
- **Key Methods**:
  - `load_pdf(file_path)`
  - `load_docx(file_path)`
  - `chunk_text(text, page)`
  - `generate_embeddings(texts)`

### Vector Store (`vector_store.py`)
- **Purpose**: Store and retrieve document vectors
- **Responsibilities**:
  - Interface with Qdrant
  - Ingest embeddings with metadata
  - Perform similarity searches
  - Apply filters (manual type, doctrine area)
- **Key Methods**:
  - `ingest_chunks(chunks, embeddings)`
  - `search(query_embedding, limit, filters)`
  - `search_by_manual_type(...)`
  - `search_by_doctrine_area(...)`

### Configuration (`config.py`)
- **Purpose**: Centralize all settings
- **Contains**:
  - API keys and model names
  - System message for agent
  - Chunk sizes and parameters
  - Classification levels
  - File paths

## Security & Compliance

### Classification Handling
```
Document → Extract Classification → Store in Metadata
                                            │
                                            ▼
                                    Agent Checks on Access
                                            │
                                            ▼
                                    If Classified → log_access
                                            │
                                            ▼
                                    Audit Log Created
```

### Audit Trail
- Every classified access generates unique audit ID
- Logs include: timestamp, user, document, classification
- Stored in `./audit_logs/` as JSON Lines format
- Immutable append-only log

## Scalability Considerations

### Current (Demo) Scale
- **Documents**: 4 PDFs (~50 pages)
- **Chunks**: ~200 chunks
- **Vector DB**: Local Qdrant (in-memory)
- **Performance**: Sub-second search

### Production Scale
- **Documents**: 1000s of PDFs
- **Chunks**: Millions of chunks
- **Vector DB**: Qdrant cluster (distributed)
- **Performance**: Still sub-second with proper indexing

### Bottlenecks & Solutions

| Component | Bottleneck | Solution |
|-----------|------------|----------|
| Embedding | API rate limits | Batch processing, parallel requests |
| Search | Vector dimensionality | Qdrant handles this efficiently |
| Agent | LLM latency | Cache common queries, use streaming |
| Storage | Disk space | Compress older embeddings, archive |

## Technology Choices

### Why Cohere?
- ✅ Enterprise-ready with flexible deployment
- ✅ Excellent RAG capabilities
- ✅ Built-in citation support
- ✅ Multi-step tool use (not just function calling)
- ✅ State-of-the-art embeddings

### Why Qdrant?
- ✅ Purpose-built for vector search
- ✅ Excellent performance at scale
- ✅ Rich filtering capabilities
- ✅ Easy local development, production-ready deployment
- ✅ Active development and community

### Why Python?
- ✅ Excellent AI/ML library ecosystem
- ✅ Cohere SDK well-maintained
- ✅ Easy prototyping and demo building
- ✅ Production-ready with proper engineering

## Extension Points

### Easy to Add
1. **New Tools**: Add to `tools.py`, register schema
2. **New Document Types**: Extend `document_processor.py`
3. **New Filters**: Add to vector store search
4. **UI Layer**: Streamlit app (basic structure included)

### More Complex
1. **Conversation Memory**: Track conversation history
2. **Reranking**: Add Cohere rerank step
3. **Multi-modal**: Handle images in documents
4. **Fine-tuning**: Custom embeddings for domain

---

**Architecture Version**: 1.0
**Last Updated**: 2025-10-20

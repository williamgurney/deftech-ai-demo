# DefTech AI Document Assistant - Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- Cohere API key ([get one here](https://dashboard.cohere.com/api-keys))
- 500MB free disk space

## Setup (5 minutes)

### Option 1: Automated Setup (Recommended)

```bash
chmod +x setup_demo.sh
./setup_demo.sh
```

The script will:
1. Install dependencies
2. Create .env file (you'll need to add your API key)
3. Initialize the system
4. Create sample documents
5. Ingest documents into vector database

### Option 2: Manual Setup

**Step 1: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Configure API key**
```bash
cp .env.example .env
# Edit .env and add your COHERE_API_KEY
```

**Step 3: Initialize system**
```bash
python init_demo.py
```

**Step 4: Create sample documents**
```bash
python create_sample_docs.py
```

**Step 5: Ingest documents**
```bash
python ingest_documents.py
```

## Running the Demo

### Interactive Demo (Recommended)

Run the complete demo with 4 sample queries:

```bash
python demo_queries.py
```

This will demonstrate:
1. Simple document retrieval
2. Multi-document synthesis
3. Classified document access with audit logging
4. Comparison queries with multi-step reasoning

### Custom Queries

Use the Python API directly:

```python
from init_demo import init_cohere_client, init_qdrant_client
from document_processor import DocumentProcessor
from vector_store import VectorStore
from tools import DefTechTools
from agent import DefTechAgent

# Initialize
cohere_client = init_cohere_client()
qdrant_client = init_qdrant_client()
processor = DocumentProcessor(cohere_client)
vector_store = VectorStore(qdrant_client)
tools = DefTechTools(processor, vector_store)
agent = DefTechAgent(cohere_client, tools)

# Run query
result = agent.run("Your query here", user_id="user_123")

# Access results
print(result['answer'])
print(result['citations'])
print(result['audit_logs'])
```

## Project Structure

```
def-tech/
├── config.py                    # Configuration settings
├── init_demo.py                 # System initialization
├── document_processor.py        # PDF/DOCX processing & embeddings
├── vector_store.py             # Qdrant vector database operations
├── tools.py                    # Agent tools (search, logging)
├── agent.py                    # Cohere multi-step agent
├── demo_queries.py             # Demo script
├── create_sample_docs.py       # Generate sample documents
├── ingest_documents.py         # Document ingestion pipeline
├── sample_docs/                # Sample defense documents
├── qdrant_data/               # Vector database storage
└── audit_logs/                # Compliance audit logs
```

## Sample Queries to Try

**Equipment Maintenance:**
- "What is the procedure for equipment inspection?"
- "How do I troubleshoot hydraulic system issues?"
- "What are the weekly maintenance tasks?"

**Safety:**
- "What PPE is required for maintenance operations?"
- "How should I handle fuel spills?"
- "What are the lockout/tagout procedures?"

**Winter Operations:**
- "What are the safety protocols for winter maintenance?"
- "How do I winterize equipment?"
- "What are the cold weather starting procedures?"

**Tactical Doctrine (Classified):**
- "Show me urban operations doctrine"
- "What are the building entry procedures?"
- "How should units move in urban terrain?"

**Multi-Document Synthesis:**
- "What are the safety protocols for maintenance during winter?"
- "Compare equipment type A and type B maintenance procedures"

## Understanding the Output

Each query shows:

1. **Answer**: The agent's response with information from documents
2. **Tools Used**: Which tools the agent called (search_manuals, search_doctrine, log_access)
3. **Citations**: Source documents, page numbers, and classification levels
4. **Audit Logs**: Compliance records for classified document access
5. **Metadata**: Steps taken, number of tools called, etc.

## Troubleshooting

**"COHERE_API_KEY not found"**
- Make sure you created `.env` file and added your API key

**"No documents found in vector database"**
- Run `python create_sample_docs.py` then `python ingest_documents.py`

**"Module not found" errors**
- Run `pip install -r requirements.txt`

**Slow first query**
- First query initializes models and caches - subsequent queries are faster

## Next Steps

### For Your Presentation

1. **Run the demo**: `python demo_queries.py` to see all capabilities
2. **Review the code**: Start with `agent.py` to understand the agent loop
3. **Customize queries**: Try queries specific to your use case
4. **Show audit logs**: Demonstrate compliance tracking in `./audit_logs/`

### Customization

1. **Add your own documents**: Place PDFs/DOCX in `./sample_docs/` and run ingestion
2. **Modify system message**: Edit `config.py` SYSTEM_MESSAGE
3. **Adjust search results**: Change TOP_K_RESULTS in `config.py`
4. **Add new tools**: Define in `tools.py` following the existing pattern

### Production Considerations (Not Needed for Demo)

- Replace in-memory audit logs with database
- Add user authentication
- Use production Qdrant instance
- Implement proper document access controls
- Add rate limiting and error handling
- Deploy with proper secrets management

## Support

For issues with:
- **Cohere API**: [Cohere Documentation](https://docs.cohere.com/)
- **This demo**: Check code comments or review implementation files

## License

Demo code for educational and presentation purposes.

# DefTech AI Document Assistant Demo

A complete demonstration application showcasing Cohere's AI capabilities for defense document interrogation, featuring RAG-based search, multi-step agents, and compliance logging.

**Status:** ✅ Ready for Presentation

## Features

- **RAG-based Document Search**: Vector search across defense manuals, procedures, and doctrine documents
- **Multi-step Agent**: Powered by Cohere's Command-R+ with native tool use
- **Citation System**: Exact source document, page number, and classification level tracking
- **Compliance Logging**: Automatic audit trail for classified document access
- **Multi-Document Synthesis**: Combines information from multiple sources intelligently

## Quick Start

### Automated Setup (Recommended)

```bash
./setup_demo.sh
```

The script will install dependencies, create sample documents, and set up the vector database. You'll just need to add your Cohere API key to `.env`.

### Manual Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your Cohere API key:**
```bash
cp .env.example .env
# Edit .env and add your COHERE_API_KEY
```

3. **Create sample documents:**
```bash
python create_sample_docs.py
```

4. **Ingest documents into vector database:**
```bash
python ingest_documents.py
```

5. **Verify setup:**
```bash
python test_setup.py
```

6. **Run the demo:**
```bash
python demo_queries.py
```

## Demo Options

### Option 1: Streamlit Web UI (Recommended for Presentations) 🌟
```bash
streamlit run streamlit_app.py
```
Beautiful web interface with:
- Visual query interface
- Pre-loaded demo queries
- Real-time results display
- Tool call visualization
- Audit log tracking
- Perfect for live demos!

Open http://localhost:8501 in your browser.

### Option 2: Automated CLI Demo
```bash
python demo_auto.py
```
Runs all 4 demo queries automatically (no keyboard input needed).

### Option 3: Interactive CLI Demo
```bash
python demo_queries.py
```
Interactive demo with pauses between queries.

### Option 4: Jupyter Notebook
```bash
jupyter notebook demo_notebook.ipynb
```
Hands-on exploration with code cells you can modify and re-run.

### Option 5: Custom Python Script
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
result = agent.run("What is the equipment inspection procedure?")
print(result['answer'])
```

## Project Structure

```
def-tech/
├── config.py                      # Configuration and system message
├── init_demo.py                   # System initialization
├── document_processor.py          # PDF/DOCX processing & embeddings
├── vector_store.py               # Qdrant vector database operations
├── tools.py                      # Agent tools (search, logging)
├── agent.py                      # Cohere multi-step agent loop
├── demo_queries.py               # CLI demo with 4 sample queries
├── demo_notebook.ipynb           # Jupyter notebook demo
├── create_sample_docs.py         # Generate sample documents
├── ingest_documents.py           # Document ingestion pipeline
├── test_setup.py                 # Verify system setup
├── setup_demo.sh                 # Automated setup script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── QUICKSTART.md                 # Detailed setup guide
├── PRESENTATION_GUIDE.md         # How to present the demo
├── ARCHITECTURE.md               # System architecture diagrams
├── PROJECT_SUMMARY.md            # Complete project overview
├── sample_docs/                  # Generated PDF documents
├── qdrant_data/                  # Vector database storage
└── audit_logs/                   # Compliance logs (JSON)
```

## Sample Documents

The demo includes realistic defense documents (simulated content):

| Document | Classification | Pages | Type |
|----------|---------------|-------|------|
| Equipment Maintenance Manual v3.2 | UNCLASSIFIED | 12 | Manual |
| Safety Guidelines 2024 | UNCLASSIFIED | 10 | Manual |
| Tactical Doctrine TD-2023-04 | SECRET* | 8 | Doctrine |
| Winter Operations Procedures | UNCLASSIFIED | 10 | Manual |

*Simulated for demo purposes only

## Demo Queries

The demo showcases 4 different capabilities:

### 1. Simple Retrieval
**Query:** "What is the procedure for equipment inspection?"

**Demonstrates:**
- Basic RAG search
- Citation with page numbers
- Single document retrieval

### 2. Multi-Document Synthesis
**Query:** "What are the safety protocols for maintenance during winter operations?"

**Demonstrates:**
- Searching multiple documents
- Information synthesis
- Multiple citations

### 3. Classified Document Access
**Query:** "Show me classified tactical doctrine for urban operations"

**Demonstrates:**
- Doctrine search
- Automatic compliance logging
- Audit trail generation

### 4. Comparison Query
**Query:** "Compare inspection procedures for equipment type A versus equipment type B"

**Demonstrates:**
- Multi-step reasoning
- Structured comparison
- Complex query handling

## Technical Stack

- **LLM**: Cohere Command-R+ (command-r-plus-08-2024)
- **Embeddings**: Cohere Embed v3 (embed-english-v3.0, 1024 dimensions)
- **Vector DB**: Qdrant (local mode, production-ready cluster available)
- **Framework**: Python 3.9+
- **Document Formats**: PDF, DOCX

## Key Capabilities

### 1. Multi-Step Agent
The agent can make multiple tool calls and use results to inform subsequent actions:
```
Query → Analyze → Call Tool 1 → Process Results → Call Tool 2 → Synthesize Answer
```

### 2. Three Tools
- **search_manuals**: Search maintenance, safety, operations, training manuals
- **search_doctrine**: Search tactical, strategic, logistics, personnel doctrine
- **log_access**: Create audit logs for classified document access

### 3. Automatic Compliance
When the agent accesses classified documents, it automatically:
- Calls the log_access tool
- Generates unique audit ID
- Records timestamp, user, document, classification
- Saves to persistent log file

## Documentation

### Getting Started
- **QUICKSTART.md**: Step-by-step setup instructions
- **SUCCESS.md**: Quick success guide and verification
- **PRESENTATION_GUIDE.md**: How to present this demo effectively

### Technical Documentation
- **ARCHITECTURE.md**: System architecture with diagrams
- **PROJECT_SUMMARY.md**: Complete project overview
- **FINAL_CHECKLIST.md**: Pre-presentation checklist

### Production Deployment (NEW)
- **SAGEMAKER_DEPLOYMENT.md**: AWS SageMaker production architecture 🌟
- **SECURITY_MODEL.md**: Security & compliance for defense applications 🔒
- **DEPLOYMENT_COMPARISON.md**: Comparison of deployment options 📊

## Troubleshooting

**Problem:** "COHERE_API_KEY not found"
```bash
cp .env.example .env
# Edit .env and add your API key
```

**Problem:** "No documents found in vector database"
```bash
python create_sample_docs.py
python ingest_documents.py
```

**Problem:** "Module not found" errors
```bash
pip install -r requirements.txt
```

**Verify everything works:**
```bash
python test_setup.py
```

## For Presenters

See **PRESENTATION_GUIDE.md** for a complete walkthrough including:
- Pre-presentation checklist
- Live demo flow (30 minutes)
- Code walkthrough talking points
- Q&A preparation
- Backup plans

## Next Steps

### After the Demo

1. **Customize**: Add your own documents to `./sample_docs/`
2. **Extend**: Add new tools in `tools.py`
3. **Deploy**: Move to production Qdrant cluster
4. **Integrate**: Connect with existing systems

### Production Considerations

For production deployment, enhance:
- User authentication and access control
- Database-backed audit logs
- Document security and encryption
- Rate limiting and monitoring
- Scalability testing

See **PROJECT_SUMMARY.md** for detailed production roadmap.

## License

Demo code for educational and presentation purposes.

## Support

- **Cohere Documentation**: https://docs.cohere.com/
- **Issues**: Check code comments or contact your demo creator

# DefTech AI Demo - Presentation Guide

This guide will help you present the Cohere-powered defense document assistant effectively.

## Pre-Presentation Setup (15 minutes before)

### 1. Verify System is Ready

```bash
# Test that everything works
python demo_queries.py
```

Press Ctrl+C after the first query completes if you don't want to run all 4 queries yet.

### 2. Open Files for Code Walkthrough

Have these files ready to show:
- `agent.py` - The multi-step agent (lines 30-120)
- `tools.py` - Tool definitions (lines 150-250 for schemas)
- `config.py` - System message and settings

### 3. Terminal Setup

Open 2 terminals:
- **Terminal 1**: For running the demo
- **Terminal 2**: For showing audit logs (`tail -f ./audit_logs/*.jsonl`)

## Presentation Flow (20-30 minutes)

### Part 1: Introduction (3 minutes)

**Talking Points:**

> "Today I'll demonstrate a RAG-powered AI assistant for defense personnel, built using Cohere's Command-R+ model. This system helps staff quickly find accurate information from complex defense manuals, procedures, and doctrine documents."

**Key Capabilities to Highlight:**
- Multi-step reasoning with tool use
- Source citation with page numbers and classification levels
- Automatic compliance logging for classified access
- Synthesis across multiple documents

### Part 2: Architecture Overview (5 minutes)

**Show the architecture diagram (describe on whiteboard or slide):**

```
User Query
    ↓
Cohere Agent (Command-R+)
    ↓
[Decides which tools to use]
    ↓
┌─────────────┬──────────────┬──────────────┐
│ search_     │ search_      │ log_access   │
│ manuals     │ doctrine     │              │
└─────────────┴──────────────┴──────────────┘
    ↓               ↓               ↓
Vector Search   Vector Search   Audit Log
(Qdrant)        (Qdrant)        (JSON)
    ↓
Cohere Embeddings (v3)
    ↓
Final Answer with Citations
```

**Talking Points:**

> "The system uses Cohere's embed model to create vector representations of documents. When a query comes in, the agent decides which tools to use - it can search manuals, search doctrine documents, or log access to classified materials. The agent can make multiple tool calls and synthesize information before responding."

### Part 3: Code Walkthrough (7 minutes)

#### 3.1 Show Tool Definitions (`tools.py`)

**Navigate to line 150-250** (tool schemas):

```python
{
    "type": "function",
    "function": {
        "name": "search_manuals",
        "description": "Searches operational procedures...",
        ...
    }
}
```

**Talking Point:**

> "Each tool has a schema that tells the Cohere model what it does and what parameters it accepts. The model uses these schemas to decide when and how to call each tool."

#### 3.2 Show Agent Loop (`agent.py`)

**Navigate to lines 35-80** (main agent loop):

```python
for step in range(config.MAX_AGENT_STEPS):
    response = self.client.chat(
        model=config.COHERE_MODEL,
        messages=messages,
        tools=self.tool_schemas,
        ...
    )

    if response.message.tool_calls:
        # Execute tools
        ...
    else:
        # Return final answer
        ...
```

**Talking Point:**

> "This is Cohere's multi-step pattern. The agent can make multiple tool calls in a loop, using the results from each call to inform the next action. It continues until it has enough information to answer the user's question."

#### 3.3 Show System Message (`config.py`)

**Navigate to line 50-65** (SYSTEM_MESSAGE):

**Talking Point:**

> "The system message instructs the agent on how to behave - prioritizing accuracy, citing sources, and ensuring compliance by logging classified access."

### Part 4: Live Demo (10 minutes)

#### Demo Query 1: Simple Retrieval

**Run:**
```bash
python demo_queries.py
```

**Query:** "What is the procedure for equipment inspection?"

**What to Point Out:**
- Agent calls `search_manuals` tool
- Results include: manual name, page number, section
- Answer synthesizes information from search results
- Shows classification level (UNCLASSIFIED)

**Talking Point:**

> "For this straightforward query, the agent searches the maintenance manual and returns a clear answer with exact citations. Notice it shows the source manual, page number, and classification level."

#### Demo Query 2: Multi-Document Synthesis

**Query:** "What are the safety protocols for maintenance during winter operations?"

**What to Point Out:**
- Agent makes TWO tool calls: searches safety AND winter operations
- Synthesizes information from both documents
- Multiple citations from different sources

**Talking Point:**

> "Here the agent recognizes it needs information from multiple sources. It searches both the Safety Guidelines and Winter Operations manual, then synthesizes the information into a cohesive answer."

#### Demo Query 3: Classified Access

**Query:** "Show me classified tactical doctrine for urban operations"

**What to Point Out:**
- Agent calls `search_doctrine`
- **Automatically** calls `log_access` tool
- Audit log created with timestamp and unique ID
- In Terminal 2, show the audit log file updating

**Talking Point:**

> "This is where compliance comes in. The agent recognizes it's accessing classified information and automatically logs the access. Every classified document access is tracked with a unique audit ID and timestamp for regulatory compliance."

**In Terminal 2, show:**
```bash
tail -f ./audit_logs/*.jsonl
```

Point out the JSON audit record.

#### Demo Query 4: Comparison

**Query:** "Compare inspection procedures for equipment type A versus equipment type B"

**What to Point Out:**
- Multiple search queries to gather comprehensive information
- Multi-step reasoning
- Structured comparison in response

**Talking Point:**

> "This demonstrates the agent's multi-step reasoning capability. It searches for information about both equipment types, then compares them systematically."

### Part 5: Key Differentiators (3 minutes)

**Cohere-Specific Advantages:**

1. **Enterprise-Ready**: Cohere is built for enterprise with deployment flexibility
2. **Citation Quality**: Built-in citation support helps with traceability
3. **Tool Use**: Native multi-step reasoning with tools (not just function calling)
4. **Embed v3**: State-of-the-art embeddings with good multilingual support
5. **Retrieval-Augmented Generation**: Cohere pioneered many RAG techniques

**Talking Point:**

> "Why Cohere? Beyond the strong model performance, Cohere offers enterprise-focused features like flexible deployment, excellent citation capabilities, and production-ready RAG infrastructure. Their models are specifically designed for knowledge-intensive tasks like this."

### Part 6: Production Considerations (2 minutes)

**What Would Change for Production:**
- Real user authentication and access control
- Database-backed audit logs (not in-memory)
- Production Qdrant cluster (not local)
- Document access controls based on clearance levels
- Rate limiting and monitoring
- Secure secrets management

**Talking Point:**

> "This is a demo, but moving to production would require proper authentication, persistent database storage, and additional security controls. The core architecture - Cohere's RAG with tool use - would remain the same."

## Q&A Preparation

### Common Questions:

**Q: How accurate are the citations?**
> A: Cohere's Command-R+ has built-in citation support. It links specific parts of the answer to source documents. In our tests, citation accuracy is high, but we'd validate thoroughly before production deployment.

**Q: What about hallucinations?**
> A: By grounding answers in retrieved documents and using low temperature (0.1), we minimize hallucination risk. The citation system also helps verify claims against sources.

**Q: How does this scale?**
> A: Qdrant is a production-grade vector database that scales horizontally. Cohere's API handles scaling automatically. For millions of documents, we'd use a distributed Qdrant cluster.

**Q: Can it handle other document formats?**
> A: Currently PDF and DOCX. We could easily add support for TXT, HTML, Markdown, or other formats by extending the document processor.

**Q: What about document updates?**
> A: When a document is updated, we'd re-process and re-embed it. Qdrant supports upsert operations, so we can replace old versions atomically.

**Q: Cost considerations?**
> A: Main costs are Cohere API calls (embeddings + chat) and Qdrant infrastructure. We could optimize by caching embeddings and batching operations. For this demo scale, costs are minimal.

**Q: How long does ingestion take?**
> A: For the 4 sample docs (~50 pages total), about 30 seconds. Cohere's embed API is fast - we process documents in parallel batches.

**Q: Can it handle more complex queries?**
> A: Yes, the multi-step agent can handle complex multi-part questions, comparisons, and reasoning tasks. We could extend it with additional tools (calculation, external APIs, etc.).

## Technical Deep-Dive (If Requested)

### Embedding Strategy
- Model: `embed-english-v3.0` (1024 dimensions)
- Input type: "search_document" for indexing, "search_query" for queries
- Chunking: ~500 tokens with 50 token overlap
- Distance metric: Cosine similarity

### Agent Parameters
- Temperature: 0.1 (low for factual accuracy)
- Max steps: 10
- Top-K retrieval: 5 documents per search

### Tool Schema Format
- Follows Cohere's function calling specification
- JSON Schema for parameters
- Descriptive prompts help model decision-making

## Post-Demo Resources

**For Attendees:**
- GitHub repo (if you publish it)
- Cohere documentation: https://docs.cohere.com/
- Your contact for questions

**Next Steps:**
- Pilot with real defense documents (subject to security review)
- Integrate with existing systems
- Explore other Cohere features (reranking, etc.)

---

## Backup Demos (If Main Demo Fails)

### Fallback 1: Jupyter Notebook
If the terminal demo has issues, switch to the Jupyter notebook:
```bash
jupyter notebook demo_notebook.ipynb
```

### Fallback 2: Code Walkthrough Only
Walk through the code without running it, using the architecture diagram and explaining the logic.

### Fallback 3: Pre-recorded Output
Have a text file with sample output from a successful run that you can show and discuss.

---

## Final Checklist

Before you present:
- [ ] API key is set in .env
- [ ] Documents are ingested (check with `python init_demo.py`)
- [ ] Demo runs successfully end-to-end
- [ ] Code files are open in editor
- [ ] Two terminals ready
- [ ] Internet connection stable (for Cohere API)
- [ ] Backup plan ready

**Good luck with your presentation!**

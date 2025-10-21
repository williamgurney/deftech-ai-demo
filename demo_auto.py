"""
Automatic demo script - runs all 4 queries without interactive prompts
"""
from init_demo import init_cohere_client, init_qdrant_client
from document_processor import DocumentProcessor
from vector_store import VectorStore
from tools import DefTechTools
from agent import DefTechAgent
import config


def print_separator(char="=", length=80):
    """Print a visual separator"""
    print("\n" + char * length + "\n")


def format_tool_calls_display(result: dict):
    """Format and display tool calls from agent result"""
    if not result.get('tool_calls'):
        return

    print("\n🔧 TOOLS USED:")
    print_separator("-", 80)

    for i, tool_call in enumerate(result['tool_calls'], 1):
        print(f"{i}. {tool_call['tool']}")
        print(f"   Parameters: {tool_call['parameters']}")
        print(f"   Result: {tool_call['result_summary']}")
        print()


def format_audit_display(result: dict):
    """Format and display audit logs from agent result"""
    if not result.get('audit_logs'):
        return

    print("\n🔒 COMPLIANCE AUDIT LOGS:")
    print_separator("-", 80)

    for log in result['audit_logs']:
        print(f"Audit ID: {log['audit_id']}")
        print(f"Timestamp: {log['timestamp']}")
        print(f"Status: {log['message']}")
        print()


def run_demo_query(agent: DefTechAgent, query: str, description: str):
    """Run a single demo query and display formatted results"""
    print_separator("=", 80)
    print(f"DEMO QUERY {description}")
    print_separator("=", 80)
    print(f"\nQuery: \"{query}\"")
    print()

    # Run agent
    result = agent.run(query, user_id="demo_user_001")

    # Display results
    print_separator("=", 80)
    print("RESULTS")
    print_separator("=", 80)

    print("\n💬 ANSWER:")
    print_separator("-", 80)
    print(result['answer'])
    print()

    # Display tool calls
    format_tool_calls_display(result)

    # Display audit logs
    format_audit_display(result)

    # Display metadata
    print(f"\n📊 METADATA:")
    print_separator("-", 80)
    print(f"Agent steps taken: {result['steps_taken']}")
    print(f"Tools called: {len(result['tool_calls'])}")
    print(f"Audit logs generated: {len(result['audit_logs'])}")

    print_separator("=", 80)
    print("\n✓ Query complete\n")


def main():
    """Run the complete demo with multiple queries"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║           DefTech AI Document Assistant - Demo                      ║
    ║                                                                      ║
    ║           Powered by Cohere Command-R+                              ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    print("\n🚀 Initializing system...")

    # Initialize clients
    cohere_client = init_cohere_client()
    qdrant_client = init_qdrant_client()

    # Initialize components
    processor = DocumentProcessor(cohere_client)
    vector_store = VectorStore(qdrant_client)
    tools = DefTechTools(processor, vector_store)

    # Check if documents are ingested
    collection_info = vector_store.get_collection_info()
    if collection_info['points_count'] == 0:
        print("\n⚠️  WARNING: No documents found in vector database!")
        print("Please run 'python ingest_documents.py' first to index documents.")
        return

    # Initialize agent
    agent = DefTechAgent(cohere_client, tools)

    print("\n✓ System ready!")
    print(f"✓ Vector database: {collection_info['points_count']} document chunks indexed")
    print(f"✓ Agent model: {config.COHERE_MODEL}")
    print(f"✓ Tools available: search_manuals, search_doctrine, log_access")

    print("\n" + "=" * 80)
    print("Running 4 demo queries...")
    print("=" * 80)

    # Demo Query 1: Simple equipment procedure
    run_demo_query(
        agent=agent,
        query="What is the procedure for equipment inspection?",
        description="#1 - Simple Retrieval"
    )

    # Demo Query 2: Multi-document synthesis
    run_demo_query(
        agent=agent,
        query="What are the safety protocols for maintenance during winter operations?",
        description="#2 - Multi-Document Synthesis"
    )

    # Demo Query 3: Classified access (triggers audit logging)
    run_demo_query(
        agent=agent,
        query="Show me classified tactical doctrine for urban operations",
        description="#3 - Classified Document Access"
    )

    # Demo Query 4: Comparison requiring multi-step reasoning
    run_demo_query(
        agent=agent,
        query="Compare inspection procedures for equipment type A versus equipment type B",
        description="#4 - Comparison Query"
    )

    # Final summary
    print_separator("=", 80)
    print("DEMO COMPLETE")
    print_separator("=", 80)

    print("""
    ✓ Demonstrated capabilities:
      • RAG-based document search across multiple manuals
      • Multi-step agent reasoning with tool use
      • Citation system linking answers to source documents
      • Compliance logging for classified document access
      • Multi-document synthesis and comparison

    📁 Audit logs saved to: ./audit_logs/

    🔍 For more details, examine the code in:
      • agent.py - Multi-step agent implementation
      • tools.py - Tool definitions and execution
      • document_processor.py - Document ingestion pipeline
      • vector_store.py - Vector database operations

    Thank you for trying the DefTech AI Document Assistant demo!
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        print("\nPlease ensure:")
        print("1. COHERE_API_KEY is set in .env file")
        print("2. All dependencies are installed: pip install -r requirements.txt")
        print("3. Documents are ingested: python ingest_documents.py")
        raise

"""
Quick demo - runs one query to verify system is working
"""
from init_demo import init_cohere_client, init_qdrant_client
from document_processor import DocumentProcessor
from vector_store import VectorStore
from tools import DefTechTools
from agent import DefTechAgent

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           DefTech AI Document Assistant - Quick Demo                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

print("Initializing system...")
cohere_client = init_cohere_client()
qdrant_client = init_qdrant_client()
processor = DocumentProcessor(cohere_client)
vector_store = VectorStore(qdrant_client)
tools = DefTechTools(processor, vector_store)
agent = DefTechAgent(cohere_client, tools)

print("✓ System ready!\n")
print("=" * 70)
print("DEMO QUERY: What are the safety protocols for cold weather maintenance?")
print("=" * 70)

result = agent.run(
    "What are the safety protocols for cold weather maintenance?",
    user_id="demo_user"
)

print("\n" + "=" * 70)
print("RESULT")
print("=" * 70)
print(f"\nAnswer:\n{result['answer']}\n")
print(f"Tools used: {len(result['tool_calls'])}")
print(f"Agent steps: {result['steps_taken']}")
print(f"Audit logs: {len(result['audit_logs'])}")

print("\n" + "=" * 70)
print("✓ Demo Complete!")
print("=" * 70)
print("\nTo run the full demo with 4 queries:")
print("  python demo_queries.py")
print("\nOr use the Jupyter notebook:")
print("  jupyter notebook demo_notebook.ipynb")

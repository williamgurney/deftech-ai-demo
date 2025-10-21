"""
Quick test script to verify the DefTech system is properly set up
Run this after setup to ensure everything works before the demo
"""
import sys
import os


def test_imports():
    """Test that all required modules can be imported"""
    print("\n[1/6] Testing imports...")

    try:
        import cohere
        print("  ✓ cohere")
    except ImportError as e:
        print(f"  ✗ cohere: {e}")
        return False

    try:
        from qdrant_client import QdrantClient
        print("  ✓ qdrant_client")
    except ImportError as e:
        print(f"  ✗ qdrant_client: {e}")
        return False

    try:
        import PyPDF2
        print("  ✓ PyPDF2")
    except ImportError as e:
        print(f"  ✗ PyPDF2: {e}")
        return False

    try:
        from docx import Document
        print("  ✓ python-docx")
    except ImportError as e:
        print(f"  ✗ python-docx: {e}")
        return False

    try:
        from reportlab.lib.pagesizes import letter
        print("  ✓ reportlab")
    except ImportError as e:
        print(f"  ✗ reportlab: {e}")
        return False

    return True


def test_env_file():
    """Test that .env file exists and has API key"""
    print("\n[2/6] Testing .env configuration...")

    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        print("    Create it with: cp .env.example .env")
        return False

    print("  ✓ .env file exists")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        print("  ✗ COHERE_API_KEY not set in .env")
        return False

    if api_key == "your_cohere_api_key_here":
        print("  ✗ COHERE_API_KEY still has placeholder value")
        return False

    print("  ✓ COHERE_API_KEY is set")
    return True


def test_cohere_connection():
    """Test Cohere API connection"""
    print("\n[3/6] Testing Cohere API connection...")

    try:
        from init_demo import init_cohere_client
        client = init_cohere_client()
        print("  ✓ Cohere client initialized")
        return True
    except Exception as e:
        print(f"  ✗ Cohere connection failed: {e}")
        return False


def test_qdrant():
    """Test Qdrant setup"""
    print("\n[4/6] Testing Qdrant vector database...")

    try:
        from init_demo import init_qdrant_client
        client = init_qdrant_client()
        print("  ✓ Qdrant client initialized")
        return True
    except Exception as e:
        print(f"  ✗ Qdrant setup failed: {e}")
        return False


def test_sample_docs():
    """Test that sample documents exist"""
    print("\n[5/6] Testing sample documents...")

    docs = [
        './sample_docs/equipment_maintenance_manual.pdf',
        './sample_docs/safety_guidelines.pdf',
        './sample_docs/tactical_doctrine.pdf',
        './sample_docs/winter_operations.pdf'
    ]

    all_exist = True
    for doc in docs:
        if os.path.exists(doc):
            print(f"  ✓ {os.path.basename(doc)}")
        else:
            print(f"  ✗ {os.path.basename(doc)} not found")
            all_exist = False

    if not all_exist:
        print("\n  Run: python create_sample_docs.py")
        return False

    return True


def test_vector_db_populated():
    """Test that documents are ingested"""
    print("\n[6/6] Testing vector database population...")

    try:
        from init_demo import init_qdrant_client
        from vector_store import VectorStore

        client = init_qdrant_client()
        vector_store = VectorStore(client)

        info = vector_store.get_collection_info()

        if info['points_count'] == 0:
            print(f"  ⚠ Vector database is empty (0 chunks)")
            print("    Run: python ingest_documents.py")
            return False
        else:
            print(f"  ✓ Vector database populated ({info['points_count']} chunks)")
            return True

    except Exception as e:
        print(f"  ✗ Vector database check failed: {e}")
        return False


def main():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║           DefTech AI Document Assistant - Setup Test                ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    tests = [
        ("Imports", test_imports),
        ("Environment", test_env_file),
        ("Cohere API", test_cohere_connection),
        ("Qdrant", test_qdrant),
        ("Sample Documents", test_sample_docs),
        ("Vector Database", test_vector_db_populated)
    ]

    results = []
    for name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"\n  ✗ Unexpected error in {name}: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(results)
    total = len(results)

    for i, (name, _) in enumerate(tests):
        status = "✓ PASS" if results[i] else "✗ FAIL"
        print(f"  [{status}] {name}")

    print("\n" + "=" * 70)

    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("\nSystem is ready! Run the demo with:")
        print("  python demo_queries.py")
        print("\nOr open the Jupyter notebook:")
        print("  jupyter notebook demo_notebook.ipynb")
        return 0
    else:
        print(f"❌ Some tests failed ({passed}/{total} passed)")
        print("\nPlease fix the issues above before running the demo.")

        if not results[0]:  # Imports failed
            print("\nInstall dependencies with:")
            print("  pip install -r requirements.txt")

        if not results[1]:  # Env file failed
            print("\nSet up your API key:")
            print("  cp .env.example .env")
            print("  # Edit .env and add your COHERE_API_KEY")

        if not results[4]:  # Sample docs missing
            print("\nCreate sample documents:")
            print("  python create_sample_docs.py")

        if not results[5]:  # Vector DB empty
            print("\nIngest documents:")
            print("  python ingest_documents.py")

        return 1


if __name__ == "__main__":
    sys.exit(main())

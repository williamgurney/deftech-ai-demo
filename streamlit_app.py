"""
Streamlit web interface for DefTech AI Document Assistant
Provides an interactive UI for querying defense documents
"""
import streamlit as st
import sys
from init_demo import init_cohere_client, init_qdrant_client
from document_processor import DocumentProcessor
from vector_store import VectorStore
from tools import DefTechTools
from agent import DefTechAgent
import config

# Page configuration
st.set_page_config(
    page_title="DefTech AI Document Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .tool-call {
        background-color: #e3f2fd;
        padding: 1rem;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
    .answer-box {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .audit-log {
        background-color: #fff3e0;
        padding: 1rem;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.cohere_client = None
    st.session_state.agent = None
    st.session_state.query_history = []

@st.cache_resource
def initialize_system():
    """Initialize the DefTech system (cached) - auto-runs on startup"""
    try:
        cohere_client = init_cohere_client()
        qdrant_client = init_qdrant_client()
        processor = DocumentProcessor(cohere_client)
        vector_store = VectorStore(qdrant_client)
        tools = DefTechTools(processor, vector_store)
        agent = DefTechAgent(cohere_client, tools)

        # Get collection info
        collection_info = vector_store.get_collection_info()

        return {
            'agent': agent,
            'cohere_client': cohere_client,
            'vector_store': vector_store,
            'collection_info': collection_info,
            'status': 'success'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

# Auto-initialize on first load
if not st.session_state.initialized:
    with st.spinner("🚀 Initializing DefTech AI system..."):
        result = initialize_system()
        if result['status'] == 'success':
            st.session_state.initialized = True
            st.session_state.agent = result['agent']
            st.session_state.collection_info = result['collection_info']
        else:
            st.error(f"❌ Initialization failed: {result['error']}")

# Header
st.markdown('<div class="main-header">🛡️ DefTech AI Document Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Cohere Command-R+ | RAG-based Defense Document Search</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 System Status")

    if st.session_state.initialized:
        st.success("✓ System Ready")

        # System metrics
        st.markdown("### 📈 Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", st.session_state.collection_info['points_count'])
        with col2:
            st.metric("Status", "Online", delta="✓")

        st.markdown("### 🔧 Tools Available")
        st.markdown("""
        - `search_manuals` - Search manuals
        - `search_doctrine` - Search doctrine
        - `log_access` - Audit logging
        """)

        st.markdown("### 📚 Document Types")
        st.markdown("""
        - Equipment Maintenance (UNCLASS)
        - Safety Guidelines (UNCLASS)
        - Tactical Doctrine (SECRET*)
        - Winter Operations (UNCLASS)

        *Simulated for demo
        """)

        # Query history
        if st.session_state.query_history:
            st.markdown("### 📜 Query History")
            for i, query in enumerate(reversed(st.session_state.query_history[-5:]), 1):
                st.caption(f"{i}. {query[:50]}...")
    else:
        st.error("❌ System initialization failed - check logs above")

    st.markdown("---")
    st.markdown("### 🎯 Demo Queries")
    demo_queries = {
        "Equipment Inspection": "What is the procedure for equipment inspection?",
        "Winter Safety": "What are the safety protocols for maintenance during winter operations?",
        "Urban Doctrine": "Show me classified tactical doctrine for urban operations",
        "Equipment Comparison": "Compare inspection procedures for equipment type A versus equipment type B"
    }

    selected_demo = st.selectbox("Select a demo query:", list(demo_queries.keys()))
    if st.button("▶️ Run Demo Query", use_container_width=True):
        st.session_state.demo_query = demo_queries[selected_demo]

# Main content area
if not st.session_state.initialized:
    st.error("❌ System failed to initialize. Please check the error message in the sidebar and refresh the page.")

    # Show system overview
    st.markdown("## 🎯 System Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🤖 AI Agent")
        st.markdown("""
        - **Model**: Command-R+
        - **Embeddings**: Cohere v3
        - **Multi-step**: Up to 10 steps
        - **Tools**: 3 specialized tools
        """)

    with col2:
        st.markdown("### 📊 Vector Database")
        st.markdown("""
        - **Engine**: Qdrant
        - **Dimensions**: 1024
        - **Distance**: Cosine
        - **Chunks**: ~16 indexed
        """)

    with col3:
        st.markdown("### 🔒 Compliance")
        st.markdown("""
        - **Audit Logs**: Automatic
        - **Classifications**: 4 levels
        - **Citations**: Page-level
        - **Tracking**: Unique IDs
        """)

else:
    # Query input
    st.markdown("## 💬 Ask a Question")

    # Use demo query if set
    default_query = ""
    if hasattr(st.session_state, 'demo_query'):
        default_query = st.session_state.demo_query
        delattr(st.session_state, 'demo_query')

    query = st.text_area(
        "Enter your question about defense procedures, manuals, or doctrine:",
        value=default_query,
        height=100,
        placeholder="Example: What are the safety protocols for fuel handling?"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("🔍 Search", type="primary", use_container_width=True)
    with col2:
        user_id = st.text_input("User ID (for audit logs):", value="demo_user", label_visibility="collapsed")

    if submit and query:
        st.session_state.query_history.append(query)

        with st.spinner("🤔 Agent is thinking..."):
            # Capture output
            result = st.session_state.agent.run(query, user_id=user_id)

        # Display results
        st.markdown("## 📋 Results")

        # Answer
        st.markdown("### 💡 Answer")
        st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)

        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["🔧 Tools Used", "🔒 Audit Logs", "📊 Metadata", "🔍 Debug Info"])

        with tab1:
            if result['tool_calls']:
                st.markdown(f"**{len(result['tool_calls'])} tool(s) called:**")
                for i, tool_call in enumerate(result['tool_calls'], 1):
                    with st.expander(f"Tool {i}: {tool_call['tool']}", expanded=True):
                        st.json(tool_call['parameters'])
                        st.caption(f"Result: {tool_call['result_summary']}")
            else:
                st.info("No tools were used for this query")

        with tab2:
            if result['audit_logs']:
                st.warning(f"⚠️ {len(result['audit_logs'])} classified document(s) accessed")
                for log in result['audit_logs']:
                    st.markdown(f"""
                    <div class="audit-log">
                    <strong>Audit ID:</strong> {log['audit_id']}<br>
                    <strong>Timestamp:</strong> {log['timestamp']}<br>
                    <strong>Message:</strong> {log['message']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✓ No classified documents accessed")

        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agent Steps", result['steps_taken'])
            with col2:
                st.metric("Tools Called", len(result['tool_calls']))
            with col3:
                st.metric("Audit Logs", len(result['audit_logs']))

        with tab4:
            st.json(result)

    elif submit:
        st.warning("⚠️ Please enter a question")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 Powered by Cohere")
with col2:
    st.caption("🔍 Vector DB: Qdrant")
with col3:
    st.caption("🛡️ DefTech Demo v1.0")

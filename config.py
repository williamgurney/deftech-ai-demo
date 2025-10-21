"""
Configuration settings for DefTech AI Document Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cohere API Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_MODEL = "command-r-plus-08-2024"  # Latest Command-R+ model
COHERE_EMBED_MODEL = "embed-english-v3.0"
TEMPERATURE = 0.1  # Low temperature for accuracy

# Qdrant Configuration
QDRANT_COLLECTION = "defense_docs"
QDRANT_PATH = "./qdrant_data"  # Local storage path
EMBEDDING_DIM = 1024  # Cohere Embed v3 dimension

# Document Processing Configuration
CHUNK_SIZE = 500  # Tokens per chunk
CHUNK_OVERLAP = 50  # Token overlap between chunks
SUPPORTED_FORMATS = [".pdf", ".docx"]

# Search Configuration
TOP_K_RESULTS = 5  # Number of results to return per search

# Classification Levels
CLASSIFICATION_LEVELS = [
    "unclassified",
    "confidential",
    "secret",
    "top_secret"
]

# Manual Types
MANUAL_TYPES = [
    "maintenance",
    "safety",
    "operations",
    "training"
]

# Doctrine Areas
DOCTRINE_AREAS = [
    "tactics",
    "strategy",
    "logistics",
    "personnel"
]

# Agent Configuration
MAX_AGENT_STEPS = 10
SYSTEM_MESSAGE = """You are a defense assistant for DefTech staff. Your role is to help personnel find accurate information from defense manuals, procedures, and doctrine documents.

Guidelines:
1. Prioritize accuracy over speed - if you're not certain, search for more information
2. Always cite sources with manual name, page number, and classification level
3. When accessing classified documents, you MUST use the log_access tool to maintain audit compliance
4. Synthesize information from multiple sources when needed
5. If a query requires classified information, acknowledge the classification level in your response
6. Be concise but comprehensive in your answers

Available Tools:
- search_manuals: Search operational procedures, maintenance manuals, and technical documents
- search_doctrine: Search military doctrine and strategic documents
- log_access: Log access to classified documents for audit trail
"""

# Audit Log Configuration
AUDIT_LOG_DIR = "./audit_logs"
os.makedirs(AUDIT_LOG_DIR, exist_ok=True)

"""
Tool implementations for DefTech AI Document Assistant
Provides search_manuals, search_doctrine, and log_access tools for the Cohere agent
"""
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import os
import config
from document_processor import DocumentProcessor
from vector_store import VectorStore


# In-memory audit log for demo purposes
audit_log_store = []


class DefTechTools:
    """Container for all DefTech agent tools"""

    def __init__(self, processor: DocumentProcessor, vector_store: VectorStore):
        self.processor = processor
        self.vector_store = vector_store

    def search_manuals(
        self,
        query: str,
        manual_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search operational procedures, maintenance manuals, and technical documents

        Args:
            query: Search query string
            manual_type: Optional filter (maintenance, safety, operations, training)

        Returns:
            List of relevant document chunks with metadata
        """
        print(f"\n[TOOL] search_manuals(query='{query}', manual_type={manual_type})")

        # Generate query embedding
        query_embedding = self.processor.embed_query(query)

        if not query_embedding:
            return []

        # Search with manual type filter if provided
        results = self.vector_store.search_by_manual_type(
            query_embedding=query_embedding,
            manual_type=manual_type,
            limit=config.TOP_K_RESULTS
        )

        # Format results for agent
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append({
                'rank': i,
                'manual_name': result['manual_name'],
                'page': result['page'],
                'section': result['section'],
                'classification': result['classification'],
                'text': result['text'][:500] + ('...' if len(result['text']) > 500 else ''),  # Truncate for context
                'relevance_score': round(result['score'], 3)
            })

        print(f"[TOOL] Found {len(formatted_results)} results")
        return formatted_results

    def search_doctrine(
        self,
        query: str,
        doctrine_area: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search military doctrine and strategic documents

        Args:
            query: Search query string
            doctrine_area: Optional filter (tactics, strategy, logistics, personnel)

        Returns:
            List of relevant doctrine chunks with metadata
        """
        print(f"\n[TOOL] search_doctrine(query='{query}', doctrine_area={doctrine_area})")

        # Generate query embedding
        query_embedding = self.processor.embed_query(query)

        if not query_embedding:
            return []

        # Search with doctrine area filter if provided
        results = self.vector_store.search_by_doctrine_area(
            query_embedding=query_embedding,
            doctrine_area=doctrine_area,
            limit=config.TOP_K_RESULTS
        )

        # Format results for agent
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append({
                'rank': i,
                'manual_name': result['manual_name'],
                'page': result['page'],
                'section': result['section'],
                'classification': result['classification'],
                'text': result['text'][:500] + ('...' if len(result['text']) > 500 else ''),
                'relevance_score': round(result['score'], 3)
            })

        print(f"[TOOL] Found {len(formatted_results)} results")
        return formatted_results

    def log_access(
        self,
        document_id: str,
        user_id: str,
        classification_level: str
    ) -> Dict[str, Any]:
        """
        Log access to classified documents for audit trail

        Args:
            document_id: Identifier for the accessed document
            user_id: User identifier
            classification_level: Classification level (unclassified, confidential, secret, top_secret)

        Returns:
            Confirmation with timestamp and audit_id
        """
        print(f"\n[TOOL] log_access(document='{document_id}', user='{user_id}', classification='{classification_level}')")

        # Validate classification level
        if classification_level.lower() not in config.CLASSIFICATION_LEVELS:
            return {
                'success': False,
                'error': f'Invalid classification level. Must be one of: {", ".join(config.CLASSIFICATION_LEVELS)}'
            }

        # Generate audit entry
        timestamp = datetime.now().isoformat()
        audit_id = f"AUD-{len(audit_log_store) + 1:06d}"

        audit_entry = {
            'audit_id': audit_id,
            'timestamp': timestamp,
            'document_id': document_id,
            'user_id': user_id,
            'classification_level': classification_level.upper(),
            'action': 'DOCUMENT_ACCESS'
        }

        # Store in memory
        audit_log_store.append(audit_entry)

        # Also write to file for persistence
        log_file = os.path.join(config.AUDIT_LOG_DIR, f"audit_log_{datetime.now().strftime('%Y%m%d')}.jsonl")
        with open(log_file, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')

        print(f"[TOOL] Logged access with audit_id: {audit_id}")

        return {
            'success': True,
            'audit_id': audit_id,
            'timestamp': timestamp,
            'message': f'Access to {classification_level.upper()} document logged successfully'
        }


# Cohere tool schemas (for agent registration)
def get_tool_schemas():
    """
    Get Cohere-compatible tool schemas for all DefTech tools

    Returns:
        List of tool schema dictionaries
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "search_manuals",
                "description": (
                    "Searches operational procedures, maintenance manuals, and technical documents. "
                    "Use this tool to find information about equipment maintenance, safety procedures, "
                    "operational guidelines, and training materials. Returns relevant document chunks "
                    "with source manual name, page number, section, and classification level."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query describing what information to find"
                        },
                        "manual_type": {
                            "type": "string",
                            "description": "Optional filter for manual type",
                            "enum": ["maintenance", "safety", "operations", "training"]
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_doctrine",
                "description": (
                    "Searches military doctrine and strategic documents. "
                    "Use this tool to find tactical guidance, strategic principles, logistics doctrine, "
                    "and personnel policies. Returns relevant doctrine chunks with source document, "
                    "page number, section, and classification level."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query describing what doctrine information to find"
                        },
                        "doctrine_area": {
                            "type": "string",
                            "description": "Optional filter for doctrine area",
                            "enum": ["tactics", "strategy", "logistics", "personnel"]
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "log_access",
                "description": (
                    "Logs access to classified documents for audit trail and compliance. "
                    "MUST be called when accessing any classified document (CONFIDENTIAL, SECRET, or TOP_SECRET). "
                    "Creates a permanent audit record with timestamp and unique audit ID. "
                    "This is required for regulatory compliance and security monitoring."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "Identifier for the accessed document (typically the manual name)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User identifier of the person accessing the document"
                        },
                        "classification_level": {
                            "type": "string",
                            "description": "Classification level of the accessed document",
                            "enum": ["unclassified", "confidential", "secret", "top_secret"]
                        }
                    },
                    "required": ["document_id", "user_id", "classification_level"]
                }
            }
        }
    ]


def execute_tool(
    tools_instance: DefTechTools,
    tool_name: str,
    parameters: Dict[str, Any]
) -> Any:
    """
    Execute a tool by name with given parameters

    Args:
        tools_instance: Instance of DefTechTools
        tool_name: Name of the tool to execute
        parameters: Tool parameters

    Returns:
        Tool execution result
    """
    if tool_name == "search_manuals":
        return tools_instance.search_manuals(**parameters)
    elif tool_name == "search_doctrine":
        return tools_instance.search_doctrine(**parameters)
    elif tool_name == "log_access":
        return tools_instance.log_access(**parameters)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")


if __name__ == "__main__":
    # Test tool schemas
    schemas = get_tool_schemas()
    print("\n=== DefTech Tool Schemas ===\n")
    for schema in schemas:
        print(f"Tool: {schema['function']['name']}")
        print(f"Description: {schema['function']['description'][:100]}...")
        print(f"Parameters: {list(schema['function']['parameters']['properties'].keys())}")
        print()

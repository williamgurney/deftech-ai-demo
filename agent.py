"""
Cohere multi-step agent implementation for DefTech AI Document Assistant
Implements tool use pattern with search and compliance logging capabilities
"""
import json
from typing import List, Dict, Any
import cohere
from cohere.types import ToolCall
import config
from tools import DefTechTools, get_tool_schemas, execute_tool


class DefTechAgent:
    """Multi-step agent using Cohere's Command-R+ with tool use"""

    def __init__(self, cohere_client: cohere.ClientV2, tools: DefTechTools):
        self.client = cohere_client
        self.tools = tools
        self.tool_schemas = get_tool_schemas()

    def run(self, query: str, user_id: str = "demo_user") -> Dict[str, Any]:
        """
        Run the agent with a user query

        Args:
            query: User's question or request
            user_id: User identifier for audit logging

        Returns:
            Dictionary with answer, citations, tool_calls, and audit_logs
        """
        print("\n" + "=" * 70)
        print(f"USER QUERY: {query}")
        print("=" * 70)

        # Initialize conversation history
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # Track all tool calls and audit logs for summary
        all_tool_calls = []
        all_audit_logs = []

        # Agent loop
        for step in range(config.MAX_AGENT_STEPS):
            print(f"\n--- Agent Step {step + 1} ---")

            # Call Cohere API with tools
            response = self.client.chat(
                model=config.COHERE_MODEL,
                messages=messages,
                tools=self.tool_schemas,
                temperature=config.TEMPERATURE
            )

            # Check if agent wants to use tools
            if response.message.tool_calls:
                print(f"\nAgent plans to use {len(response.message.tool_calls)} tool(s):")

                # Add assistant's message to history
                messages.append({
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in response.message.tool_calls
                    ]
                })

                # Execute each tool call
                tool_results = []

                for tool_call in response.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    print(f"\n  → {tool_name}({json.dumps(tool_args, indent=4)})")

                    # Execute tool
                    try:
                        # Add user_id if this is log_access
                        if tool_name == "log_access" and "user_id" not in tool_args:
                            tool_args["user_id"] = user_id

                        result = execute_tool(self.tools, tool_name, tool_args)

                        # Track audit logs
                        if tool_name == "log_access" and result.get('success'):
                            all_audit_logs.append(result)

                        # Track tool call
                        all_tool_calls.append({
                            'tool': tool_name,
                            'parameters': tool_args,
                            'result_summary': f"{len(result)} results" if isinstance(result, list) else str(result.get('success', 'completed'))
                        })

                        # Format result for agent
                        result_str = json.dumps(result, indent=2)
                        print(f"    Result: {result_str[:200]}..." if len(result_str) > 200 else f"    Result: {result_str}")

                        tool_results.append({
                            "call": {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": json.dumps(tool_args)
                                }
                            },
                            "outputs": [{"result": result_str}]
                        })

                    except Exception as e:
                        error_msg = f"Error executing {tool_name}: {str(e)}"
                        print(f"    ✗ {error_msg}")

                        tool_results.append({
                            "call": {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": json.dumps(tool_args)
                                }
                            },
                            "outputs": [{"error": error_msg}]
                        })

                # Add tool results to conversation - one message per tool call
                for tool_result in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_result["call"]["id"],
                        "content": tool_result["outputs"][0].get("result", tool_result["outputs"][0].get("error", ""))
                    })

                # Continue loop - agent will process tool results

            else:
                # Agent has final answer
                print("\n--- Agent Response ---")
                final_text = response.message.content[0].text if response.message.content else "No response generated"
                print(f"\n{final_text}\n")

                # Extract citations if present
                citations = []
                if hasattr(response, 'citations') and response.citations:
                    citations = self._format_citations(response.citations)

                return {
                    'answer': final_text,
                    'citations': citations,
                    'tool_calls': all_tool_calls,
                    'audit_logs': all_audit_logs,
                    'steps_taken': step + 1
                }

        # Max steps reached
        print("\n⚠ Maximum agent steps reached")
        return {
            'answer': "Unable to complete request within step limit.",
            'citations': [],
            'tool_calls': all_tool_calls,
            'audit_logs': all_audit_logs,
            'steps_taken': config.MAX_AGENT_STEPS
        }

    def _format_citations(self, citations) -> List[Dict[str, Any]]:
        """
        Format Cohere citations for display

        Args:
            citations: Raw Cohere citations

        Returns:
            List of formatted citation dictionaries
        """
        formatted = []

        for citation in citations:
            formatted.append({
                'text': citation.text,
                'sources': citation.sources,
                'start': citation.start,
                'end': citation.end
            })

        return formatted


def create_system_message() -> str:
    """Create the system message for the agent"""
    return config.SYSTEM_MESSAGE


if __name__ == "__main__":
    print("\n=== DefTech Agent Test ===\n")
    print("This module provides the agent implementation.")
    print("Run demo_queries.py for interactive demo.\n")

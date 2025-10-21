"""
Test Cohere API connectivity and basic functionality
"""
import os
from dotenv import load_dotenv
import cohere

load_dotenv()

print("="*60)
print("Testing Cohere API Connection")
print("="*60)
print()

# Check API key
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    print("❌ COHERE_API_KEY not found in .env file")
    exit(1)

print(f"✓ API key found: {api_key[:8]}...{api_key[-4:]}")
print()

# Test 1: Initialize client
print("Test 1: Initialize Cohere client")
try:
    client = cohere.ClientV2(api_key=api_key)
    print("✓ Client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    exit(1)

print()

# Test 2: Simple chat completion
print("Test 2: Simple chat completion")
try:
    response = client.chat(
        model="command-r-plus-08-2024",
        messages=[
            {
                "role": "user",
                "content": "Say 'Hello, DefTech!' and nothing else."
            }
        ]
    )

    answer = response.message.content[0].text
    print(f"✓ Chat API works")
    print(f"  Response: {answer}")
except Exception as e:
    print(f"❌ Chat API failed: {e}")
    exit(1)

print()

# Test 3: Embedding generation
print("Test 3: Embedding generation")
try:
    response = client.embed(
        model="embed-english-v3.0",
        texts=["equipment inspection procedure"],
        input_type="search_query",
        embedding_types=["float"]
    )

    embedding = response.embeddings.float_[0]
    print(f"✓ Embed API works")
    print(f"  Embedding dimensions: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
except Exception as e:
    print(f"❌ Embed API failed: {e}")
    exit(1)

print()

# Test 4: Chat with tools (agent mode)
print("Test 4: Chat with tool definitions")
try:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "test_tool",
                "description": "A test tool",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Test query"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]

    response = client.chat(
        model="command-r-plus-08-2024",
        messages=[
            {
                "role": "user",
                "content": "Just say hello, don't use any tools."
            }
        ],
        tools=tools
    )

    answer = response.message.content[0].text if response.message.content else "No content"
    print(f"✓ Chat with tools works")
    print(f"  Response: {answer}")
except Exception as e:
    print(f"❌ Chat with tools failed: {e}")
    exit(1)

print()
print("="*60)
print("✅ ALL COHERE API TESTS PASSED")
print("="*60)
print()
print("Summary:")
print("  ✓ API key is valid")
print("  ✓ Chat API (Command-R+) is working")
print("  ✓ Embed API (Embed v3) is working")
print("  ✓ Tool use capability is working")
print()
print("The Cohere API is fully functional!")

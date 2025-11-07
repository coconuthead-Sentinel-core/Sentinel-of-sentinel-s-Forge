"""
Response collector for Sentinel Forge AI evaluation.
Calls the /api/v1/ai/chat endpoint with test queries and saves responses.
"""
import json
import requests
import time
from pathlib import Path


def load_queries(queries_path: str) -> list[dict]:
    """Load test queries from JSON file."""
    with open(queries_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_response(base_url: str, query: str, context: str) -> dict:
    """
    Call the AI chat endpoint and collect response.
    
    Args:
        base_url: Base URL of the API (e.g., "http://localhost:8000")
        query: The user query text
        context: Additional context for the query
    
    Returns:
        Response data including the AI's answer
    """
    endpoint = f"{base_url}/api/v1/ai/chat"
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": f"You are the Sentinel Forge AI assistant. Context: {context}"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "model": None,  # Uses default model
        "temperature": 0.7
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        response.raise_for_status()
        return {
            "success": True,
            "response": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "response": None
        }


def main():
    """Main execution: load queries, collect responses, save results."""
    
    # Configuration
    base_url = "http://localhost:8000"
    eval_dir = Path(__file__).parent
    queries_file = eval_dir / "test_queries.json"
    responses_file = eval_dir / "test_responses.json"
    
    print("🚀 Starting response collection for Sentinel Forge AI...")
    print(f"📂 Loading queries from: {queries_file}")
    
    # Load queries
    queries = load_queries(str(queries_file))
    print(f"✅ Loaded {len(queries)} test queries")
    
    # Collect responses
    responses = []
    print("\n📡 Collecting responses from AI chat endpoint...")
    
    for i, query_data in enumerate(queries, 1):
        query_id = query_data["id"]
        query_text = query_data["query"]
        context = query_data.get("context", "")
        
        print(f"\n[{i}/{len(queries)}] Processing: {query_id}")
        print(f"  Query: {query_text[:60]}...")
        
        result = collect_response(base_url, query_text, context)
        
        response_entry = {
            "query_id": query_id,
            "query": query_text,
            "context": context,
            "timestamp": time.time(),
            "success": result["success"]
        }
        
        if result["success"]:
            chat_response = result["response"]
            # Extract the assistant's message content
            response_entry["response"] = chat_response.get("content", "")
            response_entry["model"] = chat_response.get("model", "unknown")
            print(f"  ✅ Response collected ({len(response_entry['response'])} chars)")
        else:
            response_entry["error"] = result.get("error", "Unknown error")
            print(f"  ❌ Failed: {response_entry['error']}")
        
        responses.append(response_entry)
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.5)
    
    # Save responses
    print(f"\n💾 Saving responses to: {responses_file}")
    with open(responses_file, 'w', encoding='utf-8') as f:
        json.dump(responses, f, indent=2, ensure_ascii=False)
    
    # Summary
    successful = sum(1 for r in responses if r["success"])
    print(f"\n🎯 Collection complete!")
    print(f"  ✅ Successful: {successful}/{len(responses)}")
    print(f"  ❌ Failed: {len(responses) - successful}/{len(responses)}")
    print(f"  📄 Saved to: {responses_file}")


if __name__ == "__main__":
    main()

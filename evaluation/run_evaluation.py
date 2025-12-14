"""
Evaluation Engine for Sentinel Forge.
Uses Azure AI Evaluation SDK (or mocks if missing) to score AI responses.
"""
import json
import os
import statistics
import random
from pathlib import Path
from typing import List, Dict, Any

# Try to import Azure AI Evaluation SDK
try:
    from azure.ai.evaluation import (
        RelevanceEvaluator,
        CoherenceEvaluator,
        GroundednessEvaluator
    )
    HAS_AZURE_EVAL = True
except ImportError:
    HAS_AZURE_EVAL = False

def load_json(file_path: Path) -> List[Dict[str, Any]]:
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def mock_score(metric: str) -> dict:
    """Simulate a score for testing the pipeline without costs."""
    return {metric: round(random.uniform(3.0, 5.0), 1)}

def main():
    # 1. Setup Paths
    eval_dir = Path(__file__).parent
    responses_file = eval_dir / "test_responses.json"
    results_file = eval_dir / "eval_results.json"
    
    # 2. Configure Azure OpenAI (if available)
    model_config = {
        "azure_endpoint": os.getenv("AOAI_ENDPOINT", ""),
        "api_key": os.getenv("AOAI_KEY") or os.getenv("AZURE_OPENAI_API_KEY", ""),
        "azure_deployment": os.getenv("AOAI_CHAT_DEPLOYMENT", "gpt-4"),
        "api_version": os.getenv("AOAI_API_VERSION", "2024-02-15-preview"),
    }

    # 3. Initialize Evaluators
    print("🚀 Initializing Evaluation Engine...")
    if HAS_AZURE_EVAL and model_config["api_key"]:
        relevance = RelevanceEvaluator(model_config)
        coherence = CoherenceEvaluator(model_config)
        groundedness = GroundednessEvaluator(model_config)
        print("   ✅ Azure Evaluators loaded.")
    else:
        relevance = coherence = groundedness = None
        print("   ℹ️  Azure AI Evaluation SDK not found or API key missing.")
        print("   ⚠️  Running in MOCK MODE (Simulated Scores).")
        print("       To enable real scoring: pip install azure-ai-evaluation[remote]")

    # 4. Load Data
    responses = load_json(responses_file)
    if not responses:
        print(f"❌ No responses found in {responses_file}. Run collect_responses.py first.")
        return

    print(f"   Processing {len(responses)} responses...")
    results = []

    # 5. Run Scoring Loop
    for item in responses:
        if not item.get("success"):
            continue
            
        q_id = item.get("query_id", "unknown")
        query = item.get("query", "")
        response = item.get("response", "")
        context = item.get("context", "No context provided.")
        
        print(f"   ⚖️  Scoring {q_id}...")
        
        scores = {}
        
        # Relevance
        if relevance:
            try:
                s = relevance(query=query, response=response)
                scores["relevance"] = s.get("relevance", 0)
            except Exception as e:
                print(f"     Error scoring relevance: {e}")
                scores["relevance"] = 0
        else:
            scores.update(mock_score("relevance"))

        # Coherence
        if coherence:
            try:
                s = coherence(query=query, response=response)
                scores["coherence"] = s.get("coherence", 0)
            except Exception as e:
                print(f"     Error scoring coherence: {e}")
                scores["coherence"] = 0
        else:
            scores.update(mock_score("coherence"))

        # Groundedness
        if groundedness:
            try:
                s = groundedness(query=query, response=response, context=context)
                scores["groundedness"] = s.get("groundedness", 0)
            except Exception as e:
                print(f"     Error scoring groundedness: {e}")
                scores["groundedness"] = 0
        else:
            scores.update(mock_score("groundedness"))

        results.append({
            **item,
            "scores": scores
        })

    # 6. Save & Summarize
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n📊 Evaluation Summary:")
    for metric in ["relevance", "coherence", "groundedness"]:
        vals = [r["scores"].get(metric, 0) for r in results]
        if vals:
            avg = statistics.mean(vals)
            print(f"   {metric.capitalize()}: {avg:.2f} / 5.0")
    
    print(f"\n✅ Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()

import { useEffect, useState } from "react";
import {
  cogGetMemory,
  cogGetRules,
  cogGetSuggestions,
  cogGetThreads,
  type CogThread,
  type MemorySnapshot,
  type Suggestions,
  type SymbolicRules,
} from "../lib/api";

export default function InsightsPage() {
  const [memory, setMemory] = useState<MemorySnapshot | null>(null);
  const [rules, setRules] = useState<SymbolicRules | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestions | null>(null);
  const [threads, setThreads] = useState<CogThread[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    Promise.allSettled([
      cogGetMemory(),
      cogGetRules(),
      cogGetSuggestions(),
      cogGetThreads(),
    ]).then(([memRes, rulesRes, sugRes, thRes]) => {
      if (cancelled) return;
      if (memRes.status === "fulfilled") setMemory(memRes.value);
      if (rulesRes.status === "fulfilled") setRules(rulesRes.value);
      if (sugRes.status === "fulfilled") setSuggestions(sugRes.value);
      if (thRes.status === "fulfilled") setThreads(thRes.value.threads ?? []);
      // If all failed, show error
      const allFailed = [memRes, rulesRes, sugRes, thRes].every(
        (r) => r.status === "rejected",
      );
      if (allFailed) setError("Failed to load cognitive data");
      setLoading(false);
    });
    return () => { cancelled = true; };
  }, []);

  if (loading) {
    return (
      <section className="panel">
        <h2>Insights</h2>
        <p className="text-muted">Loading cognitive data...</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2>Insights</h2>
      <p>Memory, symbolic rules, threads, and AI suggestions from the cognitive engine.</p>

      {error && <p className="error-msg">{error}</p>}

      {/* Memory */}
      {memory && (
        <>
          <h3>Memory</h3>
          <div className="kv-grid">
            <div>
              <span className="kv-label">Entries</span>
              <strong>{memory.size}</strong>
            </div>
            <div>
              <span className="kv-label">Capacity</span>
              <strong>{memory.capacity}</strong>
            </div>
            <div>
              <span className="kv-label">Usage</span>
              <strong>
                {memory.capacity > 0
                  ? ((memory.size / memory.capacity) * 100).toFixed(1) + "%"
                  : "0%"}
              </strong>
            </div>
          </div>
          {memory.top_preview.length > 0 && (
            <div className="insight-preview">
              <h4>Recent Memory Entries</h4>
              <ul>
                {memory.top_preview.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      {/* Symbolic Rules */}
      {rules && Object.keys(rules.rules).length > 0 && (
        <>
          <h3>Symbolic Rules ({Object.keys(rules.rules).length})</h3>
          <div className="rules-grid">
            {Object.entries(rules.rules).map(([key, value]) => (
              <div key={key} className="rule-card">
                <span className="rule-key">{key}</span>
                <span className="rule-value">{value}</span>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Threads */}
      {threads.length > 0 && (
        <>
          <h3>Active Threads ({threads.length})</h3>
          <div className="threads-list">
            {threads.map((t) => (
              <div key={t.id} className="thread-card">
                <span className="thread-topic">{t.topic}</span>
                <span className="thread-count">{t.count} messages</span>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Suggestions */}
      {suggestions && suggestions.suggestions.length > 0 && (
        <>
          <h3>AI Suggestions</h3>
          <div className="suggestions-list">
            {suggestions.suggestions.map((s, i) => (
              <div key={i} className="suggestion-card">
                <pre className="code-block">
                  {JSON.stringify(s, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        </>
      )}

      {!memory &&
        !rules &&
        !suggestions &&
        threads.length === 0 && (
          <p className="text-muted">
            No cognitive data available. Process some text through the
            Cognitive Processing page to populate the engine.
          </p>
        )}
    </section>
  );
}

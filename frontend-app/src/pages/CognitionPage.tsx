import { FormEvent, useState } from "react";
import { cogProcess, type ProcessResponse } from "../lib/api";

export default function CognitionPage() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<ProcessResponse | null>(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!input.trim() || processing) return;
    setError("");
    setResult(null);
    setProcessing(true);
    try {
      const resp = await cogProcess(input.trim());
      setResult(resp);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Processing failed");
    } finally {
      setProcessing(false);
    }
  }

  return (
    <section className="panel">
      <h2>Cognitive Processing</h2>
      <p>Submit text for analysis through the Sentinel cognitive pipeline.</p>

      <form onSubmit={onSubmit} className="cog-form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter text to process through the cognitive engine..."
          rows={5}
          maxLength={10000}
          disabled={processing}
        />
        <div className="cog-form-actions">
          <button type="submit" disabled={processing || !input.trim()}>
            {processing ? "Processing..." : "Process"}
          </button>
          <span className="text-muted">{input.length} / 10,000 characters</span>
        </div>
      </form>

      {error && <p className="error-msg">{error}</p>}

      {result && (
        <div className="cog-result">
          <h3>Result</h3>
          <div className="kv-grid">
            <div>
              <span className="kv-label">Processing Time</span>
              <strong>{result.processing_time.toFixed(2)} ms</strong>
            </div>
            <div>
              <span className="kv-label">Pool Used</span>
              <strong>{result.pool_used}</strong>
            </div>
            <div>
              <span className="kv-label">Input ID</span>
              <strong className="mono">{result.input_id}</strong>
            </div>
            <div>
              <span className="kv-label">Output ID</span>
              <strong className="mono">{result.output_id}</strong>
            </div>
          </div>
          <h4>Output</h4>
          <pre className="code-block">
            {typeof result.result === "string"
              ? result.result
              : JSON.stringify(result.result, null, 2)}
          </pre>
        </div>
      )}
    </section>
  );
}

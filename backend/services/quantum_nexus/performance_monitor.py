"""
Performance Monitor
Real-time operation timing, throughput, and processing count tracking
for the Quantum Nexus Forge cognitive architecture.

Tracks:
    • Per-operation durations (ms)
    • Total operations, ops/second, average latency
    • Processing counters: nodes created, symbols processed,
      neurodivergent analyses, zones allocated, forge sessions
    • Rolling window of last 50 operations for trend analysis
"""
from __future__ import annotations

import time
from typing import Any, Dict, List


_WINDOW_SIZE = 50   # operations kept in rolling log


class PerformanceMonitor:
    """Lightweight real-time performance monitor."""

    def __init__(self) -> None:
        self._start_time   = time.time()
        self._operation_log: List[Dict[str, Any]] = []
        self.counts = {
            "nodes_created":          0,
            "symbols_processed":      0,
            "neurodivergent_analyses": 0,
            "zones_allocated":        0,
            "forge_sessions":         0,
        }

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(self, operation_name: str, duration_seconds: float) -> None:
        """Record a completed operation."""
        entry = {
            "operation":   operation_name,
            "duration_ms": round(duration_seconds * 1000, 3),
            "elapsed_s":   round(time.time() - self._start_time, 3),
        }
        self._operation_log = (self._operation_log + [entry])[-_WINDOW_SIZE:]

    def increment(self, counter: str, amount: int = 1) -> None:
        """Increment a named processing counter."""
        if counter in self.counts:
            self.counts[counter] += amount

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def metrics(self) -> Dict[str, Any]:
        """Return a full performance snapshot."""
        uptime   = time.time() - self._start_time
        total_ops = len(self._operation_log)

        avg_ms   = 0.0
        if total_ops:
            avg_ms = sum(op["duration_ms"] for op in self._operation_log) / total_ops

        ops_per_sec = round(total_ops / max(uptime, 0.001), 3)

        return {
            "uptime_seconds":          round(uptime, 2),
            "total_operations":        total_ops,
            "average_operation_ms":    round(avg_ms, 3),
            "operations_per_second":   ops_per_sec,
            "processing_counts":       dict(self.counts),
            "recent_operations":       self._operation_log[-10:],
        }

    def reset(self) -> None:
        """Reset all counters (does not reset uptime)."""
        self._operation_log.clear()
        for k in self.counts:
            self.counts[k] = 0


# Module-level singleton
perf_monitor = PerformanceMonitor()

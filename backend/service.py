import threading
import time
import uuid
from typing import Any, Dict, Optional

from quantum_nexus_forge_v5_2_enhanced import QuantumNexusForge
from sentinel_cognition import SentinelCognitionGraph
from sentinel_sync import sync_coordinator


class QNFService:
    """Middle layer wrapping QuantumNexusForge with thread-safety and jobs."""

    def __init__(self) -> None:
        self._qnf = QuantumNexusForge()
        self._lock = threading.RLock()
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._jobs_lock = threading.Lock()
        # Cognitive graph based on the provided blueprint
        self._cog = SentinelCognitionGraph()

    # Core operations
    def process(self, data: Any, pool_id: Optional[str] = None) -> Dict[str, Any]:
        with self._lock:
            return self._qnf.process(data, pool_id)

    def status(self) -> Dict[str, Any]:
        # Status reads can be done without the global lock, but keep simple and safe
        with self._lock:
            return self._qnf.status()

    def create_pool(self, pool_id: str, initial_size: int = 3) -> str:
        with self._lock:
            return self._qnf.create_pool(pool_id, initial_size)

    def teardown(self) -> None:
        with self._lock:
            self._qnf.teardown_complete()

    def rebuild(self, default_pools: int = 2, pool_size: int = 5) -> None:
        with self._lock:
            self._qnf.rebuild_from_foundation(
                {"default_pools": default_pools, "pool_size": pool_size}
            )

    # Cognitive Graph operations
    def cog_process(self, data: Any) -> Dict[str, Any]:
        result = self._cog.process(data)
        return {
            "input": result.input,
            "output": result.output,
            "signature": result.signature,
            "processing_time": result.processing_time,
            "metadata": result.metadata,
        }

    def cog_status(self) -> Dict[str, Any]:
        return self._cog.status()

    def cog_get_rules(self) -> Dict[str, Any]:
        return {"rules": self._cog.get_rules()}

    def cog_set_rules(self, rules: Dict[str, str]) -> Dict[str, Any]:
        self._cog.set_rules(rules)
        return {"status": "ok", "rules": self._cog.get_rules()}

    def cog_memory_snapshot(self) -> Dict[str, Any]:
        return self._cog.memory_snapshot()

    def cog_memory_clear(self) -> Dict[str, Any]:
        self._cog.memory_clear()
        return {"status": "ok"}

    def cog_prime_metrics(self) -> Dict[str, Any]:
        return self._cog.prime_metrics()

    def cog_suggestions(self, limit: int = 5) -> Dict[str, Any]:
        return {"suggestions": self._cog.metatron_suggestions(limit=limit)}

    # --- SentinelPrimeSync (tri-node) -------------------------------------
    def sync_update(self, agent: str, state: Dict[str, Any]) -> Dict[str, Any]:
        st = sync_coordinator.update_agent_state(agent, state)
        return {
            "agent": st.agent,
            "timestamp": st.timestamp,
            "glyphic_signature": st.glyphic_signature,
            "sequence_validation": sync_coordinator.validate(sync_coordinator.sequence),
        }

    def sync_snapshot(self) -> Dict[str, Any]:
        return sync_coordinator.snapshot()

    def sync_trinode(self) -> Dict[str, Any]:
        return sync_coordinator.trinode_status()

    def sync_validate(self, sequence: list[str]) -> Dict[str, Any]:
        return sync_coordinator.validate(sequence)

    def sync_boot(self) -> List[Dict[str, Any]]:
        return sync_coordinator.boot_sequence()

    # Stress testing
    def stress_test(self, iterations: int, concurrent: bool) -> Dict[str, Any]:
        with self._lock:
            return self._qnf.stress_test(iterations=iterations, concurrent=concurrent)

    # Background jobs (for async stress tests)
    def submit_stress_job(self, iterations: int, concurrent: bool) -> str:
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        with self._jobs_lock:
            self._jobs[job_id] = {"status": "queued", "created": time.time()}

        def _run() -> None:
            self._update_job(job_id, status="running")
            try:
                result = self.stress_test(iterations=iterations, concurrent=concurrent)
                self._update_job(job_id, status="completed", result=result)
            except Exception as exc:  # pragma: no cover
                self._update_job(job_id, status="failed", error=str(exc))

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return job_id

    def _update_job(
        self, job_id: str, *, status: str, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None
    ) -> None:
        with self._jobs_lock:
            payload: Dict[str, Any] = self._jobs.get(job_id, {})
            payload.update({"status": status, "updated": time.time()})
            if result is not None:
                payload["result"] = result
            if error is not None:
                payload["error"] = error
            self._jobs[job_id] = payload

    def job_status(self, job_id: str) -> Dict[str, Any]:
        with self._jobs_lock:
            if job_id not in self._jobs:
                return {"status": "not_found", "job_id": job_id}
            payload = dict(self._jobs[job_id])
            payload["job_id"] = job_id
            return payload


# Singleton service instance
service = QNFService()

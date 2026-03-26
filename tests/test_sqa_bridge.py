"""Tests for sqa_bridge.py — Python fallback mode (no C++ module required)."""
import os
import pytest

# Ensure C++ engine is NOT active for these tests
os.environ.pop("SQA_ENGINE_ACTIVE", None)

from sqa_bridge import (
    CNOBridge,
    A1FSBridge,
    NNSBridge,
    SQAEngine,
    is_cpp_available,
    is_active,
)


class TestModuleState:
    def test_is_active_returns_false_without_env(self):
        os.environ.pop("SQA_ENGINE_ACTIVE", None)
        # Without the C++ module, is_active is always False
        assert is_active() is False

    def test_cpp_available_is_bool(self):
        assert isinstance(is_cpp_available(), bool)


class TestCNOBridge:
    def test_fallback_returns_dict(self):
        cno = CNOBridge()
        result = cno.process("hello world")
        assert isinstance(result, dict)
        assert "intent_label" in result
        assert "engine" in result

    def test_fallback_engine_label(self):
        cno = CNOBridge()
        result = cno.process("test input")
        # Without C++ module, falls back to python
        if not is_cpp_available():
            assert result["engine"] == "python_fallback"

    def test_fallback_with_atom_id(self):
        cno = CNOBridge()
        result = cno.process("test", atom_id="custom_123")
        assert result["id"] == "custom_123"

    def test_fallback_auto_id(self):
        cno = CNOBridge()
        result = cno.process("test")
        if not is_cpp_available():
            assert result["id"].startswith("cno_py_")

    def test_get_rules_fallback(self):
        cno = CNOBridge()
        if not is_cpp_available():
            assert cno.get_rules() == []

    def test_executions_fallback(self):
        cno = CNOBridge()
        if not is_cpp_available():
            assert cno.executions == 0


class TestA1FSBridge:
    def test_store_fallback(self):
        a1fs = A1FSBridge()
        mem_id = a1fs.store("test memory")
        if not is_cpp_available():
            assert mem_id.startswith("mem_py_")

    def test_retrieve_similar_fallback(self):
        a1fs = A1FSBridge()
        results = a1fs.retrieve_similar("query")
        if not is_cpp_available():
            assert results == []

    def test_snapshot_fallback(self):
        a1fs = A1FSBridge()
        snap = a1fs.snapshot()
        if not is_cpp_available():
            assert snap["engine"] == "python_fallback"

    def test_size_fallback(self):
        a1fs = A1FSBridge()
        if not is_cpp_available():
            assert a1fs.size == 0

    def test_consolidate_fallback(self):
        a1fs = A1FSBridge()
        if not is_cpp_available():
            assert a1fs.consolidate() == 0

    def test_clear_does_not_crash(self):
        a1fs = A1FSBridge()
        a1fs.clear()  # Should not raise


class TestNNSBridge:
    def test_status_fallback(self):
        nns = NNSBridge()
        status = nns.status()
        if not is_cpp_available():
            assert status["engine"] == "python_fallback"

    def test_execute_fallback(self):
        nns = NNSBridge()
        if not is_cpp_available():
            assert nns.execute({}) == []


class TestSQAEngine:
    def test_engine_creation(self):
        engine = SQAEngine()
        assert hasattr(engine, "cno")
        assert hasattr(engine, "a1fs")
        assert hasattr(engine, "nns")

    def test_process_fallback(self):
        engine = SQAEngine()
        result = engine.process("test input")
        assert isinstance(result, dict)
        assert "engine" in result
        assert "memory_id" in result
        assert "total_ms" in result

    def test_status_report(self):
        engine = SQAEngine()
        status = engine.status()
        assert "active" in status
        assert "cpp_available" in status
        assert "version" in status

    def test_active_property(self):
        engine = SQAEngine()
        # Without env var set, should not be active
        assert engine.active is False

import threading
import time
from fastapi.testclient import TestClient  # type: ignore[reportMissingImports]

from backend.main import app
from backend.eventbus import bus


def test_ws_sync_receives_published_events(monkeypatch):
    monkeypatch.delenv("QNF_API_KEY", raising=False)
    monkeypatch.setenv("QNF_REQUIRE_API_KEY", "0")
    client = TestClient(app)
    with client.websocket_connect("/ws/sync") as ws:
        # First message is the initial sync snapshot
        initial = ws.receive_text()
        assert "sync.snapshot" in initial

        # Publish an event from a background thread (simulates server-side event)
        payload = {"type": "test.event", "data": {"hello": "world"}}

        def _publish():
            time.sleep(0.1)
            bus.publish(payload)

        t = threading.Thread(target=_publish)
        t.start()

        msg = ws.receive_text()
        assert "test.event" in msg
        t.join()

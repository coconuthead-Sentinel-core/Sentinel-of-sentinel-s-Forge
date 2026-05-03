import threading
import time
from fastapi.testclient import TestClient  # type: ignore[reportMissingImports]

from backend.main import app
from backend.eventbus import bus
from backend.core.config import settings


def test_ws_sync_receives_published_events(monkeypatch):
    """Live-server WS test:
        connect -> receive snapshot -> background publish -> receive event.

    SoSF's security layer reads ``settings.API_KEY`` (not raw env vars),
    so we patch the settings singleton directly. Settings is a Pydantic
    BaseSettings instance; its attributes are mutable via
    monkeypatch.setattr.
    """
    monkeypatch.setattr(settings, "API_KEY", "")
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")

    client = TestClient(app)
    with client.websocket_connect("/ws/sync") as ws:
        # First message is the initial sync snapshot
        initial = ws.receive_text()
        assert "sync.snapshot" in initial

        # Publish from a background thread (simulates server-side event)
        payload = {"type": "test.event", "data": {"hello": "world"}}

        def _publish():
            time.sleep(0.1)
            bus.publish(payload)

        t = threading.Thread(target=_publish)
        t.start()

        msg = ws.receive_text()
        assert "test.event" in msg
        t.join()

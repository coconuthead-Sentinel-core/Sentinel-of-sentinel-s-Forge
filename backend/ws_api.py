import asyncio
import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect  # type: ignore[reportMissingImports]

from .eventbus import bus
from .security import websocket_require_api_key
from .service import service


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


@router.websocket("/ws/sync")
async def websocket_sync(websocket: WebSocket):
    """Simple echo WebSocket for testing sync operations."""
    await websocket.accept()
    logger.info("WebSocket client connected to /ws/sync")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"WebSocket received: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected from /ws/sync")


@router.websocket("/ws/sync")
async def ws_sync(websocket: WebSocket) -> Any:
    # Enforce API key if configured
    websocket_require_api_key(websocket)
    await websocket.accept()
    loop = asyncio.get_running_loop()
    # Use a bounded queue with 'latest' policy to keep UIs current under load
    queue = bus.subscribe(loop, maxsize=1000, policy="latest")
    # Send initial snapshot
    try:
        snap = await asyncio.get_running_loop().run_in_executor(None, service.sync_snapshot)
        await websocket.send_text(json.dumps({"type": "sync.snapshot", "data": snap}))
        while True:
            # Wait for next event or client ping
            payload = await queue.get()
            await websocket.send_text(json.dumps(payload))
    except WebSocketDisconnect:
        pass
    finally:
        bus.unsubscribe(queue)


@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming."""
    await manager.connect(websocket)
    try:
        from .service import service

        while True:
            # Send metrics every 2 seconds
            try:
                metrics = service.metrics()
                status = service.status()

                await websocket.send_json(
                    {
                        "type": "metrics_update",
                        "data": {
                            "metrics": metrics,
                            "status": status,
                            "timestamp": __import__("time").time(),
                        },
                    }
                )
            except Exception as e:
                print(f"Error sending metrics: {e}")

            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    """WebSocket endpoint for real-time event streaming."""
    await manager.connect(websocket)
    try:
        from .service import service

        last_event_count = 0

        while True:
            try:
                # Get recent events
                events = service.recent_events(20)
                current_count = len(events)

                # Only send if new events appeared
                if current_count > last_event_count:
                    new_events = events[last_event_count:]
                    await websocket.send_json(
                        {
                            "type": "new_events",
                            "data": new_events,
                            "timestamp": __import__("time").time(),
                        }
                    )
                    last_event_count = current_count

            except Exception as e:
                print(f"Error sending events: {e}")

            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

import json
import uuid
import hashlib
import time
import httpx
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from config import ADK_BASE_URL, DEFAULT_APP_NAME

router = APIRouter()


def _build_ephemeral_user_id(fingerprint: str, user_agent: str) -> str:
    time_bucket = int(time.time() // 1800)
    raw = f"{fingerprint}|{user_agent}|{time_bucket}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"fp_{digest}"


@router.websocket("/ws/adk")
@router.websocket("/wss")
async def adk_websocket(websocket: WebSocket):
    """
    WebSocket bidirecional:
    Frontend <-> FastAPI <-> ADK API Server
    """

    await websocket.accept()

    try:
        init_msg = await websocket.receive_text()
        try:
            init = json.loads(init_msg)
        except json.JSONDecodeError:
            await websocket.send_json({"error": "invalid init payload"})
            await websocket.close()
            return

        fingerprint = init.get("fingerprint")
        session_id = init.get("sessionId") or f"s_{uuid.uuid4().hex[:8]}"
        app_name = init.get("appName") or DEFAULT_APP_NAME

        if not fingerprint or not isinstance(fingerprint, str):
            await websocket.send_json({"error": "fingerprint is required"})
            await websocket.close()
            return

        user_agent = websocket.headers.get("user-agent", "unknown")
        user_id = _build_ephemeral_user_id(fingerprint=fingerprint, user_agent=user_agent)

        await websocket.send_json({
            "type": "connect",
            "fingerprint": fingerprint,
            "status": "validated"
        })

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    f"{ADK_BASE_URL}/apps/{app_name}/users/{user_id}/sessions/{session_id}",
                    json={}
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            await websocket.send_json({
                "error": f"failed_to_init_adk_session: {exc}"
            })
            await websocket.close()
            return

        await websocket.send_json({
            "type": "session",
            "appName": app_name,
            "fingerprint": fingerprint,
            "ephemeralUserId": user_id,
            "sessionId": session_id
        })

        while True:
            raw = await websocket.receive_text()
            payload = json.loads(raw)

            text = payload.get("text")
            if not text:
                await websocket.send_json({"error": "text field required"})
                continue

            await stream_adk(
                websocket=websocket,
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                text=text
            )

    except WebSocketDisconnect:
        print("WebSocket disconnected")

    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()


async def stream_adk(
    websocket: WebSocket,
    app_name: str,
    user_id: str,
    session_id: str,
    text: str
):
    """
    Chama /run_sse do ADK e retransmite eventos via WebSocket
    """

    body = {
        "appName": app_name,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": text}]
        },
        "streaming": True
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            f"{ADK_BASE_URL}/run_sse",
            headers={"Accept": "text/event-stream"},
            json=body,
        ) as response:

            async for line in response.aiter_lines():
                if not line:
                    continue

                if not line.startswith("data:"):
                    continue

                data = line.replace("data:", "").strip()

                try:
                    event = json.loads(data)
                except json.JSONDecodeError:
                    continue

                # Repasse direto para o frontend
                await websocket.send_json({
                    "type": "event",
                    "payload": event
                })
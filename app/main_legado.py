from fastapi import FastAPI
from app.ws_adk import router as ws_router
from app.keep_alive import keep_alive_ollama
import asyncio

app = FastAPI(title="ADK WebSocket Gateway")

app.include_router(ws_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive_ollama())
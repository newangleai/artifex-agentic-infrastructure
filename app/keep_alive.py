import asyncio
import httpx
from app.config import OLLAMA_KEEP_ALIVE_URL

OLLAMA_URL = OLLAMA_KEEP_ALIVE_URL

async def keep_alive_ollama(interval_seconds=240):
    """
    Envia requisições periódicas para o Ollama para evitar que o modelo seja descarregado da memória.
    interval_seconds: intervalo entre requisições (padrão: 240 segundos = 4 minutos)
    """
    while True:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(OLLAMA_URL, timeout=10)
                print(f"Ollama keep-alive: {resp.status_code}")
        except Exception as e:
            print(f"Ollama keep-alive error: {e}")
        await asyncio.sleep(interval_seconds)
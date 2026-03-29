from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.routers import generate, spotify, image
from backend.services.logging import setup_logging
import logging

setup_logging()
log = logging.getLogger("reverie")

app = FastAPI(title="Reverie API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(generate.router)
app.include_router(spotify.router)
app.include_router(image.router)

log.info("Reverie API started (llm=%s, image=%s)", settings.llm_provider, settings.image_provider)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


# Serve built frontend in production (must be last — catch-all route)
DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")

    @app.get("/{path:path}")
    async def spa_fallback(path: str):
        file = DIST / path
        if file.is_file():
            return FileResponse(file)
        return FileResponse(DIST / "index.html")

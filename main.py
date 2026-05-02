#!/usr/bin/env python3
import logging
import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

def _safe_path(path: str) -> Path:
    base = Path.cwd().resolve()
    target = (base / path).resolve()
    try:
        target.relative_to(base)
        return target
    except ValueError:
        return base / Path(path).name

handlers = [logging.StreamHandler()]
if os.getenv("LOG_FILE"):
    handlers.append(logging.FileHandler(str(_safe_path(os.getenv("LOG_FILE")))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=handlers,
)
logger = logging.getLogger("facade")

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

SWITCH_UA = os.getenv("SWITCH_UA", "ABC")
SWITCH_FILE = os.getenv("SWITCH_FILE", "switch.html")
DEFAULT_FILE = os.getenv("DEFAULT_FILE", "index.html")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

def _response(content: str, filename: str) -> Response:
    return HTMLResponse(content) if filename.endswith((".html", ".htm")) else PlainTextResponse(content)

def _read_page(path: str) -> str:
    try:
        return _safe_path(path).read_text(encoding="utf-8").replace("{{SWITCH_UA}}", SWITCH_UA)
    except FileNotFoundError:
        return "File not found."

@app.get("/")
async def root(request: Request) -> Response:
    user_agent = (request.headers.get("user-agent") or "").strip()
    client_ip = getattr(request.client, "host", "unknown")

    if user_agent == SWITCH_UA:
        logger.info("SWITCH  %s  %s", client_ip, user_agent)
        return _response(_read_page(SWITCH_FILE), SWITCH_FILE)

    logger.info("DECOY   %s  %s", client_ip, user_agent)
    return _response(_read_page(DEFAULT_FILE), DEFAULT_FILE)

@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException) -> Response:
    if request.url.path == "/favicon.ico":
        return Response(status_code=204)
    if exc.status_code == 404:
        return PlainTextResponse("Not Found", status_code=404)
    return PlainTextResponse("Error", status_code=exc.status_code)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)

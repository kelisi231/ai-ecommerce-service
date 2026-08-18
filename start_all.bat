@echo off
chcp 65001 >nul
cd /d "%~dp0"
start "AI-CS embedding(8001)" cmd /k "uv run uvicorn app.api.lifespan.embedding_lifespan:app --host 127.0.0.1 --port 8001"
start "AI-CS reranker(8002)" cmd /k "uv run uvicorn app.api.lifespan.reranker_lifespan:app --host 127.0.0.1 --port 8002"
start "AI-CS api(8000)"     cmd /k "uv run uvicorn main:app --host 127.0.0.1 --port 8000"
echo 3 windows opened. Close a window to stop that service.
pause

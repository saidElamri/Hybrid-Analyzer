import sys
import os
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Add the project root to sys.path so we can import 'backend'
# Vercel root is usually /var/task
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = None

try:
    from backend.main import app as application
    app = application
except Exception:
    error_trace = traceback.format_exc()
    app = FastAPI()
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(request: Request, path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application failed to start (api/index.py)",
                "detail": error_trace.split("\n")
            }
        )

import sys
import os
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Add the project root AND backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, "backend"))

app = None

try:
    # Try importing as a package first
    try:
        from backend.main import app as application
    except ImportError:
        # Fallback to direct import if backend is in path
        from main import app as application
    
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

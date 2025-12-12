import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = None

try:
    # Add current directory to path so we can import 'main'
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    from main import app as application
    app = application
except Exception:
    # Capture the full traceback
    error_trace = traceback.format_exc()
    
    # Create a fallback app to show the error
    app = FastAPI()
    
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(request: Request, path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application failed to start",
                "detail": error_trace.split("\n")
            }
        )

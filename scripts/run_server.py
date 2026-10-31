import sys
import os
import uvicorn

if __name__ == "__main__":
    # Ensure project root is in sys.path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    print("QueryMind: Initializing Uvicorn Server on http://0.0.0.0:8008...", flush=True)
    config = uvicorn.Config(
        app="backend.app.main:app",
        host="0.0.0.0",
        port=8008,
        log_level="info",
        access_log=False,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    server.run()

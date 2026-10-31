from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.api.routes import router as api_router
from backend.app.services.schema_service import schema_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-cache database schema on startup in background task so app starts instantly
    asyncio.create_task(schema_service.get_schema())
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Natural Language Database Query Assistant with NLP Pipeline, Semantic Schema Matching, and Safe Execution",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "project": "QueryMind",
        "description": "Natural Language Database Query Assistant",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "query": "/api/query",
            "schema": "/api/schema",
            "tables": "/api/tables",
            "dashboard": "/api/dashboard",
            "history": "/api/query-history"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=settings.PORT, reload=False)

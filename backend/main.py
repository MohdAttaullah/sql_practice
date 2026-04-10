"""
SQL Practice Platform — FastAPI Backend

Main application entrypoint. Registers all routers, configures CORS,
and handles startup/shutdown lifecycle events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.engine import get_connection, close_connection
from backend.routers import questions, execute, validate, datasets, progress


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: ensure DB is seeded. Shutdown: close connections."""
    # Startup — triggers seed if DB doesn't exist
    get_connection()
    print("🚀 SQL Practice Platform backend ready")
    yield
    # Shutdown
    close_connection()
    print("👋 Backend shutdown complete")


app = FastAPI(
    title="SQL Practice Platform",
    description="Interactive SQL lab for Data Engineer interview preparation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow the Next.js frontend (typically localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(questions.router)
app.include_router(execute.router)
app.include_router(validate.router)
app.include_router(datasets.router)
app.include_router(progress.router)


@app.get("/api/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "sql-practice-platform"}

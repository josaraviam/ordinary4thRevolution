# main.py
# FastAPI app entry point // Smart Health Monitoring System

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from infrastructure.database.connection import connect_db, close_db

# Import REST routers
from api.rest.health import router as health_router
from api.rest.auth import router as auth_router
from api.rest.patients import router as patients_router
from api.rest.alerts import router as alerts_router
from api.rest.overview import router as overview_router
from api.rest.reports import router as reports_router
from api.rest.settings import router as settings_router

# Import GraphQL router
from api.graphql.schema import graphql_router


# Lifespan context // handles startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[APP] Starting Smart Health Monitoring API...")
    await connect_db()
    print("[APP] GraphQL endpoint available at /graphql")
    print("[APP] GraphQL subscriptions via WebSocket at /graphql")
    yield
    # Shutdown
    await close_db()
    print("[APP] Shutdown complete")


# Create app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST + GraphQL API for Smart Health Monitoring System // SIS4415 Final Project",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# CORS middleware // allows Node-RED dashboard to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register REST routers under /api prefix
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(patients_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(overview_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(settings_router, prefix="/api")

# Register GraphQL router at /graphql
# Supports queries, mutations, and WebSocket subscriptions
app.include_router(graphql_router, prefix="/graphql")


# Root endpoint
@app.get("/")
async def root():
    """API info // redirect to docs"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "rest_docs": "/docs",
        "graphql": "/graphql",
        "health": "/api/health"
    }


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

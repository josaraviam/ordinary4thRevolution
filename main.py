# main.py
# FastAPI app entry point // Smart Health Monitoring System

from contextlib import asynccontextmanager
# Main entry point for the API
# REST + GraphQL + WebSockets
# Built with FastAPI because... well, it's fast (easier) and I like it :)

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


# CORS middleware - Who can talk to my API (especially Node-RED)
# Wildcard config because WebSockets can be picky about origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Routes
app.include_router(health_router, prefix="/api")      # Health checks (am I alive?) I hope so
app.include_router(auth_router, prefix="/api")        # Login/JWT stuff (authentication)  
app.include_router(patients_router, prefix="/api")    # Patient management (CRUD + vitals)
app.include_router(alerts_router, prefix="/api")      # Alert handling (critical vitals)
app.include_router(overview_router, prefix="/api")    # Dashboard KPIs and summaries
app.include_router(reports_router, prefix="/api")     # Export & analytics (reports, stats)
app.include_router(settings_router, prefix="/api")    # Threshold config and user prefs

# GraphQL endpoint - because sometimes we are gonna need more flexibility than REST
# Also handles WebSocket subscriptions
app.include_router(graphql_router, prefix="/graphql")


# Root endpoint - just saying hello (nothing fancy here)
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

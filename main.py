# main.py
# FastAPI app entry point // Smart Health Monitoring System

from contextlib import asynccontextmanager
# Main entry point for the API
# REST + GraphQL + WebSockets
# Built with FastAPI because... well, it's fast (easier) and I like it :)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from config.logging_config import setup_logging, get_logger
from infrastructure.database.connection import connect_db, close_db
from api.middleware.logging_middleware import log_requests_middleware

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


# Handles startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Initialize logging first
    app_logger = setup_logging()
    app_logger.info("Starting Smart Health Monitoring API...", extra={"event": "app_startup"})
    
    try:
        await connect_db()
        app_logger.info("Database connected successfully", extra={"event": "db_connected"})
        app_logger.info("GraphQL endpoint available at /graphql", extra={"event": "graphql_ready"})
        app_logger.info("GraphQL subscriptions via WebSocket at /graphql", extra={"event": "websocket_ready"})
        app_logger.info("Application startup complete", extra={"event": "app_ready"})
    except Exception as e:
        app_logger.error(f"Failed to start application: {e}", extra={"event": "app_startup_failed"}, exc_info=True)
        raise
    
    yield
    
    # Shutdown
    app_logger.info("Starting application shutdown...", extra={"event": "app_shutdown_start"})
    try:
        await close_db()
        app_logger.info("Database disconnected successfully", extra={"event": "db_disconnected"})
    except Exception as e:
        app_logger.error(f"Error during shutdown: {e}", extra={"event": "app_shutdown_error"}, exc_info=True)
    
    app_logger.info("Application shutdown complete", extra={"event": "app_shutdown_complete"})


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

# Add request logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await log_requests_middleware(request, call_next)


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

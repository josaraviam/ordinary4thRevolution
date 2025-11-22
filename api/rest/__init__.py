# api/rest/__init__.py
# REST API routers

from api.rest.health import router as health_router
from api.rest.auth import router as auth_router
from api.rest.patients import router as patients_router
from api.rest.alerts import router as alerts_router
from api.rest.overview import router as overview_router
from api.rest.reports import router as reports_router
from api.rest.settings import router as settings_router

__all__ = [
    "health_router",
    "auth_router",
    "patients_router",
    "alerts_router",
    "overview_router",
    "reports_router",
    "settings_router",
]

import logging
import logging.config
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger
from config.settings import get_settings


def setup_logging():
    """
    Configure logging for the entire application.
    Uses JSON formatting in production and simple formatting in development.
    """
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Custom JSON 
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s %(funcName)s %(lineno)d',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # For console output in dev
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.debug:
        console_handler.setFormatter(simple_formatter)
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setFormatter(json_formatter)
        console_handler.setLevel(logging.INFO)
    
    # File handler for logs
    file_handler = logging.FileHandler(logs_dir / "app.log")
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Error file handler
    error_handler = logging.FileHandler(logs_dir / "errors.log")
    error_handler.setFormatter(json_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Debug file handler
    debug_handler = None
    if settings.debug:
        debug_handler = logging.FileHandler(logs_dir / "debug.log")
        debug_handler.setFormatter(json_formatter)
        debug_handler.setLevel(logging.DEBUG)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    if debug_handler:
        root_logger.addHandler(debug_handler)
    
    # Configure third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("motor").setLevel(logging.WARNING)  # MongoDB driver
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    # Create appspecific loggers
    app_logger = logging.getLogger("health_monitoring")
    app_logger.info("Logging system initialized", extra={
        "debug_mode": settings.debug,
        "log_level": "DEBUG" if settings.debug else "INFO"
    })
    
    return app_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    Use this instead of logging.getLogger() directly.
    """
    return logging.getLogger(f"health_monitoring.{name}")

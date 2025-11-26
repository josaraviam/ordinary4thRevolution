import time
import logging
import uuid
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from config.logging_config import get_logger

logger = get_logger("middleware.logging")


async def log_requests_middleware(request: Request, call_next: Callable) -> Response:
    """
    Log all incoming HTTP requests and outgoing responses.
    Includes timing, status codes, and request details.
    """
    # Generate unique request ID for tracing
    request_id = str(uuid.uuid4())[:8]
    
    # Extract request info
    method = request.method
    url = str(request.url)
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Check if it's an authenticated request
    auth_header = request.headers.get("authorization")
    is_authenticated = bool(auth_header and auth_header.startswith("Bearer "))
    
    # Start timing
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id,
            "method": method,
            "url": url,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "is_authenticated": is_authenticated,
            "event": "request_start"
        }
    )
    
    # Add request ID to request state
    request.state.request_id = request_id
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "process_time_seconds": round(process_time, 4),
                "client_ip": client_ip,
                "event": "request_complete"
            }
        )
        
        # Add request ID to resp headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        
        return response
        
    except Exception as e:
        # Calculate time 
        process_time = time.time() - start_time
        
        # Log error
        logger.error(
            "Request failed with exception",
            extra={
                "request_id": request_id,
                "method": method,
                "url": url,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "process_time_seconds": round(process_time, 4),
                "client_ip": client_ip,
                "event": "request_error"
            },
            exc_info=True
        )
        
        # Re-raise the exception (FastAPI will handle it)
        raise


def get_request_id(request: Request) -> str:
    """
    Get the request ID from the request state.
    Returns 'unknown' if not found.
    """
    return getattr(request.state, 'request_id', 'unknown')

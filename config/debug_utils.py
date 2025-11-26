import functools
import time
from typing import Callable, Any
from config.logging_config import get_logger
from config.settings import get_settings

logger = get_logger("debug")
settings = get_settings()


def debug_timer(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.
    Only active in debug mode.
    """
    if not settings.debug:
        return func
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"Function {func.__name__} completed", extra={
                "function": func.__name__,
                "execution_time_seconds": round(execution_time, 4),
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "debug_event": "function_timing"
            })
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.debug(f"Function {func.__name__} failed", extra={
                "function": func.__name__,
                "execution_time_seconds": round(execution_time, 4),
                "error": str(e),
                "debug_event": "function_error"
            })
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"Function {func.__name__} completed", extra={
                "function": func.__name__,
                "execution_time_seconds": round(execution_time, 4),
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "debug_event": "function_timing"
            })
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.debug(f"Function {func.__name__} failed", extra={
                "function": func.__name__,
                "execution_time_seconds": round(execution_time, 4),
                "error": str(e),
                "debug_event": "function_error"
            })
            raise
    
    # Return wrapper
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def debug_log(message: str, **kwargs):
    """
    Log debug information only when in debug mode.
    """
    if settings.debug:
        logger.debug(message, extra={**kwargs, "debug_event": "manual_debug"})


def debug_vars(**variables):
    """
    Log variable values for debugging.
    Usage: debug_vars(user_id=user_id, patient_name=name)
    """
    if settings.debug:
        logger.debug("Debug variables", extra={
            "variables": variables,
            "debug_event": "variable_dump"
        })


class DebugContext:
    """
    Context manager for debugging code blocks.
    
    Usage:
    with DebugContext("processing_patient_data"):
        # Your code here
        pass
    """
    def __init__(self, context_name: str):
        self.context_name = context_name
        self.start_time = None
    
    def __enter__(self):
        if settings.debug:
            self.start_time = time.time()
            logger.debug(f"Entering debug context: {self.context_name}", extra={
                "context": self.context_name,
                "debug_event": "context_enter"
            })
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if settings.debug and self.start_time:
            execution_time = time.time() - self.start_time
            if exc_type is None:
                logger.debug(f"Exiting debug context: {self.context_name}", extra={
                    "context": self.context_name,
                    "execution_time_seconds": round(execution_time, 4),
                    "debug_event": "context_exit_success"
                })
            else:
                logger.debug(f"Exiting debug context with error: {self.context_name}", extra={
                    "context": self.context_name,
                    "execution_time_seconds": round(execution_time, 4),
                    "error_type": exc_type.__name__ if exc_type else None,
                    "error_message": str(exc_val) if exc_val else None,
                    "debug_event": "context_exit_error"
                })

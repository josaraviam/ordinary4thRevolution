#!/usr/bin/env python3
# test_logging.py
# Simple script to test the logging configuration
# Run with: python test_logging.py

import asyncio
from config.logging_config import setup_logging, get_logger
from config.debug_utils import debug_timer, debug_vars, DebugContext


@debug_timer
async def test_async_function():
    """Test async function with debug timing"""
    logger = get_logger("test")
    logger.info("Testing async function")
    await asyncio.sleep(0.1)  # Simulate some work
    return "async_result"


@debug_timer
def test_sync_function():
    """Test sync function with debug timing"""
    logger = get_logger("test")
    logger.info("Testing sync function")
    import time
    time.sleep(0.05)  # Simulate some work
    return "sync_result"


async def main():
    """Main test function"""
    # Initialize logging
    app_logger = setup_logging()
    app_logger.info("Starting logging test")
    
    # Get module-specific logger
    test_logger = get_logger("test")
    
    # Test different log levels
    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message")
    test_logger.warning("This is a warning message")
    test_logger.error("This is an error message")
    
    # Test structured logging with extra data
    test_logger.info("Testing structured logging", extra={
        "user_id": "test_user_123",
        "operation": "test_logging",
        "custom_data": {"key": "value"}
    })
    
    # Test debug utilities
    debug_vars(test_var="test_value", another_var=42)
    
    # Test debug context
    with DebugContext("test_context"):
        test_logger.info("Inside debug context")
        import time
        time.sleep(0.02)
    
    # Test debug timer decorators
    async_result = await test_async_function()
    sync_result = test_sync_function()
    
    test_logger.info("Function results", extra={
        "async_result": async_result,
        "sync_result": sync_result
    })
    
    # Test exception logging
    try:
        raise ValueError("This is a test exception")
    except Exception as e:
        test_logger.error("Caught test exception", exc_info=True)
    
    app_logger.info("Logging test completed successfully")
    print("\nLogging test completed!")
    print("Go to 'logs/' directory for log files:")
    print("   - logs/app.log (all logs)")
    print("   - logs/errors.log (errors only)")
    print("   - logs/debug.log (debug logs, only in debug mode)")


if __name__ == "__main__":
    asyncio.run(main())

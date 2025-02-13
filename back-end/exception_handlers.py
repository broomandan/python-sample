import logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
import traceback

logger = logging.getLogger(__name__)

# Custom exception handler for 404 errors
async def not_found(request: Request, exc: HTTPException):
    logger.error(f"404 Not Found: {request.url}")
    return HTMLResponse(content="Page not found.", status_code=404)

# Custom exception handler for HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Custom exception handler for RequestValidationError
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Request Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()},
    )

# Middleware for uncaught exceptions
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"Unhandled Exception: {str(exc)}")
        traceback.print_exc()  # Print the full traceback for debugging
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"},
        )
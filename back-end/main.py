import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from coins_routes import router as api_router
from exception_handlers import (
    not_found,
    http_exception_handler,
    validation_exception_handler,
    catch_exceptions_middleware,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

api = FastAPI(title="Crypto pricing API using FastAPI", description="Crypto pricing API, returns list of crypto assets, returns detail of an asset")

api.include_router(api_router)

# Register custom exception handlers
api.add_exception_handler(404, not_found)
api.add_exception_handler(HTTPException, http_exception_handler)
api.add_exception_handler(RequestValidationError, validation_exception_handler)

# Register middleware for uncaught exceptions
api.middleware("http")(catch_exceptions_middleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8080, reload=True)
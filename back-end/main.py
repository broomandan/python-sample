import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from routers.coins import router as api_router
from exception_handlers import (
    not_found,
    http_exception_handler,
    validation_exception_handler,
    catch_exceptions_middleware,
)
from security import get_api_key, APIKey

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler("api.log", maxBytes=1000000, backupCount=3)  # Add RotatingFileHandler
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

@api.get("/secure-data")
async def secure_data(api_key: APIKey = Depends(get_api_key)):
    return {"message": "This is a secure endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8080, reload=True)
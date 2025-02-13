
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from coins_routes import router as api_router

api = FastAPI(title="Crypto pricing API using FastAPI", description="Crypto pricing API, returns list of crypto assets, returns detail of an asset")

api.include_router(api_router)
@api.exception_handler(404)
async def not_found(request, exc):
    return HTMLResponse(content="Page not found.", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8080, reload=True)
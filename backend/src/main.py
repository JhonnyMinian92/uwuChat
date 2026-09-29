from fastapi import FastAPI
from src.adapters.inbound.rest.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="uwuChat API",
        description="Multi-tenant customer service platform backend",
        version="0.1.0",
    )

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "Welcome to uwuChat API"}

    return app

app = create_app()

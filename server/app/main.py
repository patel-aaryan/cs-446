from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.routers import health, auth

settings = get_settings()

app = FastAPI(
    title="Memento API",
    description="FastAPI server with Neon database backend",
    version="1.0.0",
    debug=settings.debug,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Add security requirement to protected endpoints
    # Find the /auth/me endpoint and add security requirement
    if "paths" in openapi_schema:
        if "/auth/me" in openapi_schema["paths"]:
            if "get" in openapi_schema["paths"]["/auth/me"]:
                openapi_schema["paths"]["/auth/me"]["get"]["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Memento API"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import (
    upload,
    review,
    regenerate,
    export,
    pricing,
    dashboard,
    health,
)

app = FastAPI(
    title="SmartRFP API",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(review.router)
app.include_router(regenerate.router)
app.include_router(export.router)
app.include_router(pricing.router)
app.include_router(dashboard.router)
app.include_router(health.router)
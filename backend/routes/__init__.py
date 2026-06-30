from fastapi import APIRouter

from .upload import router as upload_router
from .dashboard import router as dashboard_router
from .pricing import router as pricing_router
from .review import router as review_router
from .export import router as export_router
from .health import router as health_router
from .regenerate import router as regenerate_router
router = APIRouter()

router.include_router(upload_router, tags=["Upload"])
router.include_router(dashboard_router, tags=["Dashboard"])
router.include_router(pricing_router, tags=["Pricing"])
router.include_router(review_router, tags=["Review"])
router.include_router(export_router, tags=["Export"])
router.include_router(health_router, tags=["Health"])
router.include_router(
    regenerate_router,
    tags=["Regenerate"]
)
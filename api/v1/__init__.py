from fastapi import APIRouter
from .endpoint import home
from .endpoint import pipeline

router = APIRouter()

router.include_router(home.router, prefix="/home")
router.include_router(pipeline.router, prefix="/pipeline")
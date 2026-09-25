
from fastapi import APIRouter

from app.modules.health import service
from app.modules.health.schema import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return service.get_status()


from app.modules.health.schema import HealthResponse


def get_status() -> HealthResponse:
    return HealthResponse(status="ok")

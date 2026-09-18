from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.dependencies import get_db
from app.modules.users import service
from app.modules.users.schemas import UsersRequest, UsersResponse

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post(
    "/",
    response_model=UsersResponse,
    status_code=status.HTTP_201_CREATED
)
def users(
    req: UsersRequest,
    db: Session = Depends(get_db)
):
    user = service.create_user(req, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    return user

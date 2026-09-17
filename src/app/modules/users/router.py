from fastapi import APIRouter, HTTPException, Depends, status

from app.modules.users import service
from app.modules.users.schemas import UsersRequest, UsersResponse

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/", response_model=UsersRequest, status_code=201)
def users(req: UsersResponse):
    return service.get_users(req)
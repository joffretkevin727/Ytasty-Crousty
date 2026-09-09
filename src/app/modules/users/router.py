from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field

from app.modules.users import service

users_router = APIRouter(prefix="/users", tags=["Users"])

class UsersRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role: str = Field(..., pattern="^(admin|staff|direction)$")
    restaurant_id: int

class UsersResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    role: str = Field(..., pattern="^(admin|staff|direction)$")
    restaurant_id: int

@users_router.post("/", response_model=UsersRequest, status_code=201)
def users(req: UsersResponse):
    return service.get_users(req)
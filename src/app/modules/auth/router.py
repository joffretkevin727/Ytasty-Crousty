from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from app.modules.auth import service
from app.modules.auth.repository import LoginRequest, LoginResponse

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/post", response_model=LoginRequest, status_code=201)
def auth(req: LoginResponse):
    result = service.auth(req.username, req.password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        ) 
    return result
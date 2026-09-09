from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from app.modules.auth import service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    access_token: str
    token_type: str

@auth_router.post("/post", response_model=RegisterResponse, status_code=201)
def auth(req: RegisterRequest):
    return service.auth(req.username, req.password)
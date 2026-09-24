from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.common.dependencies import get_db

from app.modules.auth import service
from app.modules.auth.schemas import LoginRequest, LoginResponse

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=LoginResponse, status_code=201)
def auth(req: LoginRequest, db: Session = Depends(get_db)):
    result = service.auth(req, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        ) 
    return result
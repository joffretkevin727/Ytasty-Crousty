from fastapi import FastAPI

from src.app.modules.users.router import users_router
from src.app.modules.auth.router import auth_router 
from app.modules.health.router import router as health_router
from app.modules.restaurant.router import restaurant_router

app = FastAPI(title="Toasty-Crousty")

app.include_router(health_router)
app.include_router(auth_router) 

app.include_router(users_router)  

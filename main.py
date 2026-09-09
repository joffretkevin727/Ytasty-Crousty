from fastapi import FastAPI

from src.app.modules.auth.router import auth_router
from src.app.modules.users.router import users_router

app = FastAPI(title="Toasty-Crousty")

app.include_router(auth_router)  
app.include_router(users_router)  

@app.get("/health")
def root():
    return {"status": "ok"}
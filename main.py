from fastapi import FastAPI

from src.app.modules.users.router import users_router

app = FastAPI(title="Toasty-Crousty")

app.include_router(users_router)  

@app.get("/health")
def root():
    return {"status": "ok"}
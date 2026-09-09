from fastapi import FastAPI

from src.app.modules.auth.router import auth_router

app = FastAPI(title="Toasty-Crousty")

app.include_router(auth_router)  

@app.get("/health")
def root():
    return {"status": "ok"}
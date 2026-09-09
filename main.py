from fastapi import FastAPI
from src.app.modules.auth.router import auth_router 
from app.modules.health.router import router as health_router

app = FastAPI(title="Toasty-Crousty")
app.include_router(health_router)
app.include_router(auth_router) 


print("L'API est en cours d'exécution sur http://localhost:8000")
print("Pour vérifier l'état de l'API, accédez à http://localhost:8000/health")
print("Pour accéder à la documentation interactive de l'API, accédez à http://localhost:8000/docs")


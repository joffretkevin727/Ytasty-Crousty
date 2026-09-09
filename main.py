from fastapi import FastAPI

app = FastAPI(title="Ytasty-Crousty")

print("test")

@app.get("/health")
def root():
    return {"status": "ok"}
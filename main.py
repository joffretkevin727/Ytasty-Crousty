from fastapi import FastAPI

app = FastAPI(title="Toasty-Crousty")

print("test")

@app.get("/health")
def root():
    return {"status": "ok"}
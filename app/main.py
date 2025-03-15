from fastapi import FastAPI # type: ignore
from app.routes import upload, ask

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Server running!"}

# Include routers
app.include_router(upload.router)
app.include_router(ask.router)

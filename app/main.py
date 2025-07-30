from fastapi import FastAPI
from app.routes import url, auth  # (we'll create these soon)

app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(url.router, prefix="/url", tags=["url"])

@app.get("/")
def root():
    return {"message": "Welcome to the DevOps-Powered URL Shortener"}

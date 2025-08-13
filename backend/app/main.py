from fastapi import FastAPI
from app.api.users import router as users_router

app = FastAPI(
    title="Billboard Watch API",
    description="API for detecting, reporting, and managing unauthorized billboards.",
    version="1.0.0"
)

app.include_router(users_router, prefix="/api/v1", tags=["Users"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "Welcome to the Billboard Watch API!"}
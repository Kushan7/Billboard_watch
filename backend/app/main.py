from fastapi import FastAPI
from app.api.users import router as users_router
from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.login import router as login_router # Add this import

app = FastAPI(
    title="Billboard Watch API",
    # ...
)

app.include_router(users_router, prefix="/api/v1", tags=["Users"])
app.include_router(login_router, prefix="/api/v1", tags=["Login"]) # Add this line


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
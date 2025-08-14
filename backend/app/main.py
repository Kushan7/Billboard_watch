from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.login import router as login_router
from app.api.reports import router as reports_router # Add this import

app = FastAPI(
    title="Billboard Watch API",
    description="API for detecting, reporting, and managing unauthorized billboards.",
    version="1.0.0"
)

# Include all routers
app.include_router(users_router, prefix="/api/v1", tags=["Users"])
app.include_router(login_router, prefix="/api/v1", tags=["Login"])
app.include_router(reports_router, prefix="/api/v1", tags=["Reports"]) # Add this line

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "Welcome to the Billboard Watch API!"}
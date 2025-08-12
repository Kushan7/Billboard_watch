from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI(
    title="Billboard Watch API",
    description="API for detecting, reporting, and managing unauthorized billboards.",
    version="1.0.0"
)

# Define a root endpoint for health checks
@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "Welcome to the Billboard Watch API!"}
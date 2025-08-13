import os
from dotenv import load_dotenv

# This line loads the .env file from your 'backend' directory
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PROJECT_NAME: str = "Billboard Watch"
    API_V1_STR: str = "/api/v1"

settings = Settings()
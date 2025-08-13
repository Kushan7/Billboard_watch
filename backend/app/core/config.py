import os
from dotenv import load_dotenv

# This line loads the .env file from your 'backend' directory
load_dotenv()

# In config.py
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PROJECT_NAME: str = "Billboard Watch"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY") # Add this
    ALGORITHM: str = os.getenv("ALGORITHM") # Add this
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) # Add this

settings = Settings()
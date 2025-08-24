# Step 1: Use an official lightweight Python image as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Set environment variables
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Step 4: Copy the requirements file and install dependencies
# This is done in a separate step to leverage Docker's layer caching.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Step 5: Copy the rest of the application code into the container
# This includes your 'app' folder, 'alembic', 'gis_data', etc.
COPY . .

# Step 6: Expose the port the app runs on
EXPOSE 8000

# Step 7: Define the command to run your app
# Use uvicorn to run the FastAPI app. Host 0.0.0.0 makes it accessible
# from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
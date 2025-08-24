# Billboard Watch - System Architecture

This project is built on a classic **Client-Server architecture** designed for scalability, security, and separation of concerns. The system is composed of three main layers: the Client, the Backend Server, and the Data/Services layer.

---
## 1. Client Layer (Mobile App)

The client is a cross-platform mobile application responsible for user interaction and data capture.

* **Framework**: React Native or Flutter
* **Responsibilities**:
    * **User Interface**: Provides screens for user registration, login, and submitting a new billboard report.
    * **Data Capture**: Uses the device's camera to capture an image and the GPS to get the current latitude and longitude.
    * **API Communication**:
        * Makes secure HTTPS requests to the Backend API.
        * Manages the **JWT (JSON Web Token)** for authenticating protected requests.

---
## 2. Backend Layer (FastAPI Server)

The backend is the core engine of the application, handling all business logic, data processing, and AI analysis.

* **Framework**: Python 3 with **FastAPI**
* **Hosting**: Designed to be containerized with **Docker** and deployed on a cloud service (e.g., AWS, GCP).
* **Components**:
    * **API Routers**:
        * `/users`: Public endpoint for user registration.
        * `/login`: Public endpoint for user authentication and issuing JWT access tokens.
        * `/reports`: **Protected endpoint** that requires a valid JWT to accept new billboard reports.
    * **Core Services (Business Logic)**:
        * **Authentication Service**: Manages user creation, password hashing (`passlib`), and JWT generation/validation (`python-jose`).
        * **Report Service**: Handles the logic for creating report records, saving images, and triggering the analysis pipeline.
        * **Analysis Service (The "Smart" Pipeline)**:
            * **OCR Module**: Integrates with **Google Cloud Vision API** to perform text extraction.
            * **NLP Module**: Uses a **Hugging Face Transformers** model to analyze extracted text for content violations.
            * **GIS Module**: Uses the **Shapely** library to perform geofencing checks against a GeoJSON file of "No Hoarding Zones".
            * **(Bypassed) Object Detection Module**: Designed for a custom-trained **YOLOv8** model to detect billboards.

---
## 3. Data & External Services Layer

This layer includes the database, file storage, and all third-party services the backend relies on.

* **Primary Database**:
    * **PostgreSQL**: A robust relational database for storing all persistent data (`users`, `reports`, `images` tables).
    * **Alembic**: Used for managing all database schema migrations.
* **Image Storage**:
    * **Local File System (`uploaded_images/`)**: For the prototype, images are stored on the server's local disk.
* **Third-Party APIs**:
    * **Google Cloud Platform**: Provides the Vision AI service for OCR.
    * **Hugging Face Hub**: Provides the pre-trained NLP model for text analysis.

---
## ## Data Flow for a New Report

1.  A **logged-in user** on the mobile app takes a picture of a billboard.
2.  The app captures the **image** and the phone's **GPS coordinates**.
3.  The app makes a `POST` request to the `/api/v1/reports/` endpoint, sending the image and coordinates. The **JWT access token** is included in the request header.
4.  The FastAPI backend receives the request. The **Auth dependency** validates the JWT token, confirming the user is authenticated.
5.  The **Report Service** creates a new record in the `reports` table in **PostgreSQL** and saves the image to the server's file system.
6.  The service immediately runs the **Analysis Pipeline**:
    * It sends the image to the **Google Cloud Vision API** for OCR.
    * It runs the extracted text through the **Transformers NLP model**.
    * It checks the report's coordinates with the **GIS Module**.
7.  The analysis results are saved to the `violation_details` column of the report in the database.
8.  A `201 Created` response, including the report details and the full analysis results, is sent back to the user's app.
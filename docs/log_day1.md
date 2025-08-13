## Yesterday’s Log: Building the Foundation

Our first session was all about laying the groundwork for the backend. We set up the entire project structure and all the core components needed to support our application.

    Project and Code Structure

        Established the main project folders: backend, mobile_app, and docs.

        Set up the backend with a logical structure, creating directories like app, api, core, db, and services.

    Initial Server and Database Code

        Wrote the first version of our FastAPI app in main.py.

        Defined all our database tables (User, Report, Image, etc.) as Python classes in db/models.py.

        Created the requirements.txt file to list all our Python dependencies like fastapi, sqlalchemy, and psycopg2.

    Database Configuration and Migrations

        Set up a secure configuration by creating the .env file to hold our secret DATABASE_URL.

        Wrote the core/config.py file to load these secrets into the application.

        Created the db/database.py file to manage the connection to our PostgreSQL database.

        Initialized Alembic, our database migration tool, to prepare for creating the tables.
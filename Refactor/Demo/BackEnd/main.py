from fastapi import FastAPI
from api.routes import books
from infra.database.db_connection import create_database

app = FastAPI()

# Include API routes
app.include_router(books.router)

# Initialize database
create_database()

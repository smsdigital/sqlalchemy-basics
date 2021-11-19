# Get environment variables for creating database engine
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import metadata

user_name = os.getenv("DB_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")

# Specify engine driver, username, password, host and a database port
engine = create_engine(
    f"postgresql+psycopg2://{user_name}:{password}@localhost:5432",
    echo=True, # Magic spell to print engine's SQL queries to stdout, you don't always need this
)

metadata.create_all(engine)
session_factory = sessionmaker(bind=engine())


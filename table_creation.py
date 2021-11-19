import os
from datetime import datetime

from sqlalchemy import (
    MetaData,
    Integer,
    String,
    Column,
    create_engine,
    insert,
    select,
    Date, update, delete, text
)
from sqlalchemy.testing.schema import Table

# Get environment variables for creating database engine
user_name = os.getenv("DB_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")

# Specify engine driver, username, password, host and a database port
engine = create_engine(
    f"postgresql+psycopg2://{user_name}:{password}@localhost:5432",
    echo=True, # Magic spell to print engine's SQL queries to stdout, you don't always need this
)

# metadata is a container object that will keep our table
metadata_obj = MetaData()

# Let's define a table using SQLAlchemy Core
table = Table(
    'some_table',  # table name in the database
    metadata_obj,  # bind table to metadata object
    Column('id', Integer, primary_key=True),  # and
    Column('name', String(100), nullable=False),  # some
    Column('birth_date', Date, nullable=True),  # columns
    schema="public"
)

# create all tables bound to a metadata container object using a database engine
metadata_obj.create_all(engine)

# Let's select rows from a table.
# Option #1: raw SQL execution

# create a connection using database engine
connection = engine.connect()
# Create a raw text SQL query.
# If you happen to rename the table, you may overlook to update the query :(
statement = text("""select * from some_table""")
# execute a statement, get a Result object
result = connection.execute(statement)
# get actual Rows as a list from the Result
print("Empty table:", result.fetchall())
# Close the connection explicitly, don't leave it hanging :(
connection.close()


# Option #2: use SQLAlchemy Core statements
def select_all(table: Table) -> list:
    """Select all entries from the specified SQLAlchemy table"""

    # Basic select statement applied to a table will return all its columns.
    # No explicit table name mentioned, just a table object, yay!
    statement = select(table)

    # Use a context manager (with- statement) so connection is auto-closed in the end 🦾
    with engine.connect() as connection:
        # The rest is the same as in option #1
        return connection.execute(statement).fetchall()


print("Yup, still no rows:", select_all(table))

# Create a statement inserting a single record
stmt = insert(table).values(
    name="Spongebob Squarepants",
    birth_date=datetime.now().date()
)
# Execute it
with engine.connect() as conn:
    conn.execute(stmt)

# Select to make sure data exists
print("Look, it's SpongeBob!", select_all(table))

# Inserting multiple records using bulk insert
with engine.connect() as conn:
    conn.execute(
        insert(table),
        [
            {"name": "Sandy Cheeks", "birth_date": datetime.now()},
            {"name": "Patrick", "birth_date": datetime.now()}
        ]
    )

# Select to make sure more data added
print("Characters:", select_all(table))

# Update a record, change a character's name
stmt = update(table).where(table.c.name == "Patrick").values(name="Patrick Star")
with engine.connect() as conn:
    conn.execute(stmt)

# Select to make sure more data added
print("Pay attention to Patrick:", select_all(table))

# Delete records
stmt = delete(table).where(table.c.name == "Patrick Star")
with engine.connect() as conn:
    conn.execute(stmt)

# Select to make sure more data added
print("No Patrick:", select_all(table))

# drop table after work
table.drop(engine)

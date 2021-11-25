from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata

SCHEMA_NAME = "public"

_default_true = text("True")
_default_timestamp = text("CURRENT_TIMESTAMP")


# Define a table in a declarative way
class Users(Base):
    """Defines the users with all parameters to authenticate them."""

    __tablename__ = "users"
    __table_args__ = {
        "schema": SCHEMA_NAME,
        "comment": "Users of our app"
    }

    id = Column(
        Integer(),
        primary_key=True,
        unique=True,
        autoincrement=True,
        comment="Unique identifier for the user. Also known as user id.",
    )
    username = Column(
        String(length=64),
        nullable=False,
        index=True,
        comment="The namely identifier of the user.",
    )
    # a user can have a job, therefore can reference it
    job_id = Column(
        ForeignKey(
            f"{SCHEMA_NAME}.jobs.id",  # job table primary key column
            name=f"fk_{SCHEMA_NAME.lower()}_user_job",  # use standard foreign key naming convention
        ),
    )


# This what is called an "association table".
# It's the linking table for Jobs <--M2M--> Companies.
# We'll define Jobs and Companies right after it.
class CompanyToJobs(Base):
    __tablename__ = "jobs_to_companies"
    id = Column(
        Integer(),
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    # Association table should refer to both tables of the ManyToMany relationship.
    company_id = Column(
        ForeignKey(
            f"{SCHEMA_NAME}.companies.id",
            name=f"fk_{SCHEMA_NAME.lower()}_company",
        ),
    )
    job_id = Column(
        ForeignKey(
            f"{SCHEMA_NAME}.jobs.id",
            name=f"fk_{SCHEMA_NAME.lower()}_job",
        ),
    )


class Jobs(Base):
    __tablename__ = "jobs"
    __table_args__ = {
        "schema": SCHEMA_NAME,
    }
    id = Column(
        Integer(),
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    name = Column(String(100), unique=True, index=True, nullable=False)

    # Refer companies that have this job using an associated table above.
    companies = relationship("Companies", secondary=CompanyToJobs.__table__, back_populates="jobs")
    # Having this line above, later you can write smth like
    # my_favorite_job.companies
    # and see which companies have this job!

    # ... or you write it like on the commented line below and then
    # you don't need to declare similar stuff in the Companies table.
    # Pay attention to the back_ref part:
    # companies = relationship("Companies", secondary=CompanyToJobs.__table__, back_ref="jobs")

    # We can fetch users who have this job based on the foreign key defined in the Users table
    users = relationship("Users", backref="job")


class Companies(Base):
    __tablename__ = "companies"
    __table_args__ = {
        "schema": SCHEMA_NAME,
    }

    id = Column(
        Integer(),
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    name = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    # second part of the Jobs <--M2M--> Companies
    jobs = relationship("Jobs", secondary=CompanyToJobs.__table__, back_populates="companies")

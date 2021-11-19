from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata

SCHEMA_NAME = "public"

_default_true = text("True")
_default_timestamp = text("CURRENT_TIMESTAMP")


class Users(Base):
    """Defines the users with all parameters to authenticate them."""

    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA_NAME, "comment": "Users of our app"}

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
    job_id = Column(
        ForeignKey(
            f"{SCHEMA_NAME}.jobs.id",
            name=f"fk_{SCHEMA_NAME.lower()}_user_job",
        ),
    )


class CompanyToJobs(Base):
    __tablename__ = "jobs_in_companies"
    id = Column(
        Integer(),
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    company = Column(
        ForeignKey(
            f"{SCHEMA_NAME}.companies.id",
            name=f"fk_{SCHEMA_NAME.lower()}_company",
        ),
    )
    job = Column(
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
    company = relationship("Companies", secondary=CompanyToJobs.__table__)
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
    name = Column(String(100), unique=True, index=True, nullable=False)

    job = relationship("Jobs", secondary=CompanyToJobs.__table__)

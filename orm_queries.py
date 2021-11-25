from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker, Session

from engine import engine
from models import metadata, Users, Jobs, Companies, CompanyToJobs

# Create all tables defined in 'models.py'
metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)


def select_all(session: Session, table: type(Table)) -> list:
    """Select all entries from the specified SQLAlchemy table"""
    return session.query(table).all()


with session_factory() as session:
    print(
        "All tables are empty: ",
        select_all(session, Users),
        select_all(session, Jobs),
        select_all(session, Companies),
        select_all(session, CompanyToJobs),
    )

# Add some jobs one by one
with session_factory() as session:
    session.add(Jobs(name="Programmer"))
    session.add(Jobs(name="Manager"))
    session.add(Jobs(name="CEO"))
    session.commit()  # Deliver transaction to DB, records now available

# Add companies by a list
with session_factory() as session:
    new_companies = [
        Companies(name="Digital"),
        Companies(name="Gruppe"),
        Companies(name="SMS"),
    ]
    session.bulk_save_objects(new_companies)
    session.commit()

# Add many-to-many table to match Companies with available Jobs
with session_factory() as session:
    #  fetch ids
    digital_id = (
        session.query(Companies.id).filter(Companies.name == "Digital").scalar()
    )
    gruppe_id = session.query(Companies.id).filter(Companies.name == "Gruppe").scalar()
    sms_id = session.query(Companies.id).filter(Companies.name == "SMS").scalar()

    programmer_id = session.query(Jobs.id).filter(Jobs.name == "Programmer").scalar()
    manager_id = session.query(Jobs.id).filter(Jobs.name == "Manager").scalar()
    ceo_id = session.query(Jobs.id).filter(Jobs.name == "CEO").scalar()

    # Add records
    session.add(CompanyToJobs(company_id=digital_id, job_id=ceo_id))
    session.add(CompanyToJobs(company_id=digital_id, job_id=programmer_id))

    session.add(CompanyToJobs(company_id=gruppe_id, job_id=manager_id))
    session.add(CompanyToJobs(company_id=gruppe_id, job_id=programmer_id))

    session.add(CompanyToJobs(company_id=sms_id, job_id=manager_id))
    session.add(CompanyToJobs(company_id=sms_id, job_id=ceo_id))

    session.commit()
with session_factory() as session:
    companies = select_all(session, Companies)
    company_to_jobs = {
        company.name: [job.name for job in company.jobs] for company in companies
    }
    print("Companies have following jobs:", company_to_jobs)


# Add Users
with session_factory() as session:

    programmer_id = session.query(Jobs.id).filter(Jobs.name == "Programmer").scalar()
    manager_id = session.query(Jobs.id).filter(Jobs.name == "Manager").scalar()

    session.add(Users(username="admin", job_id=programmer_id))
    session.add(Users(username="worker", job_id=programmer_id))
    session.add(Users(username="reader", job_id=manager_id))
    session.commit()  # Deliver transaction to DB, records now available

# Update users
with session_factory() as session:
    ceo_id = session.query(Jobs.id).filter(Jobs.name == "CEO").scalar()
    reader = session.query(Users).filter(Users.username == "reader").first()
    reader.job_id = ceo_id
    session.flush()  # now in session user have new job, but not in DB yet

    admin = session.query(Users).filter(Users.username == "admin").first()
    admin.username = "Administrator"
    session.merge(
        admin
    )  #  merge will create new record, or update existing if PK present
    session.commit()

# Delete Job
with session_factory() as session:
    programmer = session.query(Jobs).filter(Jobs.name == "Programmer").first()
    session.delete(programmer)
    session.commit()

metadata.drop_all(engine)

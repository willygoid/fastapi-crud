from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite default connection
DATABASE_URL = "sqlite:///./siveno.db"

# Set up a switch for MySQL if needed
# For MySQL: "mysql+pymysql://user:password@localhost/dbname"
# DATABASE_URL = "mysql+pymysql://root:password@localhost/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

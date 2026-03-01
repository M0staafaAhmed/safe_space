from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# الرابط الجديد اللي أنت بعته
URL_DATABASE = "mysql+pymysql://avnadmin:AVNS_PQXhaPTA18ColZlJn00@safe-space-saffe-space.j.aivencloud.com:10399/defaultdb"

# إضافة connect_args عشان الـ SSL
engine = create_engine(
    URL_DATABASE, 
    connect_args={"ssl": {"ca": None}} # Aiven بيقبل الاتصال المشفر كده مع sqlalchemy
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()                  
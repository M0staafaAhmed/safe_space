from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Username = Column(String(50), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Password = Column(String(255), nullable=False) # هنخزن الباسوورد هنا
    
class Doctor(Base):
    __tablename__ = 'doctors'
    DoctorID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Specialty = Column(String(100))
    ImageUrl = Column(String(500))

class TestType(Base):
    __tablename__ = 'testtypes'
    TestTypeID = Column(Integer, primary_key=True, index=True)
    TestName = Column(String(100))
    Description = Column(String(300))

class TestResult(Base):
    __tablename__ = 'testresults'
    TestResultID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"))
    DoctorID = Column(Integer, nullable=True)
    TestTypeID = Column(Integer, ForeignKey("testtypes.TestTypeID"))
    ResultValue = Column(String(100))
    ResultDate = Column(DateTime, default=datetime.utcnow)
    Notes = Column(Text)
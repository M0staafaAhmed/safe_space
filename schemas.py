from pydantic import BaseModel
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional, Literal

# شكل البيانات عند حفظ نتيجة اختبار
class TestResultCreate(BaseModel):
    user_id: int
    test_id: int
    score: str
    notes: str
    doctor_id: Optional[int] = 1

# شكل البيانات عند عرض النتيجة (للفلاتر)
class TestResultResponse(BaseModel):
    TestResultID: int
    ResultValue: str
    ResultDate: datetime
    Notes: Optional[str]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    FirstName: str
    LastName: str
    password: str
    Email: EmailStr
    Phone: str
    # هنا بنجبره يختار من الاتنين دول بس، والـ Optional عشان لو مبعتش خالص
    Gender: Literal["male", "female"]
    DateOfBirth: Optional[str] = None
    Address: Optional[str] = None

# بيانات تسجيل الدخول (Login)
class UserLogin(BaseModel):
    Email: EmailStr
    password: str

# الرد اللي هيروح للموبايل بعد النجاح
class UserResponse(BaseModel):
    UserID: int
    FirstName: str
    Email: str

    class Config:
        from_attributes = True
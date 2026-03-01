from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

# استيراد ملفاتنا اللي قسمناها
import models
import schemas
from database import engine, get_db
from auth_utils import create_access_token, verify_token

# إنشاء الجداول في قاعدة البيانات لو مش موجودة
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Safe Space Mental Health API")

# --- 1. تسجيل مستخدم جديد (Signup) ---
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # التأكد إن الإيميل مش موجود قبل كده
    existing_user = db.query(models.User).filter(models.User.Email == user_data.Email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="هذا الإيميل مسجل بالفعل")
    
    new_user = models.User(
        FirstName=user_data.FirstName,
        LastName=user_data.LastName,
        Gender=user_data.Gender,
        DateOfBirth=user_data.DateOfBirth,
        password=user_data.password, # نصيحة: يفضل تشفيرها لاحقاً
        Phone=user_data.Phone,
        Email=user_data.Email,
        Address=user_data.Address
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- 2. تسجيل الدخول واستخراج التوكن (Login) ---
@app.post("/login")
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.Email == login_data.Email,
        models.User.password == login_data.password
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="الإيميل أو كلمة المرور خطأ")
    
    # صنع التوكن لليوزر ده
    access_token = create_access_token(data={"user_id": user.UserID, "email": user.Email})
    
    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.UserID,
            "name": f"{user.FirstName} {user.LastName}"
        }
    }

# --- 3. حفظ نتيجة اختبار (محمي بالتوكن) ---
@app.post("/save_result")
def save_test_result(
    data: schemas.TestResultCreate, 
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token) # لازم يبعت التوكن في الـ Header
):
    # بنجيب الـ UserID من التوكن نفسه عشان نضمن الأمان
    current_user_id = token_data.get("user_id")
    
    new_record = models.TestResult(
        UserID=current_user_id,
        TestTypeID=data.test_id,
        DoctorID=data.doctor_id,
        ResultValue=data.score,
        Notes=data.notes,
        ResultDate=datetime.now()
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"status": "success", "record_id": new_record.TestResultID}

# --- 4. عرض السجل المرضي لليوزر الحالي (محمي بالتوكن) ---
@app.get("/my_history", response_model=List[schemas.TestResultResponse])
def get_my_history(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    current_user_id = token_data.get("user_id")
    results = db.query(models.TestResult).filter(models.TestResult.UserID == current_user_id).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="لا يوجد سجلات لهذا المستخدم")
    return results

# --- 5. عرض قائمة الدكاترة ---
@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

# --- 2. عرض كل أنواع الاختبارات ---
@app.get("/tests")
def read_tests(db: Session = Depends(get_db)):
    return db.query(models.TestType).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
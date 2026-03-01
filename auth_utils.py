import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header

SECRET_KEY = "mesa men dakhel elbackend" # سر خاص بيك ماحدش يعرفه
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    # التوكن هيخلص صلاحيته بعد 24 ساعة
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Token missing")
    
    try:
        # بنشيل كلمة "Bearer " من أول التوكن
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # بيرجع الـ data اللي جوه التوكن (user_id, email)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
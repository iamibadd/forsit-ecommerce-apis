from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(
        tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

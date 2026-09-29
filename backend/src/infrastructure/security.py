import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    SECRET_KEY: str = "super-secret-jwt-key-change-in-production-uwuchat"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

security_settings = SecuritySettings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], enterprise_id: Union[str, Any], role: str, expires_delta: Union[timedelta, None] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=security_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(subject),
        "enterprise_id": str(enterprise_id),
        "role": role,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, security_settings.SECRET_KEY, algorithm=security_settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, security_settings.SECRET_KEY, algorithms=[security_settings.ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        raise ValueError("Could not validate credentials") from e

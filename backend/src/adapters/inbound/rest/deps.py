import uuid
from typing import AsyncGenerator, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import AsyncSessionLocal
from src.infrastructure.models.domain import User, UserRole
from src.infrastructure.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = uuid.UUID(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception
        
    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: UserRole) -> Callable:
    role_hierarchy = {
        UserRole.AGENT: 1,
        UserRole.SUPERVISOR: 2,
        UserRole.ADMIN: 3
    }
    
    async def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        user_level = role_hierarchy.get(current_user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this role"
            )
        return current_user
        
    return role_dependency

import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.main import create_app
from src.infrastructure.models.base import Base
from src.infrastructure.models.domain import Enterprise, User, UserRole
from src.infrastructure.security import get_password_hash, create_access_token
from src.adapters.inbound.rest.deps import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session

app = create_app()
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.anyio
async def test_login_and_me():
    async with TestingSessionLocal() as session:
        ent = Enterprise(id=uuid.uuid4(), name="Test Corp", plan="pro")
        session.add(ent)
        await session.commit()
        
        user = User(
            id=uuid.uuid4(),
            enterprise_id=ent.id,
            email="agent@test.com",
            hashed_password=get_password_hash("secret123"),
            full_name="Test Agent",
            role=UserRole.AGENT
        )
        session.add(user)
        await session.commit()

    response = client.post("/api/v1/auth/login", json={"email": "agent@test.com", "password": "secret123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]

    res_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    me_data = res_me.json()
    assert me_data["email"] == "agent@test.com"
    assert me_data["role"] == "agent"

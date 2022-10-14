#  Copyright 2022 Pavel Suprunov
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest

from datetime import datetime, timezone
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine
)
from sqlalchemy.orm import sessionmaker

from app.core.settings.app import AppSettings
from app.database.repositories import UsersRepository
from app.database.repositories.api_keys import ApiKeysRepository
from app.database.repositories.vehicles import VehiclesRepository
from app.models.domain.api_key import ApiKey
from app.models.domain.user import User
from app.models.domain.vehicle import Vehicle
from app.services import jwt


@pytest.fixture
def settings() -> AppSettings:
    from app.core.config import get_app_settings

    return get_app_settings()


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
async def engine(settings: AppSettings) -> AsyncEngine:
    engine = create_async_engine(settings.get_database_url)

    return engine


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncSession:
    connection = await engine.connect()
    transaction = await connection.begin()

    async_session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = async_session()

    try:
        yield session

    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()


@pytest.fixture
async def initialized_app(app: FastAPI, session: AsyncSession) -> FastAPI:
    app.state.session = session

    return app


@pytest.fixture
async def api_key(session: AsyncSession) -> str:
    api_keys_repo = ApiKeysRepository(session)

    api_key: ApiKey = await api_keys_repo.create_key("Temp key for tests")

    return api_key.key


@pytest.fixture
async def client(app: FastAPI, api_key: str) -> AsyncClient:
    async with AsyncClient(
            app=app,
            base_url="http://localhost:10000",
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": api_key
            },
    ) as client:
        yield client


@pytest.fixture
async def test_user(session: AsyncSession) -> User:
    users_repo = UsersRepository(session)

    user: User = await users_repo.create_user(
        username="username",
        phone="+375257654321",
        password="password",
    )

    return user


@pytest.fixture
def authorization_prefix(settings: AppSettings) -> str:
    jwt_token_prefix = settings.jwt_token_prefix

    return jwt_token_prefix


@pytest.fixture
def token(test_user: User) -> str:
    return jwt.create_access_token_for_user(
        user_id=test_user.id,
        username=test_user.username,
        phone=test_user.phone,
        secret_key="secret_key"
    )


@pytest.fixture
def authorized_client(client: AsyncClient, authorization_prefix: str, token: str) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }
    return client


# @pytest.fixture
# async def test_profile(test_user: User, session: AsyncSession) -> Profile:
#     profiles_repo = ProfilesRepository(session)
#
#     return await profiles_repo.create_profile_by_user_id(
#         test_user.id,
#     )


@pytest.fixture
async def test_location(session: AsyncSession) -> Location:
    locations_repo = LocationsRepository(session)

    return await locations_repo.create_location(
        description="Test location",
        latitude=1.234,
        longitude=5.678,
    )


@pytest.fixture
async def test_post(test_user: User, session: AsyncSession) -> Post:
    posts_repo = PostsRepository(session)

    return await posts_repo.create_post_by_user_id(
        test_user.id,
        title="Test post",
        description="Slug for tests",
        thumbnail="",
        body="Test " * 100,
    )


@pytest.fixture
async def test_event(session: AsyncSession, test_user: User, test_location: Location) -> Event:
    events_repo = EventsRepository(session)

    return await events_repo.create_event_by_user_id(
        test_user.id,
        title="Test event",
        description="Test event",
        thumbnail="",
        body="Test " * 100,
        started_at=datetime.now().replace(tzinfo=timezone.utc),
        location=test_location
    )


@pytest.fixture
async def test_vehicle(session: AsyncSession, test_user: User) -> Vehicle:
    vehicles_repo = VehiclesRepository(session)

    return await vehicles_repo.create_vehicle_by_user_id(
        test_user.id,
        brand="honda",
        model="xl1000v",
        gen=3,
        year=2008,
        color="Silver",
        mileage=65500,
        vin="JVM01234567891011",
        registration_plate="9112AB2",
        name="Bullfinch",
    )


@pytest.fixture
async def test_service_type(session: AsyncSession) -> ServiceType:
    services_types_repo = ServicesTypesRepository(session)

    return await services_types_repo.create_service_type("Test service", "Test service in description")

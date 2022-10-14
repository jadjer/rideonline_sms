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

from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.repositories.profiles import ProfilesRepository
from app.database.repositories.users import UsersRepository
from app.models.domain.profile import Profile
from app.models.domain.user import UserInDB, User
from app.models.schemas.user import UserInResponse


@pytest.fixture(params=("", "value", "Token value", "JWT value", "Bearer value"))
def wrong_authorization_header(request) -> str:
    return request.param


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "api_method, route_name",
    (("GET", "users:get-current-user"), ("PUT", "users:update-current-user")),
)
async def test_user_can_not_access_own_profile_if_not_logged_in(
        initialized_app: FastAPI,
        client: AsyncClient,
        test_user: User,
        api_method: str,
        route_name: str,
) -> None:
    response = await client.request(api_method, initialized_app.url_path_for(route_name))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "api_method, route_name",
    (("GET", "users:get-current-user"), ("PUT", "users:update-current-user")),
)
async def test_user_can_not_retrieve_own_profile_if_wrong_token(
        initialized_app: FastAPI,
        client: AsyncClient,
        test_user: User,
        api_method: str,
        route_name: str,
        wrong_authorization_header: str,
) -> None:
    response = await client.request(
        api_method,
        initialized_app.url_path_for(route_name),
        headers={"Authorization": wrong_authorization_header},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_user_can_retrieve_own_profile(
        initialized_app: FastAPI, authorized_client: AsyncClient, test_user: User, token: str
) -> None:
    response = await authorized_client.get(initialized_app.url_path_for("users:get-current-user"))
    assert response.status_code == status.HTTP_200_OK

    user_profile = UserInResponse(**response.json())
    assert user_profile.user.username == test_user.username


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field, update_value",
    (
            ("username", "new_username"),
            ("phone", "+375257654321"),
    ),
)
async def test_user_can_update_own_profile(
        initialized_app: FastAPI,
        authorized_client: AsyncClient,
        test_user: User,
        token: str,
        update_value: str,
        update_field: str,
) -> None:
    response = await authorized_client.put(
        initialized_app.url_path_for("users:update-current-user"),
        json={"user": {update_field: update_value}},
    )
    assert response.status_code == status.HTTP_200_OK

    user_profile = UserInResponse(**response.json()).dict()
    assert user_profile["user"][update_field] == update_value


@pytest.mark.asyncio
async def test_user_can_change_password(
        initialized_app: FastAPI,
        authorized_client: AsyncClient,
        test_user: User,
        session: AsyncSession,
) -> None:
    password = "new_password"

    response = await authorized_client.put(
        initialized_app.url_path_for("users:update-current-user"),
        json={"user": {"password": password}},
    )

    assert response.status_code == status.HTTP_200_OK
    user_profile = UserInResponse(**response.json())

    users_repo = UsersRepository(session)
    user: UserInDB = await users_repo.get_user_by_username(
        username=user_profile.user.username
    )

    assert user.check_password(password)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "credentials_part, credentials_value",
    (
            ("username", "taken_username"),
            ("phone", "+375257654323")
    ),
)
async def test_user_can_not_take_already_used_credentials(
        initialized_app: FastAPI,
        authorized_client: AsyncClient,
        session: AsyncSession,
        credentials_part: str,
        credentials_value: str,
) -> None:
    user_dict = {
        "username": "not_taken_username",
        "password": "password",
        "phone": "+375257654322",
    }
    user_dict.update({credentials_part: credentials_value})
    users_repo = UsersRepository(session)
    await users_repo.create_user(**user_dict)

    response = await authorized_client.put(
        initialized_app.url_path_for("users:update-current-user"),
        json={"user": {credentials_part: credentials_value}},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

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

from app.database.repositories.users import UsersRepository
from app.database.repositories.verification_codes import VerificationRepository
from app.models.domain.user import User


@pytest.mark.asyncio
async def test_user_success_registration(
        initialized_app: FastAPI, client: AsyncClient, session: AsyncSession
) -> None:
    phone = "+375257654321"
    username = "username"
    password = "password"

    verification_repo = VerificationRepository(session)
    verification_code = await verification_repo.create_verification_code_by_phone(phone)

    registration_json = {
        "phone": phone,
        "username": username,
        "password": password,
        "verification_code": verification_code
    }
    response = await client.post(
        initialized_app.url_path_for("auth:register"), json={"user": registration_json}
    )
    assert response.status_code == status.HTTP_201_CREATED

    users_repo = UsersRepository(session)
    user = await users_repo.get_user_by_username(username=username)

    assert user.username == username
    assert user.phone == phone
    assert user.check_password(password)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "credentials_part, credentials_value",
    (
            ("username", "free_username"),
            ("phone", "+375257654322")
    ),
)
async def test_failed_user_registration_when_some_credentials_are_taken(
        initialized_app: FastAPI,
        client: AsyncClient,
        test_user: User,
        session: AsyncSession,
        credentials_part: str,
        credentials_value: str,
) -> None:
    phone = "+375257654321"

    verification_repo = VerificationRepository(session)
    verification_code = await verification_repo.create_verification_code_by_phone(phone)

    registration_json = {
        "user": {
            "phone": phone,
            "username": "username",
            "password": "password",
            "verification_code": verification_code
        }
    }
    registration_json["user"][credentials_part] = credentials_value

    response = await client.post(
        initialized_app.url_path_for("auth:register"), json=registration_json
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

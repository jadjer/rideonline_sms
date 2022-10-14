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

from app.models.domain.user import User


@pytest.mark.asyncio
async def test_user_successful_login(
        initialized_app: FastAPI, client: AsyncClient, test_user: User
) -> None:
    login_json = {"user": {"username": "username", "password": "password"}}

    response = await client.post(initialized_app.url_path_for("auth:login"), json=login_json)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "credentials_part, credentials_value",
    (("email", "wrong@test.com"), ("password", "wrong")),
)
async def test_user_login_when_credential_part_does_not_match(
        initialized_app: FastAPI,
        client: AsyncClient,
        test_user: User,
        credentials_part: str,
        credentials_value: str,
) -> None:
    login_json = {"user": {"username": "test@test.com", "password": "password"}}
    login_json["user"][credentials_part] = credentials_value

    response = await client.post(initialized_app.url_path_for("auth:login"), json=login_json)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

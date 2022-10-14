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

from app.services.jwt import create_access_token_for_user


@pytest.mark.asyncio
async def test_unable_to_login_with_wrong_jwt_prefix(
        initialized_app: FastAPI, client: AsyncClient, token: str
) -> None:
    response = await client.get(
        initialized_app.url_path_for("users:get-current-user"),
        headers={
            "Authorization": f"WrongPrefix {token}"
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_unable_to_login_when_user_does_not_exist_any_more(
        initialized_app: FastAPI, client: AsyncClient, authorization_prefix: str
) -> None:
    token = create_access_token_for_user(
        user_id=9999999999999,
        username="test_user",
        phone="+375123456789",
        secret_key="secret"
    )
    response = await client.get(
        initialized_app.url_path_for("users:get-current-user"),
        headers={
            "Authorization": f"{authorization_prefix} {token}"
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

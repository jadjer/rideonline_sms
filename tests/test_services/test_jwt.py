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

from datetime import timedelta

import jwt
import pytest

from app.models.domain.user import UserInDB
from app.services.jwt import (
    ALGORITHM,
    create_access_token_for_user,
    create_jwt_token,
    get_user_id_from_token,
    get_username_from_token,
    get_phone_from_token,
)


def test_creating_jwt_token() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    parsed_payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])

    assert parsed_payload["content"] == "payload"


def test_creating_token_for_user(test_user: UserInDB) -> None:
    token = create_access_token_for_user(
        user_id=test_user.id,
        username=test_user.username,
        phone=test_user.phone,
        secret_key="secret"
    )
    parsed_payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])

    assert parsed_payload["username"] == test_user.username


def test_retrieving_token_from_user(test_user: UserInDB) -> None:
    token = create_access_token_for_user(
        user_id=test_user.id,
        username=test_user.username,
        phone=test_user.phone,
        secret_key="secret"
    )

    user_id = get_user_id_from_token(token, "secret")
    assert user_id == test_user.id

    username = get_username_from_token(token, "secret")
    assert username == test_user.username

    phone = get_phone_from_token(token, "secret")
    assert phone == test_user.phone


def test_error_when_wrong_token() -> None:
    with pytest.raises(ValueError):
        get_username_from_token("asdf", "asdf")


def test_error_when_wrong_token_shape() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    with pytest.raises(ValueError):
        get_username_from_token(token, "secret")

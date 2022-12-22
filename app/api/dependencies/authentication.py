#  Copyright 2022 Pavel Suprunov
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from loguru import logger
from typing import Callable

from fastapi import Depends, HTTPException, Security, status

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.repositories.user_repository import UserRepository
from app.models.domain.user import UserInDB
from app.resources import strings
from app.services.auth_token_header import AuthTokenHeader
from app.services.token import get_user_id_from_access_token

HEADER_KEY = "Authorization"


def get_current_user_authorizer() -> Callable:
    return _get_current_user


def _get_authorization_header(
        api_key: str = Security(AuthTokenHeader(name=HEADER_KEY)),
        settings: AppSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError as exception:
        logger.error(exception)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.WRONG_TOKEN_PREFIX)

    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.WRONG_TOKEN_PREFIX)

    return token


async def _get_user_id_from_token(
        token: str = Depends(_get_authorization_header),
        settings: AppSettings = Depends(get_app_settings),
) -> int:
    user_id = get_user_id_from_access_token(token, settings.secret_key.get_secret_value())
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.MALFORMED_PAYLOAD)

    return user_id


async def _get_current_user(
        user_id: int = Depends(_get_user_id_from_token),
        user_repository: UserRepository = Depends(get_repository(UserRepository))
) -> UserInDB:
    user = await user_repository.get_user_by_id(user_id)
    if not user:
        logger.error(f"User with ID {user_id} doesn't found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.USER_DOES_NOT_EXIST_ERROR)

    return user

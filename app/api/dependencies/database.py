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

from typing import Callable, Type

from fastapi import Depends
from fastapi.requests import Request
from neo4j import AsyncSession

from app.database.repositories.base_repository import BaseRepository


def _get_db_session(request: Request) -> AsyncSession:
    return request.app.state.session


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session=Depends(_get_db_session)) -> BaseRepository:
        return repo_type(session)

    return _get_repo

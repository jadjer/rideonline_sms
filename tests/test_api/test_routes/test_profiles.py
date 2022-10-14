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

from app.database.repositories.users import UsersRepository
from app.models.domain.profile import Profile
from app.models.domain.user import UserInDB
from app.models.schemas.user import UserInResponse


# async def test_unregistered_user_will_receive_profile(
#     app: FastAPI, client: AsyncClient, test_profile: Profile
# ) -> None:
#     response = await client.get(
#         app.url_path_for("profiles:get-profile", user_id=str(test_profile.user_id))
#     )
#     profile = UserInResponse(**response.json())
#     assert profile.user..username == test_user.username


# async def test_unregistered_user_will_receive_profile_without_following(
#     app: FastAPI, client: AsyncClient, test_user: UserInDB
# ) -> None:
#     response = await client.get(
#         app.url_path_for("profiles:get-profile", username=test_user.username)
#     )
#     profile = UserInResponse(**response.json())
#     assert profile.profile.username == test_user.username
#     assert not profile.profile.following


# async def test_user_that_does_not_follows_another_will_receive_profile_without_follow(
#     app: FastAPI, authorized_client: AsyncClient, pool: Pool
# ) -> None:
#     async with pool.acquire() as conn:
#         users_repo = UsersRepository(conn)
#         user = await users_repo.create_user(
#             username="user_for_following",
#             email="test-for-following@email.com",
#             password="password",
#         )
#
#     response = await authorized_client.get(
#         app.url_path_for("profiles:get-profile", username=user.username)
#     )
#     profile = UserInResponse(**response.json())
#     assert profile.profile.username == user.username
#     assert not profile.profile.following


# async def test_user_that_follows_another_will_receive_profile_with_follow(
#     app: FastAPI, authorized_client: AsyncClient, pool: Pool, test_user: UserInDB
# ) -> None:
#     async with pool.acquire() as conn:
#         users_repo = UsersRepository(conn)
#         user = await users_repo.create_user(
#             username="user_for_following",
#             email="test-for-following@email.com",
#             password="password",
#         )
#
#         profiles_repo = UsersRepository(conn)
#         await profiles_repo.add_user_into_followers(
#             target_user=user, requested_user=test_user
#         )
#
#     response = await authorized_client.get(
#         app.url_path_for("profiles:get-profile", username=user.username)
#     )
#     profile = UserInResponse(**response.json())
#     assert profile.profile.username == user.username
#     assert profile.profile.following


# @pytest.mark.parametrize(
#     "api_method, route_name",
#     (
#         ("GET", "profiles:get-profile"),
#         ("POST", "profiles:follow-user"),
#         ("DELETE", "profiles:unsubscribe-from-user"),
#     ),
# )
# async def test_user_can_not_retrieve_not_existing_profile(
#     app: FastAPI, authorized_client: AsyncClient, api_method: str, route_name: str
# ) -> None:
#     response = await authorized_client.request(
#         api_method, app.url_path_for(route_name, username="not_existing_user")
#     )
#     assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.parametrize(
#     "api_method, route_name, following",
#     (
#         ("POST", "profiles:follow-user", True),
#         ("DELETE", "profiles:unsubscribe-from-user", False),
#     ),
# )
# async def test_user_can_change_following_for_another_user(
#     app: FastAPI,
#     authorized_client: AsyncClient,
#     pool: Pool,
#     test_user: UserInDB,
#     api_method: str,
#     route_name: str,
#     following: bool,
# ) -> None:
#     async with pool.acquire() as conn:
#         users_repo = UsersRepository(conn)
#         user = await users_repo.create_user(
#             username="user_for_following",
#             email="test-for-following@email.com",
#             password="password",
#         )
#
#         if not following:
#             profiles_repo = UsersRepository(conn)
#             await profiles_repo.add_user_into_followers(
#                 target_user=user, requested_user=test_user
#             )
#
#     change_following_response = await authorized_client.request(
#         api_method, app.url_path_for(route_name, username=user.username)
#     )
#     assert change_following_response.status_code == status.HTTP_200_OK
#
#     response = await authorized_client.get(
#         app.url_path_for("profiles:get-profile", username=user.username)
#     )
#     profile = UserInResponse(**response.json())
#     assert profile.profile.username == user.username
#     assert profile.profile.following == following


# @pytest.mark.parametrize(
#     "api_method, route_name, following",
#     (
#         ("POST", "profiles:follow-user", True),
#         ("DELETE", "profiles:unsubscribe-from-user", False),
#     ),
# )
# async def test_user_can_not_change_following_state_to_the_same_twice(
#     app: FastAPI,
#     authorized_client: AsyncClient,
#     pool: Pool,
#     test_user: UserInDB,
#     api_method: str,
#     route_name: str,
#     following: bool,
# ) -> None:
#     async with pool.acquire() as conn:
#         users_repo = UsersRepository(conn)
#         user = await users_repo.create_user(
#             username="user_for_following",
#             email="test-for-following@email.com",
#             password="password",
#         )
#
#         if following:
#             profiles_repo = UsersRepository(conn)
#             await profiles_repo.add_user_into_followers(
#                 target_user=user, requested_user=test_user
#             )
#
#     response = await authorized_client.request(
#         api_method, app.url_path_for(route_name, username=user.username)
#     )
#
#     assert response.status_code == status.HTTP_400_BAD_REQUEST


# @pytest.mark.parametrize(
#     "api_method, route_name",
#     (("POST", "profiles:follow-user"), ("DELETE", "profiles:unsubscribe-from-user")),
# )
# async def test_user_can_not_change_following_state_for_him_self(
#     app: FastAPI,
#     authorized_client: AsyncClient,
#     test_user: UserInDB,
#     api_method: str,
#     route_name: str,
# ) -> None:
#     response = await authorized_client.request(
#         api_method, app.url_path_for(route_name, username=test_user.username)
#     )
#
#     assert response.status_code == status.HTTP_400_BAD_REQUEST

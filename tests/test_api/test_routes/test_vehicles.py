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

from app.models.domain.vehicle import Vehicle
from app.models.schemas.vehicle import VehicleInResponse


@pytest.mark.asyncio
async def test_user_can_add_vehicle(
        initialized_app: FastAPI, authorized_client: AsyncClient
) -> None:
    vehicle_data = {
        "brand": "honda",
        "model": "xl1000v",
        "gen": 3,
        "year": 2008,
        "color": "silver",
        "mileage": 65500,
        "vin": "JVM0935G46622",
        "registration_plate": "9112AB2",
        "name": "Bullfinch"
    }

    response = await authorized_client.post(
        initialized_app.url_path_for("vehicles:create-vehicle"), json={"vehicle": vehicle_data}
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_unauthorised_user_can_not_add_vehicle(
        initialized_app: FastAPI, client: AsyncClient
) -> None:
    vehicle_data = {
        "brand": "honda",
        "model": "xl1000v",
        "gen": 3,
        "year": 2008,
        "color": "silver",
        "mileage": 65500,
        "vin": "JVM0935G46622",
        "registration_plate": "9112AB2",
        "name": "Bullfinch"
    }

    response = await client.post(
        initialized_app.url_path_for("vehicles:create-vehicle"), json={"vehicle": vehicle_data}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parameter_name, parameter_value",
    (
            ("vin", "JVM01234567891011"),
            ("registration_plate", "9112AB2")
    ),
)
async def test_user_can_not_add_vehicle_with_duplicated_params(
        initialized_app: FastAPI,
        authorized_client: AsyncClient,
        test_vehicle: Vehicle,
        parameter_name: str,
        parameter_value: str,
) -> None:
    vehicle_data = {
        "vehicle": {
            "brand": "honda",
            "model": "xl1000v",
            "gen": 3,
            "year": 2008,
            "color": "silver",
            "mileage": 65500,
            "vin": "JVM0935G46622",
            "registration_plate": "9112AB2",
            "name": "Bullfinch"
        }
    }

    vehicle_data["vehicle"][parameter_name] = parameter_value

    response = await authorized_client.post(
        initialized_app.url_path_for("vehicles:create-vehicle"), json=vehicle_data
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field, update_value",
    (
            ("brand", "Kawasaki"),
            ("model", "qwe123"),
            ("gen", 2),
            ("year", 2022),
            ("color", "black"),
            ("mileage", 70000),
            ("vin", "ABC11109876543210"),
            ("registration_plate", "1234AB1"),
            ("name", "Test name"),
    ),
)
async def test_user_can_update_vehicle(
        initialized_app: FastAPI,
        authorized_client: AsyncClient,
        test_vehicle: Vehicle,
        update_field: str,
        update_value
) -> None:
    response = await authorized_client.put(
        initialized_app.url_path_for("vehicles:update-vehicle", vehicle_id=str(test_vehicle.id)),
        json={"vehicle": {update_field: update_value}},
    )

    assert response.status_code == status.HTTP_200_OK

    vehicle = VehicleInResponse(**response.json()).vehicle
    vehicle_as_dict = vehicle.dict()

    assert vehicle_as_dict[update_field] == update_value


@pytest.mark.asyncio
async def test_user_can_not_reduce_vehicle_mileage(
        initialized_app: FastAPI,
        authorized_client: AsyncClient,
        test_vehicle: Vehicle,
) -> None:
    reduce_mileage = test_vehicle.mileage - 1
    
    response = await authorized_client.put(
        initialized_app.url_path_for("vehicles:update-vehicle", vehicle_id=str(test_vehicle.id)),
        json={"vehicle": {"mileage": reduce_mileage}},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

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
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.worker import get_worker
from app.models.domain.sms import SMS
from app.models.schemas.sms import SmsRequest, SmsCountResponse
from app.models.schemas.wrapper import WrapperResponse
from app.api.validators.phone_number_validator import check_phone_is_valid
from app.resources import strings
from app.worker.worker import Worker

router = APIRouter()


@router.post("/send", status_code=status.HTTP_200_OK, name="sms:send")
async def send_sms(
        request: SmsRequest,
        worker: Worker = Depends(get_worker),
) -> WrapperResponse:
    if not check_phone_is_valid(request.phone):
        logger.error(strings.PHONE_NUMBER_INVALID_ERROR)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.PHONE_NUMBER_INVALID_ERROR)

    # if not sms_service.is_hilink():
    #     logger.error(strings.SERVICE_UNAVAILABLE)
    #     raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=strings.SERVICE_UNAVAILABLE)

    if not await worker.add_task(SMS(phone=request.phone, message=request.message)):
        logger.error(strings.VERIFICATION_SEND_SMS_ERROR)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.VERIFICATION_SEND_SMS_ERROR)

    return WrapperResponse()


@router.get("/task_count", status_code=status.HTTP_200_OK, name="sms:task_count")
def get_task_count(worker: Worker = Depends(get_worker)) -> WrapperResponse:
    return WrapperResponse(
        payload=SmsCountResponse(count=worker.task_count()).model_dump(),
    )

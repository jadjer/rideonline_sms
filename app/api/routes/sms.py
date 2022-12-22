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

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings

from app.models.schemas.sms import SmsSend
from app.services.phone_number_validator import check_phone_is_valid
from app.services.sms import is_hilink, send_sms_to_phone
from app.resources import strings

router = APIRouter()


@router.post("/send", status_code=status.HTTP_200_OK, name="sms:send")
async def send_sms(
        request: SmsSend,
        settings: AppSettings = Depends(get_app_settings),
) -> None:
    if not check_phone_is_valid(request.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.PHONE_NUMBER_INVALID_ERROR)

    if not is_hilink(settings.hilink):
        logger.error(strings.SERVICE_UNAVAILABLE)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=strings.SERVICE_UNAVAILABLE)

    if not send_sms_to_phone(settings.hilink, request.phone, request.message):
        logger.error(strings.VERIFICATION_SEND_SMS_ERROR)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.VERIFICATION_SEND_SMS_ERROR)

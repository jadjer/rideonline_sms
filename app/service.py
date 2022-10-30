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

from loguru import logger

from protos.status_pb2 import Status
from protos.service.sms_pb2 import SmsSendRequest, SmsSendResponse
from protos.service.sms_pb2_grpc import SmsServicer

from app.core.settings.app import AppSettings
from app.resources import strings
from app.services.sms import is_hilink, send_sms_to_phone
from app.services.phone_number_validator import check_phone_is_valid


class Service(SmsServicer):
    def __init__(self, settings: AppSettings):
        self.settings = settings

    def send(self, request: SmsSendRequest, context) -> SmsSendResponse:
        logger.debug("{} <= {}".format(request.phone, request.message))

        if not check_phone_is_valid(request.phone):
            logger.error(strings.PHONE_NUMBER_INVALID_ERROR)
            return SmsSendResponse(status=Status(
                in_error=True, error_message=strings.PHONE_NUMBER_INVALID_ERROR
            ))

        if not is_hilink(self.settings.sms_api_host):
            logger.error(strings.VERIFICATION_SERVICE_TEMPORARY_UNAVAILABLE)
            return SmsSendResponse(status=Status(
                in_error=True, error_message=strings.VERIFICATION_SERVICE_TEMPORARY_UNAVAILABLE
            ))

        if not send_sms_to_phone(self.settings.sms_api_host, request.phone, request.message):
            logger.error(strings.VERIFICATION_SERVICE_SEND_SMS_ERROR)
            return SmsSendResponse(status=Status(
                in_error=True, error_message=strings.VERIFICATION_SERVICE_SEND_SMS_ERROR
            ))

        return SmsSendResponse(status=Status(in_error=False, error_message=""))

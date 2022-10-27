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
from multiprocessing import Queue

from app.core.settings.app import AppSettings
from app.models.schemas.sms import Message
from app.resources import strings
from app.services.phone_number_validator import check_phone_is_valid
from app.services.sms import is_hilink, send_sms_to_phone


class SmsManager(object):
    settings: AppSettings

    def __init__(self, settings: AppSettings):
        self.settings = settings

    def run(self, queue: Queue):
        while True:
            data = queue.get()
            self.process(data)

    def process(self, data: str) -> bool:
        try:
            message = Message.parse_raw(data)
        except BaseException as exception:
            logger.error(exception)
            return False

        logger.debug("{} <= {}".format(message.phone, message.text))

        if not check_phone_is_valid(message.phone):
            logger.error(strings.PHONE_NUMBER_INVALID_ERROR)
            return False

        if not is_hilink(self.settings.sms_api_host):
            logger.error(strings.VERIFICATION_SERVICE_TEMPORARY_UNAVAILABLE)
            return False

        if not send_sms_to_phone(self.settings.sms_api_host, message.phone, message.text):
            logger.error(strings.VERIFICATION_SERVICE_SEND_SMS_ERROR)
            return False

        return True

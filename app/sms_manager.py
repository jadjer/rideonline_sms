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

import asyncio

from app.logger import log_info
from app.models.command import Command
from app.services.hilink import HiLinkAssistant
from app.services.validator import check_phone_is_valid
from app.settings import AppSettings


async def sms_handler(settings: AppSettings, queue: asyncio.Queue):
    hilink = HiLinkAssistant(settings.sms_api_host, settings.sms_api_user, settings.sms_api_pass)

    while True:
        await log_info("Await new message from kafka")
        message: Command = await queue.get()

        await log_info("Get new message from queue")

        if await check_phone_is_valid(message.phone):
            await hilink.send_sms_to_phone(message.phone, message.message)

        queue.task_done()

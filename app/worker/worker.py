#  Copyright 2023 Pavel Suprunov
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

import asyncio

from pydantic import HttpUrl
from loguru import logger

from app.models.domain.sms import SMS
from app.services.sms_service import SmsService


class Worker:
    def __init__(self, host: HttpUrl):
        self._queue = asyncio.Queue()
        self._sms = SmsService(device_host=host)

        self._enabled = True

    async def add_task(self, task) -> bool:
        if not self._enabled:
            return False

        await self._queue.put(task)
        logger.info(f"Task added: {task}")

        return True

    def task_count(self) -> int:
        return self._queue.qsize()

    async def loop(self):
        self._enabled = True

        while self._enabled:
            task: SMS = await self._queue.get()

            send_sms_task = await asyncio.to_thread(self._sms.send_sms, task.phone, task.message)
            if send_sms_task:
                logger.info(f"Task sent to {task.phone}")
                self._queue.task_done()
            else:
                logger.error(f"Task failed to send to {task.phone}")
                await self._queue.put(task)

            await asyncio.sleep(15)

    async def stop(self):
        self._enabled = False

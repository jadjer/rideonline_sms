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

import enum
from loguru import logger

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer()


class LogLevel(enum.Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3


async def send_log_message(message: str):
    future = producer.send("logger", b"{} {}".format())

    try:
        future.get(timeout=10)
        logger.exception()

    except KafkaError:
        # Decide what to do if produce request failed...
        logger.exception()
        pass

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

from .logger_producer import send_log_message


async def log_info(message):
    logger.info(message)
    await send_log_message("INFO", message)


async def log_warning(message):
    logger.warning(message)
    await send_log_message("WARNING", message)


async def log_error(message):
    logger.error(message)
    await send_log_message("ERROR", message)


async def log_critical(message):
    logger.critical(message)
    await send_log_message("CRITICAL", message)

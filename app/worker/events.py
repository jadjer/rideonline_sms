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

from fastapi import FastAPI
from loguru import logger

from app.worker.worker import Worker
from app.core.settings.app import AppSettings


async def worker_start(app: FastAPI, settings: AppSettings) -> Worker:
    logger.info("Starting worker")

    worker = Worker(settings.hilink)

    asyncio.create_task(worker.loop())

    logger.info("Worker started")

    app.state.worker = worker

    return worker


async def worker_stop(app: FastAPI) -> None:
    logger.info("Stopping sender worker")

    worker: Worker = app.state.worker

    await worker.stop()

    logger.info("Worker stopped")

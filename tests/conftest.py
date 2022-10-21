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
from queue import Queue
from app.core.settings.app import AppSettings
from app.sms_manager import SmsManager


@pytest.fixture
def settings() -> AppSettings:
    from app.core.config import get_app_settings

    return get_app_settings()


@pytest.fixture
def queue() -> Queue:
    queue = Queue()

    return queue


@pytest.fixture
def sms_manager(settings: AppSettings, queue: Queue) -> SmsManager:
    sms_manager = SmsManager(settings, queue)

    return sms_manager

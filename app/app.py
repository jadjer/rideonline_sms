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

import multiprocessing

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.rabbitmq_client import RabbitMQClient
from app.sms_manager import SmsManager


class App(object):
    settings: AppSettings
    sms_manager: SmsManager
    rabbit_client: RabbitMQClient

    def __init__(self):
        self.settings = get_app_settings()
        self.sms_manager = SmsManager(self.settings)
        self.rabbit_client = RabbitMQClient(self.settings)

    def run(self):
        queue = multiprocessing.Queue()

        sms_manager = multiprocessing.Process(target=self.sms_manager.run, args=(queue,))
        rabbit_client = multiprocessing.Process(target=self.rabbit_client.run, args=(queue,))

        sms_manager.start(), rabbit_client.start()
        sms_manager.join(), rabbit_client.join()

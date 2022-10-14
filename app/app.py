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

from queue import Queue
from threading import Thread

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.rabbitmq_client import RabbitMQClient
from app.sms_manager import SmsManager


class App(object):
    __queue: Queue
    __thread: Thread
    __settings: AppSettings
    __sms_manager: SmsManager
    __rabbit_client: RabbitMQClient

    def __init__(self):
        self.__queue = Queue()
        self.__settings = get_app_settings()
        self.__sms_manager = SmsManager(self.__settings, self.__queue)
        self.__rabbit_client = RabbitMQClient(self.__settings, self.__queue)

    def run(self):
        self.__thread = Thread(target=self.__sms_manager.spin)
        self.__thread.start()

        self.__rabbit_client.start()

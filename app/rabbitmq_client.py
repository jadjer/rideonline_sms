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

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from loguru import logger

from app.core.settings.app import AppSettings


class RabbitMQClient(object):
    __queue: Queue
    __settings: AppSettings
    __connection: BlockingConnection

    def __init__(self, settings: AppSettings, queue: Queue):
        self.__queue = queue
        self.__settings = settings

        credentials = PlainCredentials(self.__settings.rabbitmq_user, self.__settings.rabbitmq_pass)
        parameters = ConnectionParameters(self.__settings.rabbitmq_server, credentials=credentials)

        self.__connection = BlockingConnection(parameters)

    def start(self):
        channel = self.__connection.channel()
        channel.queue_declare(queue=self.__settings.rabbitmq_channel)

        def callback(cb, method, parameters, body):
            self.__queue.put(body)

        channel.basic_consume(queue=self.__settings.rabbitmq_channel, on_message_callback=callback, auto_ack=True)

        logger.info("Started RabbitMQ client on {server} server".format(server=self.__settings.rabbitmq_server))

        channel.start_consuming()

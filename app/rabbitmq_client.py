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

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from loguru import logger
from multiprocessing import Queue

from app.core.settings.app import AppSettings


class RabbitMQClient(object):
    settings: AppSettings

    def __init__(self, settings: AppSettings):
        self.settings = settings

    def run(self, queue: Queue):
        def callback(cb, method, parameters, body):
            queue.put(body)

        logger.info("Started RabbitMQ client on {server} server".format(server=self.settings.rabbitmq_server))

        credentials = PlainCredentials(self.settings.rabbitmq_user, self.settings.rabbitmq_pass)
        parameters = ConnectionParameters(self.settings.rabbitmq_server, credentials=credentials)
        connection = BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue=self.settings.rabbitmq_channel)
        channel.basic_consume(queue=self.settings.rabbitmq_channel, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

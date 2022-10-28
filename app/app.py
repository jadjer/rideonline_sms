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

import grpc

from loguru import logger
from concurrent import futures

from app.service import Service
from protos.service import sms_pb2_grpc

from app.core.config import get_app_settings


class App(sms_pb2_grpc.SmsServicer):

    def __init__(self):
        self.settings = get_app_settings()

    def run(self):
        port = 50051

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        sms_pb2_grpc.add_SmsServicer_to_server(Service(), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()

        logger.info(f"Server started, listening on {port}")
        server.wait_for_termination()

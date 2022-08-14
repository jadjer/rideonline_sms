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

from pydantic import HttpUrl
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = True
    title: str = "sms_manager"
    version: str = "0.0.1"

    kafka_host: str

    sms_api_host: HttpUrl = "http://192.168.1.1"
    sms_api_user: str = ""
    sms_api_pass: str = ""
    sms_max_chars: int = 160

    class Config:
        validate_assignment = True

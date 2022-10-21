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

from app.sms_manager import SmsManager


def test_send_empty_message(sms_manager: SmsManager):
    payload = ""

    assert not sms_manager.process(payload)


def test_send_wrong_message(sms_manager: SmsManager):
    payload = "qwe"

    assert not sms_manager.process(payload)


def test_send_incorrect_message_with_failure_phone_number(sms_manager: SmsManager):
    payload = '{"phone": "+123456789", "text": "test"}'

    assert not sms_manager.process(payload)


def test_send_correct_message_with_failure_data_field_name(sms_manager: SmsManager):
    payload = '{"phone": "+375257133519", "message": "test"}'

    assert not sms_manager.process(payload)

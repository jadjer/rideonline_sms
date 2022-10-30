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

from protos.service.sms_pb2 import SmsSendRequest, SmsSendResponse


def test_send_empty_message(sms_service):
    request: SmsSendRequest = SmsSendRequest()
    response: SmsSendResponse = sms_service.send(request, None)

    assert response.status.in_error


def test_send_incorrect_message_with_failure_phone_number(sms_service):
    request: SmsSendRequest = SmsSendRequest(phone="+123456789", message="test")
    response: SmsSendResponse = sms_service.send(request, None)

    assert response.status.in_error

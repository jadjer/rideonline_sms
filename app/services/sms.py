#  Copyright 2022 Pavel Suprunov
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

import contextlib
from datetime import datetime
from typing import List

import httpx
import xmltodict as xmltodict
from httpx import Client
from pydantic import HttpUrl

SMS_LIST_TEMPLATE = """<request>
    <PageIndex>1</PageIndex>
    <ReadCount>20</ReadCount>
    <BoxType>1</BoxType>
    <SortType>0</SortType>
    <Ascending>0</Ascending>
    <UnreadPreferred>0</UnreadPreferred>
    </request>"""

SMS_DEL_TEMPLATE = """<request>
    <Index>{index}</Index>
    </request>"""

SMS_SEND_TEMPLATE = """<request>
    <Index>-1</Index>
    <Phones><Phone>{phone}</Phone></Phones>
    <Sca></Sca>
    <Content>{content}</Content>
    <Length>{length}</Length>
    <Reserved>1</Reserved>
    <Date>{timestamp}</Date>
    </request>"""


def is_hilink(device_host: HttpUrl) -> bool:
    with Client(base_url=device_host) as client:
        try:
            response = client.get("/api/device/information", timeout=2.0)
        except httpx.ConnectTimeout as err:
            return False

    if response.status_code != 200:
        return False

    return True


def get_headers(device_host: HttpUrl) -> dict:
    token = None
    session_id = None

    with Client(base_url=device_host) as client:
        try:
            response = client.get("/api/webserver/SesTokInfo")
        except httpx.ConnectTimeout as err:
            return {}

    if response.status_code != 200:
        return {'__RequestVerificationToken': token, 'Cookie': session_id}

    with contextlib.suppress(Exception):
        response_data = xmltodict.parse(response.text, xml_attribs=True)
        if 'response' in response_data and 'TokInfo' in response_data["response"]:
            token = response_data['response']['TokInfo']

        if 'response' in response_data and 'SesInfo' in response_data['response']:
            session_id = response_data['response']['SesInfo']

        headers = {'__RequestVerificationToken': token, 'Cookie': session_id}

    return headers


def get_sms(device_host: HttpUrl, headers: dict):
    payload = SMS_LIST_TEMPLATE

    with Client(base_url=device_host) as client:
        try:
            response = client.post("/api/sms/sms-list", data=payload, headers=headers)
        except httpx.ConnectTimeout as err:
            pass

    response_data = xmltodict.parse(response.text, xml_attribs=True)
    num_messages = int(response_data['response']['Count'])
    messages_r = response_data['response']['Messages']['Message']

    if num_messages == 1:
        temp = messages_r
        messages_r = [temp]

    messages = get_content(messages_r, num_messages)
    return messages, messages_r


def get_content(data, num_messages) -> List[str]:
    messages = []
    for i in range(num_messages):
        message = data[i]
        number = message['Phone']
        content = message['Content']
        date = message['Date']
        messages.append('Message from ' + number + ' recieved ' + date + ' : ' + str(content))

    return messages


def del_message(device_host: HttpUrl, headers: dict, index: int) -> None:
    payload = SMS_DEL_TEMPLATE.format(index=index)

    with Client(base_url=device_host) as client:
        try:
            response = client.post("/api/sms/delete-sms", data=payload, headers=headers)
        except httpx.ConnectTimeout as err:
            pass

    response_data = xmltodict.parse(response.text, xml_attribs=True)
    print(response_data['response'])


def get_unread(device_host: HttpUrl, headers: dict) -> int:
    with Client(base_url=device_host) as client:
        try:
            response = client.get("/api/monitoring/check-notifications", headers=headers)
        except httpx.ConnectTimeout as err:
            return False

    response_data = xmltodict.parse(response.text, xml_attribs=True)
    unread = int(response_data['response']['UnreadMessage'])

    return unread


def wait_send_sms_to_phone(device_host: HttpUrl, phone_number: str) -> bool:
    with Client(base_url=device_host) as client:
        try:
            response = client.get("/api/sms/send-status")
        except httpx.ConnectTimeout as err:
            return False

    response_data = xmltodict.parse(response.text, xml_attribs=True)
    phone = response_data["response"]["Phone"]
    phone_success = response_data["response"]["SucPhone"]
    phone_fail = response_data["response"]["FailPhone"]
    total_count = response_data["response"]["TotalCount"]
    current_index = response_data["response"]["CurIndex"]

    if phone and phone != phone_number:
        return False
    if phone_success and phone_success != phone_number:
        return False
    if phone_fail and phone_fail == phone_number:
        return False

    if current_index < total_count:
        return False

    return True


def send_sms_to_phone(device_host: HttpUrl, phone: str, message: str) -> bool:
    payload = SMS_SEND_TEMPLATE.format(
        phone=phone,
        content=message,
        length=len(message),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    with Client(base_url=device_host) as client:
        try:
            response = client.post("/api/sms/send-sms", data=payload)
            if response.status_code != 200:
                return False

            response_data = xmltodict.parse(response.text, xml_attribs=True)

            return response_data["response"] == "OK"

        except httpx.ConnectTimeout as err:
            return False

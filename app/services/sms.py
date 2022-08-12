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

import contextlib
from typing import List

import xmltodict as xmltodict
from httpx import AsyncClient
from datetime import datetime

from pydantic import HttpUrl

MAX_CHARS_IN_MESSAGE = 160

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


async def is_hilink(device_host: HttpUrl) -> bool:
    async with AsyncClient(base_url=device_host) as client:
        response = await client.get("/api/device/information", timeout=2.0)

    if response.status_code != 200:
        return False

    return True


async def get_headers(device_host: HttpUrl) -> dict:
    token = None
    session_id = None

    async with AsyncClient(base_url=device_host) as client:
        response = await client.get("/api/webserver/SesTokInfo")

    if response.status_code != 200:
        return {'__RequestVerificationToken': token, 'Cookie': session_id}

    with contextlib.suppress(Exception):
        d = xmltodict.parse(response.text, xml_attribs=True)
        if 'response' in d and 'TokInfo' in d["response"]:
            token = d['response']['TokInfo']

        if 'response' in d and 'SesInfo' in d['response']:
            session_id = d['response']['SesInfo']

        headers = {'__RequestVerificationToken': token, 'Cookie': session_id}

    return headers


async def get_sms(device_host: HttpUrl, headers: dict):
    payload = SMS_LIST_TEMPLATE

    async with AsyncClient(base_url=device_host) as client:
        response = await client.post("/api/sms/sms-list", data=payload, headers=headers)

    d = xmltodict.parse(response.text, xml_attribs=True)
    num_messages = int(d['response']['Count'])
    messages_r = d['response']['Messages']['Message']

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


async def del_message(device_host: HttpUrl, headers: dict, index: int) -> None:
    payload = SMS_DEL_TEMPLATE.format(index=index)

    async with AsyncClient(base_url=device_host) as client:
        response = await client.post("/api/sms/delete-sms", data=payload, headers=headers)

    d = xmltodict.parse(response.text, xml_attribs=True)
    print(d['response'])


async def get_unread(device_host: HttpUrl, headers: dict) -> int:
    async with AsyncClient(base_url=device_host) as client:
        response = await client.get("/api/monitoring/check-notifications", headers=headers)

    d = xmltodict.parse(response.text, xml_attribs=True)
    unread = int(d['response']['UnreadMessage'])

    return unread


async def wait_send_sms_to_phone(device_host: HttpUrl, phone_number: str) -> bool:
    async with AsyncClient(base_url=device_host) as client:
        response = await client.get("/api/sms/send-status")

    d = xmltodict.parse(response.text, xml_attribs=True)
    phone = d["response"]["Phone"]
    phone_success = d["response"]["SucPhone"]
    phone_fail = d["response"]["FailPhone"]
    total_count = d["response"]["TotalCount"]
    current_index = d["response"]["CurIndex"]

    if phone and phone != phone_number:
        return False
    if phone_success and phone_success != phone_number:
        return False
    if phone_fail and phone_fail == phone_number:
        return False

    if current_index < total_count:
        return False

    return True


async def send_sms_to_phone(device_host: HttpUrl, phone: str, message: str) -> bool:
    payload = SMS_SEND_TEMPLATE.format(
        phone=phone,
        content=message,
        length=len(message),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    async with AsyncClient(base_url=device_host) as client:
        response_send = await client.post("/api/sms/send-sms", data=payload)
        if response_send.status_code != 200:
            return False

    return True


async def send_verify_code_to_phone(device_host: HttpUrl, phone: str, verify_code: int) -> bool:
    verification_message = "{code} is your verification code.".format(code=verify_code)

    return await send_sms_to_phone(device_host, phone, verification_message)

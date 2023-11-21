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

import httpx
import xmltodict

from typing import List
from httpx import Client
from pydantic import HttpUrl
from loguru import logger
from datetime import datetime


class SmsService:
    def __init__(self, device_host: HttpUrl):
        self._client = Client(base_url=device_host.__str__(), headers=self._build_headers(), timeout=5.0)

    def is_hilink(self) -> bool:
        try:
            response = self._client.get("/api/device/information")
        except httpx.ConnectTimeout as err:
            logger.error(err)
            return False

        if response.status_code != 200:
            return False

        return True

    def send_sms(self, phone: str, content: str) -> bool:
        """
        Sends an SMS to the specified phone number with the given content.

        Parameters:
            phone (str): The phone number to send the SMS to.
            content (str): The content of the SMS.

        Returns:
            bool: True if the SMS was sent successfully, False otherwise.
        """
        payload = self._build_sms_send_payload(phone, content)

        try:
            # noinspection PyTypeChecker
            response = self._client.post("/api/sms/send-sms", data=payload)
        except httpx.ConnectTimeout as err:
            logger.error(err)
            return False

        if response.status_code != 200:
            return False

        response_data = xmltodict.parse(response.text, xml_attribs=False)

        return response_data["response"] == "OK"

    def delete_sms(self, index: int) -> None:
        """
        Deletes the SMS message at the specified index.

        Parameters:
            index (int): The index of the SMS message to delete.

        Returns:
            None.
        """
        payload = self._build_sms_delete_payload(index)

        try:
            # noinspection PyTypeChecker
            self._client.post("/api/sms/delete-sms", data=payload)
        except httpx.ConnectTimeout as err:
            logger.error(err)

    def get_sms(self) -> List[str]:
        """
        Retrieves the list of SMS messages.

        Returns:
            List[str]: A list of SMS messages.
        """
        payload = self._build_sms_list_payload()

        try:
            # noinspection PyTypeChecker
            response = self._client.post("/api/sms/sms-list", data=payload)
        except httpx.ConnectTimeout as err:
            logger.error(err)
            return []

        response_data = xmltodict.parse(response.text, xml_attribs=True)
        num_messages = int(response_data['response']['Count'])
        messages_r = response_data['response']['Messages']['Message']

        if num_messages == 1:
            temp = messages_r
            messages_r = [temp]

        messages = self._get_content(messages_r, num_messages)
        return messages

    def wait_send_sms(self, phone_number: str) -> bool:
        """
        Waits for the send status of the SMS to the specified phone number.

        Parameters:
            phone_number (str): The phone number to check the send status for.

        Returns:
            bool: True if the send status is successful, False otherwise.
        """
        try:
            response = self._client.get("/api/sms/send-status")
        except httpx.ConnectTimeout as err:
            logger.error(err)
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

    def send_sms_and_wait(self, phone: str, content: str) -> bool:
        """
        Sends an SMS to the specified phone number with the given content and waits for the send status.

        Parameters:
            phone (str): The phone number to send the SMS to.
            content (str): The content of the SMS.

        Returns:
            bool: True if the SMS was sent successfully and the send status is successful, False otherwise.
        """
        self.send_sms(phone, content)
        return self.wait_send_sms(phone)

    @staticmethod
    def _build_headers() -> dict[str, str]:
        return {"Content-Type": "application/xml"}

    @staticmethod
    def _build_sms_send_payload(phone: str, content: str) -> str:
        """
        Builds the payload for sending an SMS.

        Parameters:
            phone (str): The phone number to send the SMS to.
            content (str): The content of the SMS.

        Returns:
            str: The payload for sending the SMS.
        """

        _phone = phone
        _content = content
        _content_length = len(content)
        _datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""
        <request>
            <Index>-1</Index>
            <Phones>
                <Phone>{_phone}</Phone>
            </Phones>
            <Sca></Sca>
            <Content>{_content}</Content>
            <Length>{_content_length}</Length>
            <Reserved>1</Reserved>
            <Date>{_datetime}</Date>
        </request>"""

    @staticmethod
    def _build_sms_delete_payload(index: int) -> str:
        """
        Builds the payload for deleting an SMS message.

        Parameters:
            index (int): The index of the SMS message to delete.

        Returns:
            str: The payload for deleting the SMS message.
        """
        return f"""
        <request>
            <Index>{index}</Index>
        </request>"""

    @staticmethod
    def _build_sms_list_payload() -> str:
        """
        Builds the payload for retrieving the list of SMS messages.

        Returns:
            str: The payload for retrieving the SMS messages.
        """
        return """
        <request>
            <PageIndex>1</PageIndex>
            <ReadCount>20</ReadCount>
            <BoxType>1</BoxType>
            <SortType>0</SortType>
            <Ascending>0</Ascending>
            <UnreadPreferred>0</UnreadPreferred>
        </request>"""

    @staticmethod
    def _get_content(data: List[dict], num_messages: int) -> List[str]:
        """
        Extracts the content from the list of SMS messages.

        Parameters:
            data (List[dict]): The list of SMS messages.
            num_messages (int): The number of SMS messages.

        Returns:
            List[str]: The list of SMS message contents.
        """

        messages = []
        for message in data:
            number = message["Phone"]
            date = message["Date"]
            content = message["Content"]

            messages.append(f"Message from {number} received {date}: {content}")

        return messages

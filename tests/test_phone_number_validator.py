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

from app.service import check_phone_is_valid


def test_empty_phone():
    phone = ""
    assert not check_phone_is_valid(phone)


def test_wrong_phone():
    phone = "qwe"
    assert not check_phone_is_valid(phone)


def test_incorrect_phone():
    phone = "+123456789"
    assert not check_phone_is_valid(phone)


def test_correct_phone():
    phone = "+375259876543"
    assert check_phone_is_valid(phone)

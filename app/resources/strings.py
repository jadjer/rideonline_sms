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

# API messages

API_KEY_ERROR = "API key error"
API_KEY_CREATE_ERROR = "API key create error"
API_KEY_UPDATE_ERROR = "API key update error"

USER_CREATE_ERROR = "User create error"

USER_DOES_NOT_EXIST_ERROR = "user does not exist"
ARTICLE_DOES_NOT_EXIST_ERROR = "article does not exist"
ARTICLE_ALREADY_EXISTS = "article already exists"
USER_IS_NOT_AUTHOR_OF_POST = "You are not an author of this post"
USER_IS_NOT_AUTHOR_OF_EVENT = "You are not an author of this event"

POST_DOES_NOT_EXISTS = "Post does not exists"
POST_ALREADY_EXISTS = "Post already exists"
POST_CREATE_ERROR = "Post create error"
POST_DELETE_ERROR = "Post delete error"

EVENT_DOES_NOT_EXIST_ERROR = "Event does not exist"
EVENT_ALREADY_EXISTS = "Event already exists"
EVENT_CREATE_ERROR = "Event create error"

PROFILE_DOES_NOT_EXISTS = "Profile does not exists"

VEHICLE_ALREADY_EXISTS = "Vehicle already exists"
VEHICLE_CONFLICT_VIN_ERROR = "Vehicle with current VIN already exist"
VEHICLE_CONFLICT_REGISTRATION_PLATE_ERROR = "Vehicle with current REGISTRATION PLATE already exist"
VEHICLE_DOES_NOT_EXIST_ERROR = "Vehicle does not exist"
VEHICLE_CONFLICT_VIN = "Vehicle with current VIN already exists"
VEHICLE_CONFLICT_REG_PLATE = "Vehicle with current REGISTRATION PLATE already exists"
VEHICLE_CREATE_ERROR = "Vehicle create error"
VEHICLE_GET_ERROR = "Vehicle get error"
VEHICLE_UPDATE_ERROR = "Vehicle update error"
VEHICLE_DELETE_ERROR = "Vehicle delete error"
VEHICLE_MILEAGE_REDUCE = "Vehicle mileage can't reduced"

SERVICE_CREATE_ERROR = "Service create error"
SERVICE_GET_ERROR = "Service get error"
SERVICE_UPDATE_ERROR = "Service update error"
SERVICE_DELETE_ERROR = "Service delete error"
SERVICE_TYPE_DOES_NOT_EXIST_ERROR = "Service type doesn't exist"
SERVICE_DOES_NOT_EXIST_ERROR = "Service does not exist"

REMINDER_CREATE_ERROR = "Reminder create error"
REMINDER_GET_ERROR = "Reminder get error"
REMINDER_UPDATE_ERROR = "Reminder update error"
REMINDER_DELETE_ERROR = "Reminder delete error"
REMINDER_TYPE_DOES_NOT_EXIST_ERROR = "Reminder type doesn't exist"
REMINDER_DOES_NOT_EXIST_ERROR = "Reminder does not exist"

FUEL_CREATE_ERROR = "Fuel create error"
FUEL_GET_ERROR = "Fuel get error"
FUEL_UPDATE_ERROR = "Fuel update error"
FUEL_DELETE_ERROR = "Fuel delete error"
FUEL_DOES_NOT_EXIST_ERROR = "Fuel does not exist"

LOCATION_DOES_NOT_EXIST_ERROR = "Location doesn't exist"

INCORRECT_LOGIN_INPUT = "incorrect username or password"
PHONE_TAKEN = "User with this phone already exists"
USERNAME_TAKEN = "user with this username already exists"
EMAIL_TAKEN = "user with this email already exists"
PHONE_NUMBER_INVALID_ERROR = "Invalid phone number"

VERIFICATION_SERVICE_TEMPORARY_UNAVAILABLE = "Phone validation service temporary unavailable"
VERIFICATION_SERVICE_SEND_SMS_ERROR = "Error sending sms to phone"
VERIFICATION_CODE_CREATE_ERROR = "Can't create new verification code to phone number"
VERIFICATION_CODE_DOES_NOT_EXISTS = "Verification code doesn't exists"
VERIFICATION_CODE_IS_WRONG = "Verification code is wrong"

WRONG_TOKEN_PREFIX = "Unsupported authorization type"
MALFORMED_PAYLOAD = "Could not validate credentials"

COMMENT_DOES_NOT_EXIST = "Comment does not exist"
COMMENT_CREATE_ERROR = "Comment create error"

AUTHENTICATION_REQUIRED = "Authentication required"
AUTHORIZATION_REQUIRED = "Authorization required"

PERMISSION_DENIED = "Permission denied"

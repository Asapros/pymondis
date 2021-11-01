from datetime import datetime
from enum import Enum
from typing import Type

from backoff import on_exception, expo
from httpx import HTTPStatusError

from pymondis.enums import Season
from pymondis.exceptions import NoEnumMatch

default_backoff = on_exception(
    expo,
    HTTPStatusError,
    max_tries=3,
    giveup=lambda status: 400 <= status.response.status_code < 500
)


def parse_date(string: str) -> datetime:
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")


def get_enum_element(enum: Type[Enum], value):
    for element in enum:
        if element.value == value:
            return element
    else:
        raise NoEnumMatch(enum, value)
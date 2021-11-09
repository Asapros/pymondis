from datetime import datetime
from enum import Enum
from typing import Type

from backoff import on_exception, expo
from httpx import HTTPStatusError

from pymondis.exceptions import NoEnumMatch

default_backoff = on_exception(
    expo,
    HTTPStatusError,
    max_tries=3,
    giveup=lambda status: 400 <= status.response.status_code < 500
)


def pascal2snake(string: str) -> str:
    return ''.join(['_' + char.lower() if char.isupper() else char for char in string])[1:]


def get_enum_element(enum: Type[Enum], value) -> Enum:
    for element in enum:
        if element.value == value:
            return element
    else:
        raise NoEnumMatch(enum, value)

def date_converter(string: str) -> datetime:
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")

def enum_converter(enum: Type[Enum]):
    def inner_enum_converter(value) -> Enum:
        return get_enum_element(enum, value)

    return inner_enum_converter

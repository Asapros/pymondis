from datetime import datetime
from enum import Enum
from typing import Type

from backoff import on_exception, expo
from httpx import HTTPStatusError

from ._exceptions import NoEnumMatchError

default_backoff = on_exception(
    expo,
    HTTPStatusError,
    max_tries=3,
    giveup=lambda status: 400 <= status.response.status_code < 500
)


def get_enum_element(enum: Type[Enum], value: str) -> Enum:
    """Zamienia string-a na element enum-a"""
    for element in enum:
        if element.value == value:
            return element
    else:
        raise NoEnumMatchError(enum, value)


def get_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


def get_http_date(value: datetime) -> str:
    return value.strftime("%a, %d %b %Y %H:%M:%S GMT")


def convert_date(value: str | datetime) -> datetime:
    """Zamienia string-a na datetime"""
    return value if isinstance(value, datetime) else get_date(value)


def convert_character(string: str) -> str | None:
    """
    Zamienia 'Nazwa postaci Quatromondis' na None,
    bo ktoś stwierdził, że taka będzie wartość, jak ktoś nie ma nazwy...
    """
    return None if string == "Nazwa postaci Quatromondis" else string


def convert_empty_string(string: str) -> str | None:
    """Zamienia pustego string-a na None"""
    return string if string else None


def convert_enum(enum: Type[Enum]):
    """Wrapper get_enum_element"""

    def inner_enum_converter(value: str | Enum) -> Enum:
        return value if isinstance(value, Enum) else get_enum_element(enum, value)

    return inner_enum_converter

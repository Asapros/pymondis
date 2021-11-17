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


def get_enum_element(enum: Type[Enum], value: str) -> Enum:
    """Zamienia string-a na element enum-a"""
    for element in enum:
        if element.value == value:
            return element
    else:
        raise NoEnumMatch(enum, value)


def date_converter(value: str | datetime) -> datetime:
    """Zamienia string-a na datetime"""
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


def character_converter(string: str):
    """
    Zamienia 'Nazwa postaci Quatromondis' na None,
    bo ktoś stwierdził że taka będzie wartość jak ktoś nie ma nazwy...
    """
    if string == "Nazwa postaci Quatromondis":
        return None
    return string


def enum_converter(enum: Type[Enum]):
    """Wrapper get_enum_element"""
    def inner_enum_converter(value: str | Enum) -> Enum:
        if isinstance(value, Enum):
            return value
        return get_enum_element(enum, value)

    return inner_enum_converter

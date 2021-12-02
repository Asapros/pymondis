from asyncio import sleep
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Type

from httpx import HTTPStatusError

from ._exceptions import NoEnumMatchError


def backoff(function):
    @wraps(function)
    async def inner_backoff(*args, **kwargs):
        tries: int = 0
        while True:
            try:
                response = await function(*args, **kwargs)
                response.raise_for_status()
                return response
            except HTTPStatusError as error:
                if 400 <= error.response.status_code < 500 or tries > 2:
                    raise
                await sleep(tries + 0.5)
            tries += 1

    return inner_backoff


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

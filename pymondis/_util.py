"""
Przydatne funkcje.
"""
from asyncio import sleep
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Callable, Type

from httpx import HTTPStatusError

from ._enums import EventReservationOption
from ._exceptions import NoEnumMatchError


def backoff(function):
    """
    Dekorator funkcji wykonujących zapytania.

    :param function: funkcja do wrap-owania.
    :returns: wrap-owana funkcja.
    :raises HTTPStatusError: nie udało się pomyślnie wykonać zapytania (kod błędu 400-499 lub 3 próby zakończone >= 500).
    """
    @wraps(function)
    async def inner_backoff(*args, **kwargs):
        tries: int = 0
        while True:
            try:
                response = await function(*args, **kwargs)
                response.raise_for_status()
                return response
            except HTTPStatusError as error:
                if error.response.status_code < 500:
                    if error.response.status_code >= 400 or tries > 2:
                        raise
                    return response
                await sleep(tries + 0.5)
            tries += 1

    return inner_backoff


def enum_from_str(enum: Type[Enum], value: str) -> Enum:
    """
    Zamienia string-a na członka enum.

    :param enum: enum, w którym szukane będą wartości.
    :param value: string zamieniany na członka powyższego enum-a.
    :returns: członek enum-a.
    """
    for element in enum:
        if element.value == value:
            return element
    else:
        raise NoEnumMatchError(enum, value)


def datetime_from_string(value: str) -> datetime:
    """
    Zamienia string-a na datetime (%Y-%m-%dT%H:%M:%S).

    :param value: string do zamiany.
    :returns: datetime ze string-a.
    """
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


def string_from_datetime(value: datetime) -> str:
    """
    Zamienia datetime na string-a (%Y-%m-%dT%H:%M:%S).

    :param value: datetime do zamiany.
    :returns: string z datetime.
    """
    return value.strftime("%Y-%m-%dT%H:%M:%S")


def datetime_converter(value: str | datetime) -> datetime:
    """
    Zamienia string-a na datetime (%Y-%m-%dT%H:%M:%S) jeśli to potrzebne.

    :param value: string do ewentualnej zamiany lub datetime.
    :returns: datetime ze string-a lub podany datetime.
    """
    return value if isinstance(value, datetime) else datetime_from_string(value)


def optional_character_converter(value: str) -> str | None:
    """
    Zamienia string-a "Nazwa postaci Quatromondis" na None.
    (ktoś stwierdził, że taki będzie placeholder dla imion magicznych psorów, którzy ich nie ustawili).

    :param value: string do ewentualnej zamiany.
    :returns: ``None`` jeśli string brzmiał "Nazwa postaci Quatromondis" lub podany string.
    """
    return None if value == "Nazwa postaci Quatromondis" else value


def optional_string_converter(value: str) -> str | None:
    """
    Zamienia pustego string-a na ``None``.
    (ktoś stwierdził, że taki będzie placeholder dla braku wycieczek na turnusie).

    :param value: string do ewentualnej zamiany.
    :returns: ``None`` jeśli string był pusty (długość 0) lub podany string.
    """
    return value if value else None


def acquire_enum_converter(enum: Type[Enum]) -> Callable[[str | Enum], Enum]:
    """
    Wytwarza funkcję konwertującą string-a na element enum-a.

    :param enum: enum, w którym szukany będzie element.
    :returns: funkcja, która konwertuje string-a na element podanego enum-a, jeśli to potrzebne.
    """

    def enum_converter(value: str | Enum) -> Enum:
        """
        Zamienia string-a na element enum-a.

        :param value: string do ewentualnej zamiany.
        :returns: element enum-a ze string-a lub podany element enum-a.
        """
        return value if isinstance(value, Enum) else enum_from_str(enum, value)

    return enum_converter


def price_from_ero(option: EventReservationOption) -> int:
    """
    Zamienia EventReservationOption na odpowiadającą cenę.

    :param option: opcja rezerwacji.
    :returns: cena rezerwacji.
    :raises ValueError: ta opcja nie ma przypisanej ceny.
    """
    match option:
        case EventReservationOption.CHILD:
            return 450
        case EventReservationOption.CHILD_AND_ONE_PARENT:
            return 900
        case EventReservationOption.CHILD_AND_TWO_PARENTS:
            return 1300

    raise ValueError("Opcja rezerwacji wydarzenia nie ma przypisanej ceny.")

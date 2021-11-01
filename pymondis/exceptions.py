from enum import Enum
from typing import Type


class RevoteError(Exception):
    def __init__(self, category: str):
        super().__init__("Tried to vote for category '{}' second time".format(category))
class NoEnumMatch(Exception):
    def __init__(self, enum: Type[Enum], value):
        super().__init__("Found no matching elements in {} for value: {}".format(enum, value))
from abc import abstractmethod, ABC
from typing import Iterable

from .api import ABCHTTPClient
from .models import (
    ABCCrewMember,
    ABCWebReservationModel,
    ABCPlebisciteCandidate,
    ABCParentSurveyResult,
    ABCPurchaser,
    ABCGallery,
    ABCEventReservationSummary,
    ABCCamp
)
from ..enums import Castle


class ABCClient(ABC):
    http: ABCHTTPClient

    @abstractmethod
    async def get_camps(self) -> Iterable[ABCCamp]:
        """Zwraca listę wszystkich dostępnych obozów"""

    @abstractmethod
    async def reserve_inauguration(self, reservation: ABCEventReservationSummary) -> ABC:
        """Rezerwuje miejsce inauguracji"""

    @abstractmethod
    async def get_galleries(self, castle: Castle) -> Iterable[ABCGallery]:
        """Zwraca listę wszystkich aktualnych galerii"""

    @abstractmethod
    async def order_fwb(self, purchaser: ABCPurchaser):
        """Zamawia książkę 'QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE'"""

    @abstractmethod
    async def submit_survey(self, survey_hash: str, result: ABCParentSurveyResult):
        """Chyba ankieta jakaś ale w sumie nie wiem nie znalazłem odpowiednika na stronie..."""

    @abstractmethod
    async def get_crew(self) -> Iterable[ABCCrewMember]:
        """
        Zwraca listę wszystkich psorów
        (bez biura i HY, oni są na stałe w stronę wbudowani, chyba nie planują żadnych zmian xD)
        """

    @abstractmethod
    async def apply_for_job(self):
        """Zgłasza do pracy"""

    @abstractmethod
    async def reserve_camp(self, reservation: ABCWebReservationModel) -> Iterable[str]:
        """Rezerwuje miejsce na obozie"""

    @abstractmethod
    async def get_plebiscite(self, year: int) -> Iterable[ABCPlebisciteCandidate]:
        """Zwraca listę wszystkich kandydatów plebiscytu z danego roku"""

from abc import abstractmethod, ABC
from datetime import datetime
from typing import Iterable


class ABCHTTPClient(ABC):
    BASE_URL: str

    @abstractmethod
    async def get_resource(self, url: str, cache_time: datetime | None = None, cache_content: bytes | None = None) -> bytes:
        """Zwraca resource"""

    @abstractmethod
    async def get_camps(self) -> Iterable:
        """Zwraca listę wszystkich dostępnych obozów"""

    @abstractmethod
    async def post_inauguration(self, reservation_model: dict):
        """Rezerwuje miejsce na inauguracji"""

    @abstractmethod
    async def get_galleries(self, castle: str) -> Iterable:
        """Zwraca listę wszystkich aktualnych galerii"""

    @abstractmethod
    async def get_gallery(self, gallery_id: int) -> Iterable:
        """Zwraca listę url-i do wszystkich zdjęć z galerii"""

    @abstractmethod
    async def post_fwb(self, purchaser: dict):
        """Zamawia książkę 'QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE'"""

    @abstractmethod
    async def post_survey(self, survey_hash: str, result: dict):
        """Chyba ankieta jakaś ale w sumie nie wiem nie znalazłem odpowiednika na stronie..."""

    @abstractmethod
    async def get_crew(self) -> Iterable:
        """
        Zwraca listę wszystkich psorów
        (bez biura i HY, oni są na stałe w stronę wbudowani, chyba nie planują żadnych zmian...)
        """

    @abstractmethod
    async def post_apply(self):
        """Zgłasza do pracy"""

    @abstractmethod
    async def post_subscribe(self, reservation_model: dict) -> Iterable:
        """Rezerwuje miejsce na obozie"""

    @abstractmethod
    async def post_manage(self, pri: dict) -> dict:
        """Zwraca dane rezerwacji"""

    @abstractmethod
    async def patch_vote(self, category: str, name: str):
        """Głosuje na kandydata z aktualnego plebiscytu"""

    @abstractmethod
    async def get_plebiscite(self, year: int) -> Iterable:
        """Zwraca listę wszystkich kandydatów plebiscytu z danego roku"""

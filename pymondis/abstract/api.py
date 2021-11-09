from abc import abstractmethod, ABC
from datetime import datetime
from typing import Iterable, Tuple


class ABCHTTPClient(ABC):
    BASE_URL: str

    @abstractmethod
    async def get_resource(self, url: str, cache_time: datetime | None = None, cache_content: bytes | None = None) -> bytes:
        """Get the resource and resource's last modification timestamp"""

    @abstractmethod
    async def get_camps(self) -> Iterable:
        """Get all current camps"""

    @abstractmethod
    async def post_inauguration(self, reservation_model: dict):
        """Reserve inauguration"""

    @abstractmethod
    async def get_galleries(self, castle: str) -> Iterable:
        """Get all current galleries from a castle"""

    @abstractmethod
    async def get_gallery(self, gallery_id: int) -> Iterable:
        """Get a gallery by id"""

    @abstractmethod
    async def post_fwb(self, purchaser: dict):
        """Order a 'QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE' book"""

    @abstractmethod
    async def post_survey(self, survey_hash: str, result: dict):
        """Post your opinion about a camp"""

    @abstractmethod
    async def get_crew(self) -> Iterable:
        """Get the whole crew"""

    @abstractmethod
    async def post_apply(self):
        """Apply for the job"""

    @abstractmethod
    async def post_subscribe(self, reservation_model: dict) -> Iterable:
        """Reserve a camp"""

    @abstractmethod
    async def post_manage(self, pri: dict) -> dict:
        """Manage a reservation"""

    @abstractmethod
    async def patch_vote(self, category: str, name: str):
        """Vote for a legend/hero"""

    @abstractmethod
    async def get_plebiscite(self, year: int) -> Iterable:
        """Get all candidates for the plebiscite"""

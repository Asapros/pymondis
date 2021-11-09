from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Iterable

from .api import ABCHTTPClient
from ..enums import Castle, CampLevel, World, Season, EventReservationOption


# NOT IMPLEMENTED

class ABCPlebisciteCandidate(ABC):
    pass


class ABCParentSurveyResult(ABC):
    pass


class ABCWebReservationModel(ABC):
    pass


class ABCCrewMember(ABC):
    pass


# IMPLEMENTED

class ABCEventReservationSummary(ABC):
    price: int
    option: EventReservationOption
    name: str
    surname: str
    parent_name: str
    parent_surname: str
    parent_reused: bool
    phone: str
    email: str
    first_parent_name: str | None
    first_parent_surname: str | None
    second_parent_name: str | None
    second_parent_surname: str | None

    @abstractmethod
    def to_dict(self) -> dict:
        """Zwraca dicta gotowego do wysłania"""


class ABCCamp(ABC):
    class ABCTransport(ABC):
        city: str
        one_way_price: int
        two_way_price: int

    camp_id: int
    code: str
    place: Castle
    price: int
    promo: int | None
    active: bool
    places_left: int
    program: str
    level: CampLevel
    world: World
    season: Season
    trip: str | None
    start: datetime
    end: datetime
    ages: List[str]  # Może jakieś range czy coś???
    transports: List[ABCTransport]


class ABCPersonalReservationInfo(ABC):
    reservation_id: str
    surname: str


class ABCPurchaser(ABC):
    name: str
    surname: str
    email: str
    phone: str
    parcel_locker: str

    @abstractmethod
    def to_dict(self) -> dict:
        """Zwraca dicta gotowego do wysłania"""


class ABCResource(ABC):
    url: str
    _http: ABCHTTPClient | None
    _cache_time: datetime | None
    _cache_content: bytes | None

    @abstractmethod
    async def get(
            self,
            use_cache: bool = True,
            update_cache: bool = True,
            http: ABCHTTPClient | None = None
    ) -> bytes:
        """Request a resource"""


class ABCGallery(ABC):
    class ABCPhoto(ABC):
        normal: ABCResource
        large: ABCResource

    gallery_id: int
    start: datetime
    end: datetime
    name: str
    empty: bool
    _http: ABCHTTPClient

    @abstractmethod
    async def get_photos(self, http: ABCHTTPClient | None = None) -> Iterable[ABCPhoto]:
        """Request all photos in the gallery"""


# MACROS

ABCCampTransport = ABCCamp.ABCTransport
ABCGalleryPhoto = ABCGallery.ABCPhoto

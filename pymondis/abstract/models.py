from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Iterable

from .api import ABCHTTPClient
from ..enums import Castle, CampLevel, World, Season, EventReservationOption, CrewRole, TShirtSize, SourcePoll


# NOT IMPLEMENTED

class ABCReservationManageDetails(ABC):
    pass


class ABCParentSurveyResult(ABC):
    pass


# IMPLEMENTED


class ABCPlebisciteCandidate(ABC):
    name: str
    category: str
    votes: int | None
    plebiscite: str | None
    voted: bool | None
    _http: ABCHTTPClient | None

    @classmethod
    @abstractmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "ABCPlebisciteCandidate":
        """Tworzy obiekt na podstawie dicta"""

    @abstractmethod
    async def vote(self, http: ABCHTTPClient | None):
        """Głosuje na kandydata"""


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

        @classmethod
        @abstractmethod
        def init_from_dict(cls, data: dict) -> "ABCTransport":
            """Tworzy obiekt na podstawie dicta"""

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

    @classmethod
    @abstractmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "ABCCamp":
        """Tworzy obiekt na podstawie dicta"""


class ABCPersonalReservationInfo(ABC):
    reservation_id: str
    surname: str
    _http: ABCHTTPClient | None

    @abstractmethod
    def to_dict(self) -> dict:
        """Zwraca dicta gotowego do wysłania"""

    async def get_info(self, http: ABCHTTPClient | None) -> ABCReservationManageDetails:
        """Zwraca informacje o rezerwacji"""


class ABCWebReservationModel(ABC):
    class ABCChild(ABC):
        name: str
        surname: str
        t_shirt_size: TShirtSize
        birthdate: datetime

        @abstractmethod
        def to_dict(self) -> dict:
            """Zwraca dicta gotowego do wysłania"""

    camp_id: int
    child: ABCChild
    parent_name: str
    parent_surname: str
    nip: str
    email: str
    phone: str
    poll: SourcePoll
    siblings: List[ABCChild]
    promo_code: str | None
    _http: ABCHTTPClient | None

    @abstractmethod
    def to_dict(self) -> dict:
        """Zwraca dicta gotowego do wysłania"""

    @property
    @abstractmethod
    def pri(self, **kwargs) -> ABCPersonalReservationInfo:
        """Zwraca utworzone na podstawie modelu PersonalReservationInfo"""


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
        """Zwraca resource w bajtach"""


class ABCCrewMember(ABC):
    name: str
    surname: str
    character: str
    position: CrewRole
    description: str
    photo: ABCResource

    @classmethod
    @abstractmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "ABCCrewMember":
        """Tworzy obiekt na podstawie dicta"""


class ABCGallery(ABC):
    class ABCPhoto(ABC):
        normal: ABCResource
        large: ABCResource

        @classmethod
        @abstractmethod
        def init_from_dict(cls, data: dict, **kwargs) -> "ABCPhoto":
            """Tworzy obiekt na podstawie dicta"""

    gallery_id: int
    start: datetime | None
    end: datetime | None
    name: str | None
    empty: bool | None
    _http: ABCHTTPClient | None

    @abstractmethod
    async def get_photos(self, http: ABCHTTPClient | None = None) -> Iterable[ABCPhoto]:
        """Zwraca wszystkie zdjęcia z galerii"""

    @classmethod
    @abstractmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "ABCGallery":
        """Tworzy obiekt na podstawie dicta"""


# MACROS

ABCCampTransport = ABCCamp.ABCTransport
ABCGalleryPhoto = ABCGallery.ABCPhoto
ABCChild = ABCWebReservationModel.ABCChild

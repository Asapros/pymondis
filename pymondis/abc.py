from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from pymondis.enums import Castle, CampLevel, World, Season, EventReservationOption


class ABCEventReservationSummary(ABC):
    price: int
    option: EventReservationOption
    name: str
    surname: str
    parent_name: str
    parent_surname: str
    parent_reused: bool
    phone: int
    email: str
    first_parent_name: str | None
    first_parent_surname: str | None
    second_parent_name: str | None
    second_parent_surname: str | None

    @abstractmethod
    def __init__(
            self,
            price: int,
            option: EventReservationOption,
            name: str,
            surname: str,
            phone: int,
            email: str,
            parent_reused: bool = False,
            first_parent_name: str | None = None,
            first_parent_surname: str | None = None,
            second_parent_name: str | None = None,
            second_parent_surname: str | None = None
    ):
        """Object initialization"""

    @abstractmethod
    def jsonify(self) -> dict:
        """Returns object's dict ready to be sent"""


class ABCParentSurveyResult(ABC):
    pass


class ABCWebReservationModel(ABC):
    pass


class ABCCamp(ABC):
    class ABCTransport(ABC):
        city: str
        one_way_price: int
        two_way_price: int

        @abstractmethod
        def __init__(self, city: str, one_way_price: int, two_way_price: int):
            """Object initialization"""

        @abstractmethod
        def __str__(self) -> str:
            """str(Object)"""

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

    @abstractmethod
    def __init__(self, camp_id: int, code: str, place: str, price: int, promo: int | None, active: bool,
                 places_left: int, program: str, level: str, world: str, season: str, trip: str, start: str, end: str,
                 ages: List[str], transports: List[ABCTransport]):
        """Object initialization"""

    @abstractmethod
    def __str__(self) -> str:
        """str(Object)"""



class ABCPersonalReservationInfo(ABC):
    reservation_id: int
    surname: str

    @abstractmethod
    def __init__(self, reservation_id: int, surname: str):
        """Object initialization"""

    @abstractmethod
    def __str__(self):
        """str(Object)"""


class ABCPurchaser(ABC):
    name: str
    surname: str
    email: str
    phone: int
    parcel_locker: str

    @abstractmethod
    def __init__(self, name: str, surname: str, email: str, phone: str, parcel_locker: str):
        """Object initialization"""

    @abstractmethod
    def __str__(self) -> str:
        """str(Object)"""


class ABCHTTPClient(ABC):
    BASE: str

    @abstractmethod
    async def get_camps(self):
        """Get all current camps"""

    @abstractmethod
    async def post_inauguration(self):
        """Reserve inauguration"""

    @abstractmethod
    async def get_galleries(self, castle: Castle):
        """Get all current galleries from a castle"""

    @abstractmethod
    async def get_gallery(self, gallery_id: int):
        """Get a gallery by id"""

    @abstractmethod
    async def post_fwb(self, purchaser: ABCPurchaser):
        """Order a 'QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE' book"""

    @abstractmethod
    async def post_survey(self, survey_hash: str, result: ABCParentSurveyResult):
        """Post your opinion about a camp"""

    @abstractmethod
    async def get_crew(self):
        """Get the whole crew"""

    @abstractmethod
    async def post_apply(self):
        """Apply for the job"""

    @abstractmethod
    async def post_subscribe(self, reservation: ABCWebReservationModel):
        """Reserve a camp"""

    @abstractmethod
    async def post_manage(self, pri: ABCPersonalReservationInfo):
        """Manage a reservation"""

    @abstractmethod
    async def patch_vote(self, category: str, name: str):
        """Vote for a legend/hero"""

    @abstractmethod
    async def get_plebiscite(self, year: int):
        """Get all candidates for the plebiscite"""


class ABCResource(ABC):
    _client: ABCHTTPClient
    url: str
    md5: str
    content: bytes

    @abstractmethod
    def __init__(self, url: str, client: ABCHTTPClient | None = None):
        """Object initialization"""

    @abstractmethod
    async def get(self, use_cache: bool = True, update_cache: bool = True, client: ABCHTTPClient | None = None) -> bytes:
        """Request a resource"""

    @abstractmethod
    def __str__(self) -> str:
        """str(Object)"""


class ABCGallery(ABC):
    class ABCGalleryPhoto(ABC):
        normal: ABCResource
        large: ABCResource

        @abstractmethod
        def __init__(self, url: str, enlarged_url: str):
            """Object initialization"""

    gallery_id: int
    start: datetime
    end: datetime
    name: str
    empty: bool
    _client: ABCHTTPClient

    @abstractmethod
    def __init__(self, gallery_id: int, start: str, end: str, name: str, has_photos: bool, client: ABCHTTPClient | None = None):
        """Object initialization"""

    @abstractmethod
    async def get_photos(self, client: ABCHTTPClient | None = None) -> List[ABCResource]:
        """Request all photos in the gallery"""


ABCTransport = ABCCamp.ABCTransport
ABCGalleryPhoto = ABCGallery.ABCGalleryPhoto

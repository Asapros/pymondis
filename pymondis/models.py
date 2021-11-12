from datetime import datetime
from typing import List

from attr import attrib, attrs
from attr.validators import instance_of, optional as v_optional, deep_iterable
from attr.converters import optional as c_optional

from exceptions import RevoteError
from .abstract.api import ABCHTTPClient
from .abstract.models import (
    ABCResource,
    ABCGallery,
    ABCGalleryPhoto,
    ABCCamp,
    ABCCampTransport,
    ABCPurchaser,
    ABCPersonalReservationInfo,
    ABCEventReservationSummary,
    ABCCrewMember,
    ABCPlebisciteCandidate,
    ABCWebReservationModel,
    ABCChild,
    ABCReservationManageDetails
)
from .api import HTTPClient
from .enums import Castle, CampLevel, World, Season, EventReservationOption, CrewRole, TShirtSize, SourcePoll
from .util import enum_converter, date_converter, character_converter


@attrs(repr=True, slots=True)
class Resource(ABCResource):
    url = attrib(
        type=str,
        validator=instance_of(str)
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        default=None,
        validator=v_optional(
            instance_of(ABCHTTPClient)
        ),
        repr=False
    )
    _cache_time = attrib(
        type=datetime | None,
        default=None,
        validator=v_optional(
            instance_of(datetime)
        ),
        kw_only=True,
        repr=False
    )
    _cache_content = attrib(
        type=bytes | None,
        default=None,
        kw_only=True,
        repr=False
    )

    async def get(self, use_cache: bool = True, update_cache: bool = True, http: ABCHTTPClient | None = None) -> bytes:
        arguments = self._cache_time, self._cache_content if use_cache else ()
        async with http or self._http or HTTPClient() as client:
            content = await client.get_resource(self.url, *arguments)
        if update_cache:
            self._cache_time = datetime.now()
            self._cache_content = content
        return content

    def __eq__(self, other: "Resource") -> bool:
        return self.url == other.url


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Gallery(ABCGallery):
    @attrs(repr=True, slots=True, frozen=True, hash=True)
    class Photo(ABCGalleryPhoto):
        normal = attrib(
            type=ABCResource,
            validator=instance_of(ABCResource)
        )
        large = attrib(
            type=ABCResource,
            validator=instance_of(ABCResource)
        )

        @classmethod
        def init_from_dict(cls, data: dict, **kwargs) -> "Photo":
            return cls(
                normal=Resource(data["AlbumUrl"], **kwargs),
                large=Resource(data["EnlargedUrl"], **kwargs)
            )

    gallery_id = attrib(
        type=int,
        validator=instance_of(int)
    )
    start = attrib(
        type=datetime | None,
        converter=c_optional(
            date_converter
        ),
        validator=v_optional(
            instance_of(datetime)
        ),
        default=None
    )
    end = attrib(
        type=datetime | None,
        converter=c_optional(
            date_converter
        ),
        validator=v_optional(
            instance_of(datetime)
        ),
        default=None
    )
    name = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        ),
        default=None
    )
    empty = attrib(
        type=bool | None,
        validator=v_optional(
            instance_of(bool)
        ),
        default=None
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        validator=v_optional(
            instance_of(ABCHTTPClient),
        ),
        default=None,
        repr=False
    )

    async def get_photos(self, http: ABCHTTPClient | None = None) -> List[Photo]:
        client = http or self._http or HTTPClient()
        photos = await client.get_gallery(self.gallery_id)
        return [
            self.Photo.init_from_dict(photo, http=client)
            for photo in photos
        ]

    @classmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "Gallery":
        return cls(
            gallery_id=data["Id"],
            start=data["StartDate"],
            end=data["EndDate"],
            name=data["Name"],
            empty=not data["HasPhotos"],
            **kwargs
        )


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Camp(ABCCamp):
    @attrs(repr=True, slots=True, frozen=True, hash=True)
    class Transport(ABCCampTransport):
        city = attrib(
            type=str,
            validator=instance_of(str)
        )
        one_way_price = attrib(
            type=int,
            validator=instance_of(int)
        )
        two_way_price = attrib(
            type=int,
            validator=instance_of(int)
        )

        @classmethod
        def init_from_dict(cls, data: dict) -> "Transport":
            return cls(
                city=data["City"],
                one_way_price=data["OneWayPrice"],
                two_way_price=data["TwoWayPrice"]
            )

    camp_id = attrib(
        type=int,
        validator=instance_of(int)
    )
    code = attrib(
        type=str,
        validator=instance_of(str)
    )
    place = attrib(
        type=Castle,
        converter=enum_converter(Castle),
        validator=instance_of(Castle)
    )
    price = attrib(
        type=int,
        validator=instance_of(int)
    )
    promo = attrib(
        type=int | None,
        validator=v_optional(
            instance_of(int)
        )
    )
    active = attrib(
        type=bool,
        validator=instance_of(bool)
    )
    places_left = attrib(
        type=int,
        validator=instance_of(int)
    )
    program = attrib(
        type=str,
        validator=instance_of(str)
    )
    level = attrib(
        type=CampLevel,
        converter=enum_converter(CampLevel),
        validator=instance_of(CampLevel)
    )
    world = attrib(
        type=World,
        converter=enum_converter(World),
        validator=instance_of(World)
    )
    season = attrib(
        type=Season,
        converter=enum_converter(Season),
        validator=instance_of(Season)
    )
    trip = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        )
    )
    start = attrib(
        type=datetime,
        converter=lambda value: value if isinstance(value, datetime) else date_converter(value),
        validator=instance_of(datetime)
    )
    end = attrib(
        type=datetime,
        converter=lambda value: value if isinstance(value, datetime) else date_converter(value),
        validator=instance_of(datetime)
    )
    ages = attrib(
        type=List[str],
        validator=deep_iterable(
            instance_of(str)
        )
    )
    transports = attrib(
        type=List[ABCCampTransport],
        validator=deep_iterable(
            instance_of(ABCCampTransport)
        )
    )

    @classmethod
    def init_from_dict(cls, data: dict) -> "Camp":
        return cls(
            data["Id"],
            data["Code"],
            data["Place"],
            data["Price"],
            data["Promo"],
            data["IsActive"],
            data["PlacesLeft"],
            data["Program"],
            data["Level"],
            data["World"],
            data["Season"],
            data["Trip"],
            data["StartDate"],
            data["EndDate"],
            data["Ages"],
            [
                cls.Transport.init_from_dict(transport)
                for transport in data["Transports"]
            ]
        )


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Purchaser(ABCPurchaser):
    name = attrib(
        type=str,
        validator=instance_of(str)
    )
    surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    email = attrib(
        type=str,
        validator=instance_of(str)
    )
    phone = attrib(
        type=str,
        validator=instance_of(str)
    )
    parcel_locker = attrib(
        type=str,
        validator=instance_of(str)
    )

    def to_dict(self) -> dict:
        return {
            "Name": self.name,
            "Surname": self.surname,
            "Email": self.email,
            "Phone": self.phone,
            "ParcelLocker": self.parcel_locker
        }


@attrs(repr=True, slots=True, frozen=True, hash=True)
class PersonalReservationInfo(ABCPersonalReservationInfo):
    reservation_id = attrib(
        type=str,
        validator=instance_of(str)
    )
    surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        validator=instance_of(ABCHTTPClient),
        default=None,
        repr=False
    )

    def to_dict(self) -> dict:
        return {
            "ReservationId": self.reservation_id,
            "Surname": self.surname
        }

    async def get_info(self, http: ABCHTTPClient | None) -> ABCReservationManageDetails:
        raise NotImplementedError()


@attrs(repr=True, slots=True, frozen=True, hash=True)
class WebReservationModel(ABCWebReservationModel):
    class Child(ABCChild):
        name = attrib(
            type=str,
            validator=instance_of(str)
        )
        surname = attrib(
            type=str,
            validator=instance_of(str)
        )
        t_shirt_size = attrib(
            type=TShirtSize,
            converter=enum_converter(TShirtSize),
            validator=instance_of(TShirtSize)
        )
        birthdate = attrib(
            type=datetime,
            converter=date_converter,
            validator=instance_of(datetime)
        )

        def to_dict(self) -> dict:
            return {
                "Name": self.name,
                "Surname": self.surname,
                "Tshirt": self.t_shirt_size.value,
                "Dob": self.birthdate
            }

    camp_id = attrib(
        type=int,
        validator=instance_of(int)
    )
    child = attrib(
        type=Child,
        validator=instance_of(ABCChild)
    )
    parent_name = attrib(
        type=str,
        validator=instance_of(str)
    )
    parent_surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    nip = attrib(
        type=str,
        validator=instance_of(str)
    )
    email = attrib(
        type=str,
        validator=instance_of(str)
    )
    phone = attrib(
        type=str,
        validator=instance_of(str)
    )
    poll = attrib(
        type=SourcePoll,
        converter=enum_converter(SourcePoll),
        validator=instance_of(SourcePoll)
    )
    siblings = attrib(
        type=List[ABCChild],
        validator=deep_iterable(
            instance_of(ABCChild)
        ),
        factory=list
    )
    promo_code = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        ),
        default=None
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        validator=v_optional(
            instance_of(ABCHTTPClient)
        ),
        default=None,
        repr=False
    )

    def to_dict(self) -> dict:
        return {
            "SubcampId": self.camp_id,
            "Childs": {  # English 100
                "Main": self.child.to_dict(),
                "Siblings": [sibling.to_dict() for sibling in self.siblings]
            },
            "Parent": {
                "Name": self.parent_name,
                "Surname": self.parent_surname,
                "Nip": self.nip
            },
            "Details": {
                "Email": self.email,
                "Phone": self.phone,
                "Promo": self.promo_code,
                "Poll": self.poll.value
            }
        }

    @property
    def pri(self, **kwargs) -> PersonalReservationInfo:
        kwargs = {"http": self._http} | kwargs
        return PersonalReservationInfo(self.camp_id, self.parent_surname, **kwargs)


@attrs(repr=True, slots=True, frozen=True, hash=True)
class EventReservationSummary(ABCEventReservationSummary):
    option = attrib(
        type=EventReservationOption,
        converter=enum_converter(EventReservationOption),
        validator=instance_of(EventReservationOption)
    )
    name = attrib(
        type=str,
        validator=instance_of(str)
    )
    surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    parent_name = attrib(
        type=str,
        validator=instance_of(str)
    )
    parent_surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    parent_reused = attrib(
        type=bool,
        validator=instance_of(bool)
    )
    phone = attrib(
        type=str,
        validator=instance_of(str)
    )
    email = attrib(
        type=str,
        validator=instance_of(str)
    )
    first_parent_name = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        )
    )
    first_parent_surname = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        )
    )
    second_parent_name = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        )
    )
    second_parent_surname = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        )
    )
    _price = attrib(
        type=int,
        validator=v_optional(
            instance_of(int)
        ),
        kw_only=True
    )

    @property
    def price(self) -> int:
        if self._price is None:
            match self.option:
                case EventReservationOption.CHILD:
                    return 450
                case EventReservationOption.CHILD_AND_ONE_PARENT:
                    return 900
                case EventReservationOption.CHILD_AND_TWO_PARENTS:
                    return 1300
            raise ValueError("Option is not one of the enum elements")
        return self._price

    def to_dict(self) -> dict:
        data = {
            "Price": self.price,
            "Name": self.name,
            "Surname": self.surname,
            "ParentName": self.parent_name,
            "ParentSurname": self.parent_surname,
            "IsParentReused": self.parent_reused,
            "Phone": self.phone,
            "Email": self.email
        }
        if self.option in (EventReservationOption.CHILD, EventReservationOption.CHILD_AND_PARENT):
            data.update({"FirstParentName": self.first_parent_name, "FirstParentSurname": self.first_parent_surname})
        if self.option is EventReservationOption.CHILD_AND_TWO_PARENTS:
            data.update(
                {"SecondParentName": self.second_parent_name, "SecondParentSurname": self.second_parent_surname})
        return data


@attrs(repr=True, slots=True, frozen=True, hash=True)
class CrewMember(ABCCrewMember):
    name = attrib(
        type=str,
        validator=instance_of(str)
    )
    surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    character = attrib(
        type=str | None,
        converter=character_converter,
        validator=v_optional(
            instance_of(str)
        )
    )
    position = attrib(
        type=CrewRole,
        converter=enum_converter(CrewRole),
        validator=instance_of(CrewRole)
    )
    description = attrib(
        type=str,
        validator=instance_of(str)
    )
    photo = attrib(
        type=Resource,
        validator=instance_of(Resource)
    )

    @classmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "CrewMember":
        return cls(
            name=data["Name"],
            surname=data["Surname"],
            character=data["Character"].strip(),
            position=data["Position"],
            description=data["Description"],
            photo=Resource(data["PhotoUrl"], **kwargs)
        )


@attrs(repr=True, slots=True, frozen=True, hash=True)
class PlebisciteCandidate(ABCPlebisciteCandidate):
    name = attrib(
        type=str,
        validator=instance_of(str)
    )
    category = attrib(
        type=str,
        validator=instance_of(str)
    )
    votes = attrib(
        type=int | None,
        validator=v_optional(
            instance_of(int)
        )
    )
    plebiscite = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        )
    )
    voted = attrib(
        type=bool | None,
        validator=v_optional(
            instance_of(bool)
        )
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        validator=v_optional(
            instance_of(ABCHTTPClient)
        ),
        repr=False
    )

    @classmethod
    def init_from_dict(cls, data: dict, **kwargs) -> "PlebisciteCandidate":
        return cls(
            name=data["Name"],
            votes=data["Result"],
            category=data["Category"],
            plebiscite=data["Plebiscite"],
            voted=data["WasVoted"],
            **kwargs
        )

    async def vote(self, http: ABCHTTPClient | None):
        if self.voted:
            raise RevoteError(self.category)
        async with http or self._http or HTTPClient() as client:
            await client.patch_vote(self.category, self.name)


GalleryPhoto = Gallery.Photo
CampTransport = Camp.Transport
Child = WebReservationModel.Child

from datetime import datetime
from typing import List, Tuple

from attr import attrib, attrs
from attr.validators import instance_of, optional, deep_iterable

from .abstract.api import ABCHTTPClient
from .abstract.models import ABCResource, ABCGallery, ABCGalleryPhoto, ABCCamp, ABCCampTransport, ABCPurchaser, \
    ABCPersonalReservationInfo, ABCEventReservationSummary
from .api import HTTPClient
from .enums import Castle, CampLevel, World, Season, EventReservationOption
from .util import enum_converter, date_converter


@attrs(str=True, slots=True)
class Resource(ABCResource):
    url = attrib(
        type=str,
        validator=instance_of(str)
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        default=None,
        validator=optional(
            instance_of(ABCHTTPClient)
        )
    )
    _cache_time = attrib(
        type=datetime | None,
        default=None,
        validator=optional(
            instance_of(datetime)
        ),
        kw_only=True
    )
    _cache_content = attrib(
        type=bytes | None,
        default=None,
        kw_only=True
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


@attrs(str=True, slots=True, frozen=True, hash=True)
class Gallery(ABCGallery):
    @attrs(str=True, slots=True, frozen=True, hash=True)
    class Photo(ABCGalleryPhoto):
        normal = attrib(
            type=ABCResource,
            validator=instance_of(ABCResource)
        )
        large = attrib(
            type=ABCResource,
            validator=instance_of(ABCResource)
        )

    gallery_id = attrib(
        type=int,
        validator=instance_of(int)
    )
    start = attrib(
        type=datetime,
        validator=instance_of(datetime)
    )
    end = attrib(
        type=datetime,
        validator=instance_of(datetime)
    )
    name = attrib(
        type=str,
        validator=instance_of(str)
    )
    empty = attrib(
        type=bool,
        validator=instance_of(bool)
    )
    _http = attrib(
        type=ABCHTTPClient | None,
        default=None,
        validator=optional(
            instance_of(ABCHTTPClient)
        )
    )

    async def get_photos(self, http: ABCHTTPClient | None = None) -> Tuple[Photo, ...]:
        async with http or self._http or HTTPClient() as client:
            photos = await client.get_gallery(self.gallery_id)
        return (
            self.Photo(
                Resource(photo["AlbumUrl"], client),
                Resource(photo["EnlargedUrl"], client)
            )
            for photo in photos
        )

    def __eq__(self, other: "Gallery") -> bool:
        return self.gallery_id == other.gallery_id


@attrs(str=True, slots=True, frozen=True, hash=True)
class Camp(ABCCamp):
    @attrs(str=True, slots=True, frozen=True, hash=True)
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
        validator=optional(instance_of(int))
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
        validator=optional(instance_of(str))
    )
    start = attrib(
        type=datetime,
        converter=date_converter,
        validator=instance_of(datetime)
    )
    end = attrib(
        type=datetime,
        converter=date_converter,
        validator=instance_of(datetime)
    )
    ages = attrib(
        type=List[str],
        validator=deep_iterable(instance_of(str))
    )
    transports = attrib(
        type=List[ABCCampTransport],
        validator=deep_iterable(instance_of(ABCCampTransport))
    )

    @classmethod
    def init_from_dict(cls, data: dict):
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
                CampTransport(
                    transport["City"],
                    transport["OneWayPrice"],
                    transport["TwoWayPrice"]
                ) for transport in data["Transports"]
            ]
        )


@attrs(str=True, slots=True, frozen=True, hash=True)
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


@attrs(str=True, slots=True, frozen=True, hash=True)
class PersonalReservationInfo(ABCPersonalReservationInfo):
    reservation_id = attrib(
        type=str,
        validator=instance_of(str)
    )
    surname = attrib(
        type=str,
        validator=instance_of(str)
    )


@attrs(str=True, slots=True, frozen=True, hash=True)
class EventReservationSummary(ABCEventReservationSummary):
    price = attrib(
        type=int,
        validator=instance_of(int)
    )
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
        validator=optional(instance_of(str))
    )
    first_parent_surname = attrib(
        type=str | None,
        validator=optional(instance_of(str))
    )
    second_parent_name = attrib(
        type=str | None,
        validator=optional(instance_of(str))
    )
    second_parent_surname = attrib(
        type=str | None,
        validator=optional(instance_of(str))
    )


GalleryPhoto = Gallery.Photo
CampTransport = Camp.Transport

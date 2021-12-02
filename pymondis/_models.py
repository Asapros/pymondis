from datetime import datetime
from warnings import warn

from attr import attrib, attrs
from attr.validators import instance_of, optional as v_optional, deep_iterable
from attr.converters import optional as c_optional

from ._exceptions import RevoteError, NotFullyImplementedWarning
from ._api import HTTPClient
from ._enums import Castle, CampLevel, World, Season, EventReservationOption, CrewRole, TShirtSize, SourcePoll
from ._util import convert_enum, convert_date, convert_character, convert_empty_string, out_get_date


@attrs(repr=True, slots=True, frozen=True, hash=True)
class ParentSurveyResult:
    pass


@attrs(repr=True, slots=True, frozen=True, hash=True)
class ReservationManageDetails:
    pass


@attrs(repr=True, slots=True, eq=False)
class Resource:
    url = attrib(
        type=str,
        validator=instance_of(str)
    )
    _http = attrib(
        type=HTTPClient | None,
        default=None,
        validator=v_optional(
            instance_of(HTTPClient)
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

    async def get(self, use_cache: bool = True, update_cache: bool = True, http: HTTPClient | None = None) -> bytes:
        # Spoiler - Lock-i działają wolniej w tym przypadku...
        arguments = (self._cache_time, self._cache_content) if use_cache else ()
        client = http or self._http
        content = await client.get_resource(self.url, *arguments)
        if update_cache:
            self._cache_time = datetime.now()
            self._cache_content = content
        return content

    def __eq__(self, other: "Resource") -> bool:
        return self.url == other.url


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Gallery:
    @attrs(repr=True, slots=True, frozen=True, hash=True)
    class Photo:
        normal = attrib(
            type=Resource,
            validator=instance_of(Resource)
        )
        large = attrib(
            type=Resource,
            validator=instance_of(Resource)
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
            convert_date
        ),
        validator=v_optional(
            instance_of(datetime)
        ),
        default=None
    )
    end = attrib(
        type=datetime | None,
        converter=c_optional(
            convert_date
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
        type=HTTPClient | None,
        validator=v_optional(
            instance_of(HTTPClient),
        ),
        default=None,
        repr=False
    )

    async def get_photos(self, http: HTTPClient | None = None) -> list[Photo]:
        client = http or self._http
        photos = await client.get_images_galleries(self.gallery_id)
        return [
            self.Photo.init_from_dict(photo, http=client)
            for photo in photos
        ]

    @classmethod
    def init_from_dict(cls, data: dict[str, str | int | bool], **kwargs) -> "Gallery":
        return cls(
            gallery_id=data["Id"],
            start=data["StartDate"],
            end=data["EndDate"],
            name=data["Name"],
            empty=not data["HasPhotos"],
            **kwargs
        )


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Camp:
    @attrs(repr=True, slots=True, frozen=True, hash=True)
    class Transport:
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
        def init_from_dict(cls, data: dict[str, str | int]) -> "Transport":
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
        converter=convert_enum(Castle),
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
        converter=convert_enum(CampLevel),
        validator=instance_of(CampLevel)
    )
    world = attrib(
        type=World,
        converter=convert_enum(World),
        validator=instance_of(World)
    )
    season = attrib(
        type=Season,
        converter=convert_enum(Season),
        validator=instance_of(Season)
    )
    trip = attrib(
        type=str | None,
        converter=convert_empty_string,
        validator=v_optional(
            instance_of(str)
        )
    )
    start = attrib(
        type=datetime,
        converter=convert_date,
        validator=instance_of(datetime)
    )
    end = attrib(
        type=datetime,
        converter=convert_date,
        validator=instance_of(datetime)
    )
    ages = attrib(
        type=list[str],
        validator=deep_iterable(
            instance_of(str)
        )
    )
    transports = attrib(
        type=list[Transport],
        validator=deep_iterable(
            instance_of(Transport)
        )
    )

    @classmethod
    def init_from_dict(cls, data: dict[str, str | int | bool | None | list[str | dict[str, str | int]]]) -> "Camp":
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
class Purchaser:
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

    def to_dict(self) -> dict[str, str]:
        return {
            "Name": self.name,
            "Surname": self.surname,
            "Email": self.email,
            "Phone": self.phone,
            "ParcelLocker": self.parcel_locker
        }


@attrs(repr=True, slots=True, frozen=True, hash=True)
class PersonalReservationInfo:
    reservation_id = attrib(
        type=str,
        validator=instance_of(str)
    )
    surname = attrib(
        type=str,
        validator=instance_of(str)
    )
    _http = attrib(
        type=HTTPClient | None,
        validator=instance_of(HTTPClient),
        default=None,
        repr=False
    )

    def to_dict(self) -> dict[str, str]:
        return {
            "ReservationId": self.reservation_id,
            "Surname": self.surname
        }

    async def get_details(self, http: HTTPClient | None) -> dict[str, str | bool]:
        warn(
            "Ta metoda będzie w przyszłości zwracała ReservationMangeDetails."
            "Jeśli chcesz pomóc w jej implementacji otwórz nowy issue: https://github.com/Asapros/pymondis/issues",
            NotFullyImplementedWarning
        )
        client = http or self._http
        details = await client.post_reservations_manage(self.to_dict())
        return details


@attrs(repr=True, slots=True, frozen=True, hash=True)
class WebReservationModel:
    class Child:
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
            validator=instance_of(TShirtSize)
        )
        birthdate = attrib(
            type=datetime,
            validator=instance_of(datetime)
        )

        def to_dict(self) -> dict[str, str]:
            return {
                "Name": self.name,
                "Surname": self.surname,
                "Tshirt": self.t_shirt_size.value,
                "Dob": out_get_date(self.birthdate)
            }

    camp_id = attrib(
        type=int,
        validator=instance_of(int)
    )
    child = attrib(
        type=Child,
        validator=instance_of(Child)
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
        validator=instance_of(SourcePoll)
    )
    siblings = attrib(
        type=list[Child],
        validator=deep_iterable(
            instance_of(Child)
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
        type=HTTPClient | None,
        validator=v_optional(
            instance_of(HTTPClient)
        ),
        default=None,
        repr=False
    )

    def to_dict(self) -> dict[str, int | dict[str, dict[str, str] | list[dict[str, str]]] | dict[str, str]]:
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
        return PersonalReservationInfo(self.camp_id, self.parent_surname, **{"http": self._http} | kwargs)


@attrs(repr=True, slots=True, frozen=True, hash=True)
class EventReservationSummary:
    option = attrib(
        type=EventReservationOption,
        converter=convert_enum(EventReservationOption),
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
            raise ValueError("Opcja nie jest jedną z elementów EventReservationOption")
        return self._price

    def to_dict(self) -> dict[str, str | int | bool]:
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
            data.update(
                {"FirstParentName": self.first_parent_name, "FirstParentSurname": self.first_parent_surname}
            )
        if self.option is EventReservationOption.CHILD_AND_TWO_PARENTS:
            data.update(
                {"SecondParentName": self.second_parent_name, "SecondParentSurname": self.second_parent_surname}
            )
        return data


@attrs(repr=True, slots=True, frozen=True, hash=True)
class CrewMember:
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
        converter=convert_character,
        validator=v_optional(
            instance_of(str)
        )
    )
    position = attrib(
        type=CrewRole,
        converter=convert_enum(CrewRole),
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
    def init_from_dict(cls, data: dict[str, str], **kwargs) -> "CrewMember":
        return cls(
            name=data["Name"],
            surname=data["Surname"],
            character=data["Character"].strip(),
            position=data["Position"],
            description=data["Description"],
            photo=Resource(data["PhotoUrl"], **kwargs)
        )


@attrs(repr=True, slots=True, frozen=True, hash=True)
class PlebisciteCandidate:
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
        ),
        default=None
    )
    plebiscite = attrib(
        type=str | None,
        validator=v_optional(
            instance_of(str)
        ),
        default=None
    )
    voted = attrib(
        type=bool | None,
        validator=v_optional(
            instance_of(bool)
        ),
        default=None
    )
    _http = attrib(
        type=HTTPClient | None,
        validator=v_optional(
            instance_of(HTTPClient)
        ),
        default=None,
        repr=False
    )

    @classmethod
    def init_from_dict(cls, data: dict[str, str | int | bool | None], **kwargs) -> "PlebisciteCandidate":
        return cls(
            name=data["Name"],
            votes=data["Result"],
            category=data["Category"],
            plebiscite=data["Plebiscite"],
            voted=data["WasVoted"],
            **kwargs
        )

    async def vote(self, http: HTTPClient | None = None):
        if self.voted:
            raise RevoteError(self.category)
        client = http or self._http
        await client.patch_vote(self.category, self.name)


Photo = Gallery.Photo
Transport = Camp.Transport
Child = WebReservationModel.Child

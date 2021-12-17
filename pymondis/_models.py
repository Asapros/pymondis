"""
Modele ułatwiające korzystanie z Client-a
Wszystkie modele są tworzone za pomocą biblioteki `attrs`
Wszystkie modele są zamro... niemutowa... wg. tłumacza google "niezmienne", "stałe"

Czekajcie na dokumentacje poniższych klas, bo jest puzyno i mi się nie chce
"""
# TODO dokumentacja
from datetime import datetime
from typing import AsyncIterator

from attr import attrib, attrs
from attr.validators import instance_of, optional as v_optional, deep_iterable
from attr.converters import optional as c_optional
from httpx import Response

from ._exceptions import RevoteError
from ._http import HTTPClient
from ._enums import Castle, CampLevel, World, Season, EventReservationOption, CrewRole, TShirtSize, SourcePoll
from ._util import convert_enum, convert_date, convert_character, convert_empty_string, out_get_date


@attrs(repr=True, slots=True, frozen=True, hash=True)
class ParentSurvey:
    """
    Jakaś opinia o obozach, już pewnie nie istnieje na stronach
    (na web.archive.org też nie ma)

    :ivar _http (param http): HTTPClient, który będzie używany do wysłania ankiety
    """
    _http = attrib(
        type=HTTPClient | None,
        default=None,
        validator=v_optional(
            instance_of(HTTPClient)
        ),
        repr=False
    )

    def to_dict(self) -> dict:
        """
        Zamienia siebie na dict-a

        :returns: instancja klasy w formie dict-a
        :raises NotImplementedError: klasa nie jest zaimplementowana
        """
        raise NotImplementedError(
            "Ta klasa jeszcze nie jest do końca zaimplementowana."
            "Jeśli wiesz gdzie na stronie występuje form do wysłania na /api/ParentsZone/Survey/..."
            "Możesz otworzyć nowy issue https://github.com/Asapros/pymondis/issues ('Implementacja zapytania POST')"
            "i się tym podzielić."
        )

    async def submit(self, survey_hash: str, http: HTTPClient | None = None):
        """
        Wrzuca ankietę

        :param survey_hash: Dobre pytanie
        :param http: HTTPClient, który będzie użyty zamiast tego podanego w konstruktorze
        """
        client = http or self._http
        await client.post_parents_zone_survey(survey_hash, self.to_dict())


@attrs(repr=True, slots=True, frozen=True, hash=True)
class ReservationDetails:
    """
    Dokładniejsze dane o rezerwacji
    """

    @classmethod
    def init_from_dict(cls, data: dict) -> "ReservationManageDetails":
        """
        Initializuje nową instancję za pomocą danych w dict-cie

        :param data: dict, na podstawie którego zostanie stworzona nowa instancja
        :returns: instancja klasy
        :raises NotImplementedError: klasa nie jest zaimplementowana :(
        """
        raise NotImplementedError(
            "Ta klasa jeszcze nie jest do końca zaimplementowana."
            "Jeśli masz zarezerwowany obóz i jego kod to możesz wysłać zapytanie przez"
            "HTTPClient.post_reservation_manage."
            "Otwórz nowy issue https://github.com/Asapros/pymondis/issues ('Implementacja zapytania POST')"
            "i podziel się wynikiem funkcji, nie zapomnij za cenzurować danych osobowych."
            "Możesz też dołączyć do issue przypuszczenia do czego może być każde pole."
        )


@attrs(repr=True, slots=True, eq=False)
class Resource:
    """
    Reprezentuje dane, najczęściej zdjęcie z serwera ``hymsresources.blob.core.windows.net``

    :ivar url: link do danych
    :ivar _http (param http): HTTPClient, który będzie używany do pobrania resource-a
    :ivar _cache_response (keyword cache_response): zapisana ostatnia odpowiedź serwera
    """
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
    _cache_response = attrib(
        type=Response | None,
        default=None,
        validator=v_optional(
            instance_of(Response)
        ),
        kw_only=True,
        repr=False
    )

    async def get_stream(self, use_cache: bool = True, update_cache: bool = True, chunk_size: int | None = 1024,
                         http: HTTPClient | None = None) -> AsyncIterator[bytes]:
        """
        Otwiera strumień danych z linku

        :param use_cache: czy użyć ostatniej zapisanej odpowiedzi, gdy dane nie zmieniły się?
        :param update_cache: czy zapisać odpowiedź do użycia później przez ``use_cache``
        :param chunk_size: wielkość fragmentu iterowanych danych (w bajtach)
        :param http: HTTPClient, który będzie użyty zamiast tego podanego w konstruktorze
        :returns: asynchroniczny iterator po fragmentach danych przesłanych przez serwer
        """
        # Spoiler - Lock-i działają wolniej w tym przypadku...
        client = http or self._http
        response = await client.get_resource(self.url, self._cache_response if use_cache else None)
        if update_cache:
            self._cache_response = response
        return response.aiter_bytes(chunk_size)

    async def get(self, use_cache: bool = True, update_cache: bool = True, http: HTTPClient | None = None) -> bytes:
        """
        Całkowicie pobiera dane z linku

        :param use_cache: czy użyć ostatniej zapisanej odpowiedzi, gdy dane nie zmieniły się?
        :param update_cache: czy zapisać odpowiedź do użycia później przez ``use_cache``
        :param http: HTTPClient, który będzie użyty zamiast tego podanego w konstruktorze
        :returns: dane po całkowitym ich pobraniu przez ``get_stream``
        """
        iterator = await self.get_stream(use_cache, update_cache, None, http)
        content: bytes = b""
        async for chunk in iterator:
            content += chunk
        return content

    def __eq__(self, other: "Resource") -> bool:
        return self.url == other.url


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Gallery:
    """
    Reprezentuje galerię z fotorelacji
    Lista znanych niedziałających galerii (get_photos() wznosi *500 Internal Server Error*):
        2, 6, 7, 8, 19, 20, 21, 22, 23, 24, 42, 53, 65, 69, 71, 76, 77, 85, 86, 92, 95, 107, 113, 135, 115, 129, 133

    :ivar gallery_id: id galerii
    :ivar start: data utworzenia galerii
    :ivar end: data zakończenia galerii
    :ivar name: nazwa galerii - ``Z jeśli zima + skrót zamku + numer``
    :ivar empty: czy galeria jest pusta?
    :ivar _http (param http): HTTPClient, który będzie używany do pobrania zdjęć z galerii
    """

    @attrs(repr=True, slots=True, frozen=True, hash=True)
    class Photo:
        """
        Reprezentuje zdjęcie z fotorelacji w dwóch rozdzielczościach

        :ivar normal: zdjęcie słabej rozdzielczości
        :ivar large: zdjęcie
        """
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
            r"""
            Initializuje nową instancję za pomocą danych w dict-cie

            :param data: dict, na podstawie którego zostanie stworzona nowa instancja
            :param \**kwargs: dodatkowe argumenty, przekazywane dalej do konstruktorów ``Resource``
            :returns: instancja klasy
            """
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
        """
        Pobiera wszystkie zdjęcia z galerii
        
        :param http: HTTPClient, który będzie użyty zamiast tego podanego w konstruktorze
        :returns: lista zdjęć
        """
        client = http or self._http
        photos = await client.get_images_galleries(self.gallery_id)
        return [
            self.Photo.init_from_dict(photo, http=client)
            for photo in photos
        ]

    @classmethod
    def init_from_dict(cls, data: dict[str, str | int | bool], **kwargs) -> "Gallery":
        r"""
        Initializuje nową instancję za pomocą danych w dict-cie

        :param data: dict, na podstawie którego zostanie stworzona nowa instancja
        :param \**kwargs: dodatkowe argumenty, przekazywane dalej do konstruktora
        :returns: instancja klasy
        """
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
    """
    Reprezentuje obóz
    
    :ivar camp_id: id obozu
    :ivar code: kod obozu ``Z jeśli w zimę + skrót zamku + numer turnusu + skrót programu``
    :ivar castle: zamek w którym się odbywa
    :ivar price: cena
    :ivar promo: przeceniona cena, jeśli jest
    :ivar active: aktywny? (nie ma listy rezerwowej)
    :ivar places_left: ilość pozostałych miejsc, ale jest zepsuta, bo czasem anomalnie rośnie i potrafi wynosić 75, kiedy jest lista rezerwowa...
    :ivar program: temat turnusu
    :ivar level: poziom (normal albo master)
    :ivar world: świat
    :ivar season: pora roku
    :ivar trip: opisy wycieczki/wycieczek jeśli jakieś są
    :ivar start: data rozpoczęcia
    :ivar end: data zakończenia
    :ivar ages: lista zakresów wiekowych (ciekawe czego...)
    :ivar transports: transporty na miejsce
    """
    @attrs(repr=True, slots=True, frozen=True, hash=True)
    class Transport:
        """
        Reprezentuje transport na obóz

        :ivar city: nazwa miasta
        :ivar one_way_price: cena w jedną stronę
        :ivar two_way_price: cena w dwie strony
        """
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
            """
            Initializuje nową instancję za pomocą danych w dict-cie

            :param data: dict, na podstawie którego zostanie stworzona nowa instancja
            :returns: instancja klasy
            """
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
        """
        Initializuje nową instancję za pomocą danych w dict-cie

        :param data: dict, na podstawie którego zostanie stworzona nowa instancja
        :returns: instancja klasy
        """
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
    """
    Reprezentuje osobę kupującą

    :ivar name: imię
    :ivar surname: nazwisko
    :ivar email: email
    :ivar phone: numer telefonu
    :ivar parcel_locker: dane o paczkomacie
    :ivar _http (param http): HTTPClient, który będzie używany do wysłania zamówienia
    """
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
    _http = attrib(
        type=HTTPClient | None,
        validator=v_optional(
            instance_of(HTTPClient),
        ),
        default=None,
        repr=False
    )

    def to_dict(self) -> dict[str, str]:
        """
        Zamienia siebie na dict-a

        :returns: instancja klasy w formie dict-a
        """
        return {
            "Name":         self.name,
            "Surname":      self.surname,
            "Email":        self.email,
            "Phone":        self.phone,
            "ParcelLocker": self.parcel_locker
        }

    async def order_fwb(self, http: HTTPClient | None = None):
        """
        Zamawia książkę „QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE”

        :param http: HTTPClient, który będzie użyty zamiast tego podanego w konstruktorze
        """
        client = http or self._http
        await client.post_orders_four_worlds_beginning(self.to_dict())


@attrs(repr=True, slots=True, frozen=True, hash=True)
class PersonalReservationInfo:
    """
    Dane, za których pomocą możesz uzyskać szczegóły rezerwacji (kod, nazwisko)

    :ivar reservation_id: kod rezerwacji
    :ivar surname: nazwisko zarezerwowanego
    :ivar _http (param http): HTTPClient, który będzie używany do dostania szczegółów rezerwacji
    """
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
        """
        Zamienia siebie na dict-a

        :returns: instancja klasy w formie dict-a
        """
        return {
            "ReservationId": self.reservation_id,
            "Surname":       self.surname
        }

    async def get_details(self, http: HTTPClient | None = None) -> ReservationDetails:
        """
        Dostaje dane o rezerwacji

        :returns: szczegóły rezerwacji
        """
        client = http or self._http
        details = await client.post_reservations_manage(self.to_dict())
        return ReservationDetails.init_from_dict(details)


@attrs(repr=True, slots=True, frozen=True, hash=True)
class Reservation:
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
                "Name":    self.name,
                "Surname": self.surname,
                "Tshirt":  self.t_shirt_size.value,
                "Dob":     out_get_date(self.birthdate)
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
            "Childs":    {  # English 100
                "Main":     self.child.to_dict(),
                "Siblings": [sibling.to_dict() for sibling in self.siblings]
            },
            "Parent":    {
                "Name":    self.parent_name,
                "Surname": self.parent_surname,
                "Nip":     self.nip
            },
            "Details":   {
                "Email": self.email,
                "Phone": self.phone,
                "Promo": self.promo_code,
                "Poll":  self.poll.value
            }
        }

    @property
    def pri(self, **kwargs) -> PersonalReservationInfo:
        return PersonalReservationInfo(self.camp_id, self.parent_surname, **{"http": self._http} | kwargs)

    async def reserve_camp(self, http: HTTPClient | None = None) -> list[str]:
        client = http or self._http
        return await client.post_reservations_subscribe(self.to_dict())


@attrs(repr=True, slots=True, frozen=True, hash=True)
class EventReservation:
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
    _http = attrib(
        type=HTTPClient | None,
        validator=instance_of(HTTPClient),
        default=None,
        repr=False
    )
    _price = attrib(  # TODO Factory
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
            "Price":          self.price,
            "Name":           self.name,
            "Surname":        self.surname,
            "ParentName":     self.parent_name,
            "ParentSurname":  self.parent_surname,
            "IsParentReused": self.parent_reused,
            "Phone":          self.phone,
            "Email":          self.email
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

    async def reserve_inauguration(self, http: HTTPClient | None):
        client = http or self._http
        await client.post_events_inauguration(self.to_dict())


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
Child = Reservation.Child

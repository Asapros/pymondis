from typing import List

from pymondis.abc import ABCCamp, ABCTransport, ABCEventReservationSummary, ABCResource, ABCHTTPClient
from pymondis.client import HTTPClient
from pymondis.enums import Castle, CampLevel, World, Season, EventReservationOption
from pymondis.util import parse_date, get_enum_element, default_backoff

"""
class CrewMember:
    __slots__ = "_client", "name", "surname", "character", "role", "description", "photo_url", "photo_md5", "photo"

    def __init__(self, client, name, surname, character, role, description, photo_url):
        self._client = client
        self.name = name
        self.surname = surname
        self.character = character
        self.description = description
        self.photo_url = photo_url
        self.photo_md5 = None
        self.photo = None

        for iter_role in CrewRole:
            if role == iter_role.value:
                self.role = iter_role
                break
        else:
            raise ValueError("{} is not a valid crew role".format(role))

    async def get_photo(self, use_cache=True, update_cache=True):
        content, md5 = await self._client.get_resource(self.photo_url, self.photo_md5 if use_cache else None,
                                                       self.photo)
        if update_cache:
            self.photo_md5 = md5
            self.photo = content
        return content

    def __str__(self):
        return "{}(name/surname: {} {}, character: {}, role: {})".format(self.__class__.__name__, self.name,
                                                                         self.surname, self.character, self.role.value)


class Photo:
    __slots__ = "url", "enlarged_url", "_client", "image", "large_image", "image_md5", "large_image_md5"

    def __init__(self, client, url, enlarged_url):
        self.url = url
        self._client = client
        self.enlarged_url = enlarged_url
        self.image = None
        self.image_md5 = None
        self.large_image = None
        self.large_image_md5 = None

    async def get_image(self, use_cache=True, update_cache=True):
        content, md5 = await self._client.get_resource(self.url, self.image_md5 if use_cache else None, self.image)
        if update_cache:
            self.image_md5 = md5
            self.image = content
        return content

    async def get_large_image(self, use_cache=True, update_cache=True):
        content, md5 = await self._client.get_resource(self.url, self.large_image_md5 if use_cache else None,
                                                       self.large_image)
        if update_cache:
            self.large_image_md5 = md5
            self.large_image = content
        return content

    @property
    def uuid(self):
        return UUID(self.url[-36:-1])

    def __str__(self):
        return "{}(path: {})".format(self.__class__.__name__, urlparse(self.url).path)


class PlebisciteCandidate:
    __slots__ = "_client", "name", "votes", "category", "plebiscite_name", "voted"

    def __init__(self, client, name: str, votes: int, category: str, plebiscite_name: str,
                 voted: bool):  # TODO 15+ listopada - co pokazuje się zamast wartości "votes"?
        self._client = client
        self.name = name
        self.votes = votes
        self.category = category
        self.plebiscite_name = plebiscite_name
        self.voted = voted

    @on_exception(expo, HTTPStatusError, max_tries=3, giveup=lambda status: 400 <= status.response.status_code < 500)
    async def vote(self, ignore_revote=False):
        if not ignore_revote and self.voted:
            raise RevoteError("Tried to vote for a candidate second time")
        response = await self._client.patch("{}/Vote/{}/{}".format(self._client.base_url, self.category,
                                                                   self.name))  # Dalej mnie zastanawia czemu PATCH, a nie POST...
        response.raise_for_status()

    def __str__(self):
        return "{}(name: {}, votes: {}, category: {}, plebiscite: {}, voted: {})".format(self.__class__.__name__,
                                                                                         self.name, self.votes,
                                                                                         self.category,
                                                                                         self.plebiscite_name,
                                                                                         self.voted)


class Gallery:
    __slots__ = "start", "end", "has_photos", "gallery_id", "name", "_client"

    def __init__(self, client, gallery_id: int, name: str, has_photos: bool, start: datetime, end: datetime):
        self._client = client
        self.gallery_id = gallery_id
        self.name = name
        self.has_photos = has_photos
        self.start = start
        self.end = end

    @on_exception(expo, HTTPStatusError, max_tries=3, giveup=lambda status: 400 <= status.response.status_code < 500)
    async def get_photos(self) -> List[Photo]:
        response = await self._client.get(
            "{}/Images/Galeries/{}".format(self._client.base_url, self.gallery_id),
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        photos = []
        for element in response.json():
            photos.append(Photo(self, element["AlbumUrl"], element["EnlargedUrl"]))
        return photos

    def __str__(self):
        return "{}(id: {}, name: {}, empty: {}, start: {}, end: {})".format(self.__class__.__name__, self.gallery_id,
                                                                            self.name, not self.has_photos, self.start,
                                                                            self.end)
"""


class EventReservationSummary(ABCEventReservationSummary):

    def __init__(
            self,
            option: EventReservationOption,
            name: str,
            surname: str,
            parent_name: str,
            parent_surname: str,
            phone: int,
            email: str,
            price: int | None = None,
            parent_reused: bool = False,
            first_parent_name: str | None = None,
            first_parent_surname: str | None = None,
            second_parent_name: str | None = None,
            second_parent_surname: str | None = None
    ):
        self.price = price
        self.option = option
        self.name = name
        self.surname = surname
        self.parent_name = parent_name
        self.parent_surname = parent_surname
        self.phone = phone
        self.email = email
        self.parent_reused = parent_reused
        self.first_parent_name = first_parent_name
        self.first_parent_surname = first_parent_surname
        self.second_parent_name = second_parent_name
        self.second_parent_surname = second_parent_surname
        if price is None:
            match option:
                case EventReservationOption.CHILD:
                    self.price = 450
                case EventReservationOption.CHILD_AND_ONE_PARENT:
                    self.price = 900
                case EventReservationOption.CHILD_AND_TWO_PARENTS:
                    self.price = 1300
                case _:
                    raise ValueError("Option is not one of the enum elements")

    def jsonify(self) -> dict:
        # Naśladuje dziwne zachowanie formularza na stronie, trzeba sprawdzić czy to działa w inny sposób bo te if-y na końcu to tragedia
        json = {
            "Price": str(self.price),
            "Option": self.option.value,
            "Name": self.name,
            "Surname": self.surname,
            "ParentName": self.parent_name,
            "ParentSurname": self.parent_surname,
            "IsParentReused": None if self.option is EventReservationOption.CHILD else self.parent_reused,
            "Phone": str(self.phone),
            "Email": self.email,
            "SecondParentName": self.second_parent_name,
            "SecondParentSurname": self.second_parent_surname
        }
        if not self.parent_reused:
            json.update({"FirstParentName": self.first_parent_name, "FirstParentSurname": self.first_parent_surname})
        if self.option is EventReservationOption.CHILD:
            json.update({"FirstParentName": "", "FirstParentSurname": ""})

        return json


class Camp(ABCCamp):
    class Transport(ABCTransport):

        def __init__(
                self,
                city: str,
                one_way_price: int,
                two_way_price: int
        ):
            self.city = city
            self.one_way_price = one_way_price
            self.two_way_price = two_way_price

        def __str__(self) -> str:
            return "{}(city: {}, prices (one/two way): {}/{})".format(self.__class__.__name__, self.city,
                                                                      self.one_way_price, self.two_way_price)

    def __init__(
            self,
            camp_id: int,
            code: str,
            place: str,
            price: int,
            promo: int | None,
            active: bool,
            places_left: int,
            program: str,
            level: str,
            world: str,
            season: str,
            trip: str,
            start: str,
            end: str,
            ages: List[str],
            transports: List[ABCTransport]
    ):
        self.camp_id = camp_id
        self.code = code
        self.place = get_enum_element(Castle, place)
        self.price = price
        self.promo = promo
        self.active = active
        self.places_left = places_left
        self.program = program
        self.level = get_enum_element(CampLevel, level)
        self.world = get_enum_element(World, world)
        self.season = get_enum_element(Season, season)
        self.trip = trip if trip else None
        self.start = parse_date(start)
        self.end = parse_date(end)
        self.ages = ages
        self.transports = transports

    @property
    def current_price(self) -> int:
        if self.promo is None:
            return self.price
        return self.promo

    def __str__(self):
        return "{}(id: {}, code: {}, place: {}, current price: {}, active: {}, places left: {}, program: {}, level: {}, world: {}, season: {}, trip: {}, start: {}, end: {}, transports: [{}])".format(
            self.__class__.__name__,
            self.camp_id,
            self.code,
            self.place,
            self.current_price,
            self.active,
            self.places_left,
            self.program,
            self.level.name,
            self.world.name,
            self.season.name,
            self.trip,
            self.start,
            self.end,
            ", ".join(
                [
                    str(transport) for transport in self.transports
                ]
            )
        )


class Resource(ABCResource):
    def __init__(self, url: str, client: ABCHTTPClient | None = None):
        self.url = url
        self._client = client
        self.md5 = None
        self.content = None

    @default_backoff
    async def get(self, use_cache: bool = True, update_cache: bool = True, client: HTTPClient | None = None) -> bytes:
        client = self._client or client
        if client is None:
            raise ValueError("No client found. Pass one in the constructor or directly in Resource.get")
        if use_cache:
            head = await client.head(self.url)
            head.raise_for_status()
            if self.md5 == head.headers["Content-MD5"]:
                return self.content
        response = await client.get(self.url)
        response.raise_for_status()
        if update_cache:
            self.md5 = response.headers["Content-MD5"]
            self.content = response.content
        return response.content

    def __str__(self) -> str:
        return "{}(url: {})".format(self.__class__.__name__, self.url)


Transport = Camp.Transport

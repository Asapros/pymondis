from datetime import datetime

from httpx import AsyncClient

from ._util import backoff, get_http_date
from ._metadata import __title__, __version__


class HTTPClient(AsyncClient):
    def __init__(
            self,
            timeout: float | None = None,
            *,
            base_url: str = "https://quatromondisapi.azurewebsites.net/api"
    ):
        super().__init__(timeout=timeout)
        self.base: str = base_url
        self.headers = {"User-Agent": "{}/{}".format(__title__, __version__)}

        self.request = backoff(self.request)

    async def get_resource(
            self,
            url: str,
            cache_time: datetime | None = None,
            cache_content: bytes | None = None
    ) -> bytes:
        headers = {
            "If-Modified-Since": get_http_date(cache_time)
        } if cache_time is not None else {}
        response = await self.get(
            url,
            headers=headers
        )
        if response.status_code == 304:
            return cache_content
        return response.content

    async def get_camps(self) -> list[dict[str, str | int | bool | None | list[str | dict[str, str | int]]]]:
        response = await self.get(
            self.base + "/Camps",
            headers={"Accept": "application/json"}
        )
        return response.json()

    async def post_events_inauguration(self, reservation_model: dict):
        await self.post(
            self.base + "/Events/Inauguration",
            json=reservation_model
        )

    async def get_images_galleries_castle(self, castle: str) -> list[dict[str, str | int | bool]]:
        response = await self.get(
            self.base + "/Images/Galeries/Castle/{}".format(castle),  # 'Galeries' XD
            headers={"Accept": "application/json"})

        return response.json()

    async def get_images_galleries(self, gallery_id: int) -> list[dict[str, str]]:
        response = await self.get(
            self.base + "/Images/Galeries/{}".format(gallery_id),  # Znowu 'Galeries'
            headers={"Accept": "application/json"})

        return response.json()

    async def post_orders_four_worlds_beginning(self, purchaser: dict):
        await self.post(
            self.base + "/Orders/FourWorldsBeginning",
            json=purchaser
        )

    async def post_parents_zone_survey(self, survey_hash: str, result: dict):
        await self.post(
            self.base + "/ParentsZone/Survey/{}".format(survey_hash),
            json=result
        )

    async def get_parents_zone_crew(self) -> list[dict[str, str]]:
        response = await self.get(
            self.base + "/ParentsZone/Crew",
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def post_parents_zone_apply(self):
        raise NotImplementedError(
            "Nie mogę aktualnie zaimplementować tej metody, bo nie wiem jak są wysyłane dane"
            "Jeśli jest ci potrzebna możesz otworzyć nowy issue: https://github.com/Asapros/pymondis/issues"
        )
        # Dane najprawdopodobniej są wysyłane jako form, ale nie ma tego w swagger-ze, a ja jestem borowikiem w
        # javascript-a i nie czaje, o co chodzi, dodajcie do dokumentacji pls

    async def post_reservations_subscribe(self, reservation_model: dict) -> list[str]:
        response = await self.post(
            self.base + "/Reservations/Subscribe",
            json=reservation_model,
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def post_reservations_manage(self, pri: dict[str, str]) -> dict[str, str | bool]:
        response = await self.post(
            self.base + "/Reservations/Manage",
            json=pri,
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def patch_vote(self, category: str, name: str):
        await self.patch(  # A mnie dalej zastanawia, czemu tu patch jest, a nie post...
            self.base + "/Vote/{}/{}".format(category, name)
        )

    async def get_vote_plebiscite(self, year: int) -> list[dict[str, str | int | bool]]:
        response = await self.get(
            self.base + "/Vote/plebiscite/{}".format(year),
            # Jedyny endpoint gdzie słowo w ścieżce nie się zaczyna dużą literą...
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def __aenter__(self) -> "HTTPClient":  # Type-hinting
        await super().__aenter__()
        return self

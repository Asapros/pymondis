from datetime import datetime
from typing import Dict, List

from httpx import AsyncClient

from ._util import default_backoff
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

    @default_backoff
    async def get_resource(
            self,
            url: str,
            cache_time: datetime | None = None,
            cache_content: bytes | None = None
    ) -> bytes:
        headers = {
            "If-Modified-Since": cache_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        } if cache_time is not None else {}
        response = await self.get(
            url,
            headers=headers
        )
        if response.status_code == 304:
            return cache_content
        response.raise_for_status()
        return response.content

    @default_backoff
    async def get_camps(self) -> List[dict]:
        response = await self.get(
            self.base + "/Camps",
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_events_inauguration(self, reservation_model: dict):
        response = await self.post(
            self.base + "/Events/Inauguration",
            json=reservation_model
        )
        response.raise_for_status()

    @default_backoff
    async def get_images_galleries_castle(self, castle: str) -> List[Dict[str, str | int | bool]]:
        response = await self.get(
            self.base + "/Images/Galeries/Castle/{}".format(castle),  # 'Galeries' XD
            headers={"Accept": "application/json"})
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def get_images_galleries(self, gallery_id: int) -> List[Dict[str, str]]:
        response = await self.get(
            self.base + "/Images/Galeries/{}".format(gallery_id),  # Znowu 'Galeries'
            headers={"Accept": "application/json"})
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_orders_four_worlds_beginning(self, purchaser: dict):
        response = await self.post(
            self.base + "/Orders/FourWorldsBeginning",
            json=purchaser
        )
        response.raise_for_status()

    @default_backoff
    async def post_parents_zone_survey(self, survey_hash: str, result: dict):
        response = await self.post(
            self.base + "/ParentsZone/Survey/{}".format(survey_hash),
            json=result
        )
        response.raise_for_status()

    @default_backoff
    async def get_parents_zone_crew(self) -> List[dict]:
        response = await self.get(
            self.base + "/ParentsZone/Crew",
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_parents_zone_apply(self):
        raise NotImplementedError(
            "Nie mogę aktualnie zaimplementować tej metody, bo nie wiem jak są wysyłane dane"
            "Jeśli jest ci potrzebna możesz otworzyć nowy issue: https://github.com/Asapros/pymondis/issues"
        )
        # Dane najprawdopodobniej są wysyłane jako form, ale nie ma tego w swagger-ze, a ja jestem borowikiem w
        # javascript-a i nie czaje, o co chodzi, dodajcie do dokumentacji pls

    @default_backoff
    async def post_reservations_subscribe(self, reservation_model: dict) -> List[str]:
        response = await self.post(
            self.base + "/Reservations/Subscribe",
            json=reservation_model,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_reservations_manage(self, pri: dict) -> Dict[str, str | bool]:
        response = await self.post(
            self.base + "/Reservations/Manage",
            json=pri,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def patch_vote(self, category: str, name: str):
        response = await self.patch(  # A mnie dalej zastanawia, czemu tu patch jest, a nie post...
            self.base + "/Vote/{}/{}".format(category, name)
        )
        response.raise_for_status()

    @default_backoff
    async def get_vote_plebiscite(self, year: int) -> List[Dict[str, str | int | bool]]:
        response = await self.get(
            self.base + "/Vote/plebiscite/{}".format(year),
            # Jedyny endpoint gdzie słowo w ścieżce nie się zaczyna dużą literą...
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    async def __aenter__(self) -> "HTTPClient":  # Type-hinting
        await super().__aenter__()
        return self

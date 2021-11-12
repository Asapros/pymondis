from datetime import datetime
from typing import List, Dict

from httpx import AsyncClient

from pymondis.abstract.models import ABCHTTPClient

from pymondis.util import default_backoff


class HTTPClient(ABCHTTPClient, AsyncClient):
    BASE_URL: str = "https://quatromondisapi.azurewebsites.net/api"
    TIMEOUT: int | None = None

    @default_backoff
    async def get_resource(self, url: str, cache_time: datetime | None = None, cache_content: bytes | None = None) -> bytes:
        headers = {"If-Modified-Since": cache_time.strftime("%a, %d %b %Y %H:%M:%S GMT")} if cache_time is not None else {}
        response = await self.get(url, headers=headers, timeout=self.TIMEOUT)
        if response.status_code == 304:
            return cache_content
        response.raise_for_status()
        return response.content

    @default_backoff
    async def get_camps(self) -> List[dict]:
        response = await self.get(self.BASE_URL + "/Camps", headers={"Accept": "application/json"}, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_inauguration(self, reservation_model: dict):
        response = await self.post(self.BASE_URL + "/Events/Inauguration", json=reservation_model, timeout=self.TIMEOUT)
        response.raise_for_status()

    @default_backoff
    async def get_galleries(self, castle: str) -> List[Dict[str, str | int | bool]]:
        response = await self.get(self.BASE_URL + "/Images/Galeries/Castle/{}".format(castle), headers={"Accept": "application/json"}, timeout=self.TIMEOUT)  # Galeries
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def get_gallery(self, gallery_id: int) -> List[Dict[str, str]]:
        response = await self.get(self.BASE_URL + "/Images/Galeries/{}".format(gallery_id), headers={"Accept": "application/json"}, timeout=self.TIMEOUT)  # Znowu 'Galeries'
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_fwb(self, purchaser: dict):
        response = await self.post(self.BASE_URL + "/Orders/FourWorldsBeginning", json=purchaser, timeout=self.TIMEOUT)
        response.raise_for_status()

    @default_backoff
    async def post_survey(self, survey_hash: str, result: dict):
        response = await self.post(self.BASE_URL + "/ParentsZone/Survey/{}".format(survey_hash), json=result, timeout=self.TIMEOUT)
        response.raise_for_status()

    @default_backoff
    async def get_crew(self) -> List[dict]:
        response = await self.get(self.BASE_URL + "/ParentsZone/Crew", headers={"Accept":"application/json"}, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_apply(self):
        raise NotImplementedError()  # TODO Zaimplementuj
        # Dane najprawdopodobnie są wysyłane jako form, ale nie ma tego w swaggerze, a ja jestem borowikiem w javascripta i nie czaje o co chodzi
        # Dodajcie do dokumentacji pls

    @default_backoff
    async def post_subscribe(self, reservation_model: dict) -> List[str]:
        response = await self.post(self.BASE_URL + "/Reservations/Subscribe", json=reservation_model, headers={"Accept": "application/json"}, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def post_manage(self, pri: dict) -> Dict[str, str | bool]:
        response = await self.post(self.BASE_URL + "/Reservations/Manage", json=pri, headers={"Accept": "application/json"}, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    @default_backoff
    async def patch_vote(self, category: str, name: str):
        response = await self.patch(self.BASE_URL + "/Vote/{}/{}".format(category, name), timeout=self.TIMEOUT)
        response.raise_for_status()

    @default_backoff
    async def get_plebiscite(self, year: int) -> List[Dict[str, str | int | bool]]:
        response = await self.get(self.BASE_URL + "/Vote/plebiscite/{}".format(year), headers={"Accept": "application/json"}, timeout=self.TIMEOUT)  # Jedyny endpoint gdzie słowo w ścieżce nie się zaczyna dużą literą...
        response.raise_for_status()
        return response.json()

    async def __aenter__(self) -> "HTTPClient":  # Type-hinting
        return await super().__aenter__()
import asyncio

from httpx import AsyncClient

from pymondis.abc import ABCHTTPClient, ABCPersonalReservationInfo, ABCWebReservationModel, ABCParentSurveyResult, \
    ABCPurchaser
from pymondis.enums import Castle, EventReservationOption
from pymondis.models import Camp, Transport, EventReservationSummary
from pymondis.util import default_backoff


class HTTPClient(ABCHTTPClient, AsyncClient):
    BASE: str = "https://quatromondisapi.azurewebsites.net/api"

    @default_backoff
    async def get_camps(self):
        response = await self.get(self.BASE + "/Camps", headers={"Content-Type": "application/json"})
        response.raise_for_status()
        camps = [
            Camp(
                camp["Id"],
                camp["Code"],
                camp["Place"],
                camp["Price"],
                camp["Promo"],
                camp["IsActive"],
                camp["PlacesLeft"],
                camp["Program"],
                camp["Level"],
                camp["World"],
                camp["Season"],
                camp["Trip"],
                camp["StartDate"],
                camp["EndDate"],
                camp["Ages"],
                [
                    Transport(
                        transport["City"],
                        transport["OneWayPrice"],
                        transport["TwoWayPrice"]
                    ) for transport in camp["Transports"]
                ]
            ) for camp in response.json()
        ]
        return camps

    @default_backoff
    async def post_inauguration(self, summary: EventReservationSummary):
        response = await self.post(self.BASE + "/Events/Inauguration", json=summary.jsonify())
        response.raise_for_status()

    @default_backoff
    async def get_galleries(self, castle: Castle):
        raise NotImplementedError()

    @default_backoff
    async def get_gallery(self, gallery_id: int):
        raise NotImplementedError()

    @default_backoff
    async def post_fwb(self, purchaser: ABCPurchaser):
        raise NotImplementedError()

    @default_backoff
    async def post_survey(self, survey_hash: str, result: ABCParentSurveyResult):
        raise NotImplementedError()

    @default_backoff
    async def get_crew(self):
        raise NotImplementedError()

    @default_backoff
    async def post_apply(self):
        raise NotImplementedError()

    @default_backoff
    async def post_subscribe(self, reservation: ABCWebReservationModel):
        raise NotImplementedError()

    @default_backoff
    async def post_manage(self, pri: ABCPersonalReservationInfo):
        raise NotImplementedError()

    @default_backoff
    async def patch_vote(self, category: str, name: str):
        raise NotImplementedError()

    @default_backoff
    async def get_plebiscite(self, year: int):
        pass

    async def __aenter__(self) -> "HTTPClient":  # Type-hinting
        return await super().__aenter__()

async def main():
    async with HTTPClient() as c:
        await c.post_inauguration(EventReservationSummary(EventReservationOption.CHILD, name="a", surname="b", parent_name="c", parent_surname="d", phone="e", email="f"))


asyncio.run(main())

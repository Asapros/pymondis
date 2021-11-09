from typing import Iterable

from .abstract.api import ABCHTTPClient
from .abstract.client import ABCClient
from .abstract.models import ABCPlebisciteCandidate, ABCWebReservationModel, ABCCrewMember, ABCParentSurveyResult, \
    ABCPurchaser, ABCGallery, ABCEventReservationSummary
from .api import HTTPClient
from .enums import Castle
from .models import Camp


class Client(ABCClient):
    def __init__(self, http: ABCHTTPClient = None):
        if http is None:
            self.http = HTTPClient()
            return
        self.http = http

    async def get_camps(self) -> Iterable[Camp]:
        camps = await self.http.get_camps()
        return [Camp.init_from_dict(camp) for camp in camps]

    async def reserve_inauguration(self, reservation: ABCEventReservationSummary):
        pass

    async def get_galleries(self, castle: Castle) -> Iterable[ABCGallery]:
        pass

    async def order_fwb(self, purchaser: ABCPurchaser):
        await self.http.post_fwb(purchaser.to_dict())

    async def submit_survey(self, survey_hash: str, result: ABCParentSurveyResult):
        pass

    async def get_crew(self) -> Iterable[ABCCrewMember]:
        pass

    async def apply_for_job(self):
        raise NotImplementedError()
        # @ .api.HTTPClient.post_apply

    async def reserve_camp(self, reservation: ABCWebReservationModel) -> Iterable[str]:
        pass

    async def vote_for_plebiscite(self, category: str, name: str):
        pass

    async def get_plebiscite(self, year: int) -> Iterable[ABCPlebisciteCandidate]:
        pass

    async def __aenter__(self) -> "Client":
        await self.http.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.http.__aexit__(exc_type, exc_val, exc_tb)
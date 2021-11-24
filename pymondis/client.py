from typing import List


from .api import HTTPClient
from .enums import Castle
from .models import (
    Camp,
    CrewMember,
    Purchaser,
    Gallery,
    EventReservationSummary,
    PlebisciteCandidate,
    WebReservationModel,
    ParentSurveyResult
)


class Client:
    def __init__(self, http: HTTPClient = None):
        if http is None:
            self.http = HTTPClient()
            return
        self.http = http

    async def get_camps(self) -> List[Camp]:
        camps = await self.http.get_camps()
        return [Camp.init_from_dict(camp) for camp in camps]

    async def reserve_inauguration(self, reservation: EventReservationSummary):
        await self.http.post_inauguration(reservation.to_dict())

    async def get_galleries(self, castle: Castle) -> List[Gallery]:
        galleries = await self.http.get_galleries(castle.value)
        return [Gallery.init_from_dict(gallery, http=self.http) for gallery in galleries]

    async def order_fwb(self, purchaser: Purchaser):
        await self.http.post_fwb(purchaser.to_dict())

    async def submit_survey(self, survey_hash: str, result: ParentSurveyResult):
        raise NotImplementedError(
            "Żeby używać tej metody fajnie by było gdybym wiedział jakie dane są przesyłane"
            "Jeśli jest ci potrzebna możesz otworzyć nowy issue: https://github.com/Asapros/pymondis/issues"
        )

    async def get_crew(self) -> List[CrewMember]:
        crew = await self.http.get_crew()
        return [CrewMember.init_from_dict(crew_member, http=self.http) for crew_member in crew]

    async def apply_for_job(self):
        await self.http.post_apply()

    async def reserve_camp(self, reservation: WebReservationModel) -> List[str]:
        codes = await self.http.post_subscribe(reservation.to_dict())
        return codes

    async def get_plebiscite(self, year: int) -> List[PlebisciteCandidate]:
        candidates = await self.http.get_plebiscite(year)
        return [PlebisciteCandidate.init_from_dict(candidate, http=self.http) for candidate in candidates]

    async def __aenter__(self) -> "Client":
        await self.http.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.http.__aexit__(exc_type, exc_val, exc_tb)
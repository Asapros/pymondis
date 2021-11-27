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
    def __init__(self, http: HTTPClient | None = None):
        self.http: HTTPClient = HTTPClient() if http is None else http

    async def get_camps(self) -> List[Camp]:
        camps = await self.http.get_camps()
        return [Camp.init_from_dict(camp) for camp in camps]

    async def reserve_inauguration(self, reservation: EventReservationSummary):
        await self.http.post_events_inauguration(reservation.to_dict())

    async def get_galleries(self, castle: Castle) -> List[Gallery]:
        galleries = await self.http.get_images_galleries_castle(castle.value)
        return [Gallery.init_from_dict(gallery, http=self.http) for gallery in galleries]

    async def order_fwb(self, purchaser: Purchaser):
        await self.http.post_orders_four_worlds_beginning(purchaser.to_dict())

    async def submit_survey(self, survey_hash: str, result: ParentSurveyResult):
        raise NotImplementedError(
            "Ta metoda będzie brała ParentSurveyResult jako drugi argument"
            "Jeśli chcesz pomóc w jej implementacji otwórz nowy issue: https://github.com/Asapros/pymondis/issues"
        )

    async def get_crew(self) -> List[CrewMember]:
        crew = await self.http.get_parents_zone_crew()
        return [CrewMember.init_from_dict(crew_member, http=self.http) for crew_member in crew]

    async def apply_for_job(self):
        await self.http.post_parents_zone_apply()

    async def reserve_camp(self, reservation: WebReservationModel) -> List[str]:
        codes = await self.http.post_reservations_subscribe(reservation.to_dict())
        return codes

    async def get_plebiscite(self, year: int) -> List[PlebisciteCandidate]:
        candidates = await self.http.get_vote_plebiscite(year)
        return [PlebisciteCandidate.init_from_dict(candidate, http=self.http) for candidate in candidates]

    async def __aenter__(self) -> "Client":
        await self.http.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.http.__aexit__(exc_type, exc_val, exc_tb)
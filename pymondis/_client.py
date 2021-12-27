from ._enums import Castle
from ._http import HTTPClient
from ._models import (
    Camp,
    CrewMember,
    Gallery,
    PlebisciteCandidate
)


class Client:
    """
    Pozwala na wykonywanie asynchronicznych zapytań do Quatromondis API
    """
    def __init__(self, http: HTTPClient | None = None):
        """
        Initializuje instancję Client-a

        :param http: HTTPClient, który będzie używany zamiast tworzenia zupełnie nowego
        """
        self.http: HTTPClient = HTTPClient() if http is None else http

    async def get_camps(self) -> list[Camp]:
        """
        Dostaje listę obozów

        :returns: lista aktualnie dostępnych na stronie obozów
        """
        camps = await self.http.get_camps()
        return [Camp.from_dict(camp) for camp in camps]

    async def get_galleries(self, castle: Castle) -> list[Gallery]:
        """
        Dostaje listę galerii z danego zamku

        :param castle: zamek, z którego są szukane galerie
        :returns: lista aktualnych galerii z podanego zamku
        """
        galleries = await self.http.get_images_galleries_castle(castle.value)
        return [Gallery.from_dict(gallery, http=self.http) for gallery in galleries]

    async def get_crew(self) -> list[CrewMember]:
        """
        Dostaje członków kadry z obozów

        :returns: lista psorów i kierowników
        """
        crew = await self.http.get_parents_zone_crew()
        return [CrewMember.from_dict(crew_member, http=self.http) for crew_member in crew]

    async def get_plebiscite(self, year: int) -> list[PlebisciteCandidate]:
        """
        Dostaje listę kandydatów plebiscytu

        :param year: rok, z którego szukani są kandydaci plebiscytu
        :returns: lista kandydatów plebiscytu z podanego roku
        """
        candidates = await self.http.get_vote_plebiscite(year)
        return [PlebisciteCandidate.from_dict(candidate, http=self.http) for candidate in candidates]

    async def apply_for_job(self):
        """
        Zgłasza aplikację o pracę
        """
        await self.http.post_parents_zone_apply()

    async def __aenter__(self) -> "Client":
        await self.http.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.http.__aexit__(exc_type, exc_val, exc_tb)

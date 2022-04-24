"""
Trochę synchronicznych metod do użycia w konsoli.
"""
__all__ = "get_camps", "get_plebiscite", "get_castles", "get_crew"

from asyncio import run

from ._client import Client
from ._enums import Castle
from ._http import HTTPClient
from ._models import Camp, CastleGalleries, CrewMember, Gallery, Photo, PlebisciteCandidate


async def _open_and_request(client_class, function, *args, **kwargs):
	async with client_class() as client:
		return await function(client, *args, **kwargs)


def get_camps() -> list[Camp]:
	return run(_open_and_request(Client, Client.get_camps))._cache_camps


def get_plebiscite(year: int) -> list[PlebisciteCandidate]:
	return run(_open_and_request(Client, Client.get_plebiscite, year))


def get_castles() -> list[CastleGalleries]:
	return run(_open_and_request(Client, Client.get_castles))


def get_crew() -> list[CrewMember]:
	return run(_open_and_request(Client, Client.get_crew))


def get_galleries(castle: Castle) -> list[Gallery]:
	return run(_open_and_request(HTTPClient, CastleGalleries(castle).get))


def get_photos(gallery_id: int) -> list[Photo]:
	return run(_open_and_request(HTTPClient, Gallery(gallery_id).get_photos))

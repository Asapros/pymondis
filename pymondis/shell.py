"""
Trochę synchronicznych metod do użycia w konsoli.
"""
__all__ = "get_camps", "get_plebiscite", "get_castles", "get_crew", "apply_for_job"

from asyncio import run

from ._client import Client
from ._enums import Castle
from ._http import HTTPClient
from ._models import CastleGalleries


async def _open_and_request(client_class, method, *args, **kwargs):
    async with client_class() as client:
        return await method(client, *args, **kwargs)


def get_camps():
    run(_open_and_request(Client, Client.get_camps))


def get_plebiscite(year: int):
    run(_open_and_request(Client, Client.get_plebiscite, year))


def get_castles():
    run(_open_and_request(Client, Client.get_castles))


def get_crew():
    run(_open_and_request(Client, Client.get_crew))


def apply_for_job():
    run(_open_and_request(Client, Client.apply_for_job))


def get_galleries(castle: Castle):
    run(_open_and_request(HTTPClient, CastleGalleries(castle).get))

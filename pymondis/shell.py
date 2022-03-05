"""
Trochę synchronicznych metod do użycia w konsoli.
"""
__all__ = "get_camps", "get_plebiscite", "get_castles", "get_crew"

from asyncio import run

from ._client import Client
from ._enums import Castle
from ._http import HTTPClient
from ._models import CastleGalleries


async def _open_and_request(client_class, method, *args, **kwargs):
    async with client_class() as client:
        return await method(client, *args, **kwargs)


def get_camps():
    return run(_open_and_request(Client, Client.get_camps))._cache_camps


def get_plebiscite(year: int):
    return run(_open_and_request(Client, Client.get_plebiscite, year))


def get_castles():
    return run(_open_and_request(Client, Client.get_castles))


def get_crew():
    return run(_open_and_request(Client, Client.get_crew))


def get_galleries(castle: Castle):
    return run(_open_and_request(HTTPClient, CastleGalleries(castle).get))
from asyncio import gather
from datetime import datetime
from unittest import IsolatedAsyncioTestCase


class TestHTTPClient(IsolatedAsyncioTestCase):
    async def test_imports(self):
        from pymondis import api, client, enums, exceptions, models, util

    async def test_gets(self):
        from pymondis.client import Client
        async with Client() as client:
            await gather(
                client.get_crew(),
                client.get_camps()
            )

    async def test_plebiscite(self):
        from pymondis.client import Client
        async with Client() as client:
            await client.get_plebiscite(datetime.now().year)

    async def test_galleries(self):
        from pymondis.enums import Castle
        from pymondis.client import Client
        async with Client() as client:
            await gather(*[client.get_galleries(castle) for castle in Castle])

    async def test_photos(self):
        from pymondis.models import Gallery
        from pymondis.client import Client
        async with Client() as client:
            gallery = Gallery(1)
            await gallery.get_photos(client.http)


if __name__ == "__main__":
    TestHTTPClient.run()

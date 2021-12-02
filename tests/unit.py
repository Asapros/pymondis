from asyncio import gather
from datetime import datetime
from unittest import IsolatedAsyncioTestCase


class TestHTTPClient(IsolatedAsyncioTestCase):
    async def test_imports(self):
        import pymondis

    async def test_gets(self):
        from pymondis import Client
        async with Client() as client:
            await gather(
                client.get_crew(),
                client.get_camps()
            )

    async def test_plebiscite(self):
        from pymondis import Client
        async with Client() as client:
            await client.get_plebiscite(datetime.now().year)

    async def test_galleries(self):
        from pymondis import Castle, Client
        async with Client() as client:
            await gather(*[client.get_galleries(castle) for castle in Castle])

    async def test_photos(self):
        from pymondis import Gallery, HTTPClient
        async with HTTPClient() as http:
            await Gallery(73).get_photos(http)


if __name__ == "__main__":
    TestHTTPClient.run()

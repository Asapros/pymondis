from asyncio import gather
from datetime import datetime
from unittest import IsolatedAsyncioTestCase, main


class TestClient(IsolatedAsyncioTestCase):
    async def test_import(self):
        import pymondis  # A ja sobie włączyłem usuwanie niepotrzebnych importów przed commit-em, dlatego tu "pass" było
        _ = pymondis.__all__

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

    async def test_photos(self):  # TODO do httpclient
        from pymondis import Gallery, HTTPClient
        async with HTTPClient() as http:
            photos = await Gallery(1).get_photos(http)
            await gather(photos[0].normal.get(), photos[-1].large.get_stream(chunk_size=32))


if __name__ == "__main__":
    main()

from unittest import IsolatedAsyncioTestCase


class TestHTTPClient(IsolatedAsyncioTestCase):
    async def test_imports(self):
        from pymondis import api, client, enums, exceptions, models, util, abstract
    async def test_camps(self):
        from pymondis.client import Client
        async with Client() as c:
            print(await c.get_camps())

if __name__ == "__main__":
    TestHTTPClient.run()
from unittest import TestCase, main

from pymondis import Castle
from pymondis.shell import get_camps, get_crew, get_galleries, get_plebiscite


class TestClient(TestCase):
    def test_camps(self):
        get_camps()

    def test_plebiscite(self):
        get_plebiscite(2021)

    def test_galleries(self):
        get_galleries(Castle.MOSZNA)

    def test_crew(self):
        get_crew()


if __name__ == "__main__":
    main()

from unittest import TestCase, main

from pymondis import Castle
from pymondis.shell import get_camps, get_castles, get_crew, get_galleries, get_plebiscite


class TestClient(TestCase):
    def test_camps(self):
        print("obozy:", get_camps())

    def test_plebiscite(self):
        YEAR = 2021
        print("plebiscyt {}:".format(YEAR), get_plebiscite(YEAR))

    def test_castles(self):
        print("zamki fotorelacji:", get_castles())

    def test_crew(self):
        print("załoga:", get_crew())

    def test_galleries(self):
        CASTLE = Castle.RACOT
        print("galerie {}:".format(CASTLE), get_galleries(CASTLE))


if __name__ == "__main__":
    main()

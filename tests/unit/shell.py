from unittest import TestCase, main

from pymondis import Castle
from pymondis.shell import get_camps, get_castles, get_crew, get_galleries, get_photos, get_plebiscite


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
        galleries = get_galleries(CASTLE)
        print("galerie {}:".format(CASTLE), galleries)
        print("zdjęcia {}:".format(galleries[0].gallery_id), get_photos(galleries[0].gallery_id))


if __name__ == "__main__":
    main()

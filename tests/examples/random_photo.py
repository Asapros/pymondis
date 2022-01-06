"""
Pokazuje losowe zdjęcie z losowej galerii z losowego zamku (Może trochę zająć - 3 synchroniczne zapytania).
"""

from asyncio import run
from io import BytesIO
from random import choice

from PIL import Image  # pip install pillow

from pymondis import Castle, Client


async def main():
    async with Client() as client:
        random_castle = choice(list(Castle))  # Losuje zamek
        galleries = await client.get_galleries(random_castle)  # Pobiera galerie
        random_gallery = choice(galleries)
        photos = await random_gallery.get_photos()  # Pobiera zdjęcia
        random_photo = choice(photos)
        image_data = await random_photo.large.get()  # Pobiera zawartość zdjęcia
        Image.open(BytesIO(image_data)).show()  # Pokazuje zdjęcie


if __name__ == "__main__":
    run(main())

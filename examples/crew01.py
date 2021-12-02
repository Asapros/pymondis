"""
Pokazuje imię i zdjęcie psora, który ma najwięcej wystąpień wylosowanej litery w opisie (wiem, bardzo kreatywnie)
"""

from asyncio import run
from string import ascii_lowercase
from random import choice
from io import BytesIO

from pymondis import Client, CrewRole
from PIL import Image  # pip install pillow


async def main():
    async with Client() as client:
        crew = await client.get_crew()
        psor_list = filter(  # 'psors' nie brzmi dobrze...
            lambda crew_member: crew_member.position == CrewRole.PSOR,
            crew
        )  # Filtruje wszystkich kierowników (no, na pozycji nie-psora)
        random_letter = choice(ascii_lowercase)
        psor_list_sorted = sorted(
            psor_list,
            key=lambda psor: psor.description.lower().count(random_letter),
            reverse=True
        )  # Sortuje psorów wg. rosnącej ilości jej wystąpień
        psor = psor_list_sorted[0]  # Pierwszy psor z listy ma najwięcej wystąpień szukanej litery
        photo = await psor.photo.get()  # Pobieranie zdjęcia
        print("Litera: {}, Psor: {} {}{}, Wystąpienia: {}"
              .format(random_letter, psor.name, psor.surname,
                      "" if psor.character is None else " ({})".format(psor.character),
                      psor.description.lower().count(random_letter))
              )
        Image.open(BytesIO(photo)).show()


if __name__ == "__main__":
    run(main())

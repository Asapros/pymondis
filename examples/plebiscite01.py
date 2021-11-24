"""
Pokazuję dane wylosowanego kandydata tegorocznego plebiscytu i na niego głosuje
"""

from asyncio import run
from datetime import datetime
from random import choice

from pymondis.client import Client


async def main():
    async with Client() as client:
        current_year = datetime.now().year
        candidates = await client.get_plebiscite(current_year)  # Pobiera kandydatów tegorocznego plebiscytu
        not_voted = list(
            filter(lambda candidate: not candidate.voted, candidates)
        )  # Filtruje kandydatów kategorii na którą już dzisiaj głosowałeś
        if not not_voted:  # Lista jest pusta
            print("Zagłosowałeś już dzisiaj we wszystkich kategoriach!")
            return
        candidate = choice(not_voted)
        print("Wylosowano: {} ({} głosów, kategoria {})".format(
            candidate.name,
            candidate.votes,
            candidate.category
        ))
        await candidate.vote()  # Głosuje na niego


if __name__ == "__main__":
    run(main())

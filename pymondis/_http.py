from typing import NoReturn

from httpx import AsyncClient, Response

from ._util import backoff
from .metadata import __title__ as project_name, __version__ as project_version


class HTTPClient(AsyncClient):
    """
    Podstawowa klasa bezpośrednio wykonująca zapytania.
    Zwraca surowe dane.
    Jest używana wewnętrznie przez klasę ``Client`` (zalecane jest korzystanie tylko z niego).
    """
    def __init__(
            self,
            timeout: float | None = None,
            *,
            base_url: str = "https://quatromondisapi.azurewebsites.net/api"
    ):
        """
        Initializuje instancję.

        :param timeout: czas, po którym client zostanie samoistnie rozłączony gdy, nie uzyska odpowiedzi.
        :param base_url: podstawowy url, na który będą kierowane zapytania (z wyjątkiem ``get_resource``).
        """
        super().__init__(timeout=timeout)
        self.base: str = base_url
        self.headers = {"User-Agent": "{}/{}".format(project_name, project_version)}

        self.request = backoff(self.request)

    async def get_resource(
            self,
            url: str,
            cache_response: Response | None = None
    ) -> Response:
        """
        Pobiera dane z serwera z zasobami.

        :param url: URL, na którym znajdują się dane (najczęściej na ``hymsresources.blob.core.windows.net``).
        :param cache_response: zapisana wcześniej odpowiedź (będzie wykorzystana, gdy dane się nie zmieniły).
        :returns: odpowiedź serwera (świeża lub z ``cache_response``).
        """
        headers = {}
        if cache_response is not None:
            if cache_response.headers["Last-Modified"] is not None:
                headers["If-Modified-Since"] = cache_response.headers["Last-Modified"]
            if cache_response.headers["ETag"] is not None:
                headers["If-None-Match"] = cache_response.headers["ETag"]
        response = await self.get(
            url,
            headers=headers
        )
        if response.status_code == 304:
            return cache_response
        return response

    async def get_camps(self) -> list[dict[str, str | int | bool | None | list[str | dict[str, str | int]]]]:
        """
        Zwraca dane o aktualnych obozach.

        :returns: lista informacji o obozach.
        """
        response = await self.get(
            self.base + "/Camps",
            headers={"Accept": "application/json"}
        )
        return response.json()

    async def post_events_inauguration(self, reservation_model: dict):
        """
        Rezerwuje inaugurację.

        :param reservation_model: dane o rezerwacji.
        """
        await self.post(
            self.base + "/Events/Inauguration",
            json=reservation_model
        )

    async def get_images_galleries_castle(self, castle: str) -> list[dict[str, str | int | bool]]:
        """
        Dostaje podstawowe dane na temat aktualnych galerii z danego zamku.

        :param castle: nazwa zamku, z którego pobierana jest lista galerii.
        :returns: lista reprezentująca aktualne galerie z zamku.
        """
        response = await self.get(
            self.base + "/Images/Galeries/Castle/{}".format(castle),  # 'Galeries' - English 100
            headers={"Accept": "application/json"})

        return response.json()

    async def get_images_galleries(self, gallery_id: int) -> list[dict[str, str]]:
        """
        Dostaje linki do zdjęć znajdujących się w galerii o danym ID.

        :param gallery_id: numer/ID galerii.
        :returns: lista linków do zdjęć w dwóch jakościach.
        """
        response = await self.get(
            self.base + "/Images/Galeries/{}".format(gallery_id),  # Znowu 'Galeries'
            headers={"Accept": "application/json"})

        return response.json()

    async def post_orders_four_worlds_beginning(self, purchaser: dict):
        """
        Zamawia książkę „QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE”.

        :param purchaser: dane o osobie zamawiającej.
        """
        await self.post(
            self.base + "/Orders/FourWorldsBeginning",
            json=purchaser
        )

    async def post_parents_zone_survey(self, survey_hash: str, result: dict):
        """
        Prawdopodobnie nieobowiązujący już endpoint do jakiejś ankiety.

        :param survey_hash: ?
        :param result: opinia na temat obozu/obozów (?).
        """
        await self.post(
            self.base + "/ParentsZone/Survey/{}".format(survey_hash),
            json=result
        )

    async def get_parents_zone_crew(self) -> list[dict[str, str]]:
        """
        Zwraca dane wszystkich psorów i kierowników.

        :returns: lista danych o kadrze
        """
        response = await self.get(
            self.base + "/ParentsZone/Crew",
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def post_parents_zone_apply(self):
        """
        Zgłasza cię do pracy.

        :raises ``NotImplementedError``: zawsze, bo metoda nie jest zaimplementowana -.-
        """
        raise NotImplementedError(
            "Ta metoda nie jest jeszcze zaimplementowana."
            "Zamiast niej możesz skorzystać z tradycyjnego formularza na stronie, śledząc wysyłane zapytania - "
            "może devtools w tab-ie NETWORK czy coś innego (nie znam się)."
            "Pamiętaj żeby nie wysyłać niczego gdy rzeczywiście nie chcesz zgłosić się do pracy."
            "Później otwórz nowy issue (https://github.com/Asapros/pymondis/issues (Implementacja zapytania POST)"
            "i podziel się nagranym zapytaniem (nie zapomnij za cenzurować danych osobowych)"
        )
        # Dane najprawdopodobniej są wysyłane jako form, ale nie ma tego w swagger-ze, a ja jestem borowikiem w
        # javascript-a i nie czaje, o co chodzi, dodajcie do dokumentacji pls

    async def post_reservations_subscribe(self, reservation_model: dict) -> list[str]:
        """
        Rezerwuje obóz.

        :param reservation_model: dane o osobie rezerwującej.
        :returns: lista kodów rezerwacji.
        """
        response = await self.post(
            self.base + "/Reservations/Subscribe",
            json=reservation_model,
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def post_reservations_manage(self, pri: dict[str, str]) -> dict[str, str | bool]:
        """
        Dostaje dane o rezerwacji na podstawie jej kodu i nazwiska osoby rezerwującej.

        :param pri: kod i nazwisko.
        :returns: dokładniejsze dane o rezerwacji.
        """
        response = await self.post(
            self.base + "/Reservations/Manage",
            json=pri,
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def patch_vote(self, category: str, name: str):
        """
        Głosuje na kandydata plebiscytu.

        :param category: kategoria, w której startuje kandydat.
        :param name: nazwa kandydata (najczęściej nazwisko).
        """
        await self.patch(  # A mnie dalej zastanawia, czemu tu patch jest, a nie post...
            self.base + "/Vote/{}/{}".format(category, name)
        )

    async def get_vote_plebiscite(self, year: int) -> list[dict[str, str | int | bool]]:
        """
        Zwraca surowe dane o kandydatach plebiscytu z danego roku (bez opisów :/).

        :param year: rok, z którego szukani są kandydaci (>= 2019).
        :returns: lista reprezentująca kandydatów.
        """
        response = await self.get(
            self.base + "/Vote/plebiscite/{}".format(year),  # Jedyny endpoint nie w PascalCase
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def __aenter__(self) -> "HTTPClient":  # Type-hinting
        await super().__aenter__()
        return self

    def __enter__(self) -> NoReturn:
        raise RuntimeError("'with' nie można używać na HTTPClient'cie. Może chodziło ci o 'async with'?")

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

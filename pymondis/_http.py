from httpx import AsyncClient, Response

from ._util import backoff
from ._metadata import __title__, __version__


class HTTPClient(AsyncClient):
    """
    Podstawowa klasa bezpośrednio wykonująca zapytania
    Zwraca surowe dane
    Jest używana wewnętrznie przez Client - zalecane jest korzystanie z niego
    """
    def __init__(
            self,
            timeout: float | None = None,
            *,
            base_url: str = "https://quatromondisapi.azurewebsites.net/api"
    ):
        """
        Initializuje instancję klasy HTTPClient

        :param timeout: czas, po którym client zostanie samoistnie rozłączony gdy, nie uzyska odpowiedzi
        :param base_url: podstawowy url, na który będą kierowane zapytania (z wyjątkiem get_resource)
        """
        super().__init__(timeout=timeout)
        self.base: str = base_url
        self.headers = {"User-Agent": "{}/{}".format(__title__, __version__)}

        self.request = backoff(self.request)

    async def get_resource(
            self,
            url: str,
            cache_response: Response | None = None
    ) -> Response:
        """

        :param url: url, na którym znajdują się dane - najczęściej hymsresources.blob.core.windows.net
        :param cache_response: zapisana wcześniej odpowiedź - będzie wykorzystana, gdy dane się nie zmieniły
        :returns: odpowiedź serwera - świeżą, lub podaną w ``cache_response``
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
        Zwraca surowe dane o aktualnych obozach

        :returns: lista surowych dict-ów reprezentujących obozy
        """
        response = await self.get(
            self.base + "/Camps",
            headers={"Accept": "application/json"}
        )
        return response.json()

    async def post_events_inauguration(self, reservation_model: dict):
        """
        Rezerwuje inaugurację za pomocą surowych danych

        :param reservation_model: dane o razerwacji w dict-cie
        """
        await self.post(
            self.base + "/Events/Inauguration",
            json=reservation_model
        )

    async def get_images_galleries_castle(self, castle: str) -> list[dict[str, str | int | bool]]:
        """
        Dostaje podstawowe dane na temat aktualnych galerii z danego zamku w postaci surowych danych

        :param castle: nazwa zamku, z którego pobierana jest lista galerii
        :returns: lista surowych dict-ów reprezentujących aktualne galerie z zamku
        """
        response = await self.get(
            self.base + "/Images/Galeries/Castle/{}".format(castle),  # 'Galeries' XD
            headers={"Accept": "application/json"})

        return response.json()

    async def get_images_galleries(self, gallery_id: int) -> list[dict[str, str]]:
        """
        Dostaje linki do zdjęć znajdujących się w galerii o danym ID

        :param gallery_id: numer/ID galerii
        :returns: surowe dict-y reprezentujące zdjęcia w dwóch jakościach
        """
        response = await self.get(
            self.base + "/Images/Galeries/{}".format(gallery_id),  # Znowu 'Galeries'
            headers={"Accept": "application/json"})

        return response.json()

    async def post_orders_four_worlds_beginning(self, purchaser: dict):
        """
        Zamawia książkę „QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE” za pomocą surowych danych

        :param purchaser: surowe dane o osobie zamawiającej
        """
        await self.post(
            self.base + "/Orders/FourWorldsBeginning",
            json=purchaser
        )

    async def post_parents_zone_survey(self, survey_hash: str, result: dict):
        """
        Prawdopodobnie nieobowiązujący już endpoint do jakiejś ankiety

        :param survey_hash: EEE ???
        :param result: opinia na temat obozu/obozów (?) w postaci dict-a
        """
        await self.post(
            self.base + "/ParentsZone/Survey/{}".format(survey_hash),
            json=result
        )

    async def get_parents_zone_crew(self) -> list[dict[str, str]]:
        """
        Zwraca dane wszystkich psorów i kierowników

        :returns: lista surowych danych o kadrze
        """
        response = await self.get(
            self.base + "/ParentsZone/Crew",
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def post_parents_zone_apply(self):
        """
        Zgłasza cię do pracy na podstawie surowych danych

        :raises ``NotImplementedError``: zawsze, bo metoda nie jest zaimplementowana -.-
        """
        raise NotImplementedError(
            "Ta metoda nie jest jeszcze zaimplementowana."
            "Zamiast niej możesz skorzystać z tradycyjnego formularza na stronie, śledząc wysyłane zapytania - "
            "może devtools w tab-ie NETWORK (chrome) czy coś innego (nie znam się)."
            "Pamiętaj żeby nie wysyłać niczego gdy rzeczywiście nie chcesz zgłosić się do pracy."
            "Później otwórz nowy issue (https://github.com/Asapros/pymondis/issues (Implementacja zapytania POST)"
            "i podziel się nagranym zapytaniem (nie zapomnij za cenzurować danych osobowych)"
        )
        # Dane najprawdopodobniej są wysyłane jako form, ale nie ma tego w swagger-ze, a ja jestem borowikiem w
        # javascript-a i nie czaje, o co chodzi, dodajcie do dokumentacji pls

    async def post_reservations_subscribe(self, reservation_model: dict) -> list[str]:
        """
        Rezerwuje obóz na podstawie surowych danych

        :param reservation_model: surowe dane o osobie rezerwującej
        :returns: lista kodów rezerwacji
        """
        response = await self.post(
            self.base + "/Reservations/Subscribe",
            json=reservation_model,
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def post_reservations_manage(self, pri: dict[str, str]) -> dict[str, str | bool]:
        """
        Dostaje surowe dane o rezerwacji na podstawie jej kodu i nazwiska osoby rezerwującej

        :param pri: kod (ReservationId) i nazwisko (Surname)
        :returns: dokładniejsze dane o rezerwacji
        """
        response = await self.post(
            self.base + "/Reservations/Manage",
            json=pri,
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def patch_vote(self, category: str, name: str):
        """
        Głosuje na kandydata plebiscytu

        :param category: kategoria, w której startuje kandydat
        :param name: nazwa kandydata (najczęściej nazwisko)
        """
        await self.patch(  # A mnie dalej zastanawia, czemu tu patch jest, a nie post...
            self.base + "/Vote/{}/{}".format(category, name)
        )

    async def get_vote_plebiscite(self, year: int) -> list[dict[str, str | int | bool]]:
        """
        Zwraca surowe dane o kandydatach plebiscytu z danego roku (bez opisów :/)

        :param year: rok z którego szukani są kandydaci (>= 2018)
        :returns: lista dict-ów reprezentująca kandydatów
        """
        response = await self.get(
            self.base + "/Vote/plebiscite/{}".format(year),
            # Jedyny endpoint gdzie słowo w ścieżce nie się zaczyna dużą literą...
            headers={"Accept": "application/json"}
        )

        return response.json()

    async def __aenter__(self) -> "HTTPClient":  # Type-hinting
        await super().__aenter__()
        return self

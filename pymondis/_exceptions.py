from enum import Enum


class RevoteError(Exception):
    """
    Wznoszone podczas próby zagłosowania na tą samą kategorię w inauguracji drugi raz.
    """

    def __init__(self, category: str):
        super().__init__("Próbowałeś zagłosować na kategorię '{}' drugi raz.".format(category))


class NoEnumMatchError(Exception):
    """
    Wznoszone, gdy podjęta została nieudana próba konwersji string-a serwowanego przez API na enum.
    """

    def __init__(self, enum: type[Enum], value):
        super().__init__("Nie znaleziono żadnych pasujących elementów w {} dla wartości: {}.".format(enum, value))


class InvalidGalleryError(Exception):
    """
    Wznoszone podczas próby pobrania zdjęć z galerii będącej na liście niedziałających.
    """

    def __init__(self, gallery_id: int):
        super().__init__(
            "Galeria o ID {} jest usunięta/uszkodzona."
            "Próba pobrania zdjęć prawdopodobnie zakończy się statusem 500 Internal Server Error.".format(gallery_id)
        )
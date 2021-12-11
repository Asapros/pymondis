from enum import Enum


class CrewRole(Enum):
    """
    Role członka kadry

    PSOR - psor
    HEADMASTER - kierownik
    """
    PSOR = "Tutor"
    HEADMASTER = "HeadMaster"


class Castle(Enum):
    """
    Zamki, w których organizowane są obozy
    """
    BARANOW = "Zamek w Baranowie Sandomierskim"
    CZOCHA = "Zamek Czocha"
    GNIEW = "Zamek Gniew"
    GOLUB = "Zamek Golub Dobrzyń"
    KLICZKOW = "Zamek Kliczków"
    KRASICZYN = "Zamek w Krasiczynie"
    MOSZNA = "Zamek Moszna"
    NIDZICA = "Zamek w Nidzicy"
    PLUTSK = "Zamek w Pułtusku"
    RACOT = "Pałac Racot"
    RYBOKARTY = "Pałac Rybokarty"
    TUCZNO = "Zamek Tuczno"
    WITASZYCE = "Pałac Witaszyce"


class CampLevel(Enum):
    """
    Poziomy obozów

    MASTER - master
    NORMAL - reszta
    """
    NORMAL = "Normal"
    MASTER = "Master"


class World(Enum):
    """
    Światy, w których organizowane są obozy

    WIZARDS - czarodzieje
    PATHFINDERS - tropiciele
    RECRUITS - rekruci
    SANGUINS - sanguini
    ALL - wszystkie 4 światy
    VARIOUS - tematyczne turnusy, np. "Smocza Straż", "Sekret Zamkowej Krypty", "Księżniczki i Rycerze"
    """
    WIZARDS = "Wizzards"
    # English 100
    PATHFINDERS = "Pathfinders"
    RECRUITS = "Recruits"
    SANGUINS = "Sanguins"

    VARIOUS = "Various"

    ALL = "All"


class Season(Enum):
    """
    Pory roku (ale tylko dwie :P)

    SUMMER - lato
    WINTER - zima
    """
    SUMMER = "Summer"
    WINTER = "Winter"


class EventReservationOption(Enum):
    """
    Opcje rezerwacji inauguracji

    CHILD - dziecko
    CHILD_AND_ONE_PARENT - dziecko z rodzicem
    CHILD_AND_TWO_PARENTS - dziecko z rodzicami
    """
    CHILD = "Tylko dziecko"
    CHILD_AND_ONE_PARENT = "Dziecko + Rodzic"
    CHILD_AND_TWO_PARENTS = "Dziecko + 2 Rodziców"


class TShirtSize(Enum):
    """
    Rozmiary koszulki
    """
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class SourcePoll(Enum):
    """
    Źródło dowiedzenia się o Quatromondis
    """
    INTERNET = "Internet"
    SOCIALS = "Socials"
    RADIO = "Radio"
    TV = "TV"
    FRIENDS = "Friends"
    FLYERS = "Flyers"
    PRESS = "Press"

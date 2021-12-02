from enum import Enum


class CrewRole(Enum):
    PSOR = "Tutor"
    HEADMASTER = "HeadMaster"


class Castle(Enum):
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
    NORMAL = "Normal"
    MASTER = "Master"


class World(Enum):
    WIZARDS = "Wizzards"  # English 100
    PATHFINDERS = "Pathfinders"
    RECRUITS = "Recruits"
    SANGUINS = "Sanguins"

    VARIOUS = "Various"  # Okazjonalne (miejmy nadzieje) tematyczne turnusy -
    # Aktualnie "Smocza Straż", "Sekret Zamkowej Krypty", "Księżniczki i Rycerze" XDDDDD
    ALL = "All"


class Season(Enum):
    SUMMER = "Summer"
    WINTER = "Winter"


class EventReservationOption(Enum):
    CHILD = "Tylko dziecko"
    CHILD_AND_ONE_PARENT = "Dziecko + Rodzic"
    CHILD_AND_TWO_PARENTS = "Dziecko + 2 Rodziców"


class TShirtSize(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class SourcePoll(Enum):
    INTERNET = "Internet"
    SOCIALS = "Socials"
    RADIO = "Radio"
    TV = "TV"
    FRIENDS = "Friends"
    FLYERS = "Flyers"
    PRESS = "Press"

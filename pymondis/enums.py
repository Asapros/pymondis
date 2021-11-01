from enum import Enum

class CrewRole(Enum):
    TUTOR = "Tutor"
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
    WIZARDS = "Wizzards"  # XD
    PATHFINDERS = "Pathfinders"
    RECRUITS = "Recruits"
    SANGUINS = "Sanguins"

    ALL = "All"

class Season(Enum):
    SUMMER = "Summer"
    WINTER = "Winter"

class EventReservationOption(Enum):
    CHILD = "Tylko dziecko"
    CHILD_AND_ONE_PARENT = "Dziecko + Rodzic"
    CHILD_AND_TWO_PARENTS = "Dziecko + 2 Rodziców"



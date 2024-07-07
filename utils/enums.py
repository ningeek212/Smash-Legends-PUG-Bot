from enum import Enum


class Gamemode(Enum):
    DUEL = 1
    DUO = 2
    DOMINION = 3


class SignupState(Enum):
    Stopped = 0
    Started = 1
    Launching = 2


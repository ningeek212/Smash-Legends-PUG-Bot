from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from utils.enums import Gamemode

if TYPE_CHECKING:
    from utils.types import Signups

class Game():
    def __init__(self, id: UUID, signups: Signups, gamemode: Gamemode):
        self.id = id
        self.signups = signups
        self.gamemode = gamemode

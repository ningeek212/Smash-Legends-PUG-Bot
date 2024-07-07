from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from games.Game import Game
from utils.enums import Gamemode

if TYPE_CHECKING:
    from utils.types import Games, Signups

class GameManager():
    def __init__(self):
        self.games: Games = {}
    
    def add_game(self, signups: Signups, gamemode: Gamemode) -> Game:
        id = uuid4()
        new_game = Game(id, signups, gamemode)
        self.games[id] = new_game
        return new_game
    
    def get_game(self, id: UUID) -> Game:
        if not id in self.games.keys:
            return None
        return self.games[id]

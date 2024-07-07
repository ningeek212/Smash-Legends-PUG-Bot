from uuid import UUID

from interactions import Member, Snowflake

from games.Game import Game
from games.GameSignup import GameSignup

type Signups = list[Member]
type Games = dict[UUID, Game]
type GameSignups = dict[Snowflake, GameSignup]
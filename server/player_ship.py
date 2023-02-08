from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from server.game_objects import game

router = APIRouter()


class ShipInstruction(BaseModel):
    module: str
    attribute: str
    value: Any


class ShipReading(BaseModel):
    module: str
    attribute: str


@router.post("/set_attr")
async def set_attr(ship_instruction: ShipInstruction):
    module = getattr(game.player_ship.modules, ship_instruction.module)
    setattr(module, ship_instruction.attribute, ship_instruction.value)
    return {}


@router.post("/get_attr")
async def get_attr(ship_reading: ShipReading):
    module = getattr(game.player_ship.modules, ship_reading.module)
    value = getattr(module, ship_reading.attribute)
    return {"value": value}

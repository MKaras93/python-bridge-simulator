from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, validator

from server.game_objects import game

router = APIRouter()


def _validate_no_private(value: str):
    """
    Raises an error if the value seems to be a name of a private attribute/method (begins with "_")
    """
    if value.startswith("_"):
        raise ValueError(
            "Names beginning with '_' are considered private and can't be accessed by this endpoint."
        )
    return value


class ShipInstruction(BaseModel):
    module: str
    attribute: str
    value: Any

    # validators
    disallow_private = validator("module", "attribute", allow_reuse=True)(
        _validate_no_private
    )


class ShipReading(BaseModel):
    module: str
    attribute: str

    # validators
    disallow_private = validator("module", "attribute", allow_reuse=True)(
        _validate_no_private
    )


@router.post("/set_attr")
async def set_attr(ship_instruction: ShipInstruction):
    # TODO validate module and attribute or handle errors
    module: str = getattr(game.player_ship.modules, ship_instruction.module)
    setattr(module, ship_instruction.attribute, ship_instruction.value)
    return {}


@router.post("/get_attr")
async def get_attr(ship_reading: ShipReading):
    # TODO validate module and attribute or handle errors
    module = getattr(game.player_ship.modules, ship_reading.module)
    value = getattr(module, ship_reading.attribute)
    return {"value": value}


@router.get("/mothership/modules")
async def mothership():
    return game.player_ship.module_names

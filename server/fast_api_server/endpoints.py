from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from game.errors import NoSuchModuleException, NoSuchModuleAttributeException

router = APIRouter()

# TODO: endpoint should only pass value in payload - module name and attribute in path.


class ShipInstruction(BaseModel):
    module: str
    attribute: str
    value: Any


class ShipReading(BaseModel):
    module: str
    attribute: str


@router.post("/set_attr")
async def set_attr(ship_instruction: ShipInstruction):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.set_attribute(
            user_name,
            ship_instruction.module,
            ship_instruction.attribute,
            ship_instruction.value,
        )
    except NoSuchModuleException:
        response = JSONResponse(
            {"module_name": f"Module '{ship_instruction.module}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchModuleAttributeException:
        response = JSONResponse(
            {
                "module_name": f"Attribute '{ship_instruction.attribute}' doesn't exist for module"
                f" '{ship_instruction.module}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {"value": value}

    return response


@router.post("/get_attr")
async def get_attr(ship_reading: ShipReading):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.get_attribute(
            user_name, ship_reading.module, ship_reading.attribute
        )
    except NoSuchModuleException:
        response = JSONResponse(
            {"module_name": f"Module '{ship_reading.module}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchModuleAttributeException:
        response = JSONResponse(
            {
                "module_name": f"Attribute '{ship_reading.attribute}' doesn't exist for module"
                f" '{ship_reading.module}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {"value": value}

    return response

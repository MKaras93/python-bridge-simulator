from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from game.errors import NoSuchModuleException, NoSuchModuleAttributeException

router = APIRouter()


# TODO: endpoint should only pass value in payload - module name and attribute in path.


class SetAttributePayload(BaseModel):
    module: str
    attribute: str
    value: Any


class GetAttributePayload(BaseModel):
    module: str
    attribute: str


class CallMethodPayload(BaseModel):
    module: str
    method: str
    kwargs: dict


@router.post("/set_attr")
async def set_attr(set_attribute_payload: SetAttributePayload):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.set_attribute(
            user_name,
            set_attribute_payload.module,
            set_attribute_payload.attribute,
            set_attribute_payload.value,
        )
    except NoSuchModuleException:
        response = JSONResponse(
            {"module_name": f"Module '{set_attribute_payload.module}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchModuleAttributeException:
        response = JSONResponse(
            {
                "module_name": f"Attribute '{set_attribute_payload.attribute}' doesn't exist for module"
                               f" '{set_attribute_payload.module}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {"value": value}

    return response


@router.post("/get_attr")
async def get_attr(get_attribute_payload: GetAttributePayload):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.get_attribute(
            user_name, get_attribute_payload.module, get_attribute_payload.attribute
        )
    except NoSuchModuleException:
        response = JSONResponse(
            {"module_name": f"Module '{get_attribute_payload.module}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchModuleAttributeException:
        response = JSONResponse(
            {
                "module_name": f"Attribute '{get_attribute_payload.attribute}' doesn't exist for module"
                               f" '{get_attribute_payload.module}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {"value": value}

    return response


@router.post("/call_method")
async def call_method(call_method_payload: CallMethodPayload):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.call_method(
            user_name,
            call_method_payload.module,
            call_method_payload.method,
            **call_method_payload.kwargs,
        )
    except NoSuchModuleException:
        response = JSONResponse(
            {"module_name": f"Module '{call_method_payload.module}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchModuleAttributeException:
        response = JSONResponse(
            {
                "module_name": f"Method '{call_method_payload.method}' doesn't exist for module"
                               f" '{call_method_payload.module}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {"value": value}

    return response

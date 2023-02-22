from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from game.errors import NoSuchPanelException, NoSuchPanelAttributeException

router = APIRouter()


class SetAttributePayload(BaseModel):
    panel: str
    attribute: str
    value: Any


class GetAttributePayload(BaseModel):
    panel: str
    attribute: str


class CallMethodPayload(BaseModel):
    panel: str
    method: str
    kwargs: dict


@router.post("/set_attr")
async def set_attr(set_attribute_payload: SetAttributePayload):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.set_attribute(
            user_name,
            set_attribute_payload.panel,
            set_attribute_payload.attribute,
            set_attribute_payload.value,
        )
    except NoSuchPanelException:
        response = JSONResponse(
            {"panel_name": f"Panel '{set_attribute_payload.panel}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchPanelAttributeException:
        response = JSONResponse(
            {
                "panel_name": f"Attribute '{set_attribute_payload.attribute}' doesn't exist for panel"
                f" '{set_attribute_payload.panel}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {
            "value": value,
            "logs": router.server.get_and_clear_user_log_buffer(user_name),
        }

    return response


@router.post("/get_attr")
async def get_attr(get_attribute_payload: GetAttributePayload):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.get_attribute(
            user_name, get_attribute_payload.panel, get_attribute_payload.attribute
        )
    except NoSuchPanelException:
        response = JSONResponse(
            {"panel_name": f"Panel '{get_attribute_payload.panel}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchPanelAttributeException:
        response = JSONResponse(
            {
                "panel_name": f"Attribute '{get_attribute_payload.attribute}' doesn't exist for panel"
                f" '{get_attribute_payload.panel}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {
            "value": value,
            "logs": router.server.get_and_clear_user_log_buffer(user_name),
        }

    return response


@router.post("/call_method")
async def call_method(call_method_payload: CallMethodPayload):
    user_name = "test"  # TODO: get username

    try:
        value = router.server.game.call_method(
            user_name,
            call_method_payload.panel,
            call_method_payload.method,
            **call_method_payload.kwargs,
        )
    except NoSuchPanelException:
        response = JSONResponse(
            {"panel_name": f"Panel '{call_method_payload.panel}' doesn't exist."},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except NoSuchPanelAttributeException:
        response = JSONResponse(
            {
                "panel_name": f"Method '{call_method_payload.method}' doesn't exist for panel"
                f" '{call_method_payload.panel}'"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        response = {
            "value": value,
            "logs": router.server.get_and_clear_user_log_buffer(user_name),
        }

    return response

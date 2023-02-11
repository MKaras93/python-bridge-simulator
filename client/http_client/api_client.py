from __future__ import annotations

import abc

from urllib import parse

import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.bridge import MotherShip
    from typing import Union, Any


class BaseClient(abc.ABC):
    def __init__(self, mother_ship: MotherShip):
        self.mother_ship = mother_ship

    def set_attribute(self, module: str, attribute: str, value: Any) -> Any:
        raise NotImplemented()

    def get_attribute(self, module: str, attribute: str) -> Any:
        raise NotImplemented()

    def call_method(self, module: str, method: str, **kwargs) -> Any:
        raise NotImplemented()


class APIClient(BaseClient):
    API_URL = "http://localhost:8000"

    def __init__(self, mother_ship):
        super().__init__(mother_ship)
        self.session = requests.Session()

    def _get_request(self, path="", **kwargs):
        url = parse.urljoin(self.API_URL, path)
        response = self.session.get(url, params=kwargs)
        return response.json()

    def _post_request(self, path="", payload: Union[dict, list] = None, **kwargs):
        url = parse.urljoin(self.API_URL, path)
        response = self.session.post(url, json=payload, params=kwargs)
        return response.json()

    def set_attribute(self, module: str, attribute: str, value: Any) -> Any:
        payload = {
            "module": module,
            "attribute": attribute,
            "value": value,
        }
        response_data = self._post_request("set_attr", payload)
        self._handle_logging(response_data)
        return response_data["value"]

    def get_attribute(self, module: str, attribute: str) -> Any:
        payload = {
            "module": module,
            "attribute": attribute,
        }
        response_data = self._post_request("get_attr", payload)
        self._handle_logging(response_data)
        return response_data["value"]

    def call_method(self, module: str, method: str, **kwargs) -> Any:
        payload = {
            "module": module,
            "method": method,
            "kwargs": kwargs
        }
        response_data = self._post_request("call_method", payload)
        self._handle_logging(response_data)
        return response_data["value"]

    def _handle_logging(self, response_data):
        logs = response_data.get("logs")
        for log in logs:
            self.mother_ship.log(module=log["module"],
                                 level=log["level"],
                                 message=log["message"],
                                 user=log["user"],
                                 timestamp=log["timestamp"])


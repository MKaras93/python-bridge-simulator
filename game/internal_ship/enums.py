from __future__ import annotations

from enum import Enum


class PhenomenonState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DELETED = "deleted"

"""State operations."""

from __future__ import annotations
from typing import Any


class StatesMixin:
    def list_states(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "states/"))

    def create_state(self, project_id: str, *, name: str, color: str, group: str, **kwargs: Any) -> dict:
        return self._post(
            self._project_url(project_id, "states/"),
            {"name": name, "color": color, "group": group, **kwargs},
        )

    def get_state(self, project_id: str, state_id: str) -> dict:
        return self._get(self._project_url(project_id, f"states/{state_id}/"))

    def update_state(self, project_id: str, state_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"states/{state_id}/"), kwargs)

    def delete_state(self, project_id: str, state_id: str) -> None:
        return self._delete(self._project_url(project_id, f"states/{state_id}/"))

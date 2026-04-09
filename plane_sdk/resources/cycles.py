"""Cycle operations.

Note: OSS API v1 uses 'cycle-issues' (not 'cycle-work-items')
and the payload key is 'issues' (not 'work_items').
Cycle create requires 'project_id' in the payload body.
"""

from __future__ import annotations
from typing import Any


class CyclesMixin:
    def list_cycles(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "cycles/"))

    def create_cycle(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        # OSS requires project_id in payload
        return self._post(
            self._project_url(project_id, "cycles/"),
            {"name": name, "project_id": project_id, **kwargs},
        )

    def get_cycle(self, project_id: str, cycle_id: str) -> dict:
        return self._get(self._project_url(project_id, f"cycles/{cycle_id}/"))

    def update_cycle(self, project_id: str, cycle_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"cycles/{cycle_id}/"), kwargs)

    def delete_cycle(self, project_id: str, cycle_id: str) -> None:
        return self._delete(self._project_url(project_id, f"cycles/{cycle_id}/"))

    def archive_cycle(self, project_id: str, cycle_id: str) -> dict:
        return self._post(self._project_url(project_id, f"cycles/{cycle_id}/archive/"))

    def unarchive_cycle(self, project_id: str, cycle_id: str) -> None:
        return self._delete(self._project_url(project_id, f"archived-cycles/{cycle_id}/unarchive/"))

    def list_archived_cycles(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "archived-cycles/"))

    # -- cycle issues (OSS uses 'cycle-issues' path + 'issues' payload) -----

    def list_cycle_work_items(self, project_id: str, cycle_id: str) -> dict:
        return self._get(self._project_url(project_id, f"cycles/{cycle_id}/cycle-issues/"))

    def add_work_items_to_cycle(self, project_id: str, cycle_id: str, work_item_ids: list[str]) -> list:
        return self._post(
            self._project_url(project_id, f"cycles/{cycle_id}/cycle-issues/"),
            {"issues": work_item_ids},
        )

    def remove_work_item_from_cycle(self, project_id: str, cycle_id: str, work_item_id: str) -> None:
        return self._delete(
            self._project_url(project_id, f"cycles/{cycle_id}/cycle-issues/{work_item_id}/")
        )

    def transfer_cycle_work_items(self, project_id: str, cycle_id: str, *, new_cycle_id: str) -> dict:
        return self._post(
            self._project_url(project_id, f"cycles/{cycle_id}/transfer-issues/"),
            {"new_cycle_id": new_cycle_id},
        )

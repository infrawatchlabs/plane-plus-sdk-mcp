"""Intake (triage) operations."""

from __future__ import annotations
from typing import Any


class IntakeMixin:
    def list_intake_work_items(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "intake-issues/"))

    def create_intake_work_item(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._project_url(project_id, "intake-issues/"), {"name": name, **kwargs})

    def get_intake_work_item(self, project_id: str, intake_id: str) -> dict:
        return self._get(self._project_url(project_id, f"intake-issues/{intake_id}/"))

    def update_intake_work_item(self, project_id: str, intake_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"intake-issues/{intake_id}/"), kwargs)

    def delete_intake_work_item(self, project_id: str, intake_id: str) -> None:
        return self._delete(self._project_url(project_id, f"intake-issues/{intake_id}/"))

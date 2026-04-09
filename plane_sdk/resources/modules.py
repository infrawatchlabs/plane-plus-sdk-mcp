"""Module operations.

Note: OSS API v1 uses 'module-issues' (not 'module-work-items')
and the payload key is 'issues' (not 'work_items').
"""

from __future__ import annotations
from typing import Any


class ModulesMixin:
    def list_modules(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "modules/"))

    def create_module(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._project_url(project_id, "modules/"), {"name": name, **kwargs})

    def get_module(self, project_id: str, module_id: str) -> dict:
        return self._get(self._project_url(project_id, f"modules/{module_id}/"))

    def update_module(self, project_id: str, module_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"modules/{module_id}/"), kwargs)

    def delete_module(self, project_id: str, module_id: str) -> None:
        return self._delete(self._project_url(project_id, f"modules/{module_id}/"))

    def archive_module(self, project_id: str, module_id: str) -> dict:
        return self._post(self._project_url(project_id, f"modules/{module_id}/archive/"))

    def unarchive_module(self, project_id: str, module_id: str) -> None:
        return self._delete(self._project_url(project_id, f"archived-modules/{module_id}/unarchive/"))

    def list_archived_modules(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "archived-modules/"))

    # -- module issues (OSS uses 'module-issues' path + 'issues' payload) ----

    def list_module_work_items(self, project_id: str, module_id: str) -> dict:
        return self._get(self._project_url(project_id, f"modules/{module_id}/module-issues/"))

    def add_work_items_to_module(self, project_id: str, module_id: str, work_item_ids: list[str]) -> list:
        return self._post(
            self._project_url(project_id, f"modules/{module_id}/module-issues/"),
            {"issues": work_item_ids},
        )

    def remove_work_item_from_module(self, project_id: str, module_id: str, work_item_id: str) -> None:
        return self._delete(
            self._project_url(project_id, f"modules/{module_id}/module-issues/{work_item_id}/")
        )

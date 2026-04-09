"""Project operations."""

from __future__ import annotations
from typing import Any


class ProjectsMixin:
    def list_projects(self) -> dict:
        return self._get(self._url("projects/"))

    def create_project(self, *, name: str, identifier: str, **kwargs: Any) -> dict:
        project = self._post(self._url("projects/"), {"name": name, "identifier": identifier, **kwargs})
        # OSS defaults module_view and cycle_view to False — enable them
        if not project.get("module_view") or not project.get("cycle_view"):
            project = self.update_project(
                project["id"], module_view=True, cycle_view=True,
                page_view=True, intake_view=True,
            )
        return project

    def get_project(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id))

    def update_project(self, project_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id), kwargs)

    def delete_project(self, project_id: str) -> None:
        return self._delete(self._project_url(project_id))

"""Member operations."""

from __future__ import annotations


class MembersMixin:
    def list_workspace_members(self) -> list:
        return self._get(self._url("members/"))

    def list_project_members(self, project_id: str) -> list:
        return self._get(self._project_url(project_id, "members/"))

"""Workspace page operations (wiki pages scoped to workspace, not project)."""

from __future__ import annotations
from typing import Any


class WorkspacePagesMixin:
    def list_workspace_pages(self) -> dict:
        return self._get(self._url("pages/"))

    def create_workspace_page(self, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._url("pages/"), {"name": name, **kwargs})

    def get_workspace_page(self, page_id: str) -> dict:
        return self._get(self._url(f"pages/{page_id}/"))

    def update_workspace_page(self, page_id: str, **kwargs: Any) -> dict:
        return self._patch(self._url(f"pages/{page_id}/"), kwargs)

    def delete_workspace_page(self, page_id: str) -> None:
        return self._delete(self._url(f"pages/{page_id}/"))

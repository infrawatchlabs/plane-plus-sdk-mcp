"""Plane SDK — HTTP client for Plane OSS API v1."""

from __future__ import annotations

from typing import Any

import httpx

from .resources.projects import ProjectsMixin
from .resources.work_items import WorkItemsMixin
from .resources.states import StatesMixin
from .resources.labels import LabelsMixin
from .resources.modules import ModulesMixin
from .resources.cycles import CyclesMixin
from .resources.pages import PagesMixin
from .resources.members import MembersMixin
from .resources.intake import IntakeMixin
from .resources.epics import EpicsMixin
from .resources.workspace_pages import WorkspacePagesMixin


class PlaneClient(
    ProjectsMixin,
    WorkItemsMixin,
    StatesMixin,
    LabelsMixin,
    ModulesMixin,
    CyclesMixin,
    PagesMixin,
    MembersMixin,
    IntakeMixin,
    EpicsMixin,
    WorkspacePagesMixin,
):
    """Synchronous client for the Plane OSS API v1.

    Usage::

        client = PlaneClient(
            base_url="https://plane.example.com",
            api_key="plane_api_...",
            workspace_slug="my-workspace",
        )
        projects = client.list_projects()
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        workspace_slug: str,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.workspace_slug = workspace_slug
        self._http = httpx.Client(
            base_url=f"{self.base_url}/api/v1",
            headers={"x-api-key": api_key, "Content-Type": "application/json"},
            timeout=timeout,
        )

    # -- low-level helpers ---------------------------------------------------

    def _url(self, path: str) -> str:
        """Build a workspace-scoped path."""
        return f"/workspaces/{self.workspace_slug}/{path}"

    def _project_url(self, project_id: str, path: str = "") -> str:
        """Build a project-scoped path."""
        suffix = f"/{path}" if path else "/"
        return self._url(f"projects/{project_id}{suffix}")

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        resp = self._http.request(method, path, **kwargs)
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        return resp.json()

    def _get(self, path: str, **params: Any) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, data: dict | None = None) -> Any:
        return self._request("POST", path, json=data or {})

    def _patch(self, path: str, data: dict) -> Any:
        return self._request("PATCH", path, json=data)

    def _delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    # -- user ----------------------------------------------------------------

    def get_me(self) -> dict:
        """Get the authenticated user."""
        return self._get("/users/me/")

    def close(self) -> None:
        self._http.close()

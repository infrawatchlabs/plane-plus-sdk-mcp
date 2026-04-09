"""Work item (issue) operations."""

from __future__ import annotations
from typing import Any


class WorkItemsMixin:
    # -- work items ----------------------------------------------------------

    def list_work_items(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "work-items/"))

    def create_work_item(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._project_url(project_id, "work-items/"), {"name": name, **kwargs})

    def get_work_item(self, project_id: str, work_item_id: str) -> dict:
        return self._get(self._project_url(project_id, f"work-items/{work_item_id}/"))

    def update_work_item(self, project_id: str, work_item_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"work-items/{work_item_id}/"), kwargs)

    def delete_work_item(self, project_id: str, work_item_id: str) -> None:
        return self._delete(self._project_url(project_id, f"work-items/{work_item_id}/"))

    # -- comments ------------------------------------------------------------

    def list_comments(self, project_id: str, work_item_id: str) -> dict:
        return self._get(self._project_url(project_id, f"work-items/{work_item_id}/comments/"))

    def create_comment(self, project_id: str, work_item_id: str, *, comment_html: str, **kwargs: Any) -> dict:
        return self._post(
            self._project_url(project_id, f"work-items/{work_item_id}/comments/"),
            {"comment_html": comment_html, **kwargs},
        )

    def update_comment(self, project_id: str, work_item_id: str, comment_id: str, **kwargs: Any) -> dict:
        return self._patch(
            self._project_url(project_id, f"work-items/{work_item_id}/comments/{comment_id}/"), kwargs
        )

    def delete_comment(self, project_id: str, work_item_id: str, comment_id: str) -> None:
        return self._delete(self._project_url(project_id, f"work-items/{work_item_id}/comments/{comment_id}/"))

    # -- links ---------------------------------------------------------------

    def list_links(self, project_id: str, work_item_id: str) -> dict:
        return self._get(self._project_url(project_id, f"work-items/{work_item_id}/links/"))

    def create_link(self, project_id: str, work_item_id: str, *, url: str, **kwargs: Any) -> dict:
        return self._post(
            self._project_url(project_id, f"work-items/{work_item_id}/links/"),
            {"url": url, **kwargs},
        )

    def delete_link(self, project_id: str, work_item_id: str, link_id: str) -> None:
        return self._delete(self._project_url(project_id, f"work-items/{work_item_id}/links/{link_id}/"))

    # -- activities ----------------------------------------------------------

    def list_activities(self, project_id: str, work_item_id: str) -> dict:
        return self._get(self._project_url(project_id, f"work-items/{work_item_id}/activities/"))

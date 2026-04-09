"""Page operations."""

from __future__ import annotations
from typing import Any


class PagesMixin:
    def list_pages(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "pages/"))

    def create_page(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._project_url(project_id, "pages/"), {"name": name, **kwargs})

    def get_page(self, project_id: str, page_id: str) -> dict:
        return self._get(self._project_url(project_id, f"pages/{page_id}/"))

    def update_page(self, project_id: str, page_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"pages/{page_id}/"), kwargs)

    def delete_page(self, project_id: str, page_id: str) -> None:
        return self._delete(self._project_url(project_id, f"pages/{page_id}/"))

    def update_page_content(self, project_id: str, page_id: str, content_html: str) -> dict:
        """Replace the full page content (body). Uses the InfraWatch custom endpoint.

        The underlying API field is 'description_html' but we expose it
        as 'content' since that's what it actually is — the page body.
        """
        return self._patch(
            self._project_url(project_id, f"pages/{page_id}/description/"),
            {"description_html": content_html},
        )

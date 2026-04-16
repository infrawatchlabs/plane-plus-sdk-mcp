"""Page operations."""

from __future__ import annotations
from typing import Any


class PagesMixin:
    def list_pages(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "pages/"))

    def create_page(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._project_url(project_id, "pages/"), {"name": name, **kwargs})

    def get_page(self, project_id: str, page_id: str, response_format: str = "html") -> dict:
        """Get page details.

        Args:
            response_format: "html" (default) or "markdown". When "markdown",
                the response includes a ``description_markdown`` field.
        """
        params = {}
        if response_format == "markdown":
            params["format"] = "markdown"
        return self._get(self._project_url(project_id, f"pages/{page_id}/"), **params)

    def update_page(self, project_id: str, page_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"pages/{page_id}/"), kwargs)

    def delete_page(self, project_id: str, page_id: str) -> None:
        return self._delete(self._project_url(project_id, f"pages/{page_id}/"))

    def update_page_content(
        self,
        project_id: str,
        page_id: str,
        content_html: str,
        content_format: str = "html",
    ) -> dict:
        """Replace the full page content (body). Uses the InfraWatch custom endpoint.

        The underlying API field is 'description_html' but we expose it
        as 'content' since that's what it actually is — the page body.

        Args:
            content_format: "html" (default) or "markdown". When "markdown",
                the server converts MD to HTML before saving.
        """
        payload = {"description_html": content_html}
        if content_format == "markdown":
            payload["content_format"] = "markdown"
        return self._patch(
            self._project_url(project_id, f"pages/{page_id}/description/"),
            payload,
        )

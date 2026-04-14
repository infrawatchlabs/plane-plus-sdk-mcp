"""Epic operations — epics are issues with type.is_epic=True."""

from __future__ import annotations
from typing import Any


class EpicsMixin:
    # -- epics ----------------------------------------------------------------

    def list_epics(self, project_id: str) -> dict:
        """List all epics in a project."""
        return self._get(self._project_url(project_id, "iw-epics/"))

    def create_epic(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        """Create an epic. The API auto-sets the epic issue type."""
        return self._post(self._project_url(project_id, "iw-epics/"), {"name": name, **kwargs})

    def get_epic(self, project_id: str, epic_id: str) -> dict:
        """Retrieve a single epic by ID."""
        return self._get(self._project_url(project_id, f"iw-epics/{epic_id}/"))

    def update_epic(self, project_id: str, epic_id: str, **kwargs: Any) -> dict:
        """Update an epic (partial update)."""
        return self._patch(self._project_url(project_id, f"iw-epics/{epic_id}/"), kwargs)

    def delete_epic(self, project_id: str, epic_id: str) -> None:
        """Delete an epic."""
        return self._delete(self._project_url(project_id, f"iw-epics/{epic_id}/"))

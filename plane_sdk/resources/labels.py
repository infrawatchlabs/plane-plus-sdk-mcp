"""Label operations."""

from __future__ import annotations
from typing import Any


class LabelsMixin:
    def list_labels(self, project_id: str) -> dict:
        return self._get(self._project_url(project_id, "labels/"))

    def create_label(self, project_id: str, *, name: str, **kwargs: Any) -> dict:
        return self._post(self._project_url(project_id, "labels/"), {"name": name, **kwargs})

    def get_label(self, project_id: str, label_id: str) -> dict:
        return self._get(self._project_url(project_id, f"labels/{label_id}/"))

    def update_label(self, project_id: str, label_id: str, **kwargs: Any) -> dict:
        return self._patch(self._project_url(project_id, f"labels/{label_id}/"), kwargs)

    def delete_label(self, project_id: str, label_id: str) -> None:
        return self._delete(self._project_url(project_id, f"labels/{label_id}/"))

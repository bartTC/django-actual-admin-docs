from __future__ import annotations

from pathlib import Path

from django.apps import AppConfig
from django.conf import settings
from django.http import HttpRequest
from django.utils.safestring import mark_safe


class ActualAdminDocsConfig(AppConfig):
    name = "actual_admin_docs"
    verbose_name = "Actual Admin Docs"

    def get_docs_root(self) -> Path:
        return settings.DOCS_ROOT.resolve()

    def get_index_document(self) -> str:
        return getattr(settings, "DOCS_INDEX", "index.md")

    def permission_check(self, request: HttpRequest) -> bool:
        return request.user.is_active and request.user.is_staff

    @mark_safe  # noqa: S308
    def render_document(self, request: HttpRequest, path: Path) -> str:
        from markdown_it import MarkdownIt
        from mdit_py_plugins.anchors import anchors_plugin
        from mdit_py_plugins.footnote import footnote_plugin

        md = (
            MarkdownIt(
                "gfm-like",
                {
                    "breaks": False,
                    "html": True,
                    "linkify": True,
                    "typographer": True,
                },
            )
            .use(footnote_plugin)
            .use(anchors_plugin, permalink=True)
            .enable("table")
            .enable("strikethrough")
            .enable("linkify")
        )

        try:
            return md.render(path.read_text())
        except Exception as e:  # pragma: nocover
            if settings.DEBUG:
                raise
            return f"Unable to render document: <em>{e}</em>"

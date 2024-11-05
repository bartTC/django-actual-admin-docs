from __future__ import annotations

from pathlib import Path
from typing import Any

from django.apps import AppConfig
from django.conf import settings
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound


class ActualAdminDocsConfig(AppConfig):
    name = "actual_admin_docs"
    verbose_name = "Actual Admin Docs"

    docs_root: Path = settings.DOCS_ROOT
    index_document: str = getattr(settings, "DOCS_INDEX", "index.md")

    def get_docs_root(self) -> Path:
        return self.docs_root.resolve()

    def get_index_document(self) -> str:
        return self.index_document

    def permission_check(self, request: HttpRequest) -> bool:
        return request.user.is_active and request.user.is_staff

    def highlight_code(self, code: str, name: str, attrs: Any) -> str:
        """Highlight a block of code"""
        if not name:
            return code

        try:
            lexer = get_lexer_by_name(name)
        except ClassNotFound:
            lexer = TextLexer()

        formatter = HtmlFormatter(nowrap=True)
        return highlight(code, lexer, formatter)

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
                    "highlight": self.highlight_code,
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

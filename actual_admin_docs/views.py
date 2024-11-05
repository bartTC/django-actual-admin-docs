from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.apps import apps
from django.contrib import admin
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpRequest, HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView

from actual_admin_docs.apps import ActualAdminDocsConfig

config: ActualAdminDocsConfig = apps.get_app_config("actual_admin_docs")

DOCS_ROOT = config.get_docs_root()
INDEX_DOCUMENT = config.get_index_document()


@dataclass
class Breadcrumb:
    name: str
    url: str | None


class DocsView(TemplateView):
    template_name = "admin/docs/page.html"
    page: str
    docs_root: Path
    document_path: Path

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.docs_root = DOCS_ROOT
        self.index_document = INDEX_DOCUMENT

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Checks if the user is active and a staff member.
        If neither condition is met, it raises a Http404 exception
        """
        if not config.permission_check(request):
            msg = "No permission to access admin docs."
            raise Http404(msg)
        return super().dispatch(request, *args, **kwargs)

    def get(
        self, request: HttpRequest, page: str | None = None, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """
        If the requested file is a binary, we serve it as is. Otherwise, fallback to
        regular GET handler which renders a template.
        """
        self.page = page or self.index_document
        self.document_path = self.docs_root.joinpath(self.page).resolve()

        # Make sure, the document path is inside the docs root,
        # and nobody traversed up using ../ in some fashion.
        if self.docs_root.resolve() not in self.document_path.parents:
            msg = "Invalid document path."
            raise SuspiciousOperation(msg)

        # Make sure the given link is a file.
        if not self.document_path.is_file():
            msg = f"{self.document_path} is not a file."
            raise Http404(msg)

        mimetype, _ = mimetypes.guess_type(self.document_path)
        if mimetype == "text/markdown":
            return super().get(request, *args, **kwargs)

        with self.document_path.open("rb") as f:
            response = HttpResponse(f.read(), content_type=mimetype)
            response["Content-Disposition"] = f"inline; filename={page}"
            return response

    def _breadcrumb_url(self, path: Path) -> str | None:
        """
        Return the Admin URL of the breadcrumb.

        If the path is a folder, and that folder contains an index.md document,
        we link to that.
        """
        if path.is_dir():
            if (path / "index.md").is_file():
                path = path / "index.md"
            else:
                return None

        return reverse(
            "actual-admin-docs:page",
            kwargs={
                "page": str(path).removeprefix(str(self.docs_root)).removeprefix("/")
            },
        )

    def _breadcrumb_name(self, path: Path) -> str:
        """Unslug the filename to use it as the breadcrumb name."""
        return path.name.replace("_", " ").replace("-", " ").removesuffix(".md").title()

    def build_breadcrumbs(self) -> list[Breadcrumb]:
        """Build generic breadcrumbs out of the folder name and document filename."""

        crumbs = [
            Breadcrumb(
                self._breadcrumb_name(self.document_path),
                self._breadcrumb_url(self.document_path),
            )
        ]

        for folder in self.document_path.parents:
            if folder == self.docs_root:
                break

            crumbs.append(
                Breadcrumb(
                    self._breadcrumb_name(folder),
                    self._breadcrumb_url(folder),
                )
            )

        crumbs.reverse()
        return crumbs

    def get_context_data(self, **kwargs: Any) -> dict[Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "site_title": admin.site.site_title,
                "site_header": admin.site.site_header,
                "title": "Documentation",
                "docs_content": config.render_document(
                    self.request, self.document_path
                ),
                "breadcrumbs": self.build_breadcrumbs(),
                "page": self.page,
            }
        )
        return context

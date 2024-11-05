from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_docs(admin_client: Client) -> None:
    """Test the integrity of the admin docs views."""

    response = admin_client.get(reverse("actual-admin-docs:index"))
    assert response.status_code == HTTPStatus.OK

    response = admin_client.get(
        reverse("actual-admin-docs:page", args=["markdown-sample.md"])
    )
    assert response.status_code == HTTPStatus.OK

    response = admin_client.get(
        reverse("actual-admin-docs:page", args=["subfolder_a/subfolder_b/index.md"])
    )
    assert response.status_code == HTTPStatus.OK

    response = admin_client.get(
        reverse("actual-admin-docs:page", args=["img/cat_studying_glasses.jpg"])
    )
    assert response.status_code == HTTPStatus.OK

    response = admin_client.get(
        reverse("actual-admin-docs:page", args=["does-not-exist.md"])
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = admin_client.get(
        reverse("actual-admin-docs:page", args=["../../../../../etc/passwd"])
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_docs_anonymous(client: Client) -> None:
    """Test anonymous users can't access admin docs."""

    response = client.get(reverse("actual-admin-docs:index"))
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get(reverse("actual-admin-docs:page", args=["index.md"]))
    assert response.status_code == HTTPStatus.NOT_FOUND

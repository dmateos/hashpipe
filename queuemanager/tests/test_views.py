import pytest
from django.urls import reverse

from queuemanager.models import Endpoint


# Endpoint
@pytest.mark.django_db
def test_endpointview_loads_endpoint(client):
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    endpoint.save()

    response = client.get(reverse("endpoint", args=("abc123",)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_endpointview_error_on_invalid_endpoint(client):
    response = client.get(reverse("endpoint", args=("abc123",)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_endpointview_post(client):
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    endpoint.save()

    response = client.post(
        reverse("endpoint", args=("abc123",)), {"data": "hello world"}, follow=True
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_endpointview_post_not_found(client):
    response = client.post(
        reverse("endpoint", args=("abc123",)), {"data": "hello world"}, follow=True
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_endpointview_post_invalid_content(client):
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    endpoint.save()

    response = client.post(
        reverse("endpoint", args=("abc123",)), {"dataz": "hello world"}, follow=True
    )

    assert response.status_code == 404


# EndpointList
@pytest.mark.django_db
def test_endpointlist_lists_endpoints(client):
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    endpoint.save()

    response = client.get(reverse("endpoint_list"))

    assert response.status_code == 200
    assert "abc123" in str(response.content)


# Endpoint Create
@pytest.mark.django_db
def test_endpointcreate_creates_endpoint(client):
    response = client.post(
        reverse("endpoint_create"), {"ep_id": "abc123", "engine": "REDIS"}, follow=True
    )

    assert response.status_code == 200
    assert "abc123" in str(response.content)


# EndpointEdit
@pytest.mark.django_db
def test_endpointedit_edits_endpoint(client):
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    endpoint.save()

    response = client.post(
        reverse("endpoint_edit", args=(endpoint.id,)), {"ep_id": "xyz987"}, follow=True
    )

    assert response.status_code == 200
    assert "abc123" not in str(response.content)
    assert "xyz987" in str(response.content)

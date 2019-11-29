import pytest
from django.urls import reverse

from queuemanager.models import Endpoint


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

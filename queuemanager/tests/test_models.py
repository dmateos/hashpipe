from queuemanager.models import Endpoint


def test_endpoint_pushes_to_queue_with_redis_engine():
    endpoint = Endpoint(engine="REDIS")
    v = endpoint.push(10)
    assert v is True


def test_endpoint_pull_from_queue_with_redis_engine():
    endpoint = Endpoint(engine="REDIS")
    v = endpoint.pull()
    assert v == "10"

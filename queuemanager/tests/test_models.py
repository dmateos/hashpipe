from queuemanager.models import Endpoint


def test_endpoint_pushes_to_queue_with_redis_engine():
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    v = endpoint.push(20)
    assert v is True


def test_endpoint_pull_from_queue_with_redis_engine():
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    v = endpoint.pull()

    assert next(v) == "1"
    endpoint.push("hello")
    assert next(v) == "hello"
    endpoint.push("world")
    assert next(v) == "world"

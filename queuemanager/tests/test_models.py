from queuemanager.models import Endpoint
from threading import Thread
import time


def test_endpoint_pushes_to_queue_with_redis_engine():
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    v = endpoint.push(20)
    assert v is True


def test_endpoint_pull_from_queue_with_redis_engine():
    endpoint = Endpoint(engine="REDIS", ep_id="abc123")
    v = endpoint.pull()

    def _endpoint_push(endpoint):
        # Bit hacky but we sleep to give bellow time
        # to listen.
        time.sleep(0.1)
        endpoint.push("hello")
        endpoint.push("world")

    thread = Thread(target=_endpoint_push, args=(endpoint,))
    thread.start()

    assert next(v) == "hello"
    assert next(v) == "world"

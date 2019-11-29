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

    thread = Thread(target=_run_endpoint_push, args=(endpoint,))
    thread.start()

    assert next(v) == "hello"
    assert next(v) == "world"

    thread.join()


def _run_endpoint_push(endpoint):
    time.sleep(0.1)
    endpoint.push("hello")
    endpoint.push("world")

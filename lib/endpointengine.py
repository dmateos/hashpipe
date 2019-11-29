import redis
import time


class RedisEndpointEngine:
    def __init__(self, endpoint_id, engine_data={}):
        self.endpoint_id = endpoint_id

        if engine_data.get("host", False):
            self.r = redis.Redis(host=engine_data["host"], decode_responses=True)
        else:
            self.r = redis.Redis(decode_responses=True)

        self.p = self.r.pubsub(ignore_subscribe_messages=True)

    def push(self, x):
        self.r.publish(self.endpoint_id, x)
        return True

    def pull(self):
        self.p.subscribe(self.endpoint_id)

        for message in self.p.listen():
            data = message["data"]
            yield str(data)


# This is a dirty hack, only here for debugging purposes
# For sure data will go missing, and we are using global class state.
# Dont bother to write tests for this, dont ever use or expose to
# production.
class RamEndpointEngine:
    dirty = False
    ram_engine_cache = {}

    def __init__(self, endpoint_id, engine_data={}):
        self.endpoint_id = endpoint_id

    def push(self, x):
        RamEndpointEngine.ram_engine_cache[self.endpoint_id] = x
        RamEndpointEngine.dirty = True
        return True

    def pull(self):
        while True:
            if RamEndpointEngine.dirty:
                RamEndpointEngine.dirty = False
                try:
                    yield RamEndpointEngine.ram_engine_cache[self.endpoint_id]
                except KeyError:
                    pass
            else:
                time.sleep(0.1)

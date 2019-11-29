import redis


class RedisEndpointEngine:
    def __init__(self, endpoint_id, engine_data):
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
        count = 0

        for message in self.p.listen():
            if message:
                count += 1
                data = message["data"]
                yield str(data)

import redis


class RedisEndpointEngine:
    def __init__(self, endpoint_id, engine_data):
        self.endpoint_id = endpoint_id

        if engine_data.get("host", False):
            self.r = redis.Redis(host=engine_data["host"], decode_responses=True)
        else:
            self.r = redis.Redis(decode_responses=True)

        self.p = self.r.pubsub()

    def push(self, x):
        self.r.publish(self.endpoint_id, x)
        return True

    def pull(self):
        self.p.subscribe(self.endpoint_id)

        while True:
            message = self.p.get_message()
            if message:
                data = message["data"]
                yield str(data)

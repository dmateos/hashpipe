from django.db import models
import lib.endpointengine
import os


class Endpoint(models.Model):
    ENGINE_OPTIONS = (("REDIS", "Redis"),)
    engine = models.CharField(max_length=32, choices=ENGINE_OPTIONS, default="sqs")
    ep_id = models.CharField(max_length=16, null=False)

    def push(self, n):
        engine = self._get_engine()
        return engine.push(n)

    def pull(self):
        engine = self._get_engine()
        return engine.pull()

    def _get_engine(self):
        if self.engine == "REDIS":
            host = os.environ.get("REDIS_HOST", "localhost")
            return lib.endpointengine.RedisEndpointEngine(self.ep_id, {"host": host})


class Transformer(models.Model):
    def call(self, data):
        pass

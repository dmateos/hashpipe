import mock
import lib.endpointengine as e


def test_redis_endpoint_enigne_inits():
    with mock.patch("lib.endpointengine.redis") as mock_redis:
        e.RedisEndpointEngine(10, {})
        mock_redis.Redis.assert_called_with(decode_responses=True)


def test_redis_endpoint_engine_inits_with_host():
    with mock.patch("lib.endpointengine.redis") as mock_redis:
        e.RedisEndpointEngine(10, {"host": "testhost"})
        mock_redis.Redis.assert_called_with(host="testhost", decode_responses=True)


def test_redis_endpoint_enigne_pushes():
    with mock.patch("lib.endpointengine.redis") as mock_redis:
        r = e.RedisEndpointEngine("aeb1923", {})
        mock_redis.Redis.return_value.publish.return_value = True
        result = r.push("hello world")

        mock_redis.Redis.return_value.publish.assert_called_with(
            "aeb1923", "hello world"
        )
        assert result is True


def test_redis_endpoint_engine_gets_from_redis():
    with mock.patch("lib.endpointengine.redis") as mock_redis:
        r = e.RedisEndpointEngine("aeb1923", {})

        mock_redis.Redis.return_value.pubsub.return_value.listen.return_value = [
            {"data": "hello"},
            {"data": "world"},
        ]
        result = r.pull()

        assert next(result) == "hello"
        assert next(result) == "world"

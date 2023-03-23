from unittest import mock
# This is needed because of the caching in the main.py
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
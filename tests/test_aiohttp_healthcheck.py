import unittest
from aiohttp import ClientSession
from aio_healthcheck_python import start_healthcheck


class TestStartHealthcheck(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.sync_callable_true = self.sync_check_true
        self.async_callable_true = self.async_check_true
        self.sync_callable_false = self.sync_check_false
        self.async_callable_false = self.async_check_false
        self.runner = None

    @staticmethod
    def sync_check_true():
        return True

    @staticmethod
    async def async_check_true():
        return True

    @staticmethod
    def sync_check_false():
        return False

    @staticmethod
    async def async_check_false():
        return False

    async def test_healthcheck_success(self):
        self.runner = await start_healthcheck(
            sync_callables=[self.sync_callable_true],
            async_callables=[self.async_callable_true],
            host="127.0.0.1",
            path="/healthcheck",
            port=8000,
            success_code=200,
            error_code=500,
        )
        async with ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/healthcheck") as response:
                self.assertEqual(response.status, 200)

    async def test_healthcheck_success_defaults(self):
        self.runner = await start_healthcheck()
        async with ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/healthcheck") as response:
                self.assertEqual(response.status, 200)

    async def test_healthcheck_failure(self):
        self.runner = await start_healthcheck(
            sync_callables=[self.sync_callable_false],
            async_callables=[self.async_callable_false],
            host="127.0.0.1",
            path="/healthcheck",
            port=8000,
            success_code=200,
            error_code=500,
        )
        async with ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/healthcheck") as response:
                self.assertEqual(response.status, 500)

    async def asyncTearDown(self):
        if self.runner:
            await self.runner.cleanup()


if __name__ == "__main__":
    unittest.main()
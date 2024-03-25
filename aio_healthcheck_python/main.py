from aiohttp import web
from typing import List, Callable, Awaitable


async def start_healthcheck(
    sync_callables: List[Callable[[], bool]] = None,
    async_callables: List[Callable[[], Awaitable[bool]]] = None,
    host: str = "127.0.0.1",
    path: str = "/healthcheck",
    port: int = 8000,
    success_code: int = 200,
    error_code: int = 500,
):
    """Start the healthcheck server.
    :param sync_callables: A list of synchronous functions to check. The functions should return True if the check passes.
    :param async_callables: A list of asynchronous callables to check. The functions should return True if the check passes.
    :param host: The host to bind the healthcheck server to.
    :param path: The path to use for the healthcheck endpoint.
    :param port: The port to bind the healthcheck server to.
    :param success_code: The HTTP status code to return if all checks pass.
    :param error_code: The HTTP status code to return if any checks fail.
    :return: The web.AppRunner object. This can be used to stop the healthcheck server. e.g. runner.cleanup()
    """

    if sync_callables is None:
        sync_callables = []
    if async_callables is None:
        async_callables = []

    async def healthcheck(request):
        # Check all asynchronous callables
        for async_check in async_callables:
            if not await async_check():
                return web.Response(status=error_code)

        # Check all synchronous callables
        for sync_check in sync_callables:
            if not sync_check():
                return web.Response(status=error_code)

        return web.Response(status=success_code)

    app = web.Application()
    app.router.add_get(path, healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    return runner

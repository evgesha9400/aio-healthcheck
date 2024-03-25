# aiohttp-healthcheck

A minimalist healthcheck library using aiohttp.

## Installation

Install the package using pip:

```bash
pip install aio-healthcheck-python
```

## Usage

Here is a basic example of how to use the `aio-healthcheck-python` library:

```python
from aiohttp import web
from aio_healthcheck_python import start_healthcheck


async def check_database():
    # Implement your actual database check here.
    return True


async def handle_main_page(request):
    return web.Response(text="Hello, world")


async def start_web_server():
    app = web.Application()
    # Define routes here
    app.router.add_get('/', handle_main_page)

    # Set up and start the web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()

    print("Web server started on http://127.0.0.1:8080")
    return runner


async def main():
    # Start the web server and print its status
    web_runner = await start_web_server()

    # Start the healthcheck server with database check and print its status
    health_runner = await start_healthcheck(
        async_callables=[check_database],  # Asynchronous checks, including database
        host="127.0.0.1",
        path="/healthcheck",
        port=8000,
        success_code=200,
        error_code=500,
    )

    print("Healthcheck server started on http://127.0.0.1:8000")

    # Return the runners for potential further management
    return web_runner, health_runner


# Start the aiohttp application with the main coroutine
if __name__ == '__main__':
    web.run_app(main())

```

In this example, we define an asynchronous function `check_database` that performs a health check (in this case, it always returns `True`). We then start the healthcheck server with this function as an asynchronous callable. The server will respond with a 200 status code if the check passes, and a 500 status code if it fails.

## Testing

To run the tests, use the following command:

```bash
PYTHONPATH=aio_healthcheck_python poetry run python -m unittest discover -s tests
```

## License

This project is licensed under the terms of the Apache-2.0 license.
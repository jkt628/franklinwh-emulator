import asyncio

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config

from emulator import LoginTokenAuth, api_energy, hes_gateway, logout


async def async_main():
    config = Config()
    config.bind = ["0:8080"]
    config.certfile = "cert.crt"
    config.keyfile = "cert.key"

    app = FastAPI()
    app.include_router(api_energy.router, dependencies=[LoginTokenAuth])
    app.include_router(hes_gateway.router)

    # this generates an error but it works....
    await asyncio.wait(
        [asyncio.create_task(logout()), asyncio.create_task(serve(app, config))],  # pyright: ignore[reportArgumentType]
        return_when=asyncio.FIRST_COMPLETED,
    )


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

"""
Entry point shim.

Many hosting panels (bot-hosting.net / Pterodactyl Python eggs) run
`python main.py` no matter what your file is called. This just boots the
FastAPI app from api_test_fixed.py on the port the panel proxies to.
"""

import os
import sys

import uvicorn

from api_test_fixed import app


if __name__ == "__main__":
    _port_env = {k: v for k, v in os.environ.items() if "PORT" in k.upper()}
    port = int(
        os.environ.get("SERVER_PORT")
        or os.environ.get("PORT")
        or os.environ.get("APP_PORT")
        or 8000
    )

    print("=" * 62, flush=True)
    print("entry    : main.py (shim -> api_test_fixed:app)", flush=True)
    print(f"port env : {_port_env or '(none found)'}", flush=True)
    print(f"binding  : 0.0.0.0:{port}", flush=True)
    print("=" * 62, flush=True)

    loop = "asyncio"
    if sys.platform != "win32":
        try:
            import uvloop  # noqa: F401
            loop = "uvloop"
        except ImportError:
            pass

    uvicorn.run(app, host="0.0.0.0", port=port, workers=1, loop=loop)
